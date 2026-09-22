# The Reachable Human Phenotype

Factorized Selfhood, Morphology-Congruent Binding, and What the Decisive Experiment Costs.

Capability, body ownership, agency and identity are studied in separate literatures, and each has shown that its object can be moved: synchronous multisensory evidence produces ownership of rubber hands, third arms and virtual cat ears, avatars alter later behavior, and some communities report persistent nonhuman self-models or cultivated inner agents. We treat these findings as coordinates of one object, the reachable human phenotype, the set of configurations a nervous system can enter through physiological change, sensory perturbation, learning and context, and propose ten coordinates. A single scalar would miss the clearest available dissociation, in which ownership of virtual cat ears rose in 24 participants while proprioceptive drift did not. The one direct study of body ownership in a nonhuman-identifying community found 50 furries reporting weaker embodiment of a human rubber hand, the opposite of what global plasticity predicts. A causal-inference model of ownership with a morphology-congruence prior reproduces that sign and, from the same parameter shift, predicts ownership of a congruent nonhuman body higher by 0.22. In simulation, the design used so far recovers the true theory in 0.51 of fits and reads morphology-congruent binding as global plasticity 96.5 percent of the time; a crossed design manipulating morphology against identity congruence recovers it in 0.94 and needs about 25 participants per group for 80 percent power on the diagnostic interaction. A multiscale formalism separates fast state from slowly learned parameters, makes hysteresis measurable (55 percent of a trained gain survives the end of the perturbation), and states the SELF and OTHER binding hypothesis as a crossed prediction. None of the results is evidence about any person or community.

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

Requires `pandoc` and `xelatex` on PATH. From the workspace you can also run `papers build the-reachable-human-phenotype`.

Part of [piatra-papers](https://github.com/piatra-institute). See the workspace docs for the research and writing pipelines.
