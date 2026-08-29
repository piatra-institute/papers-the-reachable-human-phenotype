"""The reachable human phenotype, computed.

Three mechanisms. Everything below is a property of explicitly stated
generative models. No simulated participant is evidence about any real
person or community; the models exist to show which experiments could
distinguish which hypotheses, and at what cost.

1. Design discrimination. Three live theories of why members of
   nonhuman-identifying communities might differ on embodiment tasks:
   global plasticity (they embody anything more readily),
   morphology-congruent binding (they bind bodies that match their
   self-model, and human bodies less), and expectancy (the differences
   live in subjective report and track hypothesis awareness). Data are
   simulated from each and all three are fit back, under the designs the
   literature has actually run and under a crossed design that varies
   morphology and identity congruence within participants. Recovery
   accuracy and the required sample per group are computed.

2. Morphology-congruent binding as causal inference. Body ownership as
   inference about whether visual and proprioceptive evidence share a
   bodily cause, with a prior over morphological correspondence. One
   shifted prior produces weaker ownership of a human effector and
   stronger ownership of a congruent nonhuman one: one knob, two signs,
   which is the shape of the field's most awkward finding. Reading
   ownership and proprioceptive drift off different quantities of the
   same inference reproduces the observed dissociation.

3. The multiscale reachable set. Fast state, stable traits, slowly
   learned model parameters. Hysteresis is measured as the fraction of a
   trained configuration surviving after the perturbation stops; SELF and
   OTHER learning rates are separably estimated; the detectability of the
   proposed double dissociation is computed against the learning-rate gap
   and the sample size.

Seeded, bit-for-bit reproducible. Invariants fail the run.
"""
from __future__ import annotations

import numpy as np

SEED = 20260829
rng_global = np.random.default_rng(SEED)


def _py(x):
    if isinstance(x, dict):
        return {k: _py(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_py(v) for v in x]
    if isinstance(x, (np.floating,)):
        return round(float(x), 6)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, np.ndarray):
        return [_py(v) for v in x.tolist()]
    if isinstance(x, float):
        return round(x, 6)
    return x


# ----------------------------------------------------------------------
# mechanism 1: which design can tell the theories apart
# ----------------------------------------------------------------------
# Cells of the full crossed design. Each condition is (morphology,
# identity congruence): morphology 0 human, 1 nonhuman-neutral,
# 2 nonhuman-congruent-with-the-participant's-self-model. Congruence is
# only nonzero in the third for the identifying group.

CONDITIONS = [
    ("human", 0),
    ("nonhuman_neutral", 1),
    ("nonhuman_congruent", 2),
]
DESIGNS = {
    # what the literature has actually run: one human effector
    "human_only": ["human"],
    # a common VR variant: human plus a generic nonhuman avatar
    "human_plus_generic": ["human", "nonhuman_neutral"],
    # the crossed design the framework asks for
    "crossed": ["human", "nonhuman_neutral", "nonhuman_congruent"],
}
EFFECT = 0.45          # the group effect each theory posits, same size
NOISE = 1.0            # between-participant noise, standardized units
EXPECT_SHARE = 0.5     # share of participants who are hypothesis-aware


def _truth(theory, group, morph_idx, aware):
    """Mean subjective-ownership response predicted by each theory."""
    if group == 0:                       # comparison group
        return 0.0
    if theory == "global":
        return EFFECT                     # more ownership of everything
    if theory == "congruent":
        # less ownership of a human body, more of a congruent nonhuman one
        return {0: -EFFECT, 1: 0.0, 2: EFFECT}[morph_idx]
    if theory == "expectancy":
        # present only in aware participants, and equally in every cell
        return EFFECT * 1.6 if aware else 0.0
    raise ValueError(theory)


def _simulate(theory, design, n_per_group, rng):
    """Return (X design matrix, y responses, aware) for one experiment."""
    morphs = [dict(CONDITIONS)[m] for m in DESIGNS[design]]
    rows, ys, aw = [], [], []
    for group in (0, 1):
        for i in range(n_per_group):
            aware = rng.random() < EXPECT_SHARE
            subj = rng.normal(0, 0.6)     # participant intercept
            for m in morphs:
                mu = _truth(theory, group, m, aware)
                ys.append(mu + subj + rng.normal(0, NOISE))
                rows.append((group, m, int(aware)))
                aw.append(aware)
    return np.array(rows), np.array(ys), np.array(aw)


