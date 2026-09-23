# Audit

Dated log of editorial passes and verification runs. Newest first.

## 2026-09-23 — structured-evidence migration

Structured-evidence migration (references and claims).
- references.yaml: 22 CSL entries. 21 resolved through doi.org content negotiation (Crossref, DataCite for the arXiv preprint, medRxiv DOI for Byrne et al.) and checked for year, title and authors; kranjec2019 entered by hand from the OpenAlex record of eScholarship 37x5162v (CogSci 2019, pp. 596-602). In-text citations converted to Pandoc [@id]; the legacy list replaced by the citeproc-rendered list (Chicago author-date).
- Correction: krekhov2019 had been listed in the CHI PLAY 2019 proceedings, pp. 439-451, with sources.md giving DOI 10.1145/3311350.3347172; that DOI is the group's "Beyond Human" paper. The cited paper appeared at the 2019 IEEE Conference on Games, pp. 1-8, DOI 10.1109/CIG.2019.8848005.
- Correction: kranjec2019 authors "Kranjec, A., Cardillo, E. R., Chatterjee, A., et al." -> Kranjec, Lamanna, Guzman, Plante, Reysen, Gerbasi, Roberts, Fein (OpenAlex record).
- Correction: byrne2022 first author "Byrne, R. E." -> Katherine Byrne; yamamura2026 first author "R." -> Hiroo Yamamura, with Maki Sugimoto added as fifth author; luiggihernandez2025 adds Roberts and Gerbasi; full titles restored for Blom and Sharpless ("...Conceptualize Zoomorphism as a Diagnostic Spectrum"), Luiggi-Hernández et al. ("...Among Therians and Otherkin") and Yamamura et al. In-text citations all render as "et al.", so no sentence changed.
- claims.yaml: 48 claims (21 computation, 13 source, 3 definition, 3 assumption, 6 interpretation, 2 normative). All simulation numbers in abstract and body bound to results.json (the human-hand ownership decrease with scale -1 on the signed difference). Source claims checked against Crossref/DataCite/OpenAlex abstracts (Yamamura et al. 24 participants and drift null, Khan et al. n = 28, Mottelson et al. 111 articles, Roberts et al., Palmer-Cooper et al. 243, Taylor et al., Kranjec et al. direction of effect, Samad et al., Curran et al. 30 + 30, Guterstam et al., Arai et al., Won et al., Krekhov et al., Yee and Bailenson, Seth).
- Unverified, not bound: Kranjec et al. sample of 50 and the historical-comparison design (abstract gives neither); Clegg et al. predictors and the odds ratio 5.9 (2.04-17.31) (abstract gives only 112 and 265); Byrne et al. "of the 50 who had a fever" (abstract gives 3 of 244 children with consistent improvement); Grivell et al. phantom parts (abstract gives five interviews and themes only); Blom and Sharpless's caution (not in abstract); Luiggi-Hernández et al., Blanke et al. and Botvinick and Cohen (no abstract retrieved).
- Run: reachable (uv run python run_all.py); results.json reproduced byte for byte.
- metadata claims_target: claim-ledger.

## 2026-09-22 — prose revision

Prose rewritten against the house standards. Headings made descriptive (Introduction, Coordinates of the phenotype, Evidence from nonhuman-identifying and plural communities, A morphology-congruence model of body ownership, Design analysis, A multiscale formalism, Limits of the software metaphor, Natural experiments: fever in autism, Ethics and dual use, Objections, Falsification, Scope of the claims, Reproducibility).

