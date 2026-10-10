"""Schema migration and grouped calibration, without a model, network or final evaluation."""
import ast
import dataclasses
import hashlib
import json
import io
import tarfile
from collections import Counter
from pathlib import Path

import numpy as np
import pytest

from cvoice import audio, config as C, features, pipeline
from cvoice import evaluate
from cvoice.align import greedy_words, parse_transcript
from cvoice.calibrate import Null, fit_r2, grouped_nulls, grouped_rate, rate_report, region_counter, r2_stability
from cvoice.detect import clip_flags, config_hash, decode, decode_dim, fit_scales, load_detector
from cvoice.dataset import Dataset
from cvoice.explain import build, build_clip
from cvoice.events import Run, eval_clip
from cvoice.lab import measures
from cvoice.r2pool import copy_audio, corpus_rows, find_mount, inventory, pair_ids, reader_id
from cvoice.score import score
from synth import label, recording, regime, with_x
from test_align import planted_logp

ROOT = Path(__file__).resolve().parents[1]


def test_released_detector_bytes_and_hash(base):
    """The numbers of the frozen final detector on fixed synthetic edits; reader-facing text fields are left out."""
    det = load_detector(ROOT / 'models/detector.json')
    assert config_hash(det) == '782d7df7589164fa7d06e10571369a28aaee6149834a346cfbe4d90e3832f092'
    out = []
    edits = [('D1', 10, 15, -.8), ('D2', 7, 7, -1.4), ('D2', 12, 12, 1.8),
             ('D3', 10, 15, -1.9), ('D4', 10, 10, -3.), ('D5', 10, 15, -10.), ('D6', 10, 15, -2.)]
    for name in C.REGIMES:
        for dim, a, b, x in edits:
            comp = with_x(base, dim, [(a, b, x)])
            comp.dims[dim].countable[a] = True
            reg = det['regimes'][name]
            regions = decode(comp, reg, base.tr.sentence)
            sc = score(comp, regions, reg, det['score']['pmax'])
            findings = [build(r, comp, base, base, reg, m, sc, str(i)) for i, (r, m) in enumerate(zip(regions, sc.masses))]
            findings += [build_clip(k, comp, base, base, reg, sc) for k in clip_flags(comp, reg)]
            legacy = C.as_dict(3)['DIMS']
            sc_dict = dataclasses.asdict(sc)
            for field in ('P', 'S', 'pmax', 'coverage'):
                sc_dict[field] = {k: v for k, v in sc_dict[field].items() if k in legacy}
            for f in findings:
                for field in ('pattern', 'evidence', 'span_kind', 'group', 'group_pattern', 'counted', 'candidate', 'text', 'fix', 'why'):
                    f.pop(field)
            out.append({'regions': [dataclasses.asdict(r) for r in regions], 'scores': sc_dict, 'findings': findings})
    assert hashlib.sha256(pipeline.dumps(out).encode()).hexdigest() == '8aebef405915e5c7f008dbe3e627492753a8034d311298bdf6f6850c2438e5fe'


def test_detector_config_hash_covers_every_constant(pinned_detector, monkeypatch):
    names = set()
    for name in ('detect', 'compare', 'score', 'explain', 'features', 'patterns', 'calibrate', 'r2pool', 'pipeline', 'events'):
        path = ROOT / 'src/cvoice' / (name + '.py')
        if not path.exists():
            continue
        tree = ast.parse(path.read_text())
        names.update(n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute) and
                     isinstance(n.value, ast.Name) and n.value.id == 'C' and n.attr.isupper())
    assert names <= C.as_dict().keys()
    det = pinned_detector()
    old = config_hash(det)
    monkeypatch.setattr(C, 'ORPHAN_MIN_S', C.ORPHAN_MIN_S + .01)
    assert config_hash(det) != old


def test_unit_kinds_and_unknown_explanations(base):
    assert C.is_event('D2') and C.is_event('D4') and not C.is_event('D1')
    assert C.dim_of('D2+') == C.dim_of('D2 whole clip') == 'D2'
    with pytest.raises(KeyError):
        C.dim_of('D99+')
    with pytest.raises(KeyError):
        build_clip('D99', None, base, base, {}, None)


