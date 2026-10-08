"""Product prepare/cache/pool path, with one emission capture for greedy decode and character timing."""
from __future__ import annotations

import hashlib
from pathlib import Path
import traceback

import numpy as np

from cvoice import config as C
from cvoice.align import (Alignment, Transcript, align_emissions, load_aligner, parse_transcript)
from cvoice.audio import read_wav
from cvoice.features import Recording, WordStats, make_recording, window_word_time
from cvoice.features import recording_arrays as recording_arrays
from cvoice.pipeline import cache_key, prepare
from cvoice.pool import worker_aligner


def recording_view(x):
    tr = Transcript(tuple(x['disp']), tuple(x['norm']), tuple(x['sentence']), tuple(x['punctuation']),
                    tuple(x['syll']), (False,) * len(x['norm']))
    al = Alignment(x['start'], x['end'], x['compat'], float(np.mean(x['compat'])))
    ws = WordStats(x['ws_dur'], x['med_s'], x['p90_s'], x['p90_e'], x['mean_q'], x['u'])
    win = [None if a < 0 else (int(a),int(z)) for a,z in x['win']]
    return Recording(None, tr, al, None, x['regions'], ws, x['sil'], x['sil_span'], x['sil_raw'], x['m'], x['sigma'],
                     win, x['win_T'], x['win_R'], x['win_E'], x['win_Q'], window_word_time(x['start'], x['end'], win))


class Capture:
    """Adapter around the existing Aligner, capturing emissions without another model pass; local ownership chunks are 6 s."""
    def __init__(self, aligner, local):
        self.aligner, self.local, self.logp = aligner, local, None

    def emissions(self, wav):
        if not self.local or len(wav) <= 6*C.SR:
            self.logp = self.aligner.emissions(wav)
        else:
            parts, step, ctx = [], 6*C.SR, C.SR
            for a in range(0, len(wav), step):
                z = min(a+step,len(wav))
                a2,z2 = max(0,a-ctx),min(len(wav),z+ctx)
                lp = self.aligner.emissions(wav[a2:z2])
                f = (a-a2)//C.CTC_STRIDE
                keep = len(lp)-f if z==len(wav) else (z-a)//C.CTC_STRIDE
                parts.append(lp[f:f+keep])
            self.logp = np.concatenate(parts)
        return self.logp


def character_spans(logp, tr):
    al = align_emissions(logp, tr.norm)
    return np.diff(al.char_spans, axis=1).ravel(), [c for w in tr.norm for c in w]


def extract_one(row, cache, local=False):
    """A pool starmap unit catches failures per recording; local calls it directly in the sole process."""
    from .measures import compact_features
    try:
        path = Path(row['path'])
        if row.get('sha256'):
            with path.open('rb') as f:
                if hashlib.file_digest(f, 'sha256').hexdigest() != row['sha256']:
                    raise ValueError('canonical WAV checksum mismatch')
        wav = read_wav(path)
        tr = parse_transcript(row['text']) if row.get('text') else None
        proxy = tr is None
        # Text-free acoustics can run; proxy-dependent quantities are excluded from every scientific test.
        if proxy:
            tr = parse_transcript('AUDIO')
        version = hashlib.sha256(b''.join(p.read_bytes() for p in (Path(__file__),
            Path(__file__).with_name('measures.py'), Path(__file__).parent.parent / 'features.py',
            Path(C.__file__)))).hexdigest()[:12]
        Path(cache).mkdir(parents=True, exist_ok=True)
        sidecar = Path(cache) / ('lab_' + version + '_' + cache_key(wav,tr) + '.npz')
        if sidecar.exists():
            with np.load(sidecar) as z:
                return {'id': row['id'], 'features': {k:z[k] for k in z.files}, 'prompt_proxy': proxy, 'cached': True}
        if proxy:
            # A whole-clip region lets existing frame DSP serve text-free acoustics. No CTC or word claims.
            rec = make_recording(wav, tr, Alignment(np.array([0.]), np.array([len(wav)/C.SR]), np.array([np.nan]), np.nan))
            x = compact_features(rec, [], np.array([]), [])
            from .measures import runs
            from cvoice.align import pause_threshold
            silent = (rec.fr.L < pause_threshold(rec.fr.L)) & ~rec.fr.voiced
            spans = [(a*C.HOP_S,z*C.HOP_S) for a,z in runs(silent)]
            x['sil_span'] = np.array(spans).reshape(-1,2)
            x['sil'] = np.array([z-a for a,z in spans])
            x['prompt_proxy'] = np.array(True)
            np.savez_compressed(sidecar, **x)
            return {'id': row['id'], 'features': x, 'prompt_proxy': True, 'cached': False, 'alignment': 'not needed for clip acoustics'}
        aligner = worker_aligner() or load_aligner('cpu', 1)
        capture = Capture(aligner, local)
        rec = prepare(wav, tr, capture, Path(cache))
        decoded = rec.al.decoded
        durations = np.diff(rec.al.char_spans, axis=1).ravel()
        chars = [c for w in tr.norm for c in w]
        x = compact_features(rec, decoded,durations,chars)
        # Preserve independent verbatim counts even when there are no event time stamps.
        if row.get('verbatim'):
            from .measures import decode_edits
            words = [{'norm': w} for w in parse_transcript(row['verbatim']).norm]
            ins, _ = decode_edits(tr.norm,words)
            x['verbatim_insertions'] = len(ins)
        x['prompt_proxy'] = False
        x = {k:np.asarray(v) for k,v in x.items()}
        sidecar.parent.mkdir(parents=True,exist_ok=True)
        np.savez_compressed(sidecar,**x)
        return {'id':row['id'], 'features':x, 'prompt_proxy':proxy, 'cached':False}
    except Exception:
        return {'id':row['id'], 'error':traceback.format_exc()}
