"""Orchestrator: reproduces every number and all three figures in the paper.

    cd simulation
    uv run run_all.py

Writes output/results.json and output/figures/*.png. Seeded; a rerun
reproduces every number bit for bit. A failed invariant fails the run.
"""
from __future__ import annotations

import json
from pathlib import Path

from analyses import run

OUT = Path(__file__).parent / "output"


def main() -> None:
    (OUT / "figures").mkdir(parents=True, exist_ok=True)
    results = run()
    (OUT / "results.json").write_text(json.dumps(results, indent=2))

    from figures import plot_design, plot_binding, plot_reachable
    plot_design(results, str(OUT / "figures" / "design.png"))
    plot_binding(results, str(OUT / "figures" / "binding.png"))
    plot_reachable(results, str(OUT / "figures" / "reachable.png"))

    d = results["design"]
    for name, v in d["designs"].items():
        print(f"design {name}: recovery {v['recovery_accuracy']:.3f}, "
              f"congruent recovered {v['congruent_recovered']:.3f}")
    print(f"  congruent read as global under the human-only design: "
          f"{d['designs']['human_only']['confusion'][1][0]:.2f}")
    print(f"  80 percent power at n = {d['n_per_group_for_80pct']} per group")
    b = results["binding"]
    print(f"binding: one knob two signs {b['one_knob_two_signs']}; human "
          f"{b['by_morphology']['human']['ownership_difference']:+.3f}, "
          f"congruent "
          f"{b['by_morphology']['nonhuman_congruent']['ownership_difference']:+.3f}")
    print(f"  drift-to-ownership gain ratio at small discrepancy: "
          f"{b['small_discrepancy_gain_ratio']:.3f}")
    r = results["reachable"]
    print(f"reachable: crossed dissociation {r['double_dissociation_crossed']}, "
          f"gap {r['dissociation_gap']:.3f}, detectable at n = "
          f"{r['n_per_group_for_80pct']}")
    print(f"  hysteresis {r['profiles']['self_leaning']['hysteresis_self']:.3f}; "
          f"trained over fast-only {r['trained_over_fast_ratio']:.2f}")
    print("checks:", f"{sum(results['checks'].values())}/{len(results['checks'])}")
    print("wrote", OUT / "results.json")


if __name__ == "__main__":
    main()
