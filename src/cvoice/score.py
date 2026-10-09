"""Scores: severity in physical units, region mass, S_k = 100 max(0, 1 - P_k / Pmax_k), overall = mean of the
scored dimensions, and the closed-form "points lost" / "score with this penalty removed" (arithmetic on the current result)."""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from . import config as C
from .compare import Comparison, Dim
from .detect import Region, clip_flags, flagged_dims, scale, threshold
from .patterns import counted


def severity(x: float, theta: float, sat: float) -> float:
    """clip((|x| - theta) / (sat - theta), 0, 1); a deviation at or beyond saturation below the threshold counts fully."""
    if sat <= theta:
        return 1.0 if abs(x) >= theta else 0.0
    return float(np.clip((abs(x) - theta) / (sat - theta), 0.0, 1.0))


def _saturation(nominal: float, theta: float, r2: bool) -> float:
    """In R2 the saturation is at least R2_SAT_THRESHOLD_FACTOR times the threshold."""
    return max(nominal, C.R2_SAT_THRESHOLD_FACTOR * theta) if r2 else nominal


def unit_severity(dim: Dim, i: int, unit_scale: float, h: float, r2: bool = False) -> float:
    theta = h * unit_scale
    return severity(float(dim.x[i]), theta, _saturation(C.X_SAT[dim.key], theta, r2))


def region_mass(dim: Dim, region: Region, unit_scale: float, h: float, r2: bool = False) -> float:
    """m_r = sum over the region's units of w_u * sev_u."""
    return float(sum(dim.w[i] * unit_severity(dim, i, unit_scale, h, r2) for i in region.units if np.isfinite(dim.x[i])))


def clip_mass(dim: str, g: float, theta: float, r2: bool = False) -> float:
    """Mass of a whole-clip flag: the severity of the clip median g between its threshold and the dimension's saturation."""
    return severity(g, theta, _saturation(C.CLIP_SAT[dim], theta, r2))


def dim_score(P: float, pmax: float) -> float:
    return 100.0 * max(0.0, 1.0 - P / pmax)


def scored_dimensions(comp: Comparison, regions: list[Region], regime: dict) -> tuple[str, ...]:
    """Enabled dimensions with sufficient coverage or a flag on the measured evidence."""
    flagged = {r.dim for r in regions} | set(clip_flags(comp, regime))
    return tuple(k for k in flagged_dims(regime) if k in comp.dims and (comp.coverage.get(k, 1.0) >= C.MIN_MEASUREMENT_COVERAGE or k in flagged))


def overall(P: dict[str, float], pmax: dict[str, float], scored_dims: tuple[str, ...] | list[str]) -> float | None:
    """The same masked mean for runtime, score gates and every Pmax candidate."""
    return float(np.mean([dim_score(P[k], pmax[k]) for k in scored_dims])) if scored_dims else None


@dataclass
class Scored:
    """P: penalty per dimension; S: score per dimension (None where not scored); overall: mean of scored S (None when
    nothing is scored); masses: region masses in the order of the regions given; clip: mass per whole-clip flag."""
    P: dict[str, float]
    S: dict[str, float | None]
    overall: float | None
    masses: list[float]
    clip: dict[str, float]
    pmax: dict[str, float] = field(default_factory=dict)
    coverage: dict[str, float] = field(default_factory=dict)

    def points_lost(self, dim: str, mass: float) -> tuple[float, float | None]:
        """(overall points lost, score with this penalty removed) when `mass` of dimension `dim` is removed."""
        if self.overall is None or self.S[dim] is None:
            return 0.0, self.overall
        scored = tuple(k for k, v in self.S.items() if v is not None)
        penalties = {**self.P, dim: max(self.P[dim] - mass, 0.0)}
        overall_fixed = overall(penalties, self.pmax, scored)
        return overall_fixed - self.overall, overall_fixed


def score(comp: Comparison, regions: list[Region], regime: dict, pmax: dict[str, float]) -> Scored:
    """Score one comparison. A dimension with low coverage is unscored unless it carries a flag."""
    coverage = {k: comp.coverage.get(k, 1.0) for k in C.DIMS}
    scored_dims = scored_dimensions(comp, regions, regime)
    r2 = regime["name"] == "R2"
    P = {k: 0.0 for k in C.DIMS}
    masses = []
    for r in regions:
        m = region_mass(comp.dims[r.dim], r, scale(regime, r.dim, r.sign), threshold(regime, r.dim, r.sign), r2) if r.dim in scored_dims else 0.0
        masses.append(m)
    flags = clip_flags(comp, regime)
    keep = counted(comp, regions, masses, flags)
    masses = [m if j in keep else 0.0 for j, m in enumerate(masses)]
    for r, m in zip(regions, masses):
        P[r.dim] += m
    clip = {k: clip_mass(k, g, regime["clip"][k], r2) for k, g in flags.items() if k in scored_dims}
    for k, m in clip.items():
        P[k] += m
    S = {k: (dim_score(P[k], pmax[k]) if k in scored_dims else None) for k in C.DIMS}
    return Scored(P, S, overall(P, pmax, scored_dims), masses, clip, dict(pmax), coverage)