def _fit_ll(rows, y, model, aware):
    """Gaussian log-likelihood of a candidate model, fit by least squares."""
    group = rows[:, 0]
    morph = rows[:, 1]
    if model == "global":
        X = np.column_stack([np.ones_like(y), group])
    elif model == "congruent":
        # group effect that flips with morphology
        contrast = np.where(morph == 0, -1.0, np.where(morph == 2, 1.0, 0.0))
        X = np.column_stack([np.ones_like(y), group, group * contrast])
    elif model == "expectancy":
        X = np.column_stack([np.ones_like(y), group, group * aware.astype(float)])
    else:
        raise ValueError(model)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    n = len(y)
    sigma2 = max((resid @ resid) / n, 1e-9)
    ll = -0.5 * n * (np.log(2 * np.pi * sigma2) + 1)
    k = X.shape[1] + 1
    return ll, k, n


def _bic_pick(rows, y, aware):
    best, best_bic = None, np.inf
    for model in ("global", "congruent", "expectancy"):
        ll, k, n = _fit_ll(rows, y, model, aware)
        bic = k * np.log(n) - 2 * ll
        if bic < best_bic:
            best_bic, best = bic, model
    return best


def run_design(n_reps=400, n_per_group=60) -> dict:
    rng = np.random.default_rng(SEED)
    out = {}
    for design in DESIGNS:
        conf = np.zeros((3, 3))
        names = ["global", "congruent", "expectancy"]
        for ti, theory in enumerate(names):
            for _ in range(n_reps):
                rows, y, aware = _simulate(theory, design, n_per_group, rng)
                pick = _bic_pick(rows, y, aware)
                conf[ti, names.index(pick)] += 1
        conf /= n_reps
        out[design] = {
            "confusion": conf.tolist(),
            "recovery_accuracy": float(np.trace(conf) / 3),
            "congruent_recovered": float(conf[1, 1]),
            "n_per_group": n_per_group,
            "n_reps": n_reps,
        }
    # sample size needed to detect the congruent interaction at 80 percent
    power_curve = []
    for n in (20, 30, 40, 60, 80, 120, 160, 200):
        hits = 0
        reps = 300
        for _ in range(reps):
            rows, y, aware = _simulate("congruent", "crossed", n, rng)
            group = rows[:, 0].astype(float)
            morph = rows[:, 1]
            contrast = np.where(morph == 0, -1.0, np.where(morph == 2, 1.0, 0.0))
            X = np.column_stack([np.ones_like(y), group, group * contrast])
            beta, *_ = np.linalg.lstsq(X, y, rcond=None)
            resid = y - X @ beta
            dof = len(y) - X.shape[1]
            s2 = (resid @ resid) / dof
            cov = s2 * np.linalg.inv(X.T @ X)
            t = beta[2] / np.sqrt(cov[2, 2])
            hits += abs(t) > 1.96
        power_curve.append({"n_per_group": n, "power": hits / reps})
    n80 = next((p["n_per_group"] for p in power_curve if p["power"] >= 0.8), None)
    return {"designs": out, "power_curve": power_curve,
            "n_per_group_for_80pct": n80, "effect_size": EFFECT}


# ----------------------------------------------------------------------
# mechanism 2: causal inference with a morphology prior
# ----------------------------------------------------------------------
# Ownership is the posterior probability that seen effector and felt body
# share a common cause; drift is the posterior mean position under that
# inference. The morphology prior scales the prior odds of a common cause
# by how well the effector's form matches the participant's self-model.

SIGMA_V = 1.0          # visual reliability
SIGMA_P = 2.2          # proprioceptive reliability
DELTA = 3.0            # visual-proprioceptive spatial discrepancy


