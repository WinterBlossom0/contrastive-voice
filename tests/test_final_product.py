"""The shipped product after the final run: frozen detector, gallery and evaluation panel, reader-facing texts."""
import hashlib
import json
import shutil
from pathlib import Path

import pytest
from synth import local, with_x

from cvoice import audio, config as C, explain, gallery, patterns, pipeline
from cvoice.detect import Region, config_hash, load_detector
from cvoice.score import score

ROOT = Path(__file__).resolve().parents[1]
FINAL_CONFIG = '782d7df7589164fa7d06e10571369a28aaee6149834a346cfbe4d90e3832f092'
RUN = ROOT / 'build/work/kaggle_runs/last_run/x'
FIRST_FINAL = ROOT / 'docs/evidence_final_32cdd86f3d6e/results.json'
GALLERY = ROOT / 'gallery'


def gallery_results():
    return {p.stem: json.loads(p.read_text()) for p in sorted((GALLERY / 'results').glob('*.json'))}


def test_shipped_detector_is_the_frozen_final_detector():
    record = json.loads((ROOT / 'models/final_evaluations.json').read_text())
    assert hashlib.sha256((ROOT / 'models/detector.json').read_bytes()).hexdigest() == record[FINAL_CONFIG]['detector_sha256']
    assert config_hash(load_detector(ROOT / 'models/detector.json')) == FINAL_CONFIG
    assert record[FINAL_CONFIG]['r2_lockbox_modes'] == ['single', 'consensus5'] and 'test' in record[FINAL_CONFIG]['splits']


def test_gallery_results_were_made_with_the_frozen_detector():
    assert {r['pipeline']['config_sha256'] for r in gallery_results().values()} == {FINAL_CONFIG}
    assert json.loads((GALLERY / gallery.EVALUATION).read_text())['config_sha256'] == FINAL_CONFIG


def test_pause_text_follows_the_measured_direction_in_a_group(base, pinned_detector):
    reg = pinned_detector()['regimes']['R1']
    texts = {}
    for boundary, x in ((7, -.6), (7, .6), (19, .6)):   # after word 7 the transcript has a full stop, after word 19 none
        comp = with_x(base, 'D2', [(boundary, boundary, x)])
        r = local('D2', boundary, boundary, z=3 if x > 0 else -3)
        sc = score(comp, [r], reg, C.PMAX_START)
        info = {**patterns.describe(r, comp, base, base, reg.get('pattern_labels')), 'type': 'DRAG'}   # a grouped member's type
        texts[boundary, x] = explain.build(r, comp, base, base, reg, sc.masses[0], sc, 'p', info)
    shorter, longer, unmarked = texts[7, -.6], texts[7, .6], texts[19, .6]
    assert shorter['text'].startswith('Shorter pause') and shorter['fix'].startswith('Stop fully')
    assert longer['text'].startswith('Longer pause') and 'no punctuation' not in longer['text'] and longer['fix'].startswith('Shorten')
    assert 'no punctuation' in unmarked['text'] and unmarked['fix'].startswith('Carry')


def test_gallery_pause_texts_agree_with_their_sign():
    for name, res in gallery_results().items():
        for f in res['flaws']:
            if f['dimension'] != 'D2':
                continue
            assert f['text'].startswith('Shorter pause' if f['delta'] < 0 else 'Longer pause'), (name, f['id'])
            assert ('no punctuation' in f['text']) == (f['delta'] > 0 and f['context'].endswith(': none')), (name, f['id'])


def test_r2_difference_texts_name_the_flagged_direction(pinned_detector):
    reg = pinned_detector()['regimes']['R2']
    assert pipeline.threshold_text(reg, 'D3', 1, 'difference') == 'Only the other direction (narrower pitch range) is flagged.'
    assert pipeline.threshold_text(reg, 'D5', 1, 'difference') == 'Only the other direction (lower level) is flagged.'
    assert pipeline.threshold_text(reg, 'D9', -1, 'listed') == 'This dimension is not scored.'
    assert pipeline.threshold_text(reg, 'D1', -1, 'difference').startswith('Flagged below ×')
    assert pipeline.threshold_text(reg, 'D2', -1, 'difference').startswith('Flagged below −')
    for res in gallery_results().values():
        for d in res['differences']:
            if d['status'] == 'difference':
                assert 'not scored' not in d['text'] and 'Flag threshold' not in d['text'] and '..' not in d['text'], d['text']
                if 'Flagged outside' in d['text']:
                    assert 1 in C.FLAG_SIGNS[d['dimension']], d['text']


