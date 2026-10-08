# Reproducibility, packaging, deployment and documentation

Date: 2026-10-01. Topic: `repro_packaging`. This is a research handoff, not a built or published product. Paths are relative to this topic directory unless stated otherwise. The earlier runs' evidence is retained; the final version-3 outputs were recovered into `kaggle_out/` during this run. No installations, model executions, Docker builds, servers or DSP were run locally during this finishing session.

## Recommendation and evidence labels

Ship three artifacts from the same release: **a zero-install GitHub Pages gallery**, **a public prebuilt CPU image with its checkpoint and FFmpeg**, and **a Python 3.12 uv project with a committed lock**. Build data and train on Kaggle; make the final reproduction entry point accessible from the public repository. Keep the gallery usable independently of any inference host. This answers J-01, J-05 and J-13 without changing the owner's FastAPI + one static HTML/JS page decision.

- **VERIFIED_BY_RUNNING (K1/K2/K3)**: private CPU kernel `electroknight/cvoice-probe-repro-packaging`, versions 1/2/3; `kaggle_out_v1/`, `kaggle_out_v2/`, `kaggle_out/`. Elapsed times: 682.6 / 308.0 / 339.5 seconds (`results.json`, `elapsed_s`).
- **VERIFIED_BY_RUNNING (L)**: preserved earlier local outputs; these predate the current restriction or were permitted PDF probes. They do not authorize repeating those computations locally.
- **VERIFIED_BY_SOURCE (S)**: fetched official URLs, linked near claims; retained text under `web/` or in the two condensed logs.
- **UNVERIFIED (U)**: proposed integration, acceptance threshold or estimate. Product commands below are implementation contracts; the existing `recommended_lock/src/cvoice/cli.py` only prints import versions.

## 1. Reproducibility contract

**Recommendation (U):** distinguish repeatability with fixed artifacts and execution settings from numerical agreement across environments. A lock, seed and image identify inputs and software; they do not guarantee all floating-point operations are identical across CPU architectures. Test the actual published output, including decisions near thresholds.

| Source of variation | Observed evidence | Build rule |
|---|---|---|
| Decode libraries and WAV metadata | K3 `decode_compare.json`: FFmpeg versus libsndfile MP3 float32 max difference `8.3819e-7`; 0.026834% of PCM16 samples differ by one LSB. Ogg: max `4.1723e-7`, 0.027657% differ by one LSB. WAV container headers differ across binaries. | Decode a baseline once on Kaggle; distribute canonical lossless audio. Record original and decoded PCM hashes, sample count, channel policy, decoder version and crop coordinates. |
| Encoder delay/padding and crop origins | K3 `sf_mp3`: 11,280,384 frames at 44,100 Hz, 255.7910204 s; nominal duration is not an exact sample count. | Use decoded sample coordinates. Specify start/end as half-open integer samples. Preserve codec delay/padding handling; do not relabel using rounded media duration. |
| Stereo mixing | K3 `decode_compare.json`: channel correlation `-0.993384`; mean `(L+R)/2` RMS `-56.6103 dBFS`, side `(L-R)/2` `-32.3091`. | Record channel policy per source. Use left for this Reagan source; side is a documented alternative. Never silently average anti-phase stereo. Rebuild downstream labels if policy changes. |
| Resampler algorithm/build | K1 `resample_sys.json`: soxr HQ versus swr max `0.00501623`, 44.48% PCM16 disagreement; algorithms can differ by one output sample. K3 static FFmpeg soxr versus Python soxr HQ differs by `5.9605e-8` even on identical decoded input. | Use one explicit resampling path: decoded float32 → `soxr.resample(..., quality="HQ")` → 16 kHz. No implicit `librosa.load` resampling or interchangeable swr/scipy/torchaudio paths. |
| BLAS/OpenMP and Torch threads | L `det/compare.out`: emissions change by about `0.0035` with thread count; MFCC changes by `6.1035e-5` with BLAS settings. K3 one-thread emissions still differ across CPUs. | Set thread environment before imports, Torch intra/inter-op threads to 1, one analysis worker, float32 CPU inference. Log effective thread pools. |
| CPU/GPU arithmetic | L `gpu_cpu_drift.out`: CPU versus CUDA max emission difference `0.06942`; FP16 versus CUDA FP32 `0.6303`. Paths/times matched on this clip only. | CPU FP32 is the supported reproduction target. GPU/AMP needs its own validation; it is unnecessary for the tested build. |
| Numba JIT | K1 `s10_nojit`: JIT versus disabled JIT pYIN test identical; cross-session pYIN hashes matched in K3. First call pays compilation cost. | Keep pinned numba/llvmlite and JIT enabled; set `NUMBA_NUM_THREADS=1`, cache under writable `/tmp` or working directory. Do not disable JIT solely for determinism. |
| Praat RNG in duration edits | K3 `psola_p1.json`: unseeded duration x0.7 max waveform difference `0.134774`; even a duration tier of x1.0 changed between calls. Seeding fixed x0.7 within a process and x0.7/x1.4 hashes across two processes. | Reset Praat's own RNG immediately before each duration-edit recipe; Python/NumPy/Torch seeds do not seed it. Include seed in manifest. |
| ML fitting and sample order | K3 `s7_sklearn`, K2→K3 `s13_cross_session`: tested logistic regression/GBM outputs and coefficients matched. | Sort manifests, freeze group splits, pass integer `random_state`, seed generators explicitly. Repeatability does not establish model validity. |
| JSON | L `json_canon.out`: NaN/Infinity invalid for browser JSON; negative zero, key order and floating-point widening alter bytes. Rounding can disagree at bin boundaries. | Finite Python scalars; null for missing values; sorted keys, compact separators, UTF-8, fixed field precision. Keep wall-clock metadata separate. Compare numeric values before rounding. |