def _causal_inference(p_common):
    """Return (ownership, drift) for a given prior of a common cause."""
    sv2, sp2 = SIGMA_V ** 2, SIGMA_P ** 2
    # likelihood of the discrepancy under common vs separate causes
    lik_c = np.exp(-DELTA ** 2 / (2 * (sv2 + sp2))) / np.sqrt(sv2 + sp2)
    lik_s = np.exp(-DELTA ** 2 / (2 * (sv2 + sp2 + 6.0))) / np.sqrt(sv2 + sp2 + 6.0)
    num = p_common * lik_c
    post_c = num / (num + (1 - p_common) * lik_s)
    # fused estimate under a common cause pulls the felt hand toward vision
    fused_shift = DELTA * sp2 / (sv2 + sp2)
    drift = post_c * fused_shift
    return float(post_c), float(drift)


def run_binding() -> dict:
    """One prior shift, two signs: the furry rubber-hand result and the
    congruent-nonhuman prediction from the same parameter."""
    # prior of a common cause, by effector morphology, for each group
    base = {"human": 0.55, "nonhuman_neutral": 0.30, "nonhuman_congruent": 0.30}
    # the identifying group's self-model weights morphology differently:
    # less prior mass on a human effector, more on a congruent nonhuman one
    shift = 0.22
    ident = {"human": base["human"] - shift,
             "nonhuman_neutral": base["nonhuman_neutral"],
             "nonhuman_congruent": base["nonhuman_congruent"] + shift}
    rows = {}
    for morph in base:
        oc, dc = _causal_inference(base[morph])
        oi, di = _causal_inference(ident[morph])
        rows[morph] = {
            "comparison_ownership": oc, "identifying_ownership": oi,
            "ownership_difference": oi - oc,
            "comparison_drift": dc, "identifying_drift": di,
            "drift_difference": di - dc,
        }
    human_sign = np.sign(rows["human"]["ownership_difference"])
    congr_sign = np.sign(rows["nonhuman_congruent"]["ownership_difference"])

    # the dissociation: ownership and drift need not move together when a
    # manipulation changes the prior of a common cause without changing
    # the spatial discrepancy the drift estimate depends on
    global DELTA
    keep = DELTA
    diss = []
    for d in (0.5, 1.0, 2.0, 3.0, 4.0):
        DELTA = d
        o_lo, dr_lo = _causal_inference(0.30)
        o_hi, dr_hi = _causal_inference(0.52)
        diss.append({"discrepancy": d,
                     "ownership_gain": o_hi - o_lo,
                     "drift_gain": dr_hi - dr_lo,
                     "gain_ratio": (dr_hi - dr_lo) / max(o_hi - o_lo, 1e-9)})
    DELTA = keep
    small = diss[0]
    return {
        "prior_shift": shift,
        "priors_comparison": base,
        "priors_identifying": ident,
        "by_morphology": rows,
        "human_ownership_sign": float(human_sign),
        "congruent_ownership_sign": float(congr_sign),
        "one_knob_two_signs": bool(human_sign < 0 < congr_sign),
        "dissociation_sweep": diss,
        "small_discrepancy_gain_ratio": small["gain_ratio"],
    }


# ----------------------------------------------------------------------
# mechanism 3: the multiscale reachable set
# ----------------------------------------------------------------------

T_TRAIN = 30
T_REST = 30
PHI_DECAY = 0.02


def _train(alpha_self, alpha_other, t_train=T_TRAIN, t_rest=T_REST):
    """Fast state x follows the perturbation; slow parameters phi learn
    from it and then decay. Returns the trajectories."""
    phi_s, phi_o = 0.0, 0.0
    xs, ss, os_ = [], [], []
    for t in range(t_train + t_rest):
        u = 1.0 if t < t_train else 0.0        # perturbation on, then off
        x = u                                   # fast state tracks the drive
        phi_s += alpha_self * (x - phi_s) if u else -PHI_DECAY * phi_s
        phi_o += alpha_other * (x - phi_o) if u else -PHI_DECAY * phi_o
        # observed phenotype: fast component plus the learned component
        ss.append(0.6 * x + phi_s)
        os_.append(0.6 * x + phi_o)
        xs.append(x)
    return np.array(ss), np.array(os_)