def test_alignment_cache_keeps_the_decode_and_character_spans(tmp_path):
    tr = parse_transcript('Hello world.')
    lp, _ = planted_logp(tr.norm)
    wav = np.zeros(int(len(lp) * C.CTC_FRAME_S * C.SR))
    class Aligner:
        calls = 0
        def emissions(self, wav):
            self.calls += 1
            return lp
    aligner = Aligner()
    _, a = pipeline.align_wav(wav, tr, aligner, tmp_path)
    _, b = pipeline.align_wav(wav, tr, aligner, tmp_path)
    assert aligner.calls == 1
    assert a.decoded == b.decoded == greedy_words(lp)
    np.testing.assert_array_equal(a.char_spans, b.char_spans)
    assert list(tmp_path.glob('align_*_v2.npz'))


def test_lab_feature_port_matches_frozen_fixture():
    r = recording(16)
    x = features.compact_features(r, [], [], [])
    assert measures.compact_features is features.compact_features
    assert measures.spectral_arrays is features.spectral_arrays
    with np.load(Path(__file__).with_name('fixtures') / 'lab_before_port.npz') as before:
        assert x.keys() == set(before.files)
        for k in before.files:
            if k in ('stable_spans', 'stable_seconds'):
                continue  # The agreed low-F0 correction intentionally removes constant-pitch runs.
            a, b = np.asarray(x[k]), before[k]
            if a.dtype.kind in 'fiu':
                np.testing.assert_allclose(a, b, equal_nan=True, err_msg=k)
            else:
                np.testing.assert_array_equal(a, b, err_msg=k)
        assert before['stable_seconds'] > 0 and x['stable_seconds'] == 0


def test_event_scales_use_only_countable_signed_units(base):
    c = with_x(base, 'D2', [(0, 0, -.3), (1, 1, .8), (2, 2, -20), (3, 3, 30)])
    d = c.dims['D2']
    d.countable[:] = False
    d.countable[:2] = True
    scales, medians, counts = fit_scales([c])
    assert (counts['D2-'], counts['D2+']) == (1, 1)
    assert scales['D2-'] == pytest.approx(.3) and scales['D2+'] == pytest.approx(.8)
    assert medians['D2-'] == -.3 and medians['D2+'] == .8
    assert 'D1' in scales and 'D1-' not in scales and 'D2' not in scales


def test_missed_event_diagnosis_uses_its_sign_scale(base):
    comp = with_x(base, 'D2', [(7, 7, -.3)])
    scales = regime()['scales']
    scales.update({'D2-': .3, 'D2+': .8})
    run = Run(base, base, comp, [], None, 'R1', {}, scales)
    lab = label(base, 'PAUSE_DROPPED', (7, 8))
    lab['flaws'][0]['event'] = 'boundary'
    assert eval_clip(run, lab)['truth'][0]['max_z'] == 1.


def test_final_word_boundary_has_no_measurement_in_validity(base, monkeypatch):
    lab = label(base, 'PAUSE_INTRUSIVE', (len(base.tr) - 1, len(base.tr) - 1))
    lab['flaws'][0]['realised'] = {'value': .3}
    run = Run(base, base, with_x(base, 'D2', []), [], None, 'R1', {})
    clip = {'id': 'hesitation', 'split': 'val', 'kind': 'single'}
    ds = Dataset(Path('/tmp'), {'clips': [clip]})
    monkeypatch.setattr(evaluate, 'clip_runs', lambda *args: [(clip, run, lab)])
    result = evaluate.validity_section(ds, {}, ('val',))
    assert result['detail'][0]['detector_measurement'] is None


def nulls(base):
    rows = []
    for g, minutes in [('short', .2), ('long', 3.)]:
        for i in range(12):
            c = with_x(base, 'D2', [(5, 5, .15 + .025 * i)])
            c.dims['D2'].countable[5] = True
            c.dims['D1'].g = i / 10
            rows.append(Null(f'{g}:ref>{i}', c, base.tr.sentence, minutes, 'fit', g, f'{g}:{i}', f'{g}:ref'))
    return rows