Corrections found during the pass:
  - The sample size for 80 percent power on the crossed interaction was reported as "about 30 per group". 30 was the first point of a coarse grid (20, 30, 40, ...) above 0.8; power at 20 is 0.71 and at 30 is 0.89. A per-participant scan from 20 to 30 (2,000 replicates each, separate random stream) crosses 0.8 at 25. The text now says about 25 per group; new fields design.power_curve_fine and design.n_per_group_for_80pct_fine, invariant fine_n80_inside_grid_bracket. The contrast with the typical 20 per group is weaker than stated before and is now given with the power at 20.
  - The SELF and OTHER crossing was said to be detectable "at about 15 participants per group"; 15 was the first grid point and already had power 0.90. The closed-form two-sample calculation gives 11.0 per group; new field reachable.n_per_group_for_80pct_exact, invariant dissociation_closed_form_n80_below_grid (22 invariants).
  - Misclassification rates were rounded to whole percents that the values do not support (0.965 reported as 96, 0.975 as 97); now 96.5 and 97.5 percent.
  - Figure 2's power annotation was placed below the axis range and never rendered; it now shows the fine-scan value.

## 2026-08-29 — v1, draft complete; PDF build blocked by a missing TeX distribution

Scope: the entire paper, simulation, and evidence base, from the seed chat to the point where the build environment failed.

Changes:
  - Sources: 22 entries verified against Crossref, the arXiv API, or the live record. Seed corrections logged in research.md: the therian study DOI was wrong and resolves to Clegg, Collings and Roxburgh (2019) in Society and Animals; the homuncular-flexibility citation resolves to Won, Bailenson, Lee and Lanier (2015), 10.1111/jcc4.12107, where a neighbouring DOI returns an unrelated communication paper; the furry rubber-hand study is a 2019 Cognitive Science Society proceedings paper with historical comparison data, and both limitations are carried wherever the result is used; the Byrne fever study is a 2022 medRxiv preprint and is cited as such; the Veissière tulpa ethnography could not be resolved to a stable locator and was dropped, with Palmer-Cooper et al. and Taylor et al. carrying the cultivated-agent point; the seed's closed-loop optimization citations resolved only to adjacent stimulation work, so the closed-loop proposal is stated as architecture and cites no optimization result.
  - Community discipline enforced throughout: terminology used as the communities use it, no inference from unusual content to disorder, the clinical review cited strictly as a boundary condition with its authors' own caution repeated, re-identification risk in small online communities named as a design constraint, and the explicit statement that a persistent nonstandard self-model may be neutral, valuable, or distressing. The bootloader metaphor that motivated the enquiry is retired in the text with its four errors named.
  - Simulation design notes: the design-discrimination result came out sharper than the framing anticipated. The human-only design does not merely fail to discriminate at 0.51; it selects global plasticity 96 percent of the time when morphology-congruent binding is true, which means the field's one direct study could not have distinguished the account it appears to refute from the account it supports. That specific misclassification was promoted to a named finding and to an invariant. The dissociation figure's first annotation overstated the sweep, claiming ownership moves while drift barely does across the range when the model shows that only at small sensory discrepancy; the label was corrected to name the regime and its reversal.
  - Voice: draft came in at 1 error and 1 review-candidate; both fixed, then four rhythm passes took the longest run without a short sentence from 26 to 23 and raised the short-sentence share from 8 to 18 percent, with tricolon density reduced from 9.3 to 8.6 per thousand.

Verification:
  - voice: 0 errors, 0 review-candidates
  - refs: 22 in-text keys, 22 bib entries, 0 missing, 0 unused
  - claims: 106 sim values, 9 decimal claims in prose, 0 without a match
  - simulation: 20/20 invariants
  - build: 11 pages, no missing-character warnings
  - check => PASS

Environment note: the machine's TeX distribution disappeared mid-session (/usr/local/texlive removed, every symlink under /Library/TeX dangling, xelatex absent from PATH), which was confirmed environmental rather than paper-specific because a previously built paper in this workspace failed to rebuild with the identical error. BasicTeX was then installed, and it ships without `titling`, the one package in the house preamble it lacks; `titling.sty` was generated from the CTAN source and installed into the user tree at ~/Library/texmf, which needs no administrator password and leaves the system installation untouched. Both this paper and the previously built one now rebuild cleanly.

Post-build correction: the first rendered PDF revealed that the in-text figure numbers did not match document order, since the binding figure appears first but was called Figure 2 while the design figure appears second and was called Figure 1. References renumbered to document order and the paper rebuilt.
