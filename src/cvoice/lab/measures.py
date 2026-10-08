"""Report definitions on compact Recording-derived arrays; times in seconds, pitch in semitones."""
from __future__ import annotations

import numpy as np

from cvoice import config as C
from cvoice.compare import compare
from cvoice.features import stress_words, finite as finite, mean as mean, median as median, slope as slope
from cvoice.features import spectral_arrays as spectral_arrays, compact_features as compact_features, decode_edits as decode_edits
from cvoice.features import runs as runs, speech_time_ratio as speech_time_ratio
from . import BREATH_S, FUNCTION_WORDS, PAUSE_S


def correlation(a, b):
    a, b = np.asarray(a), np.asarray(b)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3 or np.std(a[ok]) < 1e-10 or np.std(b[ok]) < 1e-10:
        return np.nan
    return float(np.corrcoef(a[ok], b[ok])[0, 1])


def relative(v):
    m = median(v)
    return np.asarray(v) / m if m > 0 else np.full_like(np.asarray(v, float), np.nan)


def subtract(v, b, key):
    return np.asarray(v) if b is None else np.asarray(v) - np.asarray(b[key])


def log_ratio(v, ref):
    v, ref = np.asarray(v, float), np.asarray(ref, float)
    out = np.full(np.broadcast_shapes(v.shape, ref.shape), np.nan)
    np.log(np.divide(v, ref, out=np.ones_like(out), where=(v > 0) & (ref > 0)), out=out,
           where=(v > 0) & (ref > 0))
    return out


def sentence_match(x, b, key):
    if b is None:
        return x[key]
    out = []
    for s in np.unique(x['sentence']):
        ix = x['sentence'] == s
        a, r = x[key][ix], b[key][ix]
        valid = np.isfinite(a) & np.isfinite(r)
        c = correlation(a, r)
        out.append(1 - c * valid.mean() if np.isfinite(c) else np.nan)
    return np.asarray(out)


def within_phrase_count(x, b=None):
    """pace_pauses/REPORT.md §4 #1: count pauses ≥200 ms at unpunctuated word gaps; punctuation proxy for clauses."""
    v = np.sum((x['sil'] >= PAUSE_S) & ~x['punct'][:-1])
    return v if b is None else v - within_phrase_count(b)


def within_phrase_duration(x, b=None):
    """pace_pauses/REPORT.md §4 #1: summed within-phrase pause seconds, against the reference."""
    v = x['sil'][~x['punct'][:-1]].sum()
    return v if b is None else v - within_phrase_duration(b)


def pause_count_ratio(x, b=None):
    """pace_pauses/REPORT.md §4 #2: pause-count ratio; zero reference count is undefined, no pseudo-count."""
    v = np.sum(x['sil'] >= PAUSE_S)
    return v if b is None else (v / pause_count_ratio(b) if pause_count_ratio(b) else np.nan)


def mean_pause_ratio(x, b=None):
    """pace_pauses/REPORT.md §4 #2: mean pause-duration ratio; no pauses makes it undefined."""
    v = mean(x['sil'][x['sil'] >= PAUSE_S])
    return v if b is None else v / mean_pause_ratio(b)


def mean_run(x, b=None):
    """pace_pauses/REPORT.md §4 #4: words per run between ≥200 ms pauses; count both edge runs."""
    v = len(x['norm']) / (1 + np.sum(x['sil'] >= PAUSE_S))
    return v if b is None else v - mean_run(b)


def latency_contour(x, b=None):
    """pace_pauses/REPORT.md §2.1 C, §4 #3: per-sentence Pearson latency match; missing-value penalty; silence before word."""
    return sentence_match(x, b, 'latency')


def production_contour(x, b=None):
    """pace_pauses/REPORT.md §4 #3: per-sentence Pearson word-production match; raw CTC span, invariant to median scaling."""
    return sentence_match(x, b, 'production')


def latency_residual(x, b=None):
    """pace_pauses/REPORT.md §4 #3: largest per-word latency residual after own-median normalisation; zero median undefined."""
    v = relative(x['latency'])
    return v if b is None else v - relative(b['latency'])


