# Kaggle operations research — 2026-10-01

## Recommendation

Use one private CPU **script** kernel, a versioned private dataset containing the project source, and a locked CPU environment copied into writable storage. Run alignment with a persistent `spawn` pool of **2 workers × 1 torch thread**; use Praat autocorrelation for the inexpensive F0 path. Put environments, downloads and intermediate files in `/tmp`, and put only finished, checksummed archives and small diagnostics in `/kaggle/working`. Retrieve each run before pushing the next version of the same kernel.

**VERIFIED_BY_RUNNING:** wav2vec2-base CPU inference, forced alignment, features, DSP, managed Python, locked uv installation, multiprocessing and output retrieval all worked. Evidence: [v1 diagnostic](kaggle_out/v1/diag.json), [v3 diagnostic](kaggle_out/v3/diag.json), [v3 alignment](kaggle_out/v3/measure_Bm.json), [parallel results](kaggle_out/v3/par.json), and [failure test](probe_out/v2_status_logs.txt). The diagnostic is a component probe, not a completed product build.

**UNVERIFIED — planning estimate derived from measurements:** budget **30–90 minutes** for 200–400 total 20–40 s clips using the light feature/DSP path, accessible source files and a fast CPU TTS engine. Alignment alone projects to **10–52 minutes** with 2×1 workers. Neural TTS, source discovery/download retries and the final training/evaluation loop were not benchmarked; their costs must be added. No measured component needs a GPU.

**VERIFIED_BY_RUNNING:** this account has a **5-concurrent-batch-CPU-session cap**. Pushes were rejected with `Maximum batch CPU session count of 5 reached`; one-minute retries eventually succeeded. This is account session concurrency, separate from the worker count inside a kernel. [Rejections and successful retry](probe_out/push_v3_retry.log).

## Evidence and scope

- `VERIFIED_BY_RUNNING` identifies an actual output or earlier recorded command result.
- `VERIFIED_BY_SOURCE` identifies documentation/source fetched in this or an earlier run, with its URL.
- `UNVERIFIED` identifies a proposal, extrapolation or untested limit; it is not an observed fact.
- The earlier notes are [PREVIOUS_RUN_condensed.md](PREVIOUS_RUN_condensed.md) and [RUN2_condensed.md](RUN2_condensed.md). The question list and fixed owner decisions were read from the two workflow scripts named in `RESEARCH_RULES.md`; the relevant design and critique sections were also read.
- Earlier accepted versions were v1 (full diagnostic), v2 (deliberate failure), v3 (repeat plus managed-Python/setuptools fixes). This finishing run made **zero pushes** and changed no Kaggle resources. It retrieved the completed v3 results. `pushed/probe_v4.py` is a prepared script; there is **no v4 execution evidence**.

## Measured environment and limits

All measured rows below are **VERIFIED_BY_RUNNING**, from `kaggle_out/v1/diag.json` and `kaggle_out/v3/diag.json`, sections `system`, `packages`, `input`, `ffmpeg`, unless another file is cited. Measurements are specific to these runs, not a promise about every future Kaggle image.

| Item | Observation |
|---|---|
| Execution | Batch CPU script, `/usr/bin/python3 -u /kaggle/src/script.py`; `__name__ == '__main__'`, real `__file__`; no IPython kernel |
| Python / OS | CPython **3.12.13**, Ubuntu **22.04.5 LTS**, glibc **2.35**, Linux **6.12.90+**, x86-64 |
| CPU | **4 logical CPUs**, Intel Xeon **2.20 GHz**; topology reports 2 cores × 2 threads; affinity 4; cgroup `cpu.max = 400000 100000` |
| RAM | `/proc/meminfo` **31.35 GiB**, but cgroup `memory.max = 32212254720` bytes = **30 GiB** effective limit; no swap |
| Working disk | **20.96 GB decimal** total, **20.94 GB** free at start, approximately 19.52 GiB total |
| Scratch | `/tmp` reported **1201.72 GB** free on the host-backed overlay; this is an observation, **not a reserved capacity guarantee** |
| `/kaggle/temp` | Did not exist; use `/tmp` explicitly |
| Input | Read-only; mounted at `/kaggle/input/datasets/electroknight/cvoice-probe-audio`; all 9 input SHA-256 values matched uploaded references |
| FFmpeg / ffprobe | Both **4.4.2-0ubuntu0.22.04.1**, installed in `/usr/bin` |
| Useful FFmpeg libraries | `librubberband`, `libsoxr`, `libmp3lame`, `libopus`, `libvorbis`; filters `atempo`, `rubberband`, `aresample`, `pan`, `loudnorm`, `silencedetect`, `volume` present |
| Other tools | git, curl, wget, zip/unzip, rsync, gcc/g++, make; no docker, standalone Praat, yt-dlp, sox, espeak-ng or rubberband CLI initially |
| Added apt tools, v1 | apt worked as root on Kaggle: eSpeak NG **1.50**, SoX **14.4.2**, rubberband CLI **2.0.0**; update/install **40.79 s** total |

The actual image digest was:

```text
gcr.io/kaggle-images/python@sha256:dafd4ce5668bbf1ad422e4c109e0f18c9623c3a7c7f48b0235f13142755c40b9
BUILD_DATE=20260629-122507
GIT_COMMIT=fc61d5cda7da39530055bae9bd0e92865f995cd9
COLAB_RELEASE_TAG=release-colab-external-images_20260514-060047_RC00
```

**VERIFIED_BY_RUNNING:** the live image was built in June despite October research. Repository `main` and Colab inventories describe newer builds and must not substitute for live measurements. [Pulled v1 metadata](probe_out/pulled/cvoice-diag_v1/kernel-metadata.json).