def test_group_rates_budgets_and_reader_bounds(base, monkeypatch):
    monkeypatch.setattr(C, 'R2_BOOTSTRAPS', 30)
    ns = nulls(base)
    assert grouped_rate(ns, [1] * len(ns)) == pytest.approx((5 + 1 / 3) / 2)
    reg, tables = fit_r2(ns)
    json.dumps({'regime': reg, 'tables': tables})
    for report in reg['null']['local_by_key'].values():
        assert report['rate'] <= C.FALSE_RATE_BUDGET / 6
        assert report['bootstrap_upper95'] is None if report['flags'] == 0 else report['bootstrap_upper95'] is not None
    for report in reg['null']['clip_by_key'].values():
        assert report['rate'] <= C.FALSE_CLIP_RATE_BUDGET / 2
    report = rate_report(ns, [0] * len(ns))
    assert report['readers'] == 24 and report['rule_of_three'] is None
    repeated = rate_report(ns + ns, [0] * (2 * len(ns)))
    assert repeated['readers'] == 24
    assert r2_stability(ns)['method'] == 'leave-one-group-out'
    assert len(r2_stability(ns)['rows']) == 2


def test_bootstrap_keeps_a_reader_together_across_texts(base, monkeypatch):
    monkeypatch.setattr(C, 'R2_BOOTSTRAPS', 30)
    ns = nulls(base)
    for n in ns:
        n.reader = 'shared:' + n.reader.rsplit(':', 1)[-1]
    report = rate_report(ns, [0] * len(ns))
    assert report['readers'] == 12
    assert report['groups']['short']['readers'] == report['groups']['long']['readers'] == 12


@pytest.mark.parametrize('dim,sign', [('D1', -1), ('D1', 1), ('D2', -1), ('D2', 1)])
def test_batch_counter_matches_region_decoder(base, dim, sign):
    ns = nulls(base)
    for i, n in enumerate(ns):
        n.comp.dims[dim].x[10:15] = (-1) ** i * .5
    count = region_counter(ns, dim, C.FLOORS[dim], sign)
    for h in (1., 2., 5.):
        expected = [len(decode_dim(n.comp.dims[dim], C.FLOORS[dim], h, n.sentence, (sign,))) for n in ns]
        np.testing.assert_array_equal(count(h), expected)


def pool_rows(n=32):
    return [{'id': f'{g}_{i}', 'source': 'poetry', 'speaker_id': f'{g}:reader{i}X', 'text': text, 'duration_s': 20.}
            for g, text in [('a', 'We go.'), ('b', 'They stay.')] for i in range(n)]


def test_group_split_is_stable_disjoint_and_excludes_lab_readers():
    rows = pool_rows()
    seen = {reader_id(r) for r in rows[:6]}
    a, b = inventory(rows, seen), inventory(rows[::-1], seen)
    assert a == b
    phases = {}
    for g in a['groups']:
        for r in g['entries']:
            assert phases.setdefault(r['reader_id'], r['null_set']) == r['null_set']
            assert not (r['reader_id'] in seen and r['null_set'] == 'lockbox')
        for phase in g['sets']:
            counts = Counter(p for group, ref, p in pair_ids(a, phase) if group == g['id'])
            assert set(counts.values()) == {5}
    assert len(phases) == 32
    a['groups'][0]['sets']['fit'].pop()
    with pytest.raises(ValueError, match='split hash'):
        pair_ids(a, 'fit')


def test_lockbox_cannot_be_loaded_for_calibration():
    with pytest.raises(ValueError, match='final-evaluation'):
        grouped_nulls(None, 'lockbox')


def test_grouped_comparisons_use_only_the_requested_set(base, tmp_path):
    pool = inventory(pool_rows(32))
    entries = [r for g in pool['groups'] for r in g['entries']]
    for r in entries:
        if r['null_set'] == 'fit':
            r['clip_offset_s'] = 0.
    ds = Dataset(tmp_path, {'r2_pool': pool, 'readers': entries})
    ds._recs = {r['id']: base for r in entries if r['null_set'] == 'fit'}
    ns = grouped_nulls(ds, 'fit')
    assert len(ns) == sum(len(g['sets']['fit']) for g in pool['groups']) * 5
    assert all(n.split == 'fit' and n.reader != n.reference for n in ns)
    assert not any(r['id'] in ds._recs for r in entries if r['null_set'] == 'lockbox')


