# Contrastive Voice dashboard (DESIGN 10): slim image, ffmpeg, the locked environment (CPU torch: --extra cpu), the aligner checkpoint baked in and
# verified by SHA-256, port 7860, non-root. Build and run:
#   docker build -t cvoice . && docker run --rm -p 7860:7860 cvoice
FROM python:3.12-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:0.12.3 /uv /bin/uv
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --uid 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/app/.venv/bin:$PATH \
    UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_NO_CACHE=1 UV_PYTHON_DOWNLOADS=0
WORKDIR /home/user/app

# dependencies first (cached layer), then the project
COPY --chown=user pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project --extra cpu
COPY --chown=user . .
RUN uv sync --locked --no-dev --extra cpu

# bake the aligner checkpoint: torchaudio downloads it, load_aligner() fails the build unless its size and SHA-256
# (488fd4f16de84438ffc945334278c1b9fb9b7159a806c1080b16111a958c945d, 377,664,473 bytes) match the pinned values
RUN python -c "from cvoice.align import load_aligner; load_aligner()"

EXPOSE 7860
CMD ["python", "-m", "cvoice.app", "--host", "0.0.0.0", "--port", "7860"]
