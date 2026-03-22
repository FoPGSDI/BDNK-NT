# NT-Disk Translation: Research Notes

## Preamble: Guidelines for These Notes

*Read this section whenever updating.*

### What These Notes Should Be

Treat this as a publishable research paper, except:

- **Uncertainty is explicit** --- use markers (`[HYPOTHESIS]`, `[PRELIMINARY]`, `[SOLID]`)
- **Gaps are visible** --- mark them (`[BLOCKING]`, `[FUTURE]`), don't smooth over
- **Sections can be unbalanced** --- developed where we have results, skeletal where we don't
- **Abandoned paths are documented** --- in appendix, not omitted
- **Structure is provisional** --- may need revision as understanding evolves

**A good research note = a publishable paper with explicit, fully-enumerated holes.**

### Bidirectional Criterion

- **Forward:** Every marker, if resolved, should advance the paper
- **Backward:** Every loose end should be captured by a marker

If you see an unmarked gap, add a marker. If a marker wouldn't help when resolved, remove it.

### Update Guidelines

- **Extend existing sections** by default; new sections fragment the narrative
- **Add new section** only when content is genuinely a new thread
- **Revise in place** when information changes; don't append "UPDATE: actually..."
- **Prune to appendix** when abandoning an approach; don't delete, move
- **Restructure** when the narrative no longer fits; flag it, don't do silently

### Anti-patterns

- Smoothing gaps with hedging language instead of marking
- Hiding uncertainty to make it "read better"
- Balancing sections artificially
- Orphaned content that doesn't connect to narrative
- Premature polishing before content is settled

---

## Notes

### Thesis / Research Question

Faithfully translate the Novikov-Thorne "Astrophysics of Black Holes" paper (1973) from scanned PDF to LaTeX+BibTeX in Physical Review D format, preserving all mathematical content, equations, figures, and references. `[SOLID]`

### Motivation

This seminal paper on black hole accretion physics is only available as a scanned book chapter. A modern LaTeX version would make it citable, searchable, and accessible to current researchers.

### Translation Pipeline

1. **Stage 1 (Plan):** 28 agents scan pages, converge on math conventions `[PRELIMINARY]`
2. **Stage 2 (Translate):** 28 agents produce individual .tex/.bib files `[PRELIMINARY]`
3. **Stage 3 (Merge):** Single agent merges and compiles `[PRELIMINARY]`
4. **Stage 4 (Verify):** 10 agents x 2 rounds cross-check translations `[PRELIMINARY]`
5. **Stage 5 (Finalize):** Corrections applied, final compilation `[PRELIMINARY]`

### Convention Decisions

[To be filled during Stage 1 -- see conventions.md]

### Known Challenges

- PDF pages are rotated left with 2 book pages per PDF page
- Some equations have complex multi-line formatting
- Figure descriptions need to be preserved (figures themselves as placeholders)
- References span pages 448--450 with specific formatting
- Some text may be unclear due to scan quality

---

## Appendix

### Abandoned Approaches

[None yet]