| Preinstalled package | Measured version | Preinstalled package | Measured version |
|---|---|---|---|
| torch | **2.10.0+cpu** | torchaudio | **2.10.0+cpu** |
| numpy | **2.0.2** | scipy | **1.16.3** |
| numba | **0.60.0** | llvmlite | **0.43.0** |
| librosa | **0.11.0** | soundfile | **0.13.1** |
| scikit-learn | **1.6.1** | lightgbm | **4.6.0** |
| pandas | **2.3.3** | transformers | **5.0.0** |
| torchcodec | **0.10.0** | soxr | **1.0.0** |
| setuptools | **81.0.0** | pip | **24.1.2** |
| Kaggle CLI inside image | **2.0.2** | uv before probe install | **0.11.13** |

Praat-parselmouth and pyworld were initially absent. Package presence is not the same as tested API compatibility; the probe actually exercised torch/torchaudio, NumPy, librosa, soundfile, Praat and WORLD. Complete inventories: [v1 freeze](kaggle_out/v1/pip_freeze_system.txt), [v3 freeze](kaggle_out/v3/pip_freeze_system.txt). Local orchestration uses CLI **2.2.4**, not the image's CLI.

| Limit | Finding and evidence status |
|---|---|
| CPU / GPU execution duration | **VERIFIED_BY_SOURCE:** Kaggle docs say **12 h** for CPU/GPU, 9 h TPU. These probes used `--timeout 1800`; the maximum was not exercised. [Official docs](https://www.kaggle.com/docs/notebooks), saved `web/kaggle_docs_notebooks.rendered.md` |
| Interactive idle timeout | **VERIFIED_BY_SOURCE:** 20 min; a CLI batch script does not require the editor to stay open. Same docs |
| GPU weekly quota, this account | **VERIFIED_BY_RUNNING:** **30.00 h** total, **28.07 h** used, **1.93 h** remaining, reset **2026-10-03T00:00:00** in the saved snapshot. [quota.txt](probe_out/quota.txt); re-query `kaggle quota` for current balance |
| CPU weekly quota | **VERIFIED_BY_SOURCE:** fixed project environment says CPU runs consume no GPU quota; quota output lists GPU/TPU only. No claim of unrestricted CPU concurrency |
| Batch CPU concurrency | **VERIFIED_BY_RUNNING:** **5**, rejected then accepted after sessions became available. [push log](probe_out/push_v3_retry.log); corroborated by [Kaggle discussion](https://www.kaggle.com/product-feedback/483684) |
| GPU concurrency | **VERIFIED_BY_SOURCE:** **2** in account context and saved Kaggle discussion; not tested here because GPU use was forbidden |
| Interactive CPU concurrency | **UNVERIFIED:** historical reports say 10; irrelevant to this batch workflow and not measured |
| Saved output size | **VERIFIED_BY_SOURCE:** **20 GB** under `/kaggle/working`; scratch elsewhere is discarded. Official notebook docs; live disk agrees approximately |
| Saved output file count | **VERIFIED_BY_RUNNING:** **651 files** listed over 4 API pages, including a 600-file tree and hidden files. This disproves a universal 500-file hard cap for this run. **UNVERIFIED:** actual maximum. [Listing pages](probe_out/files_v1_page1.json), pages 2–4, `RUN2_condensed.md` |
| Historical 500-file report | **VERIFIED_BY_SOURCE:** discussion includes a reply denying an intentional cap. Treat as a historical/UI issue, not a supported ceiling. [Saved discussion](web/kaggle_forum_topic_420538.txt), [URL](https://www.kaggle.com/product-feedback/420538) |
| Dataset storage limits | **VERIFIED_BY_SOURCE:** docs state 200 GB/dataset, 200 GB private total, 50 top-level files; directories/archives recommended. These are dataset limits, **not notebook output limits**. [Dataset docs](https://www.kaggle.com/docs/datasets), saved `web/kaggle_docs_datasets.rendered.md` |

## CLI metadata, image pinning and pitfalls

**VERIFIED_BY_SOURCE:** installed CLI 2.2.4 `kernels_push` accepts the following metadata. Identity is `id` or `id_no` (numeric ID takes precedence); required source fields are `code_file`, `language` (`python`, `r`, `rmarkdown`), `kernel_type` (`script`, `notebook`). Title is needed for creation and must be at least 5 characters; its slug should match `id`. Use explicit JSON booleans. Source: [2.2.4 metadata docs](https://raw.githubusercontent.com/Kaggle/kaggle-cli/v2.2.4/docs/kernels_metadata.md) and [CLI implementation](https://raw.githubusercontent.com/Kaggle/kaggle-cli/v2.2.4/src/kaggle/api/kaggle_api_extended.py), also inspected locally.

Recommended metadata for the **future build**, shown with the already approved diagnostic ID; replace source dataset only when implementing the build:

```json
{
  "id": "electroknight/cvoice-diag",
  "title": "cvoice-diag",
  "code_file": "probe.py",
  "language": "python",
  "kernel_type": "script",
  "is_private": true,
  "enable_gpu": false,
  "enable_tpu": false,
  "enable_internet": true,
  "dataset_sources": ["electroknight/cvoice-project", "electroknight/cvoice-probe-audio"],
  "competition_sources": [],
  "kernel_sources": [],
  "model_sources": [],
  "docker_image_pinning_type": "original",
  "docker_image": "gcr.io/kaggle-images/python@sha256:dafd4ce5668bbf1ad422e4c109e0f18c9623c3a7c7f48b0235f13142755c40b9"
}
```

**VERIFIED_BY_SOURCE:** additional accepted fields include `enable_tpu`, `keywords`, `docker_image`, and `docker_image_pinning_type` (`original` or `latest`). The installed implementation defaults internet to true although metadata docs say false; specifying it avoids ambiguity. `machine_shape` is passed to the server as a string; the client has no exhaustive allowed-value validation. `--accelerator` overrides that string. Only the single `code_file` contents are sent; adjacent source modules are not uploaded by kernel push.

**VERIFIED_BY_RUNNING:** pulled CPU metadata has `machine_shape: "None"`. For CPU omit the field and all accelerator flags. **VERIFIED_BY_SOURCE:** current `main` docs list `NvidiaTeslaT4`, `NvidiaTeslaA100`, `NvidiaL4`, `NvidiaL4X1`, `NvidiaH100`, `NvidiaRtxPro6000`, `TpuV5E8`, `TpuV6E8`; some are competition/admin-only. Older 2.2.4 docs mention P100/older TPU shapes; availability is server-controlled. P100 was announced for retirement on 2026-09-15 in saved topic 735239. [Current accelerator docs](https://raw.githubusercontent.com/Kaggle/kaggle-cli/main/docs/kernels.md), [announcement](https://www.kaggle.com/discussions/product-announcements/735239). None was tested or requested.

**UNVERIFIED:** server enforcement of a newly submitted digest pin was not tested; all executed diagnostic pushes omitted explicit pins. The digest above was **observed**, and CLI accepts/transmits the fields. Pull metadata after a run and compare `KAGGLE_DOCKER_IMAGE` with the expected digest. Do not describe an arbitrary custom Docker image as supported. [Environment documentation](https://www.kaggle.com/docs/notebooks), saved environment section.

**VERIFIED_BY_RUNNING / SOURCE pitfalls:** push is asynchronous; `--timeout` limits **remote execution**, not the local HTTP call. Rejected pushes and `kernels status` reporting ERROR both returned exit code 0 in the saved tests: inspect text/state. Installed 2.2.4 has **no `--no-run`**, despite newer `main` docs. Output selection is **`--file-pattern`**, not `-f`. `pull` supports a version suffix; installed `output`, `status`, and logs parse a suffix but do not send it to their latest-session endpoints. Do not depend on `/3` to select an old run; retrieve before the next push and validate the embedded run ID.

## Shipping project source: comparison and exact update loop

| Route | Evidence / tradeoff | Decision |
|---|---|---|
| Private source dataset | **VERIFIED_BY_SOURCE:** versioned directories with `--dir-mode`; **VERIFIED_BY_RUNNING:** private audio dataset mounted, bytes preserved. Project-source upload itself untested | **Recommend** while the repo is unpublished; keep normal modules and lockfile |
| Self-contained script | **VERIFIED_BY_RUNNING:** diagnostics embedded helper files and ran successfully; only one file pushed | Suitable for probes/bootstrap; embedding the whole product makes updates harder |
| Git clone | **VERIFIED_BY_RUNNING:** public Kaggle/docker-python shallow clone succeeded in 1.5 s, v1. Private project authentication not tested | Useful once public; checkout an immutable commit, not `main` |
| Wheel dataset | **UNVERIFIED:** product wheel not built/uploaded; requires a build and still needs config/assets/lock/dependencies | No benefit over source for this hackathon; avoid local build compute |

The following is a **VERIFIED_BY_SOURCE command recipe**, not an account mutation performed during this research. The new `cvoice-project` dataset is hypothetical. Directory processing time and the full project source→dataset→pipeline loop remain **UNVERIFIED**. Stage only a small source snapshot, excluding credentials, environments, outputs and large audio; all pipeline computation stays on Kaggle.

```bash
# Future build operator: set this to the project source directory.
PROJECT_SOURCE=/absolute/path/to/project
STAGE_DIR="$PWD/code_dataset"
mkdir -p "$STAGE_DIR/project"
rsync -a --exclude '.git/' --exclude '.venv/' --exclude '.aws/' \
  --exclude '.kaggle/' --exclude '.env*' --exclude '__pycache__/' \
  --exclude 'kaggle_out/' --exclude 'outputs/' --exclude 'code_dataset/' \
  --exclude '*.wav' --exclude '*.flac' --exclude '*.mp3' --exclude '*.ogg' \
  --exclude '*.oga' --exclude '*.mp4' --exclude '*.pth' --exclude '*.safetensors' \
  "$PROJECT_SOURCE/" "$STAGE_DIR/project/"
# Use a fresh staging directory for each snapshot so removed files cannot linger.
cat > "$STAGE_DIR/dataset-metadata.json" <<'JSON'
{"title":"cvoice-project","id":"electroknight/cvoice-project",
 "licenses":[{"name":"copyright-authors"}],
 "description":"Private project source snapshot; see project/LICENSE for code terms."}
JSON
```

Generate an exact source manifest and record its digest as the bootstrap's expected snapshot. This hashes only the small staged code tree; it does not hash/build the audio corpus locally.

```bash
/usr/bin/python3 - "$STAGE_DIR/project" <<'PY'
import hashlib, pathlib, sys
root = pathlib.Path(sys.argv[1]); manifest = root / 'SOURCE_SHA256SUMS'
rows = []
for p in sorted(root.rglob('*')):
    if p.is_file() and p != manifest:
        rows.append(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(root).as_posix()}\n')
manifest.write_text(''.join(rows))
print('EXPECTED_SOURCE_MANIFEST_SHA256=' + hashlib.sha256(manifest.read_bytes()).hexdigest())
PY
# First upload: private is the default; do not supply --public.
kaggle datasets create -p "$STAGE_DIR" --dir-mode zip --keep-tabular
# After edits: restage a fresh complete snapshot, regenerate hashes, then:
kaggle datasets version -p "$STAGE_DIR" --dir-mode zip --keep-tabular \
  -m "source snapshot: recorded manifest digest and revision"
kaggle datasets status electroknight/cvoice-project --format json
kaggle datasets files electroknight/cvoice-project --page-size 200
```

**VERIFIED_BY_SOURCE:** dataset `--dir-mode` choices are `skip` (default), `zip`, `tar`; omission silently excludes directories. `--keep-tabular` avoids automatic CSV conversion. Do not use `--delete-old-versions`: retain provenance. Required filename is **`dataset-metadata.json`**, singular, despite some CLI help text spelling it differently. Dataset title is 6–50 characters and slug 3–50. Archives are processed/unpacked server-side. [2.2.4 dataset commands](https://raw.githubusercontent.com/Kaggle/kaggle-cli/v2.2.4/docs/datasets.md), [metadata docs](https://raw.githubusercontent.com/Kaggle/kaggle-cli/main/docs/datasets_metadata.md), [dataset processing docs](https://www.kaggle.com/docs/datasets).

Poll dataset status every 30 s, until **both** `status == "ready"` and `current_version_number == EXPECTED_VERSION`; then push. Do not assume a ready response for the old version proves the new one is mounted. No processing-delay duration was measured. Current source metadata validates `owner/slug`, without a dataset version suffix, so serialize dataset updates with build pushes and verify the expected source hash inside the kernel. [Observed ready response](probe_out/datasets_status_files.txt).

```bash
EXPECTED_VERSION=1  # First creation; set to the actual next version on an update.
dataset_ready=0
for attempt in $(seq 1 60); do
  timeout 18 kaggle datasets status electroknight/cvoice-project --format json \
    > dataset_status.json
  if /usr/bin/python3 - "$EXPECTED_VERSION" <<'PY'
import json, sys
try:
    d = json.load(open('dataset_status.json'))
    ok = d['status'] == 'ready' and d['current_version_number'] == int(sys.argv[1])
except (ValueError, KeyError):
    ok = False
sys.exit(0 if ok else 1)
PY
  then dataset_ready=1; break; fi
  sleep 30
done
test "$dataset_ready" -eq 1 || exit 1
```

Bootstrap requirements (proposal, **UNVERIFIED as a complete project implementation**): discover `project/pyproject.toml` below `/kaggle/input/datasets/electroknight/cvoice-project` or legacy `/kaggle/input/cvoice-project`; fail on ambiguity. Require the expected `SOURCE_SHA256SUMS` digest and verify its files before copying. Copy `project/` to `/kaggle/working/project`, synchronize its environment into `/tmp`, then invoke the product's actual build entry point with an explicit output directory in `/tmp`. An entry-point name is intentionally not invented here: the product has not been built by this research task.

Exact remote environment commands, executed by bootstrap subprocesses **on Kaggle**, after copying the project:

```bash
python3 -m pip install --disable-pip-version-check 'uv==0.12.21'
export UV_SYSTEM_PYTHON=false
export UV_PYTHON_PREFERENCE=only-managed
export UV_PYTHON_INSTALL_DIR=/tmp/cvoice-python
export UV_CACHE_DIR=/tmp/cvoice-uv-cache
export UV_PROJECT_ENVIRONMENT=/tmp/cvoice-venv
export TORCH_HOME=/tmp/cvoice-torch
export NUMBA_CACHE_DIR=/tmp/cvoice-numba
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMBA_NUM_THREADS=1
export PYTHONHASHSEED=0
uv python install 3.12.14
cd /kaggle/working/project
uv sync --locked --python 3.12.14
sha256sum uv.lock
# Use /tmp/cvoice-venv/bin/python to launch the project's build entry point.
```

The `uv.lock` must already exist and match `pyproject.toml`. Generate/update it on Kaggle during a dependency-update run and retrieve it with the outputs; subsequent builds use `--locked`. Do not run dependency installation or locking on the restricted laptop. **VERIFIED_BY_SOURCE:** `--locked` fails on an out-of-date lock; `--frozen` skips this check; `sync` installs exactly the locked environment. [uv sync docs](https://docs.astral.sh/uv/concepts/projects/sync/). Explicit patch Python avoids `3.12` drifting; managed-only selection avoids the image's system interpreter. [uv Python docs](https://docs.astral.sh/uv/concepts/python-versions/).

Push, retry only an explicit CPU-cap rejection, and poll without keeping the foreground busy:

```bash
mkdir -p run_logs
kaggle kernels push -p kaggle --timeout 7200 > run_logs/push.txt 2>&1
cat run_logs/push.txt
# Require "successfully pushed" and no invalid source warnings before polling.
# If "Maximum batch CPU session count of 5 reached", wait 60 s and retry.
# Other errors require diagnosis; an ambiguous HTTP failure may already have pushed.
(
  for attempt in $(seq 1 240); do
    status=$(timeout 18 kaggle kernels status electroknight/cvoice-diag 2>&1)
    printf '%s %s\n' "$(date -u +%FT%TZ)" "$status" >> run_logs/status.txt
    case "$status" in
      *COMPLETE*|*ERROR*|*CANCEL*) break ;;
    esac
    sleep 30
  done
) &
kaggle kernels logs electroknight/cvoice-diag > run_logs/logs.json
# A bounded live peek is also supported:
timeout 18 kaggle kernels logs electroknight/cvoice-diag --follow
```

Use the original `--timeout 1800` for diagnostics; **7200 s** above is a proposed two-hour light-build budget, not a measured Kaggle maximum. Increasing it does not make a rejected push wait for a session slot. Never stop unrelated account sessions. Compare the final remote status with the bootstrap's completion marker and manifest; a partial archive is not a successful build.

## Locked environment: measured costs, fixes and pins

**VERIFIED_BY_RUNNING:** v3 installed `uv==0.12.21` in **5.62 s**. System-Python `uv venv --python 3.12` took **0.14 s**; unpinned torch/audio installs totaled **30.89 s** (v1 **35.77 s**). A miniature source project copied into `/kaggle/working` locked and synced in **28.28 s cold** (v1 **34.20 s**); repeat sync **0.12 s** (v1 **0.14 s**) left the lock unchanged. Its installed size was **1215.6 MB apparent / 1265.4 MB allocated**. The cache was about **1239.4 MB apparent**; hardlinks made the combined unique allocation about **1292.7 MB**, not the sum of the separate trees. Cross-filesystem copies can instead approach their sum. [uv section](kaggle_out/v3/diag.json).

**VERIFIED_BY_RUNNING:** managed CPython **3.12.14** downloaded in **5.47 s**, 32.7 MiB download, **98.6 MB apparent / 107.8 MB allocated** installed. Syncing the existing lock into its fresh venv with a **warm cache** took **0.54 s**, imports **9.22 s**; the venv occupied **1249.4 MB apparent / 1302.8 MB allocated**. A fully cold managed-Python final-product build was not measured. Allow **1–3 min** setup as an **UNVERIFIED planning allowance**.

| Problem | Observed result / action |
|---|---|
| System-Python `sitecustomize` | **VERIFIED_BY_RUNNING:** isolated system-Python env prints `No module named 'wrapt'` during startup, then continues. The hook lives in the image's stdlib; managed Python starts clean. Saved hook: `web/dockerpython_patches_sitecustomize.py` |
| pyworld 0.3.5 + setuptools 84.0.0 | **VERIFIED_BY_RUNNING:** installation succeeds but import fails: `No module named 'pkg_resources'`. Bfix changed setuptools to **80.10.2**; WORLD import and feature/DSP probes then passed |
| Latest-package drift | **VERIFIED_BY_RUNNING:** unpinned install resolved torch **2.14.1+cpu**, torchaudio **2.11.0+cpu**, librosa **1.0.0**, NumPy **2.5.3**, not the preinstalled stack. These probe paths ran, but this is not a compatibility guarantee |
| Torch/torchaudio pairing | **VERIFIED_BY_SOURCE:** official installation guidance requires compatible paired releases. Recommend the measured matched **2.10.0+cpu / 2.10.0+cpu**; do not adopt the unpinned mismatch merely because this probe ran. [Torchaudio installation](https://docs.pytorch.org/audio/stable/installation.html) |
| WORLD source build | **VERIFIED_BY_RUNNING:** pyworld 0.3.5 built successfully on Kaggle; separately built wheels had different archive hashes in v1/v3. Pin package/build inputs or record the built wheel; version equality alone does not prove identical binaries |
| Preinstalled-only fallback | **VERIFIED_BY_RUNNING:** works with pinned missing Praat/WORLD installs, but pYIN was much slower, and global installs depend on the base image. Prefer isolation for the final product |

**Recommendation — UNVERIFIED as one combined final lock:** managed Python **3.12.14**, uv **0.12.21**, matched torch/torchaudio **2.10.0+cpu**, NumPy **2.0.2**, SciPy **1.16.3**, librosa **0.11.0**, soundfile **0.13.1**, numba **0.60.0**, llvmlite **0.43.0**, scikit-learn **1.6.1**, praat-parselmouth **0.4.7**, setuptools **80.10.2**. Add pyworld **0.3.5** only when WORLD edits are needed; lightgbm **4.6.0** only if choosing that model. Pin all transitive packages through the lock. These core/image packages and Praat/WORLD operations were exercised; the precise isolated combination still needs a build preflight on Kaggle. The newer measured Bfix stack is an alternative recorded in `measure_Bfix.json`, not the default recommendation.

Configure a CPU-only index explicitly in the project's TOML (proposed configuration, **VERIFIED_BY_SOURCE** syntax from [uv PyTorch guide](https://docs.astral.sh/uv/guides/integration/pytorch/)):

```toml
[[tool.uv.index]]
name = "pytorch-cpu"
url = "https://download.pytorch.org/whl/cpu"
explicit = true
[tool.uv.sources]
torch = { index = "pytorch-cpu" }
torchaudio = { index = "pytorch-cpu" }
```

Use `soundfile.read` for canonical WAV/FLAC instead of adding torchcodec for basic loading. The model is `torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H`, **94,393,245 parameters**, checkpoint **377,664,473 bytes**, SHA-256 **`488fd4f16de84438ffc945334278c1b9fb9b7159a806c1080b16111a958c945d`**. **VERIFIED_BY_RUNNING:** actual download took **1.31–1.37 s** on these sessions; do not assume that bandwidth on future runs. [Network/checkpoint evidence](kaggle_out/v3/diag.json).

## CPU feasibility and wall-clock estimate

**VERIFIED_BY_RUNNING:** 26 s Reagan opening, 16 kHz mono, warm inference below. Forced alignment additionally took about **0.005–0.006 s** in torchaudio or **0.056–0.057 s** for the NumPy Viterbi path in v3; paths matched. [v1 system timing](kaggle_out/v1/measure_S.json), [v3 system timing](kaggle_out/v3/measure_S.json).

| Threads, one model | v1 warm inference | v3 warm inference |
|---|---:|---:|
| Default (2) | 4.985 s | 3.840 s |
| Explicit 1 | 9.552 s | 7.396 s |
| Explicit 2 | 5.003 s | 3.940 s |
| Explicit 4 | 4.736 s | 3.685 s |

**VERIFIED_BY_RUNNING:** persistent spawned workers loaded the model once; jobs cycled four 25–30 s clips. Throughput below excludes maximum worker initialization, not every possible startup overhead. Use it for planning, not a precise linear guarantee. [v1 pool](kaggle_out/v1/par.json), [v3 pool](kaggle_out/v3/par.json).

| Pool | Audio / jobs | v1 total wall | v3 total wall | Warm audio-seconds/wall-second v1 / v3 |
|---|---|---:|---:|---:|
| 1×1 | 111 s / 4 | 45.17 s | 35.23 s | 2.64 / 3.42 |
| **2×1** | 111 s / 4 | **24.91 s** | **19.51 s** | **5.15 / 6.67** |
| 3×1 | 167 s / 6 | 37.65 s | not run | 5.16 / — |
| 4×1 | 222 s / 8 | 45.25 s | 35.77 s | 5.70 / 7.25 |
| 1×4 | 222 s / 8 | 43.34 s | not run | 5.54 / — |
| 2×2 | 222 s / 8 | 42.64 s | 33.94 s | 5.67 / 7.15 |

Four single-threaded workers are only about 9–11% faster in warm throughput than two, while loading four models and slowing individual jobs. Each worker peaked around **1.12–1.23 GiB RSS** (roughly 5 GiB for four). Use **2×1**, `spawn`, `chunksize=1`, a guarded `if __name__ == '__main__'`, `torch.set_num_threads(1)`, `torch.set_num_interop_threads(1)` once before work, `model.eval()` and `torch.inference_mode()`. Set BLAS/OpenMP/Numba thread limits before imports. The complete proposed thread policy was not all applied in the pool probe; the measured pool explicitly set OMP/MKL and torch intra-op threads. A serial four-threaded model is also viable when simplicity matters more than fixed-thread consistency.

**VERIFIED_BY_RUNNING:** feature timings for 30 s Reagan/JFK audio (warm, sequential); parameters: 16 kHz, 160-sample/10 ms hop; F0 floor 60 Hz, ceiling 500 Hz; pYIN frame 1024 samples centered; MFCC 13 coefficients, 400-sample FFT, 40 Mel bands; RMS 400 samples. Praat PSOLA manipulation used 10 ms step, 75–600 Hz, pitch ×1.2; WORLD used DIO→StoneMask→CheapTrick→D4C→synthesize, pitch ×1.2. These are timing-probe parameters, not an accuracy validation for every voice. [Script](src_embed/measure.py).

| Component / 30 s | Measured cost | Evidence |
|---|---:|---|
| Praat AC + MFCC + RMS | about **0.09–0.17 s** | v1 `measure_S2.json` / `measure_B.json`; v3 `measure_Bfix.json` |
| pYIN | **1.94–2.08 s** Bfix/B; **9.35–10.73 s** image stack v1 | first JIT call cost **16.5–29.5 s**; warm once per worker |
| WORLD DIO + StoneMask | **0.238–0.351 s** | Bfix v3 / S2 v1 |
| WORLD Harvest | **10.39–13.07 s** | Bfix v3 / S2 v1 |
| Praat PSOLA edit | **0.11–0.17 s** | Bfix v3 / S2 v1 |
| WORLD pitch resynthesis | **2.55–4.50 s** | Bfix v3 / S2 v1 |
| FFmpeg tempo / gain / lowpass | approximately **0.14–0.17 s** each on 26 s | v1 `diag.json`, FFmpeg hash tests |
| FFmpeg rubberband tempo / pitch | **0.41 / 0.54 s** on 26 s | same output |
| eSpeak NG TTS | **0.03 s** for **9.884 s** output | v1 `diag.json`, `apt`; not a neural TTS quality/timing proxy |

For **N distinct audio files requiring alignment**, mean duration **L**, let `A = N × L`. Do not count the shared baseline once for every pair: align/cache each unique waveform once. Training folds reuse extracted features.

```text
T_build = T_setup + T_download + T_TTS
        + A / q_align + T_DSP + T_features + T_train/eval + T_package
q_align = 5.15–6.67 audio-seconds per wall-second for measured 2×1 pool
T_align_minutes = N × L / (60 × q_align)
```

**UNVERIFIED — extrapolation** using these measured rates:

| N total clips | Mean length | Audio duration | Alignment alone, 2×1 |
|---|---:|---:|---:|
| 200 | 20 s | 66.7 min | **10.0–12.9 min** |
| 200 | 30 s | 100 min | **15.0–19.4 min** |
| 400 | 30 s | 200 min | **30.0–38.8 min** |
| 400 | 40 s | 266.7 min | **40.0–51.8 min** |

A single one-threaded model would instead project to **19.5–101 min** across the 200×20 to 400×40 endpoints. Splitting the baseline/participant into two files per counted “clip” doubles alignment work; the table assumes N is the actual unique audio-file count. Duration scaling is approximate: the transformer has sequence-length-dependent work; repeated short-clip tests do not bound long recordings.

For the light path, a conservative **UNVERIFIED budget** is alignment plus **≤5 min** basic features, **≤10 min** simple DSP, **1–3 min** environment/model setup, and **10–20 min** for accessible downloads, validation, small-model training/evaluation and packaging. This yields roughly **30–90 min** overall; 200×30 s typically budgets **35–50 min**, 400×30 s **55–80 min**. Those allowances are not measured full-pipeline timings. WORLD resynthesis on every 400×30 s clip adds **17–30 min sequential**, Harvest on all clips adds **69–87 min sequential**; old-stack pYIN adds **62–72 min**. A heavy configuration therefore can take **1–3 h or more**, before unmeasured neural TTS. Cache F0/DSP analysis per source and restrict heavy alternates to necessary variants.

**Conclusion — supported inference:** a GPU is unnecessary for the measured light pipeline at this scale. A specific neural TTS choice still needs its own CPU benchmark; this report does not establish feasibility for every TTS model. The five-session account cap means queue delay is additional and unbounded by the clip timing estimate.

## Determinism and critic responses

**VERIFIED_BY_RUNNING:** repeated fixed-thread inference produced identical emission hashes within each tested environment; the matched image stack and the newer isolated stack produced identical fixed-thread emissions on the Reagan probe, despite version changes. Across thread settings emissions differed by up to **0.003214** in log probabilities, but the 74-word alignment path and word-time hash remained identical. Across laptop/Kaggle, emissions differed but the same probe path and word times matched. [v3 `thread_cmp`, `vs_laptop`](kaggle_out/v3/diag.json), [managed alignment](kaggle_out/v3/measure_Bm.json).

**VERIFIED_BY_RUNNING:** adding 4 s of zero padding changed 12 emission argmax frames, 10 aligned path frames, one raw word end by **20 ms**, and a refined start/end by **55 ms**. Pin clip bounds and padding; identical transcripts are insufficient to reproduce alignment. This is sensitivity, not ground-truth boundary error.

**VERIFIED_BY_RUNNING:** RMS and pYIN/Praat AC outputs matched in the sampled cross-environment comparisons; MFCC values between image and isolated stacks differed by up to **6.104×10^-5** in the v1 float32 comparison recorded in `RUN2_condensed.md`. Some F0 hash differences were only float64-level: the earlier stdlib comparison found identical float32 tracks for the downloaded laptop/Kaggle samples. Do not turn this small-sample result into a guarantee across all recordings or machines.

**VERIFIED_BY_RUNNING:** FFmpeg 4.4.2 Kaggle versus 6.1.1 laptop hashes matched for 6 of 13 tested PCM transformations; Ogg decode, pitch resampling, lowpass, rubberband and a WAV→soxr resample differed. `refs/local_ffmpeg_hashes.json` and v1/v3 `ffmpeg.hashes` record them. A static FFmpeg 7.0.2 binary was inspected locally, but **no Kaggle v4 test exists** proving that binary fixes cross-machine differences. Even system soxr H13 changed between v1/v3; both used the same recorded FFmpeg version. Promise canonical artifacts, not arbitrary cross-machine byte identity.

Recommended reproducibility contract (**UNVERIFIED until the product checks run**): preserve exact source/lock/model hashes, fixed clip samples, channel choice, DSP recipe/seed, binary versions and CPU/thread settings. Save canonical 16 kHz mono PCM/FLAC and integer sample-index edit labels. Reusing these artifacts gives exact ground truth without regenerating floating-point DSP. Verify repeat builds by hashes in the same setup; test deployment environments separately and report actual maximum timestamp/score/feature differences. Proposed acceptance targets of **1 ms timestamp / 0.1 index point** are engineering targets from the critique, not verified tolerances here.

| Critic / design point | What this topic settles |
|---|---|
| **I-21: repeatability vs reproducibility** | Distinguish fixed-setup repeat hashes from cross-environment checks. Existing probe word times match across laptop/Kaggle, but emissions and decoder/DSP outputs do not universally match. Canonical audio, hash manifests and a public reproduction recipe remain required |
| **J-13: private build and invisible reproducibility** | Private source dataset is a practical development route. It does not let judges rerun the build. Publish the source/bootstrap and lock in the eventual GitHub submission; owner decides whether to additionally publish a kernel cloning an immutable public commit. Record Kaggle vs CI/container results. No kernel publication performed here |
| **I-11: exact timestamps / error propagation** | CPU throughput is settled; boundary accuracy is not. The padding test demonstrates context sensitivity. Sample-exact edit labels are distinct from inferred word boundaries; manual/reference boundary evaluation belongs to alignment research |
| **I-10: end-to-end invariance** | Hash repeatability is not invariance to gain, pitch or channels. This topic supplies the run environment and comparison mechanism, not evidence of detector score robustness |
| **J-05: fast judge experience** | Archive precomputed gallery audio/features/results with build outputs; CPU build feasibility does not establish cold dashboard latency or free hosting |
| **DESIGN_v0 §10** | Agree with private CPU kernel/source dataset/uv/archive loop. Add managed Python, fixed threads, explicit snapshot identity, small output chunks, and measured rather than blanket determinism. §2's 300–400 × 20–40 s is **1.67–4.44 h** audio; “~3 h” is plausible only for some duration/count choices |

## Retrieving and packaging results

**VERIFIED_BY_RUNNING:** the v1 600-file tree was saved and listed. ZIP and tar.gz archives and a 20 MiB binary downloaded with correct SHA-256; 3 archive/binary files took **9.51 s**, **99,308 KiB** local peak RSS. Ten small nested files plus hidden files took **15.42 s**. Paths were preserved; `kernels files` exposed basenames with duplicates. See [archive test](probe_out/output_v1_archives.txt), [small-tree test](probe_out/output_v1_tree10.txt), [manifest](kaggle_out/v1/diag.json).

**VERIFIED_BY_SOURCE:** installed 2.2.4 `kernels_output` calls `requests.get(stream=True)` but then writes `response.content`, buffering the complete file. It automatically traverses pages when no `--page-token` is supplied. Keep **each archive ≤64 MiB** (proposed operational choice) and leave local RAM headroom; a multi-GB single ZIP violates the laptop constraints. Use `--page-size 200` and explicit regex; it still downloads the log. Checksums detect truncation. [Installed/source implementation](https://raw.githubusercontent.com/Kaggle/kaggle-cli/v2.2.4/src/kaggle/api/kaggle_api_extended.py).

Proposed artifact layout (**UNVERIFIED as a product implementation**): `dataset-000.zip`, subsequent numbered archives, `features-000.zip`, `model.zip`, `metrics.json`, `run_manifest.json`, `SHA256SUMS`, `STATUS.json`. Archives contain audio, transcripts, integer-sample edit labels, alignments, compact frame/per-word features, split manifests, source/license notices, models and the precomputed gallery. Put model caches/venv/source copies outside the final output directory. Use independent ZIP chunks, not split ZIP volumes; already-compressed FLAC can use ZIP_STORED, text ZIP_DEFLATED. Include internal per-file hashes as well as archive hashes; finalize completion only after validation and hashes.

**UNVERIFIED — exact size calculation:** 16 kHz mono PCM16 needs `32000 × duration_seconds` bytes, excluding small headers. 200×20 s → **128 MB**, 400×40 s → **512 MB** audio; 400×30 s → **384 MB**. Do not duplicate the same baseline in every pair. FLAC savings depend on content; the measured 26 s example was **440,878 bytes** versus **832,044 bytes** WAV. Full speeches/video and feature formats can dominate size, so discard unnecessary downloaded originals from saved output.

Exact retrieval loop for the proposed names (run on the laptop; check status first):

```bash
kaggle kernels status electroknight/cvoice-diag
kaggle kernels logs electroknight/cvoice-diag > run_logs/final_logs.json
kaggle kernels output electroknight/cvoice-diag -p retrieved --page-size 200 \
  --file-pattern '^(run_manifest\.json|metrics\.json|STATUS\.json|SHA256SUMS)$'
# Validate run_manifest snapshot/run ID and STATUS state before accepting artifacts.
kaggle kernels output electroknight/cvoice-diag -p retrieved --page-size 200 \
  --file-pattern '^(dataset|features)-[0-9]+\.zip$|^model\.zip$'
cd retrieved
sha256sum -c SHA256SUMS
```

If a download would exceed the local ~20 s command budget, fetch one numbered chunk with an anchored regex per command; retry with `--force` after checking the intended run identity. Extraction is light I/O and can be performed one chunk at a time. Retrieve logs/partial outputs even on ERROR, but never accept them as a successful dataset. **VERIFIED_BY_RUNNING:** the v2 uncaught RuntimeError produced ERROR status and preserved `partial/before_failure.json` and nested text; its pre-failure `STATUS.json` still said RUNNING, illustrating why an application completion marker alone is insufficient. [v2 outputs](kaggle_out/v2/partial/before_failure.json), [status/logs](probe_out/v2_status_logs.txt).

## Network and remaining risks

**VERIFIED_BY_RUNNING:** v3 homepage requests succeeded for upload.wikimedia.org (0.258 s), Commons (0.164 s), TED (0.097 s), archive.org (0.281 s), Hugging Face (0.076 s), PyPI (0.049 s), GitHub (0.095 s). PyTorch domain root returned 403, but its wheel index and checkpoint returned 200 and the checkpoint downloaded. A HEAD/range check is not evidence that every file downloads successfully. [v3 network checks](kaggle_out/v3/diag.json).

**VERIFIED_BY_RUNNING:** Wikimedia behavior varies by request/User-Agent: one named NARA Commons object returned 200/206 with descriptive headers, 403 with a generic agent and 429 with another descriptive agent. Homepage success does not establish bulk-download reliability; the research rules document broader Kaggle 429 failures. Use known-working archives.gov/NARA S3/archive.org routes established by sourcing research, bounded retries, hashes and explicit fail/skip accounting. TED podcast/direct MP3 range requests returned 206; bare HLS/GraphQL roots returned 404/400, not proof their actual APIs are unusable.

The supplied research rules also report anti-phase NARA stereo transfers: a plain L+R downmix can cancel speech. This diagnostic did not test that failure (**UNVERIFIED here**). Preserve the channel-selection decision from sourcing research in the recipe (one channel or side signal where required), rather than universally applying `-ac 1`.

Remaining **UNVERIFIED** items: maximum output file count; digest-pin server enforcement; final combined product lock/preflight; directory-source upload and readiness latency; neural TTS wall-clock; final training/evaluation cost; cold managed-Python setup with all final dependencies; static FFmpeg cross-machine agreement; full detector timestamp/score agreement in Docker/CI. These do not require speculative account mutations to finish this research report.

Owner-only decisions: select the TTS engine/voices and quality tradeoff; choose actual clip count and heavy DSP coverage; decide eventual public-kernel publication. Existing private build authorization is sufficient for the recommended architecture; no new confirmation was requested and no publication occurred.

## Verified by running: evidence index

| Probe | Location / result |
|---|---|
| v1 complete | `pushed/probe_v1.py`; `kaggle_out/v1/diag.json`; start 13:32:43Z, **953.8 s**, no top-level section errors; subcomponent failures are recorded separately |
| v2 deliberate failure | `pushed/probe_v2_failure.py`; `probe_out/v2_status_logs.txt`; RuntimeError after 20 s, ERROR, partial output retrieval successful |
| v3 complete | `pushed/probe_v3.py`; `kaggle_out/v3/diag.json`; start 13:58:42Z, **843.2 s**, no top-level section errors; managed Python and Bfix verified |
| Full aligner measurements | `measure_S.json`, `measure_B.json`, `measure_Bm.json` in v3; 26 s input, repeated emissions, paths, word rows, padding sensitivity |
| Features / DSP | `kaggle_out/v1/measure_S2.json`, `kaggle_out/v3/measure_Bfix.json`; two 30 s clips, cold/warm costs and hashes |
| Parallelism | `kaggle_out/v1/par.json`, `kaggle_out/v3/par.json`; four probe files cycled across persistent spawned workers |
| Inputs / locks / mounts | v1/v3 `diag.json`; 9 input hashes; locked sync unchanged; managed Python clean; system torch stayed 2.10.0+cpu |
| Output retrieval | `probe_out/output_v1_*.txt`, `files_v1_page*.json`, downloaded archive/binary and nested files in v1 |
| Session rejection / quota | `probe_out/push_v3_retry.log`, `probe_out/quota.txt` |

## Sources

Primary online sources (saved copies/earlier fetches count as source evidence; mutable pages may differ from snapshots):

- [Kaggle notebook docs](https://www.kaggle.com/docs/notebooks): `web/kaggle_docs_notebooks.rendered.md`, technical specs and environments; direct current fetch was an empty JS shell.
- [Kaggle dataset docs](https://www.kaggle.com/docs/datasets): `web/kaggle_docs_datasets.rendered.md`, processing/archive/storage behavior.
- [CLI 2.2.4 metadata](https://raw.githubusercontent.com/Kaggle/kaggle-cli/v2.2.4/docs/kernels_metadata.md), [implementation](https://raw.githubusercontent.com/Kaggle/kaggle-cli/v2.2.4/src/kaggle/api/kaggle_api_extended.py), [dataset commands](https://raw.githubusercontent.com/Kaggle/kaggle-cli/v2.2.4/docs/datasets.md); installed CLI source/help was also inspected.
- [Current kernel command docs](https://raw.githubusercontent.com/Kaggle/kaggle-cli/main/docs/kernels.md): saved `web/cli_main_kernels.md`; accelerator list differs from pinned CLI capabilities.
- [Kaggle docker-python](https://github.com/Kaggle/docker-python): saved README, Dockerfile template, package list, sitecustomize hook and registry manifests under `web/`; live image evidence takes precedence.
- [CPU concurrency discussion](https://www.kaggle.com/product-feedback/483684) and [historical output issue](https://www.kaggle.com/product-feedback/420538): saved discussion text; current CPU cap independently observed.
- [uv locking/sync](https://docs.astral.sh/uv/concepts/projects/sync/), [Python selection](https://docs.astral.sh/uv/concepts/python-versions/), [CPU torch indexing](https://docs.astral.sh/uv/guides/integration/pytorch/).
- [Torchaudio binary compatibility](https://docs.pytorch.org/audio/stable/installation.html).
- [Measured checkpoint download URL](https://download.pytorch.org/torchaudio/models/wav2vec2_fairseq_base_ls960_asr_ls960.pth); bytes/hash above from actual Kaggle retrieval.