def production_residual(x, b=None):
    """pace_pauses/REPORT.md §4 #3: normalised per-word production residual; CTC spikes impose timing error."""
    v = relative(x['production'])
    return v if b is None else v - relative(b['production'])


def tempo_irregularity(x, b=None):
    """pace_pauses/REPORT.md §4 #5: SD of median-centred five-word ln speech-time ratio (chosen SD rather than MAD)."""
    return np.std(finite(x['win_T'])) if b is None else np.std(finite(product_delta(x, b, 'D1')))


def tempo_drift(x, b=None):
    """pace_pauses/REPORT.md §4 #6: ln(last-third/first-third speech time), then subtract reference drift; thirds by word."""
    n = len(x['norm']) // 3
    if n < 2:
        return np.nan
    t = lambda a, z: max(x['end'][z - 1] - x['start'][a] - x['sil'][a:z - 1].sum(), 1e-3)
    v = np.log(t(len(x['norm']) - n, len(x['norm'])) / t(0, n))
    return v if b is None else v - tempo_drift(b)


def breath_candidates(x, b=None):
    """pace_pauses/REPORT.md §4 #7, corrected Wang: ≥250 ms pause candidates; NOT confirmed breaths; count."""
    v = np.sum(x['sil'] >= BREATH_S)
    return v if b is None else v - breath_candidates(b)


def breath_position(x, b=None):
    """pace_pauses/REPORT.md §4 #7: share of ≥250 ms candidates without punctuation; syntax unavailable."""
    mask = x['sil'] >= BREATH_S
    v = mean(~x['punct'][:-1][mask])
    return v if b is None else v - breath_position(b)


def pre_boundary_lengthening(x, b=None):
    """pace_pauses/REPORT.md §4 #8: boundary word duration divided by syllables and own median duration/syllable."""
    v = x['production'] / x['syll']
    v = relative(v)[x['punct']]
    return v if b is None else v - pre_boundary_lengthening(b)


def silence_share(x, b=None):
    """pace_pauses/REPORT.md §4 #9: silent frame seconds/clip seconds; all frames below product floor and unvoiced."""
    return subtract(x['silence_share'], b, 'silence_share')


def product_delta(x, b, dim):
    if b is None:
        return x[{'D1': 'win_T', 'D2': 'sil_raw', 'D3': 'win_R', 'D5': 'win_E', 'D6': 'win_Q'}[dim]]
    if '_product_deltas' in b:
        return b['_product_deltas'][dim]
    from .extract import recording_view
    return compare(recording_view(b), recording_view(x)).dims[dim].x


def five_word_pace(x, b=None):
    """pace_pauses/REPORT.md §3; product compare.d1_pace: median-centred five-word ln ratio, product pause eligibility."""
    return product_delta(x, b, 'D1')


def five_word_pause(x, b=None):
    """pace_pauses/REPORT.md §3; product compare.d2_pauses: eligible raw acoustic pause differences in seconds."""
    return product_delta(x, b, 'D2')


def inserted_material(x, b=None):
    """disfluency/REPORT.md §4 #1: greedy insertions per 100 prompt words; copies/prefixes recorded separately."""
    return subtract(x['insertions_per100'], b, 'insertions_per100')


def orphan_voiced_gap(x, b=None):
    """disfluency/REPORT.md §2.6 M3, §4 #2: voiced seconds outside aligned word regions; Praat voicing replaces VAD."""
    return subtract(x['orphan_seconds'], b, 'orphan_seconds')


def stability_run(x, b=None):
    """disfluency/REPORT.md §2.6 M4, §4 #3: 5-frame pitch and 10-frame band-envelope OLS stability run seconds; chosen thresholds, not Goto P_fp."""
    return subtract(x['stable_seconds'], b, 'stable_seconds')


def within_word_silence(x, b=None):
    """disfluency/REPORT.md §4 #4: longest silent run ≥250 ms within raw aligned word span; seconds, reference subtraction."""
    return subtract(x['word_silence'], b, 'word_silence')


def word_duration_ratio(x, b=None):
    """disfluency/REPORT.md §4 #5: word duration ratio after removing each clip's overall word-duration median."""
    v = relative(x['production'])
    return v if b is None else log_ratio(v, relative(b['production']))


