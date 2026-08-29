# The Reachable Human Phenotype

Factorized Selfhood, Morphology-Congruent Binding, and What the Decisive Experiment Costs. Cognitive neuroscience studies capability, body ownership, agency, and identity in separate literatures, and each has independently shown that its object moves. This paper treats them as coordinates of one object, the set of configurations a nervous system can enter through physiological change, sensory perturbation, learning, and context. The factorization is forced rather than tidy: a 2026 experiment raised subjective ownership of virtual cat ears in 24 participants while proprioceptive drift did not follow, so any scalar strength-of-alternate-self would have erased the field's cleanest dissociation. The paper's hinge is an awkward result. The one direct study of body ownership in a nonhuman-identifying community found 50 furries reporting weaker embodiment of a human rubber hand, the opposite sign from a global-plasticity account; a causal-inference model of ownership with a morphology-congruence prior reproduces that sign and predicts stronger congruent-nonhuman ownership from the same shifted parameter, moving 0.22 in each direction, so the anomaly becomes support. The central practical contribution is a design analysis: simulating three live theories and fitting all three back, the design the literature has run recovers the truth at 0.51 and misreads morphology-congruent binding as global plasticity 96 percent of the time; adding a generic nonhuman avatar reaches 0.73; only a crossed design manipulating morphology against identity congruence reaches 0.94, needing about 30 participants per group for 80 percent power on the interaction rather than the 20 typical of embodiment work. A multiscale formalism separates fast neural state from slowly learned model parameters, makes hysteresis measurable as the 55 percent of a trained configuration surviving after the perturbation stops, and states the SELF and OTHER binding hypothesis as a crossed prediction rather than a main effect. Nothing here is evidence about any person or community; the models exist to say which experiment would be, and what it would cost.

## Simulation

```bash
cd simulation
uv run run_all.py        # -> output/results.json + output/figures/*.png
```

Seeded, bit-for-bit reproducible. Every quantity is a property of the stated generative models and none is an empirical estimate. Twenty invariant checks fail the run loudly if broken, among them: the human-only design's failure to discriminate and its specific misreading of congruent binding as global plasticity; the crossed design's recovery; the monotone power curve and its threshold; the one-knob-two-signs property with its neutral-morphology control; the ownership-over-drift regime at small sensory discrepancy and its reversal at large; positive but incomplete hysteresis; the crossed rather than main-effect form of the double dissociation; and the trained region exceeding the fast-driven baseline.

## Build

```bash
uv run build.py          # -> paper/PAPER.pdf  (vendored canonical recipe)
```

Requires `pandoc` and `xelatex` on PATH. From the workspace you can also run
`papers build the-reachable-human-phenotype`.

Part of [piatra-papers](https://github.com/piatra-institute). See the workspace
docs for the research and writing pipelines.
