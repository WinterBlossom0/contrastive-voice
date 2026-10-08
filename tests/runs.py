"""Run builders, detectors and a fake check-reader dataset that several test modules share."""
from synth import regime

from cvoice import config as C
from cvoice.detect import make_detector
from cvoice.events import Run
from cvoice.score import score

R1_ENABLED = tuple(C.REGIME_DIMS['R1'])


def r1_run(base, comp, regions=(), scored=True):
    """Run of base against itself under the synthetic R1 regime; scored=False leaves the score out."""
    result = score(comp, [], regime('R1'), C.PMAX_START) if scored else None
    return Run(base, base, comp, list(regions), result, 'R1', {}, regime('R1')['scales'], R1_ENABLED)


def two_modes():
    """Uncalibrated detector with the single-reference and the five-reader consensus R2 modes."""
    single, consensus = regime('R2'), regime('R2', 4.)
    single['reference_mode'], consensus['reference_mode'] = 'single', 'consensus5'
    return make_detector({'R1': regime('R1'), 'R2': single, 'R2_consensus': consensus}, C.PMAX_START, {'calibrated': False})


def check_reader_dataset(readers, clip, lab, reference, participant):
    """Dataset of calibration readers and one check clip: every reader recording is `reference`, the clip is `participant`."""
    class CheckReaders:
        manifest = {'readers': readers}

        def clips(self, **kw):
            return [clip]

        def entry(self, kind, id):
            return {'id': id}

        def any_entry(self, id):
            return {'id': id}

        def parent_entry(self, c):
            return {'id': c['parent']}

        def rec(self, e):
            return reference

        def recs(self, entries):
            return [reference for e in entries]

        def clip_recs(self, clips):
            return [participant for c in clips]

        def load(self, **kw):
            pass

        def labels(self, c):
            return lab

    return CheckReaders()
