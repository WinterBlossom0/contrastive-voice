"""Exploratory delivery measurements; never part of the calibrated product detector."""
from cvoice.config import EVENT_TOL_S, PAUSE_MIN_S, R2_ALIGNMENT_SECONDS_PER_AUDIO, R2_ALIGNMENT_SECONDS_PER_CLIP

SEEDS = (17, 43, 97)
REFERENCE_COUNTS = (1, 3, 5, 10)
FALSE_RATE = 0.05
EVENT_TOLERANCE_S = EVENT_TOL_S
PAUSE_S = PAUSE_MIN_S
BREATH_S = 0.25
MAX_SECONDS = 3 * 3600
RESERVE_SECONDS = 15 * 60
# Three times the measured Kaggle T4x2 rate (118 clips of about 26 s prepared in 60 s on four workers);
# the preparation loop switches to the observed rate once it is slower.
EXPECTED_WALL_PER_AUDIO = R2_ALIGNMENT_SECONDS_PER_AUDIO
EXPECTED_WALL_PER_CLIP = R2_ALIGNMENT_SECONDS_PER_CLIP
NORMAL_SOURCES = ('gettysburg', 'poetry', 'vctk', 'accent', 'ears')
SOURCE_BUDGET = {'gettysburg': 700, 'ears': 2200, 'speechocean': 1400, 'avid': 950,
                 'disfluencyspeech': 300, 'podcastfillers': 550, 'expresso': 700, 'poetry': 450,
                 'accent': 850, 'vctk': 700, 'prominence': 700, 'mdvr': 400, 'lombard': 350, 'libristutter': 350}
SOURCE_ORDER = ('gettysburg', 'ears', 'speechocean', 'avid', 'disfluencyspeech', 'podcastfillers',
                'expresso', 'poetry', 'accent', 'vctk', 'prominence', 'mdvr', 'lombard', 'libristutter', 'sep28k')
