"""Figures for *The Reachable Human Phenotype*. Each reads the results
dict and writes one PNG.

Palette (CVD-checked in a prior validation; line styles and direct labels
as secondary encoding): amber, green, blue, warm gray; red for harm or
failure.
"""
from __future__ import annotations

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK = "#1a1a1a"
GRID = "#d9d9d9"
AMBER = "#b45309"
GREEN = "#15803d"
BLUE = "#2563eb"
GRAY = "#57534e"
RED = "#b3202c"

THEORIES = ["global\nplasticity", "morphology-\ncongruent", "expectancy"]
DESIGN_LABEL = {"human_only": "human effector only\n(the design run so far)",
                "human_plus_generic": "human plus a generic\nnonhuman avatar",
                "crossed": "crossed: morphology by\nidentity congruence"}


def _style(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(INK)
    ax.tick_params(colors=INK, labelsize=8.5)
    ax.set_axisbelow(True)


def plot_design(res: dict, path: str) -> None:
    des = res["design"]
    order = ["human_only", "human_plus_generic", "crossed"]
    fig, axes = plt.subplots(1, 4, figsize=(12.4, 3.6),
                             gridspec_kw={"width_ratios": [1, 1, 1, 1.15]})
    for ax, name in zip(axes[:3], order):
        M = np.array(des["designs"][name]["confusion"])
        ax.imshow(M, cmap="Blues", vmin=0, vmax=1)
        for i in range(3):
            for j in range(3):
                ax.annotate(f"{M[i, j]:.2f}", (j, i), ha="center", va="center",
                            fontsize=8,
                            color="white" if M[i, j] > 0.5 else INK)
        ax.set_xticks(range(3))
        ax.set_xticklabels(THEORIES, fontsize=6.6)
        ax.set_yticks(range(3))
        ax.set_yticklabels(THEORIES if name == "human_only" else ["", "", ""],
                           fontsize=6.6)
        acc = des["designs"][name]["recovery_accuracy"]
        ax.set_title(f"{DESIGN_LABEL[name]}\nrecovery {acc:.2f}",
                     fontsize=8.5, color=INK)
        ax.grid(False)
        if name == "human_only":
            ax.set_ylabel("true theory", fontsize=8.5)
        ax.set_xlabel("selected", fontsize=8.5, labelpad=14)
    mis = np.array(des["designs"]["human_only"]["confusion"])[1, 0]
    axes[0].annotate(f"congruent binding is read as global plasticity "
                     f"{mis:.1%} of the time",
                     (1.0, 2.95), fontsize=7.4, color=RED, ha="center",
                     va="top", annotation_clip=False)
    ax = axes[3]
    pc = des["power_curve"]
    ax.plot([p["n_per_group"] for p in pc], [p["power"] for p in pc],
            "-o", color=BLUE, lw=1.8, ms=4)
    ax.axhline(0.8, color=GRAY, lw=0.9, ls="--")
    pf = des["power_curve_fine"]
    ax.plot([p["n_per_group"] for p in pf], [p["power"] for p in pf],
            "o", color=GREEN, ms=2.6)
    n80 = des["n_per_group_for_80pct_fine"]
    ax.axvline(n80, color=GREEN, lw=0.9, ls=":")
    ax.annotate(f"80 percent power at\n{n80} per group", (n80 + 8, 0.74),
                fontsize=7.6, color=GREEN)
    ax.set_xlabel("participants per group", fontsize=8.5)
    ax.set_ylabel("power for the interaction", fontsize=8.5)
    ax.set_title("power for the crossed interaction", fontsize=9, color=INK)
    ax.grid(True, color=GRID, lw=0.5, alpha=0.7)
    _style(ax)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_binding(res: dict, path: str) -> None:
    b = res["binding"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 3.9))
    morphs = ["human", "nonhuman_neutral", "nonhuman_congruent"]
    labels = ["human\neffector", "nonhuman,\nneutral", "nonhuman,\ncongruent"]
    comp = [b["by_morphology"][m]["comparison_ownership"] for m in morphs]
    iden = [b["by_morphology"][m]["identifying_ownership"] for m in morphs]
    x = np.arange(3)
    w = 0.36
    ax1.bar(x - w / 2, comp, width=w, color=GRAY, label="comparison group")
    ax1.bar(x + w / 2, iden, width=w, color=BLUE,
            label="identifying group (one shifted prior)")
    for i in range(3):
        d = iden[i] - comp[i]
        if abs(d) > 1e-6:
            ax1.annotate(f"{d:+.2f}", (x[i] + w / 2, iden[i]), fontsize=8,
                         ha="center", va="bottom",
                         color=RED if d < 0 else GREEN,
                         xytext=(0, 2), textcoords="offset points")
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, fontsize=8)
    ax1.set_ylabel("ownership (posterior of a common cause)", fontsize=9)
    ax1.set_title("ownership by morphology under one\n"
                  "shifted morphology-congruence prior",
                  fontsize=9.5, color=INK)
    ax1.set_ylim(0, max(max(comp), max(iden)) * 1.42)
    ax1.legend(frameon=False, fontsize=7.8, loc="upper center")
    ax1.grid(True, color=GRID, lw=0.5, alpha=0.7)
    _style(ax1)
    sw = b["dissociation_sweep"]
    d = [s["discrepancy"] for s in sw]
    ax2.plot(d, [s["ownership_gain"] for s in sw], "-o", color=BLUE, lw=1.8,
             ms=4, label="ownership gain")
    ax2.plot(d, [s["drift_gain"] for s in sw], "-s", color=AMBER, lw=1.8,
             ms=4, label="proprioceptive drift gain")
    cross = next((s["discrepancy"] for s in sw
                  if s["gain_ratio"] >= 1.0), None)
    if cross is not None:
        ax2.axvline(cross, color=GRAY, lw=0.9, ls=":")
    top = max(s["drift_gain"] for s in sw)
    ax2.set_ylim(0, top * 1.30)
    ax2.annotate("ownership moves more than drift\n"
                 "(regime of the cat-ear result)",
                 (d[0] + 0.05, top * 0.60), fontsize=7.4, color=INK)
    ax2.annotate("drift dominates here", (d[-1] - 0.1, top * 0.22),
                 fontsize=7.4, color=GRAY, ha="right")
    ax2.set_xlabel("visual-proprioceptive discrepancy", fontsize=9)
    ax2.set_ylabel("change under the same prior shift", fontsize=9)
    ax2.set_title("ownership and drift against discrepancy",
                  fontsize=9.5, color=INK)
    ax2.legend(frameon=False, fontsize=8, loc="upper left")
    ax2.grid(True, color=GRID, lw=0.5, alpha=0.7)
    _style(ax2)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_reachable(res: dict, path: str) -> None:
    r = res["reachable"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 3.9))
    prof = r["profiles"]
    names = ["self_leaning", "comparison", "other_leaning"]
    labels = ["faster SELF\nlearning", "matched", "faster OTHER\nlearning"]
    di = [prof[n]["dissociation_index"] for n in names]
    cols = [BLUE, GRAY, AMBER]
    ax1.bar(range(3), di, color=cols, width=0.55)
    for i, v in enumerate(di):
        ax1.annotate(f"{v:+.2f}", (i, v), fontsize=8.5, ha="center",
                     va="bottom" if v >= 0 else "top", color=INK,
                     xytext=(0, 3 if v >= 0 else -3),
                     textcoords="offset points")
    ax1.axhline(0, color=INK, lw=0.9)
    ax1.set_xticks(range(3))
    ax1.set_xticklabels(labels, fontsize=8)
    ax1.set_ylabel("SELF minus OTHER binding", fontsize=9)
    ax1.set_title("SELF minus OTHER binding\nby profile",
                  fontsize=9.5, color=INK)
    ax1.grid(True, color=GRID, lw=0.5, alpha=0.7)
    _style(ax1)
    # right: trained trajectory with the perturbation removed
    T = r["constants"]["T_TRAIN"]
    R = r["constants"]["T_REST"]
    base = r["fast_only_baseline"]
    peak = prof["self_leaning"]["peak_self"]
    resid = prof["self_leaning"]["residual_self"]
    t = np.arange(T + R)
    curve = np.where(t < T,
                     base + (peak - base) * (1 - np.exp(-0.16 * t)),
                     resid * np.exp(-0.02 * (t - T)) + 0.0)
    ax2.plot(t, curve, "-", color=BLUE, lw=1.9)
    ax2.axvspan(0, T, color=GREEN, alpha=0.08, lw=0)
    ax2.axhline(base, color=GRAY, lw=0.9, ls="--")
    ax2.annotate("perturbation on", (T / 2, peak * 1.02), fontsize=7.8,
                 color=GREEN, ha="center")
    ax2.annotate("fast component alone", (T + R - 1, base + 0.03),
                 fontsize=7.6, color=GRAY, ha="right")
    hy = prof["self_leaning"]["hysteresis_self"]
    ax2.annotate(f"residual after the drive:\n{hy:.0%} of the trained gain",
                 (T + 2, resid + 0.28), fontsize=7.8, color=INK)
    ax2.set_xlabel("session", fontsize=9)
    ax2.set_ylabel("SELF binding", fontsize=9)
    ax2.set_title("SELF binding during training\nand after the perturbation stops", fontsize=9.5, color=INK)
    ax2.grid(True, color=GRID, lw=0.5, alpha=0.7)
    _style(ax2)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
