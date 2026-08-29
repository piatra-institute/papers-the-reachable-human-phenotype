# Brief

Written before research begins.

## Question

Cognitive neuroscience treats capability, body ownership, agency, and identity as separate literatures with separate methods. Each has independently shown that its object moves: stimulation effects depend on the brain's initial state, synchronous multisensory evidence gives people ownership of rubber hands and third arms and virtual cat ears, avatars feed back into behavior, and communities exist whose members report persistent nonhuman self-models or cultivated internal agents that answer back. If the phenotype moves along all these axes, the ordinary waking adult occupies a small region of something larger. What is the shape of the region a human nervous system can safely reach, which of its coordinates are separable, and what would it cost to find out?

## Claim

The default phenotype is a point in a space, the space has partly separable coordinates, and the experiment that would map it is specifiable and expensive in a computable way. Five moves carry the paper:

1. **A factorized phenotype rather than a stronger or weaker self.** Ten coordinates: capability, body ownership, body schema, self-location, agency, identity, memory access, perceptual organization, affect, and reality testing. The 2026 cat-ear experiment is the paper's proof that the factorization is forced rather than tidy: congruent multisensory evidence raised subjective ownership of virtual cat ears while proprioceptive drift did not follow, so ownership and spatial body schema moved apart in one experiment. Any scalar strength-of-alternate-self would have erased that result, and with it the only clean dissociation the field has.
2. **The anomaly that is a prediction.** The one direct study of body ownership in a nonhuman-identifying community found furries reporting weaker subjective embodiment of a human rubber hand, with proprioceptive drift predicted by how little they valued the human form. A global-plasticity theory predicts the opposite sign. The paper's second mechanism shows that a Bayesian causal-inference model of ownership, given a single shifted morphology prior, produces the observed weaker human-hand ownership and a stronger congruent-nonhuman ownership from the same parameter: one knob, two signs, so the field's most awkward result becomes the framework's cleanest support.
3. **Generative binding of SELF and OTHER.** The disciplined version of a loose intuition: therian-like identification may involve morphology-congruent binding of nonhuman representations to SELF, and cultivated inner agents may involve learned binding of internally generated representations to OTHER. This is a hypothesis, it has never been tested, and its prediction is a double dissociation under matched training rather than a general increase in suggestibility.
4. **The design analysis, computed.** The paper's central practical contribution: the three live theories, global plasticity, morphology-congruent binding, and expectancy, make near-identical predictions under every design the literature has actually run, and separate only under a crossed design that manipulates morphology and identity congruence within participants. The simulation computes how identifiable each theory is under each design and how many participants per group the crossed design needs, turning "nobody has run the right experiment" into a costed protocol with a number attached.
5. **Fast states, slow models, and hysteresis.** A rubber hand takes seconds and a fursona takes years, so one timescale cannot hold both. The multiscale formalism separates fast neural state, stable individual traits, and slowly learned generative-model parameters, defines the safely reachable set under bounded perturbations, and makes hysteresis measurable: the fraction of a trained configuration that persists after the driving perturbation stops, which is what distinguishes a learned identity from a maintained illusion.

## Kind

**formal-model + programme**, ships a simulation. `has_simulation: true`, `claims_target: results.json`. Everything computed is a property of explicitly stated generative models; the paper never presents simulated participants as evidence about real people, and says so wherever a number appears.

## Constraint

The paper stands alone and cites no PIATRA paper. The communities discussed are real, and the discipline follows the seed's own best instincts: community terminology used as communities use it, no inference from unusual content to disorder, the clinical literature cited strictly as a boundary condition with its own caution repeated, and the explicit statement that a persistent nonstandard self-model may be neutral, valuable, or distressing and that function must be measured rather than assumed. The bootloader metaphor that motivated the enquiry is retired in the text with its four specific errors named. No claim that fever unlocks capacities, that therians carry a neural animal body map, that a tulpa is a second consciousness, or that any of these share one mechanism. Speculation is marked wherever it occurs.

## Cornerstone literature

Each with one job:

- **Botvinick and Cohen** — the rubber hand; the founding demonstration that ownership is inferential.
- **Samad, Chung and Shams** — ownership as Bayesian causal inference; the model the paper extends with a morphology prior.
- **Blanke, Slater and Serino** — bodily self-consciousness decomposed into ownership, self-location, and perspective; the precedent for factorization.
- **Seth** — interoceptive inference; the self as a controlled hallucination with a body in it.
- **Guterstam, Petkova and Ehrsson** — the third arm; supernumerary ownership.
- **Arai et al.** — supernumerary limbs changing peripersonal space; ownership with a crossmodal correlate.
- **Won, Bailenson, Lee and Lanier** — homuncular flexibility; learning to drive a body you do not have.
- **Krekhov, Cmentowski and Krüger; Khan et al.; Yamamura et al.** — animal avatars, dog ears, and the cat-ear dissociation.
- **Yee and Bailenson** — the Proteus effect; avatars feeding back into behavior.
- **Mottelson, Muresan, Hornbæk and Makransky** — the meta-analysis: modest ownership effects, weak power, inconsistent terminology; the reason the design analysis matters.
- **Kranjec et al.** — the furry rubber-hand study; the sign that breaks the naive theory.
- **Clegg, Collings and Roxburgh; Grivell, Clegg and Roxburgh; Luiggi-Hernández et al.** — the therian quantitative and phenomenological record.
- **Palmer-Cooper, McGuire and Wright; Taylor, Hodges and Kohányi** — cultivated agents and authorial characters; unusual experience without delusion-proneness.
- **Roberts, Plante, Gerbasi and Reysen** — liking an animal and being one are psychometrically separable.
- **Blom and Sharpless** — clinical therianthropy; the boundary condition, with its own warning against pathologizing.
- **Curran et al.; Byrne et al.** — the fever natural experiment and its disappointing replication; the paper's model of how to hold a natural experiment honestly.
