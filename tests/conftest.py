# Importing cvoice sets every config.THREAD_ENV variable to "1"; it must happen before synth imports numpy.
import cvoice  # noqa: F401
import pytest
from synth import recording, regime

from cvoice import config as C
from cvoice.detect import make_detector


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
