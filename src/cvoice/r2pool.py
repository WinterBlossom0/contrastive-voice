"""Same-text null inventory, fixed before alignment; canonical corpus WAVs are copied without conversion."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import tarfile
from collections import defaultdict
from pathlib import Path

from . import config as C
from .align import parse_transcript


def digest(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def find_mount(name: str, root=Path('/kaggle/input')) -> Path:
    for path in (root / name, *sorted(root.glob(f'*/*/{name}')), *sorted(root.glob(f'*/{name}')), *sorted(root.rglob(name))):
        if path.is_dir():
            return path
    raise FileNotFoundError(f'{name} not mounted under {root}')


def _initials(name: str) -> str:
    """Last ':' field of a reader or speaker name, without its trailing digits, in lower case."""
    return re.sub(r'\d+$', '', name.rsplit(':', 1)[-1]).lower()


def _alignment_cost(row) -> float:
    """Forecast wall time (s) to align one reading."""
    return row['duration_s'] * C.R2_ALIGNMENT_SECONDS_PER_AUDIO + C.R2_ALIGNMENT_SECONDS_PER_CLIP


def reader_id(row) -> str:
    source, speaker = row['source'], row['speaker_id']
    if source == 'poetry':
        return 'librivox:' + _initials(speaker)
    if source == 'gettysburg':
        if speaker.startswith('lv_gettysburg150_'):
            speaker = speaker.removeprefix('lv_gettysburg150_')
        elif speaker.startswith('gettysburgaddress_150anniv_1311_librivox:'):
            speaker = speaker.rsplit(':', 1)[-1]
        return 'librivox:' + speaker.lower()
    return source + ':' + speaker


def first_language(reader):
    return _initials(reader)


def partition_hash(groups):
    return digest([{'group': g['id'], 'sets': g['sets'],
                    'readers': sorted((r['id'], r['reader_id']) for r in g['entries'])} for g in groups])


def inventory(rows: list[dict], seen: set[str] = frozenset()) -> dict:
    """Deduplicate takes and split by person; project readers are always select."""
    seen = {reader_id({'source': r.split(':', 1)[0], 'speaker_id': r.split(':', 1)[1]}) if r.startswith(('poetry:', 'gettysburg:')) else r for r in seen}
    forced = {reader_id(r) for r in rows if r['id'].startswith('null_project_') or r.get('role') == 'reader_check'}
    seen = seen | forced
    groups = defaultdict(dict)
    for row in sorted(rows, key=lambda r: r['id']):
        text = ' '.join(parse_transcript(row['text']).norm)
        gid = row['source'] + ':' + digest(text)[:16]
        rid = reader_id(row)
        if '>' in rid or '>' in row['id']:
            raise ValueError('reader ids cannot contain >')
        groups[gid].setdefault(rid, {**row, 'group': gid, 'reader_id': rid})
    inventoried = {source: sum(len(members) for members in groups.values() if next(iter(members.values()))['source'] == source)
                  for source in sorted({r['source'] for members in groups.values() for r in members.values()})}
    excluded = [{'id': r['id'], 'group': gid, 'reason': 'fewer than two same-text readers'}
                for gid, members in groups.items() if len(members) < 2 for r in members.values()]
    groups = {g: rows for g, rows in groups.items() if len(rows) >= 2}
    source_readers = defaultdict(set)
    for group in groups.values():
        for rid, row in group.items():
            source_readers[rid.split(':')[0]].add(rid)
    splits = {}
    for source, readers in sorted(source_readers.items()):
        ordered = sorted(readers, key=lambda r: digest([C.SEED, source, r]))
        if source == 'accent':
            strata = defaultdict(list)
            for rid in ordered:
                strata[(first_language(rid), rid in seen)].append(rid)
            totals = dict.fromkeys(('fit','select','lockbox'), 0)
            shares = {'fit': C.R2_FIT_SHARE, 'select': C.R2_SELECT_SHARE,
                      'lockbox': 1-C.R2_FIT_SHARE-C.R2_SELECT_SHARE}
            for members in strata.values():
                n = len(members)
                counts = {phase: int(n*share) for phase,share in shares.items()}
                remaining = n-sum(counts.values())
                phases = sorted(shares, key=lambda phase: (-(n*shares[phase]-counts[phase]), totals[phase]/shares[phase]))
                for phase in phases[:remaining]:
                    counts[phase] += 1
                offset = 0
                for phase in shares:
                    splits.update({r: phase for r in members[offset:offset+counts[phase]]})
                    offset += counts[phase]
                    totals[phase] += counts[phase]
        else:
            unseen = [r for r in ordered if r not in seen]
            nlock = min(len(unseen), max(1, int(len(ordered) * (1 - C.R2_FIT_SHARE - C.R2_SELECT_SHARE))))
            lock = set(unseen[:nlock])
            remaining = [r for r in ordered if r not in lock and r not in forced]
            nfit = min(len(remaining), max(1, int(len(ordered) * C.R2_FIT_SHARE)))
            splits.update({r: 'lockbox' if r in lock else 'fit' if r in remaining[:nfit] else 'select' for r in ordered})
    # A singleton cannot make a same-text pair. Move a reader only when every donor group retains two.
    for gid, members in sorted(groups.items()):
        for phase, donor in (('select', 'fit'), ('fit', 'select')):
            if sum(splits[r] == phase for r in members) != 1:
                continue
            candidates = sorted((r for r in members if splits[r] == donor and not (phase == 'fit' and r in forced)), key=lambda r: digest([C.SEED, gid, phase, r]))
            for rid in candidates:
                if all(sum(splits[r] == donor for r in group) > 2 for group in groups.values() if rid in group):
                    splits[rid] = phase
                    break
    result = []
    forecast = sum(_alignment_cost(r) for members in groups.values() for r in members.values())
    for gid, members in sorted(groups.items()):
        chosen = sorted(members.values(), key=lambda r: digest([C.SEED, gid, r['id']]))
        # Cap evenly by text only if its share of the total forecast exceeds the build reserve.
        total = sum(_alignment_cost(r) for r in chosen)
        share = C.R2_ALIGNMENT_BUDGET_S / len(groups)
        if forecast > C.R2_ALIGNMENT_BUDGET_S and total > share and chosen[0]['source'] != 'accent':
            selected, spent = [], 0.
            for r in chosen:
                cost = _alignment_cost(r)
                if spent + cost <= share:
                    selected.append(r)
                    spent += cost
                else:
                    excluded.append({'id': r['id'], 'group': gid, 'reason': 'seeded per-group alignment budget'})
            chosen = selected
        if len(chosen) < 2:
            excluded.extend({"id": r["id"], "group": gid, "reason": "fewer than two selected readers"} for r in chosen)
            continue
        entries = [{**r, 'null_set': splits[r['reader_id']], 'first_language': first_language(r['reader_id']) if r['source'] == 'accent' else None, 'lab_seen': r['reader_id'] in seen} for r in chosen]
        sets = {s: sorted(r['id'] for r in entries if r['null_set'] == s) for s in ('fit', 'select', 'lockbox')}
        result.append({'id': gid, 'source': entries[0]['source'], 'text': entries[0]['text'], 'sets': sets,
                       'reference_shortfalls': {s: len(sets[s]) if 0 < len(sets[s]) <= C.R2_REFERENCES else 0 for s in sets},
                       'entries': entries, 'minutes': {s: sum(r['duration_s'] for r in entries if r['null_set'] == s) / 60 for s in sets}})
    return {'accent_split': 'first-language and lab-seen strata; integer rounding per stratum; lab-seen lockbox is development-only', 'schema': 1, 'seed': C.SEED, 'references_per_participant': C.R2_REFERENCES,
            'inventoried_by_source': inventoried,
            'reference_sampling': 'five distinct references when available; seeded repeats in smaller sets; singleton sets have no pairs',
            'split_sha256': partition_hash(result), 'forced_select_readers': sorted(forced), 'reader_identity': 'LibriVox initials shared across poetry and anniversary/project Gettysburg', 'lab_readers': sorted(seen), 'groups': result, 'excluded': excluded,
            'expected_alignment_seconds': sum(_alignment_cost(r) for g in result for r in g['entries'])}


def pair_ids(pool: dict, phase: str) -> list[tuple[str, str, str]]:
    if partition_hash(pool['groups']) != pool['split_sha256']:
        raise ValueError('R2 split hash mismatch')
    pairs = []
    for group in pool['groups']:
        ids = group['sets'][phase]
        for participant in ids:
            refs = sorted((r for r in ids if r != participant), key=lambda r: digest([pool['seed'], group['id'], participant, r]))
            count = pool['references_per_participant']
            refs = [refs[i % len(refs)] for i in range(count)] if refs else []
            pairs.extend((group['id'], reference, participant) for reference in refs)
    return pairs


def tar_labels(mount: Path, rows: list[dict]) -> dict[tuple[str, str], bytes]:
    wanted = defaultdict(set)
    for row in rows:
        for label in row.get('label_files', []):
            wanted[label['archive']].add(label['path'])
    out = {}
    for archive, names in wanted.items():
        with tarfile.open(mount / archive) as tar:
            for member in tar:
                if member.name in names and member.isfile():
                    out[archive, member.name] = tar.extractfile(member).read()
    return out


def corpus_rows(mount: Path, prompts: dict) -> tuple[list[dict], list[dict]]:
    rows = [r for r in json.loads((mount / 'manifest.json').read_text()) if r['source'] in ('gettysburg', 'poetry', 'ears', 'accent')
            and (r['source'] != 'ears' or r['condition'] == 'regular')]
    labels = tar_labels(mount, [r for r in rows if r['source'] == 'accent'])
    kept, missing = [], []
    for r in rows:
        text = r.get('text')
        if r['source'] == 'poetry':
            text = prompts.get(r['original_path'].split('/')[0], {}).get('text')
        if r['source'] == 'accent' and not text:
            text = next((labels[v['archive'], v['path']].decode() for v in r['label_files'] if v['path'].endswith('reading-passage.txt')), None)
        if not text:
            missing.append({'source': r['source'], 'id': r['audio_path'], 'reason': 'no independent prompt'})
            continue
        rid = 'null_' + digest([r['source'], r['archive'], r['audio_path']])[:16]
        kept.append({'id': rid, 'source': r['source'], 'speaker_id': r['speaker_id'], 'text': text,
                     'duration_s': r['duration'], 'archive': r['archive'], 'member': r['audio_path'], 'mount': str(mount),
                     'sha256': r['sha256'], 'sha256_basis': r['sha256_basis'], 'licence_basis': r['licence'], 'licence_url': r['licence_url']})
        if r['source'] == 'poetry':
            prompt = prompts[r['original_path'].split('/')[0]]
            if hashlib.sha256(text.encode()).hexdigest() != prompt['sha256']:
                raise ValueError('poem prompt checksum mismatch')
            kept[-1].update(text_origin=prompt['source_url'], prompt_sha256=prompt['sha256'])
    return kept, missing


def copy_audio(entries: list[dict], out: Path) -> None:
    from .audio import read_wav
    archives = defaultdict(list)
    for row in entries:
        if row.get('archive'):
            archives[row['mount'], row['archive']].append(row)
    for (mount, archive), rows in archives.items():
        wanted = {r['member']: r for r in rows}
        with tarfile.open(Path(mount) / archive) as tar:
            for member in tar:
                if member.name not in wanted or not member.isfile():
                    continue
                row = wanted.pop(member.name)
                path = out / row['audio']
                path.parent.mkdir(parents=True, exist_ok=True)
                with tar.extractfile(member) as src, path.open('wb') as dest:
                    shutil.copyfileobj(src, dest)
                with path.open('rb') as f:
                    if hashlib.file_digest(f, 'sha256').hexdigest() != row['sha256']:
                        raise ValueError(f"{row['id']}: corpus WAV checksum mismatch")
                wav = read_wav(path)  # verifies canonical rate and channel count; no conversion
                if abs(len(wav) / C.SR - row['duration_s']) > 1 / C.SR:
                    raise ValueError(f"{row['id']}: corpus duration mismatch")
        if wanted:
            raise FileNotFoundError(f'{archive}: missing WAV members {sorted(wanted)}')
