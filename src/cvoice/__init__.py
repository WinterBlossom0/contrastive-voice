"""Contrastive Voice: reference-relative speech delivery analysis."""
import os

from . import config as _config

for _k in _config.THREAD_ENV:  # single-threaded BLAS / OpenMP, set before numpy is first imported by a fresh process
    os.environ.setdefault(_k, "1")

__version__ = "0.1.0"