def test_small_sets_keep_five_seeded_draws_and_report_repeated_references():
    pool = inventory(pool_rows(12))
    for phase in ('fit', 'select'):
        pairs = pair_ids(pool, phase)
        assert pairs == pair_ids(pool, phase)
        assert all(b != p for _, b, p in pairs)
        assert set(Counter(p for _, _, p in pairs).values()) == {5}
    assert any(g['reference_shortfalls']['select'] for g in pool['groups'])


def test_seeded_subset_respects_the_forecast_cap(monkeypatch):
    monkeypatch.setattr(C, 'R2_ALIGNMENT_BUDGET_S', 30.)
    pool = inventory(pool_rows(32))
    assert pool['excluded'] and pool['expected_alignment_seconds'] <= 30.
    assert pool == inventory(pool_rows(32)[::-1])


def test_mount_lookup_and_no_accent_filter(tmp_path, monkeypatch):
    mount = tmp_path / 'kernels/user/cvoice-data'
    mount.mkdir(parents=True)
    assert find_mount('cvoice-data', tmp_path) == mount
    rows = [{'source': 'accent', 'speaker_id': lang, 'audio_path': lang + '.wav', 'archive': 'a.tar',
             'text': 'Please call Stella.', 'duration': 25., 'sha256': 'x', 'sha256_basis': 'file',
             'licence': 'academic', 'licence_url': 'https://example.org'} for lang in ('english1', 'spanish1')]
    (mount / 'manifest.json').write_text(json.dumps(rows))
    monkeypatch.setattr('cvoice.r2pool.tar_labels', lambda *args: {})
    kept, missing = corpus_rows(mount, {})
    assert len(kept) == 2 and not missing
    assert len(inventory(kept)['groups']) == 1


def test_corpus_audio_is_copied_without_conversion_and_checked(tmp_path):
    path = tmp_path / 'original.wav'
    wav = np.zeros(C.SR)
    audio.write_wav(path, wav)
    original = path.read_bytes()
    with tarfile.open(tmp_path / 'source.tar', 'w') as tar:
        member = tarfile.TarInfo('data/read.wav')
        member.size = len(original)
        tar.addfile(member, io.BytesIO(original))
    entry = {'id': 'r', 'archive': 'source.tar', 'member': 'data/read.wav', 'mount': str(tmp_path),
             'sha256': hashlib.sha256(original).hexdigest(), 'duration_s': 1., 'audio': 'readers/r.wav'}
    copy_audio([entry], tmp_path / 'out')
    assert (tmp_path / 'out/readers/r.wav').read_bytes() == original
    with pytest.raises(ValueError, match='checksum'):
        copy_audio([{**entry, 'sha256': 'incorrect'}], tmp_path / 'bad')


def test_bundled_prompts_cover_the_corpus_without_asr():
    prompts = json.loads((ROOT / 'src/cvoice/null_prompts.json').read_text())
    for prompt in prompts.values():
        assert prompt['sha256'] == hashlib.sha256(prompt['text'].encode()).hexdigest()
        assert prompt['source_url'].startswith('https://')
    assert len(prompts) == 20


def test_project_null_reader_takes_the_corpus_text_without_stale_word_fields():
    from cvoice.dataset import as_null_reader
    from cvoice.align import parse_transcript
    text = 'Four score and seven years ago. Now we are engaged.'
    row = as_null_reader({'id': 'null_project_x', 'text': 'Other words entirely here.', 'sentence': [0] * 4,
                          'n_sentences': 1, 'n_words': 4, 'audio': 'readers/x.wav'}, text)
    assert row['text'] == text and row['role'] == 'null_reader' and row['audio'] == 'readers/x.wav'
    assert not {'sentence', 'n_sentences', 'n_words'} & set(row)
    assert len(parse_transcript(row['text'])) == 10
