"""Draw docs/img/pipeline.png, the pipeline diagram of docs/technical.md.

Run from any directory: .venv/bin/python scripts/make_pipeline_figure.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).resolve().parent.parent / "docs" / "img" / "pipeline.png"

# (title, detail); the fifth stage is the only place where the two regimes differ
STAGES = [
    ("Inputs", "participant audio\nreference audio\ntranscript"),
    ("Decode, align", "16 kHz mono\nwav2vec 2.0 + CTC\nword times"),
    ("Features", "pitch, level, pauses\nstress points\nspectral change"),
    ("Compare", "same words in\nboth recordings\nsix differences"),
    ("Threshold rule", "scale from null pairs\nregime R1 or R2\nno trained classifier"),
    ("Result JSON", "flagged regions\nexplanations\nscores"),
    ("Dashboard", "overlay charts\nA/B playback\nupload"),
]
W, H, GAP = 0.9, 0.6, 0.115  # box width, box height, gap between boxes (inches)


def main() -> None:
    n = len(STAGES)
    width = n * W + (n - 1) * GAP
    fig = plt.figure(figsize=(width + 0.04, H + 0.04))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-0.02, width + 0.02)
    ax.set_ylim(-0.02, H + 0.02)
    ax.axis("off")
    for i, (title, detail) in enumerate(STAGES):
        x = i * (W + GAP)
        ax.add_patch(FancyBboxPatch((x, 0), W, H, boxstyle="round,pad=0,rounding_size=0.04",
                                    linewidth=0.7, edgecolor="#333333", facecolor="#f2f2f2"))
        ax.text(x + W / 2, H - 0.05, title, ha="center", va="top", fontsize=7, fontweight="bold", color="#111111")
        ax.text(x + W / 2, H - 0.19, detail, ha="center", va="top", fontsize=5.8, color="#111111", linespacing=1.15)
        if i < n - 1:
            ax.annotate("", xy=(x + W + GAP, H / 2), xytext=(x + W, H / 2),
                        arrowprops=dict(arrowstyle="-|>", linewidth=0.7, color="#333333", shrinkA=0, shrinkB=0))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=300)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
