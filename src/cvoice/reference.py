"""Word-anchored reference features shared by the product and lab."""
from __future__ import annotations

import dataclasses
import warnings
import numpy as np
from . import config as C
from .align import Alignment
from .features import WordStats


# Text fields and per-reading event spans have no median: the first reading gives them.
PASS_THROUGH_KEYS = frozenset({'norm', 'disp', 'punct', 'punctuation', 'sentence', 'syll', 'chars', 'win', 'insertion_forms',
                               'inserted_spans', 'orphan_spans', 'stable_spans', 'word_silence_spans', 'sil_span'})


def median_reference(items):
    first = items[0]
    result = {}
    for key, value in first.items():
        if key in PASS_THROUGH_KEYS or value is None:
            result[key] = value
            continue
        vals = [np.asarray(v[key]) for v in items if key in v]
        if any(v.shape != np.asarray(value).shape for v in vals):
            result[key] = np.full(np.asarray(value).shape, np.nan)
            continue
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', RuntimeWarning)
            result[key] = np.nanmedian(np.stack(vals), axis=0)
    return result



def consensus_reference(references):
    if len(references) < C.CONSENSUS_K:
        raise ValueError('consensus requires five reference readings')
    refs = references[:C.CONSENSUS_K]
    first = refs[0]
    if any(r.tr.norm != first.tr.norm for r in refs):
        raise ValueError('consensus reference transcripts differ')
    fields = ('regions', 'sil', 'sil_raw', 'm', 'sigma', 'win_T', 'win_R', 'win_E', 'win_Q',
              'win_W', 'occ', 'final_df0', 'alpha_word')
    x = median_reference([{**{k: getattr(r, k) for k in fields},
                           'start': r.al.start, 'end': r.al.end, 'compat': r.al.compat,
                           **{k: getattr(r.ws, k) for k in WordStats.__dataclass_fields__}} for r in refs])
    compat = x.pop('compat')
    al = Alignment(x.pop('start'), x.pop('end'), compat, float(np.mean(compat)))
    ws = WordStats(**{k: x.pop(k) for k in WordStats.__dataclass_fields__})
    return dataclasses.replace(first, al=al, ws=ws, **x)


def select_reference(references, detector, regime):
    refs = list(references)
    if not refs:
        raise ValueError('at least one reference reading is required')
    consensus = regime == 'R2' and len(refs) >= C.CONSENSUS_K
    if consensus and 'R2_consensus' not in detector['regimes']:
        raise ValueError('detector has no calibrated consensus mode')
    return (consensus_reference(refs) if consensus else refs[0],
            detector['regimes']['R2_consensus' if consensus else regime],
            'consensus5' if consensus else 'single', C.CONSENSUS_K if consensus else 1)
