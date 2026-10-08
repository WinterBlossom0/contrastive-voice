Added [edits_extra.py](<../../src/cvoice/edits_extra.py>) and [test_edits_extra.py](<../../tests/test_edits_extra.py>). Each recipe returns `(audio, Chain, labels)`; `level=None` is bit-identical. Configuration, dataset composition, and existing edits were unchanged.

Sources: **P** = pace_pauses/REPORT.md; **D** = disfluency/REPORT.md; **E** = pitch_emphasis/REPORT.md; **V** = volume_clarity/REPORT.md. References are §4 unless indicated. **Chosen** means an engineering setting, not published severity calibration.

| Function | L1 / L2 / L3 parameters and source | Approximation |
|---|---|---|
| `natural_rushing` | Speech rate 1.13/1.15/1.18 (P §1: 13–18% increase); pause fractions .6/.3/0, chosen | Aligned words represent speech; unclassified short gaps remain |
| `hesitation_before_word` | Duration ×1.2/1.5/1.8, chosen; silence .2/.5/1 s (P: .2–1 s) | Content-word prior |
| `word_by_word_reading` | Silence .15/.225/.3 s; every 1 or 2 words (P) | Word boundaries |
| `uneven_tempo` | Maximum duration deviations .15/.3/.45, chosen (P: mean-one random factors) | Mean-one nominal factors; integer rounding ≤½ sample per word |
| `word_repetition` | One copy; first duration ×1.05/1.10/1.15, chosen; pauses .1/.225/.35 s (D: 100–350 ms) | Function-word prior; copied waveform |
| `sound_repetition` | 2/3/4 copies; .1 s pauses (D: 2–5 copies, 100–350 ms) | First 20% onset proxy or supplied sound span; caller selects stressed word |
| `rhyme_prolongation` | Last 20% ×2/3.5/5 (D: last 20% ×5; lower factors chosen) | Fraction approximates rhyme; supplied span supported |
| `onset_prolongation` | Target .35/.65/1 s, chosen (D: onset prolongations around/exceeding 1 s) | First 20% continuant proxy or supplied span |
| `block_before_release` | Silence .5/1.25/2 s (D: .5–2 s) | Release at 80% of word or supplied sample; gap only |
| `low_vocal_effort` | Attenuation 3/6/9 dB; tilt 2/4/6 dB/oct; pitch lowering .5/1/1.5 st, all chosen (V) | Gain/tilt/F0 proxy; formants and vowel shortening omitted |
| `trailing_off` | Final attenuation 4/8/12 dB; tilt 2/4/6 dB/oct, chosen (V) | Aligned sentence ramp; lax phonation omitted |
| `misplaced_emphasis` | Function duration ×1.1/1.2/1.3, pitch +2/+4/+6 st, gain +2/+4/+6 dB; stressed-word removal .3/.6/.9, chosen (E) | Caller identifies stressed word |
| `rising_ending` | Rise 2/4/6 st, chosen; last .25 s (E: 200–300 ms) | Window clipped to final word |
| `flattened_final_fall` | Strength ⅓/⅔/1, chosen (E) | Same window; target preceding-word median pitch |
| `repeated_contour` | Strength ⅓/⅔/1, chosen (E) | Linear sentence-time warp; interpolation across unvoiced template gaps |

Both tilt recipes use a chosen 250 Hz knee.

Sample maps and event spans are exact for the implemented edits. Anatomical sound/syllable/release locations cannot be exact without finer annotation: fractional proxies carry uncertainty up to the aligned word’s duration, plus empirical alignment error of 48–89 ms. PSOLA pitch realisation is approximate. Blocks lack tense closure; vocal-effort recipes omit some physiological changes. Background noise can mask spectral-balance progression; the harmonic-rich synthetic case verifies increasing tilt.

Filled pauses are out of scope because they require a recorded filler.

Validation:

- `.venv/bin/python -m pytest -q tests/test_edits_extra.py` — **25 passed**.
- `.venv/bin/python -m pytest -q` — **259 passed, 2 deselected**.
- `.venv/bin/ruff check --select F,E9 src tests` — **passed**.

Dataset wiring needs these type registrations and secondary-effect allowances:

| Type | Primary dimension | Expected secondary dimensions |
|---|---|---|
| `NATURAL_RUSH`, `HESITATION` | D1 | D2, D4 |
| `WORD_BY_WORD` | D2 | D1 |
| `UNEVEN_TEMPO` | D1 | D4, D6 |
| `WORD_REPETITION` | DISFLUENCY | D1, D2 |
| `SOUND_REPETITION`, `BLOCK` | DISFLUENCY | D1, D2, D6 |
| `RHYME_PROLONGATION` | DISFLUENCY | D1, D4 |
| `ONSET_PROLONGATION` | DISFLUENCY | D1, D6 |
| `LOW_EFFORT` | D5 | D3, D4, D6 |
| `TRAILING_OFF` | D5 | D4, D6 |
| `MISPLACED_EMPHASIS` | D4 | D1, D3, D5 |
| `RISING_ENDING`, `FLAT_FINAL_FALL` | ENDINGS | D3, D4 |
| `REPEATED_CONTOUR` | D3 | D4 |

The adapter must preserve structured parameters, supports and inserted-copy spans; select eligible words/sentences; and supply phone annotations where available. `DISFLUENCY` and `ENDINGS` need versioned registry/scoring support without changing the released detector’s hashed configuration.