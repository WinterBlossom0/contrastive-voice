"""One-clip smoke test (slow: loads the wav2vec2 aligner, about 1.2 GB RAM, a few seconds on CPU).

Runs the pipeline on the Reagan probe clip against itself (identity, R1: no flaws, score 100) and against one locally generated flawed
copy (one RUSH L3 span).
"""
from pathlib import Path

import pytest

from cvoice import audio, config as C, flaws
from cvoice.align import parse_transcript
from cvoice.events import iou
from cvoice.pipeline import analyze, dumps, prepare

FIX = Path(__file__).parent / "fixtures"


@pytest.mark.slow
def test_reagan_clip_identity_and_one_rush_l3_span(pinned_detector):
    wav = audio.read_wav(FIX / "reagan_open_16k.wav")
    tr = parse_transcript((FIX / "reagan_open.txt").read_text())
    det = pinned_detector(3.0)
    B = prepare(wav, tr)
    assert B.al.mean_compat > 0.8 and (B.al.compat >= C.LOW_COMPAT_NOTICE).mean() > 0.9  # research: 70 of 74 words valid on this clip

    meta_b = {"id": "reagan_open", "title": "Reagan, Challenger address (opening, development clip)", "audio": "reagan_open_16k.wav"}
    ident = analyze(B, tr, B, regime="R1", detector=det, baseline_meta=meta_b, participant_meta={"id": "identity", "audio": "reagan_open_16k.wav"})
    assert ident["flaws"] == [] and ident["scores"]["overall"] == 100.0
    assert all(d["score"] is None if d["key"] in C.OWNER_LISTED["R1"] else d["score"] == 100.0 for d in ident["scores"]["dims"])

    # one RUSH L3 span of 6 words inside one sentence, chosen in the baseline for content-word density (most syllables)
    sylls = [sum(tr.syll[i:i + 6]) if len(set(tr.sentence[i:i + 6])) == 1 else -1 for i in range(len(tr) - 5)]
    i0 = max(range(len(sylls)), key=lambda i: (sylls[i], -i))
    plan = flaws.Plan([flaws.make_edit(B, "RUSH", 3, (i0, i0 + 5))])
    y, lab = flaws.inject(B, plan, "smoke_rush_l3", "reagan_open", recipe="smoke_rush_l3", seed=flaws.clip_seed("smoke_rush_l3"))
    assert lab["outside_support_identical"] and len(y) < len(wav)
    P = prepare(y, tr)
    f = lab["flaws"][0]
    truth = [{"type": "RUSH", "dimension": "D1", "level": 3, "p": [round(f["span"][0] / C.SR, 3), round(f["span"][1] / C.SR, 3)]}]
    res = analyze(P, tr, B, regime="R1", detector=det, truth=truth, baseline_meta=meta_b,
                  participant_meta={"id": "rush_l3", "audio": "reagan_open_rush_l3.wav"})
    rush = [x for x in res["flaws"] if x["type"] == "RUSH"]
    best = max([iou(tuple(x["p"]), tuple(truth[0]["p"])) for x in rush], default=0.0)
    print(f"RUSH L3 span {truth[0]['p']} words {i0}-{i0 + 5}: flagged {[x['p'] for x in rush]}, IoU {best:.2f}, overall {res['scores']['overall']}, "
          f"P compat {[round(float(c), 2) for c in P.al.compat[i0:i0 + 6]]}")
    assert best >= C.IOU_MIN and res["scores"]["overall"] < 100.0  # flagged and localised (half-maximum rule, DESIGN 5.2)

    again = analyze(P, tr, B, regime="R1", detector=det, truth=truth, baseline_meta=meta_b,
                    participant_meta={"id": "rush_l3", "audio": "reagan_open_rush_l3.wav"})
    assert dumps(again) == dumps(res)  # two runs, identical JSON
