"""Evaluation tiers, frozen exemptions and realised-edit eligibility."""
from __future__ import annotations

import json
from pathlib import Path

from . import config as C
from .r2pool import digest

LAB_VALIDATION = Path(__file__).with_name('lab_validation.json')
LAB_RECIPES = {'natural_rush': 'NATURAL_RUSH'}
STRICT_ACCOUNTING = 'one detection per change; same-change duplicates reported separately'


def tiers(validation=None):
    validation = json.loads(LAB_VALIDATION.read_text()) if validation is None else validation
    passed = tuple(t for label, t in LAB_RECIPES.items() if validation.get('labels', {}).get(label, {}).get('lab_pass') is True)
    return {'core8': C.CORE8_TYPES, 'lab_passed': passed,
            'synthetic_only': tuple(t for t in C.EXTRA_TYPES if t not in passed)}


def exemption_policy():
    lists = {t: list(C.EXPECTED_SECONDARY[t]) for t in C.FLAW_TYPES}
    return {'lists': lists, 'same_change': dict(C.SAME_CHANGE), 'sha256': digest([lists, C.SAME_CHANGE]),
            'scope': 'registry frozen before the run; strict headline: ' + STRICT_ACCOUNTING + '. A region of a same_change '
                     'key within half a window of a truth of its value key duplicates that change\'s detection: it is not a '
                     'false region, and every strict count reports the number of such duplicates beside it'}


def invalid_reason(issue):
    return issue['reason'] in ('realised change below half target or wrong sign',
                               'prominence transfer cue has wrong sign', 'final contour does not rise by at least 1 st', 'non-monotone realised ladder',
                               'missing realised measurement', 'different ladder placements')


def label_eligibility(lab, issues):
    return {**lab, 'flaws': [{**f, 'evaluation_excluded': sorted({q['reason'] for q in issues
                            if invalid_reason(q) and q['type'] == f['type'] and
                            ('level' not in q or q['level'] == f['level']) and
                            ('words' not in q or q['words'] == f['words'])})} for f in lab['flaws']]}