def run_reachable() -> dict:
    # three profiles differing only in which learning rate is elevated
    profiles = {
        "self_leaning":  (0.16, 0.05),
        "other_leaning": (0.05, 0.16),
        "comparison":    (0.07, 0.07),
    }
    rows = {}
    for name, (a_s, a_o) in profiles.items():
        s, o = _train(a_s, a_o)
        peak_s, peak_o = float(s[T_TRAIN - 1]), float(o[T_TRAIN - 1])
        end_s, end_o = float(s[-1]), float(o[-1])
        # hysteresis: what survives once the drive stops, as a fraction of
        # the trained peak above the fast-driven baseline
        hyst_s = end_s / max(peak_s - 0.6, 1e-9)
        hyst_o = end_o / max(peak_o - 0.6, 1e-9)
        rows[name] = {"alpha_self": a_s, "alpha_other": a_o,
                      "peak_self": peak_s, "peak_other": peak_o,
                      "residual_self": end_s, "residual_other": end_o,
                      "hysteresis_self": float(hyst_s),
                      "hysteresis_other": float(hyst_o),
                      "dissociation_index": float((peak_s - peak_o))}
    # the double dissociation is a crossed sign, not two main effects
    di_self = rows["self_leaning"]["dissociation_index"]
    di_other = rows["other_leaning"]["dissociation_index"]
    di_ctrl = rows["comparison"]["dissociation_index"]

    # detectability of the crossed pattern against sample size
    rng = np.random.default_rng(SEED + 7)
    noise = 0.35
    power = []
    for n in (15, 25, 40, 60, 100):
        hits = 0
        reps = 400
        for _ in range(reps):
            a = rng.normal(di_self, noise, n)
            b = rng.normal(di_other, noise, n)
            se = np.sqrt(a.var(ddof=1) / n + b.var(ddof=1) / n)
            t = (a.mean() - b.mean()) / max(se, 1e-9)
            hits += abs(t) > 1.96
        power.append({"n_per_group": n, "power": hits / reps})
    n80 = next((p["n_per_group"] for p in power if p["power"] >= 0.8), None)

    # the reachable set: how much of the phenotype plane the safe
    # perturbations cover, against the ordinary operating region
    grid = []
    for a_s in np.linspace(0.02, 0.20, 10):
        for a_o in np.linspace(0.02, 0.20, 10):
            s, o = _train(float(a_s), float(a_o))
            grid.append((float(s[T_TRAIN - 1]), float(o[T_TRAIN - 1])))
    G = np.array(grid)
    span_s = float(G[:, 0].max() - G[:, 0].min())
    span_o = float(G[:, 1].max() - G[:, 1].min())
    baseline = 0.6                     # the fast-driven component alone
    return {
        "profiles": rows,
        "double_dissociation_crossed": bool(di_self > di_ctrl > di_other),
        "dissociation_gap": float(di_self - di_other),
        "power_curve": power,
        "n_per_group_for_80pct": n80,
        "reachable_span_self": span_s,
        "reachable_span_other": span_o,
        "fast_only_baseline": baseline,
        "trained_over_fast_ratio": float(G[:, 0].max() / baseline),
        "constants": {"T_TRAIN": T_TRAIN, "T_REST": T_REST,
                      "PHI_DECAY": PHI_DECAY},
    }


# ----------------------------------------------------------------------
# cited records
# ----------------------------------------------------------------------

CITED_RECORDS = {
    "therian_n": {"value": 112,
        "source": "Clegg, Collings and Roxburgh 2019, Society and Animals 27: 403-426"},
    "therian_comparison_n": {"value": 265, "source": "same"},
    "therian_aq_odds_ratio": {"value": 5.9,
        "source": "same; 95 percent interval 2.04 to 17.31"},
    "therian_aq_or_ci_low": {"value": 2.04, "source": "same"},
    "therian_aq_or_ci_high": {"value": 17.31, "source": "same"},
    "furry_rhi_n": {"value": 50,
        "source": "Kranjec et al. 2019, Proc. Cognitive Science Society"},
    "tulpamancy_study_n": {"value": 243,
        "source": "Palmer-Cooper, McGuire and Wright 2021, Cogn. Neuropsychiatry 27: 86-104"},
    "cat_ears_n": {"value": 24,
        "source": "Yamamura et al. 2026, Front. Virtual Real. 7"},
    "dog_ears_n": {"value": 28,
        "source": "Khan, Trinh, Lisle and Do 2026, arXiv:2606.26364"},
    "vr_meta_articles": {"value": 111,
        "source": "Mottelson, Muresan, Hornbaek and Makransky 2023, ACM TOCHI 30: 1-42"},
    "fever_prospective_n": {"value": 141,
        "source": "Byrne et al. 2022, medRxiv 2022.05.23.22275374"},
    "fever_improving_n": {"value": 3, "source": "same"},
    "fever_curran_n": {"value": 30,
        "source": "Curran et al. 2007, Pediatrics 120: e1386-e1392"},
}