def character_duration_ratio(x, b=None):
    """disfluency/REPORT.md §4 #5: normalised aligned character-span ln ratios; spikes are not phone boundaries."""
    v = relative(x['char_duration'])
    return v if b is None else log_ratio(v, relative(b['char_duration']))


def percentile_span(x, b=None):
    """pitch_emphasis/REPORT.md §2.1 #1: whole-clip voiced P90-P10 semitone span (before local centring)."""
    return subtract(x['pitch_span'], b, 'pitch_span')


def five_word_range(x, b=None):
    """pitch_emphasis/REPORT.md §3; product d3_pitch: regularised median-centred five-word ln range ratio."""
    return product_delta(x, b, 'D3')


def pitch_match(x, b=None):
    """pitch_emphasis/REPORT.md §2.1 #3: §4 #1: per-sentence Pearson word median F0 (clip-centred st), multiplied by defined share; report 1-match."""
    return sentence_match(x, b, 'med_s')


def prominence_agreement(x, b=None):
    """pitch_emphasis/REPORT.md §2.2, §4 #3: equal-weight own median/MAD z-score prominence-vector agreement; 1-Pearson."""
    return sentence_match(x, b, 'prominence')


def stress_spread(x, b=None):
    """pitch_emphasis/REPORT.md §4 #3: SD of equal-weight prominence points (chosen SD; no published cutoff)."""
    v = np.std(finite(x['prominence'])) if len(finite(x['prominence'])) else np.nan
    return v if b is None else v - stress_spread(b)


def two_sided_emphasis(x, b=None):
    """pitch_emphasis/REPORT.md §4 #6: lost reference prominence plus new function-word prominence; list is chosen prior."""
    p = x['prominence']
    function = np.array([w in FUNCTION_WORDS for w in x['norm']])
    if b is None:
        return np.where(function, np.maximum(p, 0), 0)
    r = b['prominence']
    stressed = np.zeros(len(p),bool); stressed[stress_words(r)] = True
    return np.where(stressed,np.maximum(r-p,0),0) + np.where(function & ~stressed & (p>=C.STRESS_P_MIN),
                                                          np.maximum(p-r,0),0)


def final_pitch_change(x, b=None):
    """pitch_emphasis/REPORT.md §2.3: §4 #4: median final-word last 200 ms minus preceding word stretch in st; full stops only."""
    return subtract(x['final_pitch'], b, 'final_pitch')


def declination(x, b=None):
    """pitch_emphasis/REPORT.md §2.3: OLS through all voiced sentence points, st/s; centring does not change slope."""
    return subtract(x['declination'], b, 'declination')


def contour_repetition(x, b=None):
    """pitch_emphasis/REPORT.md §4 #8 proposal: mean correlation of 32-point time-normalised sentence F0 contours."""
    v = mean([correlation(a, z) for i, a in enumerate(x['contours']) for z in x['contours'][i + 1:]])
    return v if b is None else v - contour_repetition(b)


def five_word_level(x, b=None):
    """volume_clarity/REPORT.md §3; product d5_volume: median-centred five-word level delta in dB."""
    return product_delta(x, b, 'D5')


def alpha_ratio(x, b=None):
    """volume_clarity/REPORT.md §2.1: 10log10 energy(1000-5000)/energy(50-1000), voiced words, dB; retain whole shift."""
    return subtract(x['alpha'], b, 'alpha')


def alpha_relative(x, b=None):
    """volume_clarity/REPORT.md §2.1, §4 #2: word alpha ratio minus own clip median, minus reference local value, dB."""
    return subtract(x['alpha_relative'], b, 'alpha_relative')


def spectral_emphasis(x, b=None):
    """volume_clarity/REPORT.md §2.1: L-L0 dB, 4th-order Butterworth at 1.5F0; frame-local filter approximation."""
    return subtract(x['spectral_emphasis'], b, 'spectral_emphasis')


def phrase_level_slope(x, b=None):
    """volume_clarity/REPORT.md §2.2: voiced-frame level OLS dB/s over text-punctuation phrases (chosen shared boundaries)."""
    return subtract(x['level_slopes'], b, 'level_slopes')


