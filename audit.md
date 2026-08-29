# Audit

Dated log of editorial passes and verification runs. Newest first.

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
