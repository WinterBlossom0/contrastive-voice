import os

for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(k, "1")

import pytest  # noqa: E402
from synth import recording, regime  # noqa: E402

from cvoice import config as C  # noqa: E402
from cvoice.detect import make_detector  # noqa: E402


@pytest.fixture
def pinned_detector():
    """Detector with the design floors as scales, one pinned h for every flag key and the R1 design whole-clip thresholds
    in both regimes (for tests and fixtures; not calibrated)."""
    def make(h: float = 2.0):
        return make_detector({r: regime(r, h) for r in C.REGIMES}, dict(C.PMAX_START), {"calibrated": False})
    return make


@pytest.fixture(scope="module")
def base():
    """A 40-word synthetic recording with two pauses."""
    return recording(40, pauses={7: 0.7, 19: 0.8})