Recommended runtime preamble (U integration; its settings were individually probed):

```bash
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
export NUMBA_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 PYTHONHASHSEED=0
```

```python
import random
import numpy as np
import torch
random.seed(42)
np.random.seed(42)
torch.manual_seed(42)
torch.set_num_threads(1)
torch.set_num_interop_threads(1)
torch.use_deterministic_algorithms(True)
# Load model once; model.eval(); inference inside torch.inference_mode().
```

**VERIFIED_BY_RUNNING:** the Praat call is `parselmouth.praat.run("random_initializeWithSeedUnsafelyButPredictably: 42")`, immediately before the edit (`kaggle_src/psola.py`, `kaggle_out/psola_p1.json`, `psola_p2.json`, `results.json:s15_psola`). Its process-global state requires serialized calls. Seed 42 is the tested seed; per-example derived seeds need a separate regeneration test. Cross-architecture seeded PSOLA hashes have not been established.

Canonical audio: 16 kHz mono PCM16 lossless WAV/FLAC for distribution, float32 in analysis; quantize with `clip(rint(x * 32768), -32768, 32767).astype('<i2')`. Hash raw little-endian PCM bytes and separately hash file bytes. Canonical crop, fade, gain, rounding and sample-length policies belong in the recipe. This is a proposed contract; do not replace an existing dataset's quantizer without regenerating labels.

For unfamiliar containers, decode with the pinned FFmpeg binary at native rate, choose the declared channel, then resample in Python. For a known baseline, consume the canonical file directly. `-ac 1` in a generic FFmpeg command is inappropriate for the anti-phase Reagan source. Full-file bytes can differ despite identical data chunks; the earlier bitexact WAV experiment removed the encoder metadata (`decode_determinism.out`).

JSON rule (U): timestamps and displayed feature values to 3 decimals; rubric indices on a 0–100 scale to 1 decimal; preserve integer samples/frames as primary coordinates. Serialize with `json.dumps(..., sort_keys=True, separators=(",", ":"), allow_nan=False, ensure_ascii=False)` after sanitization and normalizing `-0.0`. Cache by PCM hash, normalized transcript hash, config hash, model hash and code release. Put environment/run stamps in a separate file.

### Golden tests and tolerances

For numeric arrays compare finite/missing masks and require `abs(a-b) <= atol + rtol*abs(reference)`; never compare only means. Hashes establish exact identity; tolerance comparisons establish bounded numerical agreement. They are different tests.

| Release check | Proposed acceptance (U, not measured on final scorer) |
|---|---|
| Same canonical fixture + fixed CPU profile, second call and fresh process | Exact PCM/recipe hashes, word/frame indices, region types and sanitized result JSON; if bytes differ, publish the differing fields and numeric comparison. |
| Kaggle → Docker → CI on the same canonical fixture | Identical token/word sequence, mask, category decisions and region count; timestamp max difference ≤ 0.001 s, rubric index difference ≤ 0.1 on 0–100 scale. Any threshold flip fails. |
| Diagnostic float features | MFCC `atol=1e-4, rtol=1e-5`; emitted log scores `atol=0.005, rtol=1e-5`; F0 `atol=0.01 Hz, rtol=1e-6`; RMS dB `atol=1e-4, rtol=1e-5`. Initial gates for fixed canonical audio, subject to validation. |
| Alternative decoder stress input | Report PCM max-LSB/sample mismatch and alignment/score shift separately. Do not loosen the canonical-input gate to hide a different decoder. |
| Dataset regeneration | Exact generated PCM hashes within the canonical build environment. Verify recipe, transformed sample count, label validity and split membership together. |

K3 versus preserved local one-thread reference: max emission difference `0.0034685135`, alignment integer path identical; alignment-score max `0.0004402399` (`kaggle_out/cmp_venv312.json`, `LOCAL_C_t1 vs K_t1_a`). With all thread variables set to 1, MFCC hashes matched the separately controlled local `I_omp1` run (`results.json:s3_determinism:canon_equals_laptop`). These are one-clip diagnostics, **not a tested score-tolerance contract**. Boundaries have roughly 20 ms CTC frame spacing; 1 ms is the environment-agreement gate, not a claim of 1 ms ground-truth accuracy.

I-21 is answered by separating repeatability, environment agreement and artifact regeneration. I-10/M-06/M-14 concern robustness to benign recording changes, which is distinct: K3 `gain.json` found up to 20 ms boundary shifts after changing gain. Dataset/feature research must still test noise, room, codecs and microphone effects. A deterministic scorer can remain biased or unstable under those changes.

