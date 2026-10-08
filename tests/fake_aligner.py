"""A model-free aligner for the pool tests: log-probabilities that depend only on the audio length, so equal audio gives equal
alignments in any process. Imported by pool workers through the factory string 'fake_aligner:make'."""
import os
import time

import numpy as np

from cvoice import pool
from cvoice.align import LABELS

FAIL_LEN = 12345  # audio of this length raises
DIE_LEN = 12346  # audio of this length kills the worker process


class FakeAligner:
    def __init__(self, device: str, threads: int) -> None:
        self.device, self.threads = device, threads

    def emissions(self, wav: np.ndarray) -> np.ndarray:
        if len(wav) == FAIL_LEN:
            raise RuntimeError("planted failure")
        if len(wav) == DIE_LEN:
            os._exit(3)
        frames = (len(wav) - 400) // 320 + 1
        seed = len(wav) + (1 if self.device.startswith("cuda") else 0)  # a GPU "rounds differently": same audio, other numbers
        x = np.random.default_rng(seed).normal(size=(frames, len(LABELS)))
        return (x - np.log(np.exp(x).sum(1, keepdims=True))).astype(np.float32)


def make(device: str, threads: int) -> FakeAligner:
    return FakeAligner(device, threads)


def where() -> str:
    time.sleep(0.2)
    return pool.worker_aligner().device


def square(x: int) -> int:
    if x < 0:
        raise ValueError("negative")
    return x * x
