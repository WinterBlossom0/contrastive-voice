"""Exploratory delivery measurements; never part of the calibrated product detector."""
SEEDS = (17, 43, 97)
REFERENCE_COUNTS = (1, 3, 5, 10)
FALSE_RATE = 0.05
EVENT_TOLERANCE_S = 0.20
PAUSE_S = 0.20
BREATH_S = 0.25
from cvoice.config import BLOCK_S, STABLE_S, STABLE_PITCH_ST, STABLE_SPECTRUM, CONTOUR_POINTS, FUNCTION_WORDS  # noqa: F401
MAX_SECONDS = 3 * 3600
RESERVE_SECONDS = 15 * 60
# Three times the measured Kaggle T4x2 rate (cvoice-build v7: 118 clips of about 26 s prepared in 60 s on four workers);
# the preparation loop switches to the observed rate once it is slower.
EXPECTED_WALL_PER_AUDIO = 0.06
EXPECTED_WALL_PER_CLIP = 0.3
NORMAL_SOURCES = ('gettysburg', 'poetry', 'vctk', 'accent', 'ears')
SOURCE_BUDGET = {'gettysburg': 700, 'ears': 2200, 'speechocean': 1400, 'avid': 950,
                 'disfluencyspeech': 300, 'podcastfillers': 550, 'expresso': 700, 'poetry': 450,
                 'accent': 850, 'vctk': 700, 'prominence': 700, 'mdvr': 400, 'lombard': 350, 'libristutter': 350}
SOURCE_ORDER = ('gettysburg', 'ears', 'speechocean', 'avid', 'disfluencyspeech', 'podcastfillers',
                'expresso', 'poetry', 'accent', 'vctk', 'prominence', 'mdvr', 'lombard', 'libristutter', 'sep28k')
