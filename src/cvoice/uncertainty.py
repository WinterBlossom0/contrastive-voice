"""95% intervals; bootstrap units are source speakers, never edited variants."""
from __future__ import annotations

import numpy as np
from scipy.stats import norm, chi2
from . import config as C


def wilson(k, n):
    if not n:
        return [None, None]
    z = norm.ppf(.975)
    p, d = k/n, 1+z*z/n
    c = (p+z*z/(2*n))/d
    r = z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return [max(0., float(c-r)), min(1., float(c+r))]


def proportion(k, n):
    return f"{k}/{n} (95% Wilson {wilson(k,n)})"


def cluster_interval(groups, statistic):
    values = list(groups.values())
    if len(values) < 2:
        return [None, None]
    rng = np.random.default_rng(C.SEED)
    samples = [statistic([x for i in rng.integers(len(values), size=len(values)) for x in values[i]])
               for _ in range(C.R2_BOOTSTRAPS)]
    samples = np.asarray(samples, float)
    samples = samples[np.isfinite(samples)]
    return np.quantile(samples, [.025,.975]).tolist() if len(samples) else [None,None]


# Fewer clusters give too few distinct resamples for a percentile interval (2 speakers give 3), so the per-cluster values are
# reported instead.
MIN_BOOTSTRAP_CLUSTERS = 5


def cluster_summary(groups, statistic, unit='speaker') -> dict:
    """The statistic's 95% cluster-bootstrap interval with at least MIN_BOOTSTRAP_CLUSTERS clusters; with fewer, the value
    of each cluster and their range, and no interval."""
    if len(groups) >= MIN_BOOTSTRAP_CLUSTERS:
        ci = cluster_interval(groups, statistic)
        return {'ci95': [None if v is None else round(float(v), 3) for v in ci], 'per_cluster': None, 'range': None,
                'method': f'95% {unit}-cluster percentile bootstrap ({len(groups)} {unit}s)'}
    values = {}
    for name, rows in groups.items():
        value = statistic(rows)
        values[name] = round(float(value), 3) if value is not None and np.isfinite(value) else None
    finite = [v for v in values.values() if v is not None]
    return {'ci95': [None, None], 'per_cluster': values, 'range': [min(finite), max(finite)] if finite else None,
            'method': f'per-{unit} values and their range ({len(groups)} {unit}s; no interval below {MIN_BOOTSTRAP_CLUSTERS})'}


def poisson(k, minutes):
    if minutes <= 0:
        return [None, None]
    return [float(chi2.ppf(.025, 2*k)/2/minutes) if k else 0.,
            float(chi2.ppf(.975, 2*(k+1))/2/minutes)]