## 2. Final pyproject and uv recipe

**VERIFIED_BY_RUNNING:** use `recommended_lock/pyproject.toml` and `recommended_lock/uv.lock`, not the older broad candidate locks. K3 `uv sync --locked --no-dev --group data`, import smoke, Torch/torchaudio forced-alignment path and CLI import entry all succeeded on Linux x86_64. Lock SHA256: `dcc0c301bd05b6b88fe70eedf9b73ed2b89b5737a0543c827439a008e664d819` (99,425 bytes).

```toml
[project]
name = "cvoice"
version = "0.1.0"
description = "Contrastive speech analytics and temporal flaw grounding"
readme = "README.md"
requires-python = ">=3.12,<3.13"
dependencies = [
  "torch==2.14.1", "torchaudio==2.11.0",
  "numpy==2.5.3", "scipy==1.18.1", "librosa==1.0.0",
  "numba==0.68.0", "soundfile==0.14.0", "soxr==1.1.0",
  "praat-parselmouth==0.4.7", "scikit-learn==1.9.1",
  "fastapi==0.142.2", "uvicorn==0.54.0", "python-multipart==0.0.32",
]
[project.scripts]
cvoice = "cvoice.cli:main"
[dependency-groups]
dev = ["pytest==9.1.1", "ruff==0.16.9"]
data = ["pyworld-prebuilt==0.3.6.post1", "imageio-ffmpeg==0.6.0"]
[tool.uv]
required-version = ">=0.12.3,<0.13"
exclude-newer = "2026-10-01T00:00:00Z"
required-environments = [
  "sys_platform == 'linux' and platform_machine == 'x86_64'",
  "sys_platform == 'darwin' and platform_machine == 'arm64'",
  "sys_platform == 'win32' and platform_machine == 'AMD64'",
]
[tool.uv.sources]
torch = [{ index = "pytorch-cpu" }]
torchaudio = [{ index = "pytorch-cpu" }]
[[tool.uv.index]]
name = "pytorch-cpu"
url = "https://download.pytorch.org/whl/cpu"
explicit = true
[build-system]
requires = ["uv_build>=0.12.3,<0.13.0"]
build-backend = "uv_build"
```