def test_texts_carry_the_lower_case_synthetic_clause():
    for res in gallery_results().values():
        for f in [*res['flaws'], *res['differences']]:
            assert 'Real speech' not in f['text']
            assert (explain.SYNTHETIC_ONLY_CLAUSE in f['text']) == explain.synthetic_only(f['dimension'], f['pattern']), f['text']


def test_listing_reasons_are_reader_text_with_final_run_numbers():
    summary = json.loads((GALLERY / gallery.EVALUATION).read_text())['r2_speech_tempo']
    assert f"lies on {summary['flagged_or_listed']} of {summary['edits']} natural-rush edits" in pipeline.listed_reason('R2', 'D9')
    assert '0 of 68' in C.OWNER_LISTED['R2']['D9'] and '0 of 68' in pipeline.listed_reason('R2', 'D9')
    for regime_name, k in pipeline.LISTED_REASON:
        assert 'owner decision' not in pipeline.listed_reason(regime_name, k) and 'dev v13' not in pipeline.listed_reason(regime_name, k)
    for res in gallery_results().values():
        assert not any('owner decision' in n for n in res['notices'])
        assert not any('owner decision' in d['note'] for d in res['scores']['dims'])


def test_gallery_audio_is_already_on_the_upload_path():
    """A re-upload decodes the wav and removes its DC offset (audio.load_audio): stored samples must not change there."""
    index = json.loads((GALLERY / 'index.json').read_text())
    for item in index['items']:
        wav = audio.read_wav(GALLERY / item['audio'])
        assert (audio.canonical(wav, C.SR) == wav).all(), item['id']
    if shutil.which('ffmpeg'):
        uploaded = next(it for it in index['items'] if it['id'] == 'greenman_botched')['audio']
        assert (audio.load_audio(GALLERY / uploaded)[0] == audio.read_wav(GALLERY / uploaded)).all()


def test_preregistered_accounting_moves_same_change_detections_and_counts_every_region():
    row = {'split': 'test', 'levels': 'headline (L2+L3)', 'tp': 29, 'fp': 5, 'fn': 3, 'same_change_duplicates': 3, 'every_prediction': {'false_by_key': {'D1-': 2, 'D3-': 2, 'D9-': 5}, 'same_change_detections': 1}}
    assert gallery.preregistered_counts(row) == {'tp': 28, 'fp': 9, 'fn': 4, 'f1': 0.812}


@pytest.mark.skipif(not (RUN / 'eval/results.json').exists() or not FIRST_FINAL.exists(), reason='final-run outputs are not in this checkout')
def test_evaluation_panel_equals_the_final_run_outputs():
    shipped = json.loads((GALLERY / gallery.EVALUATION).read_text())
    addendum = RUN / 'eval' / gallery.ADDENDUM
    fresh = gallery.evaluation_summary(json.loads((RUN / 'eval/results.json').read_text()),
                                       json.loads((ROOT / 'models/final_evaluations.json').read_text()), json.loads(FIRST_FINAL.read_text()),
                                       json.loads(addendum.read_text()) if addendum.exists() else None,
                                       json.loads((ROOT / 'models/detector.json').read_text()))
    assert shipped == json.loads(json.dumps(fresh))
    test = next(r for r in shipped['r1'] if r['split'] == 'test')
    assert (test['preregistered']['f1'], test['count_once']['f1'], shipped['first_final']['f1']) == (0.812, 0.879, 0.879)
    assert [round(m['rate'], 3) for m in shipped['lockbox']] == [0.46, 0.516]


def test_flags_on_an_excluded_edit_are_named_in_the_description():
    lab = {'flaws': [{'type': 'LOW_EFFORT', 'level': 3, 'span': [16000, 32000], 'words': [4, 6], 'evaluation_excluded': ['x']}]}
    regions = [Region('D5', -1, 6, 8, 7, -3.0, (6, 7, 8)), Region('D1', -1, 7, 9, 8, -3.0, (7, 8, 9)), Region('D3', 1, 0, 3, 1, 3.0, (0, 1, 2, 3))]
    ids = {0: 'd5-001', 1: 'd1-001', 2: 'd3-001'}
    # The evaluation's rule (events.on_shortfall): a shared word, whatever the time overlap or dimension.
    assert gallery.excluded_markers(lab, {'enabled': ['D1', 'D5']}, regions, ids)[0]['on_edit'] == ['d5-001']
    index = json.loads((GALLERY / 'index.json').read_text())
    natural = next(it for it in index['items'] if it['id'] == 'natural_rush')
    assert 'on the excluded low effort edit and cost' in natural['description']
    assert not any('_' in it['description'] for it in index['items'] if it['id'] == 'greenman_edited')