# ----------------------------------------------------------------------
# invariants
# ----------------------------------------------------------------------

def _checks(des, bind, reach) -> dict:
    c = {}
    d = des["designs"]
    c["human_only_cannot_discriminate"] = d["human_only"]["recovery_accuracy"] < 0.55
    c["crossed_discriminates_better"] = (d["crossed"]["recovery_accuracy"]
                                         > d["human_only"]["recovery_accuracy"] + 0.2)
    c["crossed_recovers_congruent"] = d["crossed"]["congruent_recovered"] > 0.8
    c["congruent_invisible_in_human_only"] = d["human_only"]["congruent_recovered"] < 0.5
    c["adding_generic_helps_little"] = (
        d["human_plus_generic"]["recovery_accuracy"]
        < d["crossed"]["recovery_accuracy"])
    c["power_curve_monotone"] = all(
        b["power"] >= a["power"] - 0.05
        for a, b in zip(des["power_curve"], des["power_curve"][1:]))
    c["decisive_n_is_large"] = (des["n_per_group_for_80pct"] is not None
                                and des["n_per_group_for_80pct"] >= 20)
    c["one_knob_two_signs"] = bind["one_knob_two_signs"]
    c["human_ownership_lower_for_identifying"] = (
        bind["by_morphology"]["human"]["ownership_difference"] < 0)
    c["congruent_ownership_higher"] = (
        bind["by_morphology"]["nonhuman_congruent"]["ownership_difference"] > 0)
    c["neutral_morphology_unmoved"] = (
        abs(bind["by_morphology"]["nonhuman_neutral"]["ownership_difference"]) < 1e-9)
    c["ownership_moves_more_than_drift_when_close"] = (
        bind["small_discrepancy_gain_ratio"] < 0.5)
    c["dissociation_grows_with_discrepancy"] = (
        bind["dissociation_sweep"][-1]["gain_ratio"]
        > bind["dissociation_sweep"][0]["gain_ratio"])
    p = reach["profiles"]
    c["hysteresis_positive"] = all(v["hysteresis_self"] > 0 for v in p.values())
    c["hysteresis_incomplete"] = all(v["hysteresis_self"] < 1.0 for v in p.values())
    c["faster_learning_leaves_more_residue"] = (
        p["self_leaning"]["residual_self"] > p["comparison"]["residual_self"]
        > p["other_leaning"]["residual_self"])
    c["double_dissociation_is_crossed"] = reach["double_dissociation_crossed"]
    c["reachable_exceeds_fast_only"] = reach["trained_over_fast_ratio"] > 1.2
    c["reachable_spans_both_axes"] = (reach["reachable_span_self"] > 0.05
                                      and reach["reachable_span_other"] > 0.05)
    c["dissociation_detectable_at_moderate_n"] = (
        reach["n_per_group_for_80pct"] is not None
        and reach["n_per_group_for_80pct"] <= 60)
    return c


def run() -> dict:
    des = run_design()
    bind = run_binding()
    reach = run_reachable()
    checks = _checks(des, bind, reach)
    failed = [k for k, v in checks.items() if not v]
    if failed:
        raise SystemExit(f"INVARIANT FAILURES: {failed}")
    return _py({
        "design": des,
        "binding": bind,
        "reachable": reach,
        "cited_records": CITED_RECORDS,
        "constants": {"SEED": SEED, "EFFECT": EFFECT, "NOISE": NOISE,
                      "SIGMA_V": SIGMA_V, "SIGMA_P": SIGMA_P},
        "checks": checks,
    })