The explicit index routes only Torch packages there. PEP 440 pins without `+cpu` select Linux/Windows CPU wheels while admitting macOS wheels without that suffix. The actual tested Linux pair is **torch 2.14.1+cpu / torchaudio 2.11.0+cpu**; do not substitute remembered version pairings. Source behavior: [uv PyTorch guide](https://docs.astral.sh/uv/guides/integration/pytorch/), retained `web/uv_pytorch.md`.

The source-tested build backend range is not an exact build-tool lock. **Recommendation (U):** put `uv_build==0.12.3` in `build-constraints.txt` and add `--build-constraint build-constraints.txt` to every sync; this release exists ([PyPI metadata](https://pypi.org/pypi/uv_build/0.12.3/json), `web/uv_build_0123.json`). That additional constraint was not in K3. Alternatively pin the backend directly and refresh/check the project lock in build CI. Do not call the original lock a complete OS/build-tool lock.

```bash
# On Kaggle/CI or a user's own machine; not run locally in this research session.
python -m pip install uv==0.12.3
uv python install 3.12.13
uv sync --locked --python 3.12.13 --no-dev --group data \
  --build-constraint build-constraints.txt
uv run --no-sync cvoice verify
```

Commit `.python-version` containing `3.12.13`; CI/release uses uv 0.12.3 even though project metadata permits later 0.12 patches. A normal contributor sync includes `dev`; `--no-dev` excludes it. The `data` group is not installed automatically. TTS, download/plot tools or additional detectors are **not** covered by this minimal lock; add only the chosen implementations to named groups, regenerate the lock and verify them on Kaggle before claiming a complete dataset build.

| Python/platform option | Evidence | Decision |
|---|---|---|
| Python 3.12, Linux x86_64 | K3 locked project works; all tested imports and algorithms pass | Canonical target, matching Kaggle. |
| Python 3.13 | L earlier imports and `probe_uv_py313/uv.lock`; broad superset resolution in `lock_superset_313/` | No benefit sufficient to change canonical version; final product untested. |
| Python 3.14 | K1 `s9_py314` imports/algorithms with an earlier lock; `lock_superset_314/` exposes auxiliary-package wheel gaps | Some stack components work; no promise for the final dataset/TTS stack. |
| macOS arm64 / Windows AMD64, Python 3.12 | Wheel URLs in the final lock; resolver required-environment checks | Source/resolution coverage only, not execution verification. macOS Torch wheel requires macOS 14. |

`pyworld==0.3.5` lacked Linux wheels in earlier metadata; avoid a compiler-heavy source build. `pyworld-prebuilt==0.3.6.post1` imports as `pyworld` and was run-tested in K3 for WORLD extraction/synthesis. Its wheel/platform description is [publisher metadata](https://pypi.org/pypi/pyworld-prebuilt/0.3.6.post1/json), saved `web/pyworld_prebuilt.json`. Do not install both distributions.

K3 size/time: data-group environment **1,292 MiB**, uv cache **1,292 MiB**, managed Python **104 MiB**; cold sync **10.67 s**, uv install **5.70 s**, managed Python fetch **1.85 s**, imports **5.87 s** (`results.json:s1_uv`; size values come from `du -sm`). These are observed network/cache conditions, not a startup promise. Model file adds 377,664,473 bytes (~360.17 MiB); model copies in multiple caches increase disk usage. K1 bytecode compilation increased an older environment from 1,322 to 1,505 MiB, so omit blanket bytecode compilation for the small image.

## 3. Checkpoint pinning and offline behavior

**VERIFIED_BY_RUNNING:** `WAV2VEC2_ASR_BASE_960H` checkpoint:

- URL: `https://download.pytorch.org/torchaudio/models/wav2vec2_fairseq_base_ls960_asr_ls960.pth`
- Bytes: `377664473`.
- SHA256: `488fd4f16de84438ffc945334278c1b9fb9b7159a806c1080b16111a958c945d`.
- Bundle cache: `$TORCH_HOME/hub/checkpoints/wav2vec2_fairseq_base_ls960_asr_ls960.pth`.

K2/K3 `results.json:s3a_weights` matched the preserved laptop hash. K1 `s6_offline` loaded the cached model with network socket creation denied; empty-cache negative control failed as expected. Hash it during acquisition **and at startup**; a URL or ETag alone is not the content identity. `TORCH_HOME` must point to the baked readable cache before model construction; this torchaudio path does not honor Hugging Face offline flags. See [bundle documentation](https://docs.pytorch.org/audio/2.11.0/generated/torchaudio.pipelines.Wav2Vec2ASRBundle.html).

If a selected TTS/model uses Hugging Face, freeze the full revision commit, individual artifact SHA256s, tokenizer/vocabulary/preprocessor configs and license. Use local paths or `local_files_only=True` after acquisition; set `HF_HOME`, `HF_HUB_OFFLINE=1`, `HF_HUB_DISABLE_TELEMETRY=1`, and `TRANSFORMERS_OFFLINE=1` if Transformers is used. Source: [download revision guidance](https://huggingface.co/docs/huggingface_hub/en/guides/download), [Hub environment variables](https://huggingface.co/docs/huggingface_hub/en/package_reference/environment_variables), saved `web/hf_environment.html`.

An ONNX alternative was investigated, not selected: `onnxruntime==1.30.0`, Xenova revision `a19f851b3d42865797e410752b4c570c871e4825`, FP32 model SHA256 `e46614273f03ff4b87923a965e417fa72004825522cb007c9c25633b8475490d`; 377,887,594 bytes. K3 `ort.json` showed identical emissions at 1 and 4 threads and across two AMD sessions; isolated environment 148 MiB. However `viterbi.json` failed on all inputs (`int8` predecessor/state overflow at 578 states). No end-to-end ONNX forced alignment or Torch parity was verified. Fix the state-index dtype and compare transcript-normalization/blank conventions before replacing Torch. Do not advertise this experiment as a ready smaller backend.

## 4. Docker and prebuilt image recipe

**Recommendation (U):** a single Linux amd64 Python slim image, the same lock, pinned static FFmpeg from `imageio-ffmpeg`, baked checkpoint, fixtures/gallery and fitted detector. Keep the data group in this initial image to reuse the verified stack; separating only FFmpeg into a runtime group is a later optimization. Avoid unpinned distro FFmpeg for the canonical path. K3 binary was FFmpeg **7.0.2-static**, ~79.8 MiB; no `ffprobe` binary is supplied by that wheel.

This is the final recipe to implement and validate in hosted build CI, **not a locally built/tested Dockerfile**. `PYTHON_BASE` and `UV_IMAGE` must be supplied as verified image digest references in the release workflow; exact digests do not yet exist in these notes. The Python base must contain Python 3.12.13 and match the target architecture. Use `python:3.12.13-slim-bookworm` only after checking that tag, then resolve its digest; never invent a digest.

```dockerfile
# syntax=docker/dockerfile:1
ARG PYTHON_BASE
ARG UV_IMAGE
FROM ${UV_IMAGE} AS uvbin
FROM ${PYTHON_BASE}
COPY --from=uvbin /uv /usr/local/bin/uv
ENV UV_PYTHON_DOWNLOADS=never UV_LINK_MODE=copy \
    PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
    NUMBA_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 PYTHONHASHSEED=0 \
    TORCH_HOME=/opt/torch HF_HOME=/tmp/hf HF_HUB_OFFLINE=1 \
    HF_HUB_DISABLE_TELEMETRY=1 NUMBA_CACHE_DIR=/tmp/numba
WORKDIR /app
COPY pyproject.toml uv.lock .python-version build-constraints.txt README.md ./
RUN uv sync --locked --no-dev --group data --no-install-project \
    --build-constraint build-constraints.txt --no-cache
COPY src/ ./src/
RUN uv sync --locked --no-dev --group data --no-editable \
    --build-constraint build-constraints.txt --no-cache
RUN ln -s "$(/app/.venv/bin/python -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())')" /usr/local/bin/ffmpeg
ADD --checksum=sha256:488fd4f16de84438ffc945334278c1b9fb9b7159a806c1080b16111a958c945d \
    https://download.pytorch.org/torchaudio/models/wav2vec2_fairseq_base_ls960_asr_ls960.pth \
    /opt/torch/hub/checkpoints/wav2vec2_fairseq_base_ls960_asr_ls960.pth
RUN chmod 644 /opt/torch/hub/checkpoints/*.pth
COPY frontend/ ./frontend/
COPY config/ ./config/
COPY artifacts/ ./artifacts/
COPY demo/ ./demo/
COPY LICENSES/ ./LICENSES/
RUN useradd --uid 1000 --create-home appuser
USER 1000
EXPOSE 7860
CMD ["/app/.venv/bin/uvicorn", "cvoice.api:app", "--host", "0.0.0.0", "--port", "7860", "--workers", "1"]
```

`cvoice.api:app`, configuration paths and artifact loading must be implemented by the product builder. Package static files via known `/app` paths or configure uv_build package data if locating them inside the installed package. The app loads and verifies weights/detector at startup; `/health` reports readiness; uploads use writable `/tmp` and canonical preprocessing. Start directly from the venv to avoid runtime dependency synchronization. Exclude `.git`, `.venv*`, uv/model caches, scratch outputs and full source media with `.dockerignore`; copy only required assets.

The uv image should resolve from `ghcr.io/astral-sh/uv:0.12.3`; store its digest and the Python digest in `release-manifest.json`. Retain these references and the Dockerfile frontend digest for rebuild provenance. Source patterns: [uv Docker guide](https://docs.astral.sh/uv/guides/integration/docker/) (`web/uv_docker.html`) and [Docker ADD checksum](https://docs.docker.com/reference/dockerfile/#add---checksum). A lock/checksum-pinned dependency image is still not proven byte-rebuildable until its build backend, OS and build context are frozen and tested.

**Image size (U):** installed environment plus checkpoint alone is about 1,652 MiB; Python base, static assets and OS layers add to that. A roughly 1.8–2.2 GiB uncompressed image is a planning estimate, not a measurement; compressed pull size and startup must be measured in CI. Do not promise a sub-minute first pull. Provide the gallery for instant judging.

Release CI builds and tests, then the owner publishes a public GHCR package with release tag and immutable digest. Public images allow anonymous pulls; newly published packages can default to private, so test access without credentials ([GHCR documentation](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)). Final README line, with real values replacing placeholders:

```bash
docker run --rm --platform linux/amd64 -p 127.0.0.1:7860:7860 ghcr.io/OWNER/cvoice@sha256:RELEASE_DIGEST
```

Open `http://localhost:7860/`. First pull needs internet; analysis after acquisition must work offline. For strict offline verification, CI runs a one-clip command inside `docker run --network none IMAGE ...`; port publishing cannot provide browser access with `--network none`. Test CDN failure separately, using vendored frontend scripts. Publish only tested image architectures; native arm64 image support remains unverified.

Optional Hugging Face Docker Space: root README YAML `sdk: docker`, `app_port: 7860`; bind `0.0.0.0:7860`, UID 1000, writable temp/cache paths, no dependence on persisted local uploads. **VERIFIED_BY_SOURCE:** compute Spaces currently require a paid plan to create even though CPU Basic has no hourly charge; Static Spaces are free. It is not the assumed free inference host ([Spaces overview](https://huggingface.co/docs/hub/spaces-overview), `web/spaces_overview.html`; [Docker requirements](https://huggingface.co/docs/hub/spaces-sdks-docker), `web/spaces_docker.html`).

## 5. Same environment on Kaggle

**VERIFIED_BY_RUNNING:** isolated uv environments work; using the preinstalled scientific stack is unnecessary and less controlled. Kaggle had Python 3.12.13, uv 0.11.13, Torch/torchaudio 2.10.0+cpu, NumPy 2.0.2, librosa 0.11.0 and numba 0.60.0 (K3 `s0_env`). K3 rejected old uv because the final project requires ≥0.12.3; install the tested uv explicitly.

Recipe for a future full-build CPU kernel (U integration; bootstrap primitives verified):

```python
import os
import shutil
import subprocess
import sys
from pathlib import Path
subprocess.run(["ls", "-R", "/kaggle/input"], check=True)
subprocess.run([sys.executable, "-m", "pip", "install", "uv==0.12.3"], check=True)
# Resolve this exact mount from the listing; dataset mounts are not guessed.
source = Path("/kaggle/input/ACTUAL_PROJECT_MOUNT/project")
project = Path("/kaggle/working/cvoice")
shutil.copytree(source, project, ignore=shutil.ignore_patterns(".venv*", ".git"))
env = dict(os.environ, UV_PROJECT_ENVIRONMENT="/kaggle/working/cvoice-env",
           UV_CACHE_DIR="/kaggle/working/uv-cache", TORCH_HOME="/kaggle/working/torch",
           OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1",
           NUMBA_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", PYTHONHASHSEED="0")
subprocess.run(["uv", "python", "install", "3.12.13"], env=env, check=True)
subprocess.run(["uv", "sync", "--locked", "--python", "3.12.13", "--no-dev",
                "--group", "data", "--build-constraint", "build-constraints.txt"],
               cwd=project, env=env, check=True)
for command in ("dataset", "train", "eval", "gallery", "verify"):
    subprocess.run(["uv", "run", "--no-sync", "cvoice", command],
                   cwd=project, env=env, check=True)
```

The product source bundle must contain pyproject, lock, backend constraint, package, config, recipes, manifests and verified transcript text. Bootstrap may use network; after acquisition the analysis path must use local weights. Use the same CLI/config as Docker/CI, not a second notebook implementation. Save freeze, full run stamp, hash manifest, metrics, golden comparisons and compact gallery in `/kaggle/working`; archive product outputs without environment/cache directories.

Alternative: run directly from the read-only source using a writable `UV_PROJECT_ENVIRONMENT`. K1 `s1b_readonly` tested an actually non-writable directory under a non-root user: default `.venv` creation failed; explicit external environment with `--locked` and editable or non-editable package install passed without changing project files. Copying into `/kaggle/working` is simpler for outputs and packaging.

At submission, provide a public reproduction notebook/kernel or a public notebook file runnable by a judge. It fetches the public repository at the exact release commit (with tag as human label), uses publicly accessible fixtures/assets and runs the same commands. A public notebook still requiring a private source dataset does not close J-13. **No visibility/account changes were made here**; research probes remain private as required. Future public publication is an owner/build task, not research evidence.

## 6. Zero-install gallery and README requirements

**J-05 solution (U implementation):** export the same page and result schema used by FastAPI as static files. Suggested layout: `demo/index.html`, `demo/app.js`, `demo/gallery/index.json`, `demo/gallery/results/*.json`, `demo/gallery/audio/*.wav`, `demo/vendor/`. Use relative URLs so a project site at `/REPO/` works. Publish only `demo/`; add `.nojekyll` if using branch Pages publication. GitHub Actions can upload that directory as the Pages artifact after gallery validation.

On first paint, select a complete precomputed example with waveform, feature overlay, flaw bounds, explanation and baseline/flawed playback controls. No login, Kaggle, Python, model download or API is needed to inspect it. Audio playback begins on a user gesture. Keep upload disabled in static mode with a short explanation and the exact image command. A successful backend readiness check enables uploads; timeout/failure leaves examples available. Distinguish precomputed demonstration from live inference visibly. Reuse `../dashboard/REPORT.md`'s result/gallery schema; this packaging research does not invent another schema.

Use dashboard-tested Plotly Cartesian **4.1.1** and wavesurfer **8.0.1** with Regions/Timeline. Keep exact CDN URLs/SRI from that report and vendor identical licensed fallback files for the offline image. Test the gallery in an ordinary browser with no backend, failed CDN and at the actual Pages subpath. Deployment is unverified here. GitHub Pages supports public free-plan repositories and limits the published site to 1 GB; use a small curated gallery, not full weights/data ([Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits), `web/github_pages_limits.html`).

**J-01 and J-13 README contract:** top links to Pages, image/release, public reproduction notebook, dataset, six-page PDF and video; status/CI badge, scope and known limits; then the following explicitly named sections:

| README section | Required content |
|---|---|
| **Prerequisites** | Browser only for gallery; Docker + architecture/available RAM and pull/storage measurements for image; uv 0.12.3, Python 3.12.13 and network for source setup; Kaggle account/internet for full rebuild. Exact measured resource requirements still pending. |
| **Setup** | Clone/check out release, `uv sync --locked`, checkpoint acquisition/checksum, selected data/TTS groups; no secret credentials needed for public assets. |
| **Run** | Pages URL, exact public `docker run` and localhost URL; source `make demo`; CPU Kaggle reproduction with `make dataset`, `make train`, `make eval`, `make verify`; expected output paths and failure guidance. |
| **AI assistance** | Name every actual AI tool/model and purpose, generated assets/code/documentation, human review/validation, and external models used by the system. Mirror actual usage in Devpost “Built With”. Do not invent tool usage or claim human review already happened. |
| Architecture / data / results | Small module diagram, dataset card, deterministic config, golden comparison table, reproduction log, license notices, limitations and score meaning. |

Suggested truthful disclosure draft: “OpenAI Codex assisted packaging research and drafting reproducibility documentation. Verification claims identify source or probe evidence. [List other AI tools actually used, their models and roles.] [Describe the human review actually completed.] Runtime analysis uses [actual alignment/TTS models]; delivery explanations are deterministic templates [only if implemented].” The AI disclosure requirement comes from `../../design/critique_judge_v0.md:J-01`, which cites the fetched submission guidelines; do not claim this report independently re-audited all hackathon rules.

Owner submission checklist also carries public repository/dataset access, actual names, English audio/subtitles, Devpost components and 3–10 minute YouTube video. README and packaging satisfy only their part of J-01; the owner must check the full judge checklist against the actual submission. Gallery, public image and public reproduction entry remain proposed, so J-05/J-13 are addressed in the build specification, not closed by a deployed artifact.

## 7. Repository, dataset distribution and CI

Suggested repository (U): `src/cvoice/{audio,align,features,synthesis,detector,explain,api,cli}.py`; `config/`, `recipes/`, `data/` with transcripts/alignment labels/card/manifest; `artifacts/` fitted detector and reference statistics; `frontend/`, exported `demo/`; `tests/fixtures/`, `tests/golden/`; `docs/`; `kaggle/`; root pyproject/lock/Makefile/Dockerfile/README/license notices; `.github/workflows/`.

One-command contracts: `make dataset` generates spectrum and validates labels; `make train` fits the frozen split; `make eval` reproduces tables; `make gallery` exports precomputed examples; `make verify` checks canonical hashes, boundary/feature/score goldens and manifest validity; `make demo` starts FastAPI. Full rebuild happens on Kaggle. CI runs a small published fixture plus the image/environment checks, not the full dataset on the laptop.

CI should pin checkout/setup/build Actions by audited commit, uv 0.12.3 and Python 3.12.13; sync the locked project, run schema/label tests, one-clip golden test twice in separate processes, thread-profile checks, and image offline fixture verification. Store a results artifact and badge. Validate the actual browser/static upload paths in hosted CI. Publish a table with environment, CPU, code/lock/config/model/PCM hashes, max boundary difference, max score difference and decision changes. **Kaggle/Docker/CI scoring cells remain “not measured” until run**; do not populate them with alignment-only evidence.

Dataset strategy: distribute canonical baseline **and actual generated paired examples** with transcript, label, split and recipe records. Recipes alone are insufficient for a judge to inspect the required bad spectrum. Regeneration is an additional audit path. Store small per-clip lossless files in Git when total history stays modest; larger complete archives go to a public GitHub Release or the public Drive link accepted by the brief, with checksums and anonymous-access checks. Do not commit the 377 MB checkpoint.

**VERIFIED_BY_SOURCE:** GitHub warns above **50 MiB/file**, blocks files above **100 MiB**, recommends repositories ideally below **1 GB** and strongly below **5 GB**; browser upload limit **25 MiB**. The [release-specific documentation](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases) gives **2 GiB per asset** and 1,000 assets per release (`web/github_releases.html`); the large-file page instead refers to plan-specific LFS limits. Keep archives below 2 GB conservatively. Git LFS cannot serve Pages assets ([LFS documentation](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage), `web/github_lfs.html`). File/repository limits: [large-files docs](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github), `web/github_large_files.html`. PCM16 mono 16 kHz takes `2*16000*T = 32000*T` bytes plus header: 40 seconds ≈ 1.22 MiB; 3 hours ≈ 329.59 MiB. These are arithmetic bounds, not measured FLAC sizes; all severity variants and Git history multiply storage.

Dataset card: source URLs and exact rights/provenance per recording, source/canonical hashes, crop/channel/gain/resample recipes, transcript verification, flaw levels/seeds and coordinates, counts/durations, speaker/speech groups, train/calibration/test splits, synthetic nature, intended use and known limits. Hash manifest covers generated PCM, labels, recipes, transcripts and fitted artifacts. Preserve source and transformed coordinates for rate/pause edits; storage reproducibility does not validate flawed label mathematics.

Keep code license distinct from dataset/model licenses. `web/pypi_licenses.txt` records Parselmouth GPLv3 and soxr LGPL metadata; the embedded static FFmpeg binary has its own build license. Retain dependency/model license texts and corresponding distribution notices, including vendored JS, rather than assuming a permissive top-level license covers everything. The owner decides code license and publication rights. TED redistribution/derivative constraints remain the owner's separate issue J-02; select cleared assets for the public gallery/image/fixtures. A regeneration recipe does not settle source-use rights.

## 8. PDF route for the maximum six-page document

**VERIFIED_BY_RUNNING:** earlier tooling probe found Pandoc **3.1.3**, Tectonic **0.15.0**, pdfinfo/pdftotext present; pdflatex/xelatex/lualatex, browser and LibreOffice missing (`RUN2_condensed.md:PDF tooling`, `PREVIOUS_RUN_condensed.md`). Markdown with tables, math and a PNG compiled through Pandoc → Tectonic to **5 A4 pages**, **41,320 bytes** in **8.806 s** cold / **1.204 s** warm; `pdf/test_tectonic.pdf`, `test_tectonic2.pdf`, `pdf/meta.yaml`. Same content through Typst 0.15.0 produced **7 pages** (`pdf/test_typst.pdf`), so choose the already working Tectonic route.

Final document command contract (U for actual six-page submission; example conversion verified):

```bash
pandoc docs/meta.yaml docs/technical.md --standalone --number-sections \
  --pdf-engine=tectonic --resource-path=docs \
  -o docs/technical.pdf
pdfinfo docs/technical.pdf | awk '/^Pages:/ {print $2; if ($2 > 6 || $2 < 1) exit 1; found=1} END {if (!found) exit 1}'
pdftotext -layout docs/technical.pdf docs/technical.txt
```

Use `geometry: "a4paper, margin=18mm"`, `fontsize: 10pt`, `linestretch: 1.0`, `colorlinks: true` as in `pdf/meta.yaml`. Cold Tectonic may fetch its TeX bundle; cache/freeze the bundle and fonts in hosted document CI if offline rebuild is required. Keep local compilation subject to the research machine restrictions; no new compilation was needed here. Pandoc's engine options and LaTeX variables are documented in the [manual](https://pandoc.org/MANUAL.html), fetched in the earlier notes.

Suggested six-page allocation (U): 1 problem/architecture/claim boundaries; 2 sourcing/spectrum/labels/splits; 3 alignment/features/normalization; 4 rubric/detector/explanation formulas; 5 held-out results/stress tests/ablations; 6 reproducibility/deployment/limitations/references. Count title/references/figures in the six pages. No automatic title-only page or table of contents. Check tables/figures for overflow and text readability; page count alone is insufficient. Final technical PDF is not written by this packaging research.

The two Tectonic PDFs have different whole-file hashes despite identical page counts (timestamps/metadata): document reproducibility means pinned source/toolchain and reviewed content/layout unless byte-level PDF determinism is deliberately implemented. Do not confuse this with canonical audio/result checksums.

## 9. Verified by running: scope and remaining risks

| Evidence | Result and limitation |
|---|---|
| K3 `results.json:s1_uv`, `venv312_freeze.txt` | Final minimal lock installed; 54 packages; CPU torch/torchaudio path worked. It is not the full product/TTS environment. |
| K1 `results.json:s1b_readonly` | Read-only source + external writable venv worked; failing controls documented. Source mounted directly must not rely on default `.venv`. |
| K3 `decode_compare.json`, K1 `resample_sys.json` | Decode repeatability, decoder/resampler differences, anti-phase channels quantified. Limited to these source recordings. |
| K3 `cmp_venv312.json`, `results.json:s13_cross_session` | Identical paths across local/Intel/AMD probes; cross-CPU emissions differ; same AMD sessions matched. No final score test or Docker/CI measurements yet. |
| K3 `psola_p1.json`, `psola_p2.json` | Explicit Praat seed fixes tested duration regeneration across calls/processes. Unseeded edits fail; cross-CPU seeded test pending. |
| K3 `dsp_*.json`, `results.json:s12_dsp` | Tested numpy/librosa/scipy/soxr/WORLD edits repeat; Praat duration exception resolved separately. Not a full dataset regeneration. |
| K1 `results.json:s6_offline` | Cached checkpoint loads with blocked networking; empty cache fails. Offline Docker/browser route untested. |
| K3 `ort.json`, `viterbi.json` | ONNX forward repeatable; alignment probe failed on state dtype overflow. Alternative rejected for current build. |
| L `pdf/test_tectonic.pdf`, `json_canon.out`, `gpu_cpu_drift.out` | Working PDF route, JSON edge cases, CPU/GPU drift. Historical runs only. |

Disagreements with DESIGN_v0: “deterministic outputs” needs the two-tier contract and seed fix; `ffmpeg → mono` needs explicit channel selection; a private build is insufficient for public reproduction; no-backend gallery and prebuilt image must be planned; first-use weight download moves to acquisition/build; backend/OS/model hashes matter beyond uv.lock; final six-page technical document needs a page-count gate.

Owner-only decisions: repository/Pages/GHCR namespace and final release tag; exact AI tools actually used and human review status; publication rights for selected recordings; code license; whether to pay for live hosted inference; final TTS choice and therefore additional dependency/model pins. These do not block the packaging recommendation. Product builder must validate actual scorer tolerances, image size/digests/startup, full Kaggle pipeline, public artifact access and the final PDF before submission.

## 10. Sources and retained source text

Sources were fetched in this finishing session unless marked earlier; URLs supporting individual claims are linked in the relevant sections. Long source wording stays in files.

| Source group | Retained evidence |
|---|---|
| Official uv PyTorch / Docker integration | `web/uv_pytorch.md` (earlier), `web/uv_docker.html` |
| GitHub Pages, large files, Releases, LFS, GHCR | `web/github_pages_limits.html`, `github_large_files.html`, `github_releases.html`, `github_lfs.html`, `ghcr.html` (all under `web/`) |
| Hugging Face deployment / offline variables | `web/spaces_overview.html`, `spaces_docker.html`, `hf_environment.html` (under `web/`) |
| Exact package versions/platforms/licenses | `recommended_lock/uv.lock`, `web/pyworld_prebuilt.json`, `uv_build_0123.json`, `pypi_licenses.txt`, earlier `pypi_wheels*.txt` |
| Model metadata and preprocessing | `web/hf_facebook_wav2vec2-base-960h.json`, `hf_Xenova_wav2vec2-base-960h.json`, `xenova_vocab.json`; K1–K3 checkpoint checksum results |
| Pandoc, Tectonic probe and earlier official source fetches | `PREVIOUS_RUN_condensed.md`, `RUN2_condensed.md` (PDF-tooling sections), `pdf/meta.yaml`, `pdf/test*.pdf` |
| Brief/fixed decisions/topic questions | Workflow script identified in `../../codex/RESEARCH_RULES.md`, constants BRIEF/MACHINE/DIRECTION and `repro_packaging` entry |
| Submission-rule/critic traceability | `../../design/critique_judge_v0.md` J-01/J-05/J-13; `critique_academic_v0.md` I-21; `../dashboard/REPORT.md` static/result schema |
