"""Offline manifest/label adapters. Missing text is explicit; a decode is never an independent prompt."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import tarfile
import traceback
import zipfile
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

from cvoice.align import parse_transcript
from . import EXPECTED_WALL_PER_AUDIO, EXPECTED_WALL_PER_CLIP, MAX_SECONDS, RESERVE_SECONDS, SOURCE_ORDER, SOURCE_BUDGET


def unpack(data: Path, target: Path, selected=None):
    rows = json.loads((data / 'manifest.json').read_text())
    status = json.loads((data / 'STATUS.json').read_text()) if (data / 'STATUS.json').exists() else {}
    needed = rows if selected is None else selected
    names = {x['archive'] for x in needed}
    audio = {(x['archive'], x['audio_path']) for x in needed}
    labels = {(v['archive'], v['path']) for x in needed for v in x.get('label_files', [])}
    errors = []
    for name in sorted(names):
        try:
            dest = target / name
            dest.mkdir(parents=True, exist_ok=True)
            with tarfile.open(data / name) as tar:
                for m in tar:
                    path = (dest / m.name).resolve()
                    if not path.is_relative_to(dest.resolve()) or not (m.isfile() or m.isdir()):
                        raise ValueError(f'unsafe archive member: {name}:{m.name}')
                    if m.isfile() and ((name, m.name) in audio or (name, m.name) in labels):
                        path.parent.mkdir(parents=True, exist_ok=True)
                        with tar.extractfile(m) as source, path.open('wb') as out:
                            shutil.copyfileobj(source, out)
        except Exception:
            errors.append({'archive':name, 'error':traceback.format_exc()})
    status = {**status, 'lab_unpack_errors':errors}
    return rows, status


def label_paths(row, root):
    return [root / v['archive'] / v['path'] for v in row.get('label_files', [])]


@lru_cache(maxsize=512)
def read_json(path):
    return json.loads(path.read_text())


@lru_cache(maxsize=16)
def read_csv(path):
    with path.open() as f:
        return list(csv.DictReader(f))


@lru_cache(maxsize=2)
def prominence_index(path):
    out = {}
    for batch in read_json(path).values():
        for a in batch['annotations']:
            out.setdefault(a['stem'], []).append(a)
    return out


def json_labels(paths):
    return [(p, read_json(p)) for p in paths if p.suffix == '.json']


def clean_verbatim(text):
    return re.sub(r'\s+', ' ', re.sub(r'\{[A-Z]+\s*|[{}]|<[^>]*>', ' ', text)).strip()


def annotate(row, root):
    row = dict(row)
    paths = label_paths(row, root)
    row.update(events=[], scores={}, word_scores={}, label_errors=[], text_origin='manifest')
    source = row['source']
    if source == 'accent' and not row.get('text'):
        p = next((p for p in paths if p.name == 'reading-passage.txt'), None)
        if p:
            row.update(text=p.read_text(), text_origin=str(p.relative_to(root)))
    elif source == 'disfluencyspeech':
        records = json_labels(paths)
        if records:
            _, d = records[0]
            row['verbatim'] = d.get('transcript_a', clean_verbatim(d.get('transcript_annotated', '')))
            row['text'] = d.get('transcript_b') or d.get('transcript_c')
            row['text_origin'] = 'retained fluent transcript_b/c; transcript_a is independent verbatim'
            row['annotated'] = d.get('transcript_annotated')
    elif source == 'libristutter':
        p = next((p for p in paths if p.suffix == '.csv'), None)
        if p:
            words = []
            for r in csv.reader(p.open()):
                if len(r) != 4:
                    raise ValueError('expected LibriStutter token,start,end,type rows')
                word, start, end, label = r
                if int(label):
                    row['events'].append({'start': float(start), 'end': float(end), 'kind': 'synthetic_stutter_' + label})
                elif word.upper() != 'STUTTER':
                    words.append(word)
            row.update(text=' '.join(words), text_origin='retained type-0 labelled words; synthetic events excluded')
    elif source == 'speechocean':
        stem = Path(row['original_path']).stem
        for p, d in json_labels(paths):
            item = d.get(stem)
            if not item:
                continue
            if p.name == 'scores.json':
                row['scores'] = {k: item[k] for k in ('fluency', 'prosodic', 'accuracy', 'completeness', 'total') if k in item}
                row['word_scores'] = item.get('words', [])
                row['text'] = item.get('text', row.get('text'))
            else:
                row['score_detail'] = item
    elif source == 'podcastfillers':
        full = row['condition'] == 'full_episode'
        p = next((p for p in paths if ('episode_annotations' in str(p) if full else p.name == 'PodcastFillers.csv')), None)
        if p:
            for r in read_csv(p):
                if full or int(r['pfID']) == int(Path(row['original_path']).stem):
                    origin = 'inepisode' if full else 'inclip'
                    row['events'].append({'start': float(r['event_start_' + origin]),
                                          'end': float(r['event_end_' + origin]), 'kind': r['label_full_vocab']})
                    row['clip_label'] = r['label_full_vocab']
        # One-second clips have no independent prompt. ASR episode transcripts are not human read prompts.
        row['text_origin'] = 'no independent prompt; acoustic event measures only'
    elif source == 'prominence':
        stem = Path(row['original_path']).stem
        for _, d in json_labels(paths):
            found = prominence_index(_).get(stem, [])
            if found:
                row['prominence_labels'] = found
    elif source == 'lombard' and not row.get('text'):
        code = Path(row['original_path']).stem.split('_', 2)[-1]
        p = next((p for p in paths if p.name == 'lombardgrid_json.zip'), None)
        if p:
            with zipfile.ZipFile(p) as z:
                meta = json.loads(z.read('lombardgrid/json/' + row['speaker_id'] + '.json'))
            condition = 'l' if row['condition'] == 'lombard' else 'p'
            matching = [v for v in meta if v['UTTERANCE'] == code and v['COND'] == condition]
            if matching and matching[0].get('STATUS') != 'CORRECT':
                actual = matching[0].get('TRANSCRIPTION')
                if actual and actual != '-':
                    code = actual
                else:
                    code = ''
            if code:
                row.update(text=grid_text(code), text_origin='retained GRID code; https://spandh.dcs.shef.ac.uk/avlombard/')
    row['missing_text'] = not bool(row.get('text'))
    row['path'] = str(root / row['archive'] / row['audio_path'])
    row['id'] = hashlib.sha256((row['archive'] + '/' + row['audio_path']).encode()).hexdigest()[:16]
    if row.get('text'):
        tr = parse_transcript(row['text'])
        row['text_key'] = ' '.join(tr.norm)
    else:
        row['text_key'] = ('poem:' + row['original_path'].split('/')[0]) if source == 'poetry' else None
    return row


def grid_text(code):
    """Official GRID six-slot utterance grammar; filename code is the independent prescribed prompt."""
    commands = {'b': 'bin', 'l': 'lay', 'p': 'place', 's': 'set'}
    colours = {'b': 'blue', 'g': 'green', 'r': 'red', 'w': 'white'}
    prepositions = {'a': 'at', 'b': 'by', 'i': 'in', 'w': 'with'}
    endings = {'a': 'again', 'n': 'now', 'p': 'please', 's': 'soon'}
    if len(code) != 6 or not code[3].isalpha() or not code[4].isdigit():
        raise ValueError('unsupported GRID utterance code: ' + code)
    return ' '.join((commands[code[0]], colours[code[1]], prepositions[code[2]], code[3],
                     ('zero one two three four five six seven eight nine'.split())[int(code[4])], endings[code[5]]))


@lru_cache(maxsize=32768)
def normalised_text(text):
    return ' '.join(parse_transcript(text).norm)


def group_key(row):
    source, speaker = row['source'], row.get('speaker_id') or ''
    text = normalised_text(row['text']) if row.get('text') else ''
    if source == 'ears':
        return (text, speaker)
    if source == 'avid':
        session = re.search(r'_s([12])_', row['original_path'])
        return (text, speaker, session[1] if session else '')
    if source == 'expresso':
        return (text, speaker)
    if source == 'lombard':
        return (Path(row['original_path']).stem.split('_', 2)[-1], speaker)
    if source == 'speechocean':
        return (text,)
    if source == 'vctk':
        return (speaker,)  # one reader's whole Rainbow passage, 19 sentence files
    if source == 'poetry':
        return (row['original_path'].split('/')[0],)
    return (row['audio_path'],)


def select(rows, local=False, available_seconds=None):
    """Keep entire same-speaker style/text units; fixed per-source quotas ensure every test family gets coverage.

    Aggregate forecast duration*0.4 + 1 seconds/clip is unbenchmarked. No extra sources are added
    after a quota is spent. Long podcast episodes are explicitly deferred because one-second clips
    already retain event coordinates and no independent episode prompt is available.
    """
    limits = {'gettysburg': 3, 'ears': 4, 'disfluencyspeech': 5}
    count, kept, skipped, seconds = Counter(), [], [], 0.
    capacity = MAX_SECONDS - RESERVE_SECONDS if available_seconds is None else max(0, available_seconds)
    for source in SOURCE_ORDER:
        source_rows = [r for r in rows if r['source'] == source]
        source_rows.sort(key=lambda r: (group_key(r),
            {'regular': 0, 'fast': 1, 'slow': 2, 'loud': 3, 'whisper': 4}.get(r['condition'], 0), r['audio_path']))
        if source == 'accent':
            source_rows.sort(key=lambda r: (not (r.get('speaker_id') or '').startswith('english'), r['audio_path']))
        groups = {}
        for r in source_rows:
            groups.setdefault(group_key(r) if not local else (r['audio_path'],), []).append(r)
        units = list(groups.values())
        if source in ('podcastfillers', 'mdvr', 'expresso') and not local:
            buckets = defaultdict(list)
            for unit in units:
                signature = tuple(sorted({r['condition'] for r in unit}))
                buckets[signature].append(unit)
            units = [unit for i in range(max((len(b) for b in buckets.values()), default=0))
                     for b in buckets.values() if i < len(b) for unit in [b[i]]]
        spent = 0.
        for unit in units:
            estimate = sum((r.get('duration') or 30) * EXPECTED_WALL_PER_AUDIO + EXPECTED_WALL_PER_CLIP for r in unit)
            reason = None
            if local and count[source] >= limits.get(source, 1):
                reason = 'local sample limit'
            elif not local and any(r['condition'] == 'full_episode' for r in unit):
                reason = 'episode deferred: annotated short clips cover events without an independent prompt'
            elif not local and (seconds + estimate > capacity or spent + estimate > SOURCE_BUDGET.get(source, 0)):
                reason = 'three-hour forecast budget'
            if reason:
                skipped.extend({'id': r['audio_path'], 'source': source, 'reason': reason} for r in unit)
            else:
                kept.extend(unit); count[source] += len(unit); seconds += estimate; spent += estimate
    return kept, skipped, seconds


def audit(rows, status, selected):
    """Manifest-only counts before GPU work. Label-recoverable counts are upper bounds until retained files are read."""
    from .evaluate import ACOUSTIC_ONLY, PAIR_STYLES, normal_reader
    from .measures import MEASURES
    required = {'source', 'archive', 'audio_path', 'original_path', 'speaker_id', 'condition', 'text',
                'duration', 'label_files', 'licence', 'sha256', 'sha256_basis'}
    archives = {p['file'] for s in status.get('sources', []) for p in s.get('parts', [])}
    errors = []
    for i,r in enumerate(rows):
        missing = required - r.keys()
        if missing:
            errors.append({'row':i,'missing_fields':sorted(missing)})
        if r['source'] not in SOURCE_ORDER or r['archive'] not in archives:
            errors.append({'row':i,'unknown_source_or_archive':r['source'] + ':' + r['archive']})
        for label in r.get('label_files', []):
            if set(label) != {'archive','path'} or label['archive'] not in archives:
                errors.append({'row':i,'invalid_label':label})
    def inventory(records):
        out = {'sources':{}, 'tests':{}}
        for source in SOURCE_ORDER:
            rr = [r for r in records if r['source'] == source]
            out['sources'][source] = {'recordings':len(rr), 'audio_seconds':sum(r['duration'] for r in rr),
                'speakers':len({r['speaker_id'] for r in rr if r['speaker_id']}),
                'conditions':dict(Counter(r['condition'] for r in rr)),
                'manifest_text':sum(bool(r.get('text')) for r in rr),
                'label_paths':sorted({v['path'] for r in rr for v in r['label_files']})}
        for source in ('gettysburg','poetry','vctk','accent','ears'):
            rr = [r for r in records if r['source'] == source and normal_reader(r)]
            groups = defaultdict(set)
            for r in rr:
                key = ('paragraph' if source == 'accent' else r['original_path'].split('/')[0]
                       if source == 'poetry' else ' '.join(parse_transcript(r['text']).norm) if r['text'] else 'missing')
                groups[key].add(r['speaker_id'])
            out['tests']['normal:' + source] = {'recordings':len(rr), 'distinct_readers_by_text':
                sorted([len(g) for g in groups.values()], reverse=True),
                'scope':'acoustic only without retained prompt' if source == 'poetry' else 'word and acoustic measures'}
        for source,(base,styles) in PAIR_STYLES.items():
            groups = defaultdict(list)
            for r in records:
                if r['source'] == source:
                    groups[group_key(r)].append(r)
            for style in styles:
                matches = [r for group in groups.values() if any(v['condition'] == base for v in group)
                           for r in group if r['condition'] == style]
                out['tests']['pair:' + source + ':' + style + '_vs_' + base] = {'pairs':len(matches),
                    'speakers':len({r['speaker_id'] for r in matches}),
                    'missing':None if matches else 'same speaker/session/text baseline absent'}
            if source == 'avid':
                matches = [r for group in groups.values() if any(v['condition'] == 'loud' for v in group)
                           for r in group if r['condition'] == 'soft']
                out['tests']['pair:avid:soft_vs_loud'] = {'pairs':len(matches),
                    'speakers':len({r['speaker_id'] for r in matches})}
        for test,source in (('scores','speechocean'), ('prominence','prominence'), ('verbatim','disfluencyspeech'),
                             ('events','podcastfillers'), ('synthetic_events','libristutter'), ('cohorts','mdvr')):
            out['tests'][test] = {'recordings':out['sources'][source]['recordings'],
                'conditions':out['sources'][source]['conditions']}
        for name in MEASURES:
            supported = [r for r in records if name in ACOUSTIC_ONLY or r.get('text') or
                         r['source'] in ('accent','disfluencyspeech','libristutter','lombard')]
            out['tests']['measure:' + name] = {'potential_recordings':len(supported),
                'by_source':dict(Counter(r['source'] for r in supported)),
                'scope':'upper bound; retained label parsing, finite values and extraction determine actual counts'}
        return out
    return {'manifest':inventory(rows), 'selected':inventory(selected), 'schema_errors':errors,
            'failed_sources':[{k:s.get(k) for k in ('source','stage','error')} for s in status.get('sources', [])
                              if not s.get('complete')],
            'missing_data':['VCTK absent if failed', 'poem prompt text absent', 'MDVR prompt text absent',
                            'SEP-28k has labels but no fetched audio', 'Expresso emphasis/default exact-text control absent'],
            'label_schemas':{'speechocean':'scores.json: prosodic, word stress, phones-accuracy',
                'podcastfillers':'pfID integer; event_start/end_inclip or _inepisode; label_full_vocab',
                'prominence':'root batches.annotations: stem, words triples, score',
                'lombard':'speaker JSON list: UTTERANCE, COND l/p, STATUS, TRANSCRIPTION; GRID grammar',
                'disfluencyspeech':'transcript_a verbatim, transcript_b/c fluent',
                'libristutter':'headerless token,start,end,type'}}