def last_word_drop(x, b=None):
    """volume_clarity/REPORT.md §2.2: last-word voiced level minus phrase voiced median in dB, then reference subtraction."""
    return subtract(x['last_drops'], b, 'last_drops')


def posterior_relative(x, b=None):
    """volume_clarity/REPORT.md §4 #1: aligned character posterior per word minus own clip median, minus reference value."""
    v = x['compat'] - median(x['compat'])
    return v if b is None else v - (b['compat'] - median(b['compat']))


def greedy_word_error(x, b=None):
    """volume_clarity/REPORT.md §4 #4: greedy word substitutions/deletions against prompt, binary per word; insertions separate."""
    return subtract(x['decode_errors'], b, 'decode_errors')


def band_envelope_match(x, b=None):
    """volume_clarity/REPORT.md §2.4, §4 #5: mean band envelope correlation after 32-point word warping; P-ESTOI-style proxy."""
    if b is None:
        return x['band_envelopes']
    return np.array([1 - mean([correlation(a, r) for a, r in zip(w, z)])
                     for w, z in zip(x['band_envelopes'], b['band_envelopes'])])


def modulation_depth(x, b=None):
    """volume_clarity/REPORT.md §4 #8: RMS 0.5-10 Hz envelope fluctuation / DC level; chosen band, not trained EMS/SRMR."""
    return subtract(x['modulation_depth'], b, 'modulation_depth')


def mid_band_share(x, b=None):
    """volume_clarity/REPORT.md §2.4, §4 #8: spectrum power share at 1-3 kHz on speech frames; dimensionless."""
    return subtract(x['mid_share'], b, 'mid_share')


def pause_share(x, b=None):
    """pace_pauses/REPORT.md §4 #10 open: total acoustic inter-word pause seconds divided by recording seconds."""
    v = np.sum(x['sil']) / float(x['duration'])
    return v if b is None else v - pause_share(b)


def rhythm_metrics(x, b=None):
    """pace_pauses/REPORT.md §4 #10 open: orthographic vowel %/VarcoV/nPVI on CTC character intervals; NOT phonetic rhythm."""
    ds = x['char_duration']
    v = ds[np.array([c in 'AEIOUY' for c in x['chars']])]
    if len(v) < 2 or v.mean() <= 0:
        return np.full(3, np.nan)
    out = np.array([100 * v.sum() / ds.sum(), 100 * v.std() / v.mean(),
                    100 * np.mean(np.abs(np.diff(v)) / ((v[:-1] + v[1:]) / 2))])
    return out if b is None else out - rhythm_metrics(b)


def pitch_level_baseline(x, b=None):
    """pitch_emphasis/REPORT.md §2.1 B; volume_clarity §2.3: median voiced F0 own-baseline difference in st; no anxiety labels."""
    return x['pitch_level'] if b is None else log_ratio(x['pitch_level'], b['pitch_level']) * 12 / np.log(2)


def silence_baseline(x, b=None):
    """pace_pauses/REPORT.md §2.1 B: silence-share difference against same-speaker baseline; styles do not label anxiety."""
    return silence_share(x, b)




FAMILIES = {
    'pace_pauses': (within_phrase_count, within_phrase_duration, speech_time_ratio, pause_count_ratio,
                    mean_pause_ratio, mean_run, latency_contour, production_contour, latency_residual,
                    production_residual, tempo_irregularity, tempo_drift, breath_candidates, breath_position,
                    pre_boundary_lengthening, silence_share, five_word_pace, five_word_pause),
    'disfluency': (inserted_material, orphan_voiced_gap, stability_run, within_word_silence,
                   word_duration_ratio, character_duration_ratio),
    'pitch_emphasis': (percentile_span, five_word_range, pitch_match, prominence_agreement, stress_spread,
                       two_sided_emphasis, final_pitch_change, declination, contour_repetition),
    'volume_clarity': (five_word_level, alpha_ratio, alpha_relative, spectral_emphasis, phrase_level_slope, last_word_drop,
                       posterior_relative, greedy_word_error, band_envelope_match, modulation_depth, mid_band_share),
    'open': (rhythm_metrics, pause_share, pitch_level_baseline, silence_baseline),
}
MEASURES = {fn.__name__: fn for fns in FAMILIES.values() for fn in fns}
