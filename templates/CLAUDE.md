# NT-Disk: Novikov-Thorne Astrophysics of Black Holes - LaTeX Translation

## Essentials

**Your role:** Take ownership of the project. Push it forward and maintain clear documentation. The human provides feedback and advice, but do not rely on them to keep track of the project---that's your job.

**Primary document:** The research notes. All research knowledge flows there. Follow the guidelines in the notes preamble when updating.

**Markers:**
- `[HYPOTHESIS]` / `[PRELIMINARY]` / `[SOLID]` --- confidence levels
- `[BLOCKING: ...]` --- needs human input to proceed
- `[FUTURE: ...]` --- deferred, revisit later
- `(ref: source)` --- evidence for claims

**Session start:** Read research notes -> Evaluate ("Any unmarked loose ends? Should we reframe?") -> Plan next steps

**Session end** (when human says "let's end this session" or "let's wrap up"):

Answer these questions in order, then update the notes accordingly:
1. What have I done/learned in this session (or since last update)?
2. What existing information would I update or remove?
3. What new information would I add?
4. Would I restructure the content of the notes? If yes, how?
5. Would I revise the overall narrative of the notes? If yes, how?

Then:
- Update the research notes
- Flag [BLOCKING] items for human attention
- If in a git repo: commit and push changes

**When human says "memorize this":**
- Finding, decision, research knowledge -> Add to research notes
- Workflow, code location, how-to -> Add to Technical Notes below
- Behavior, style, preference -> Add to Preferences section below

---

## Preferences and Behavior

- Use Physical Review D (PRD) LaTeX format with `revtex4-2` document class
- All equations use the paper's original numbering: (section.subsection.number)
- Preserve ALL mathematical detail---no simplification or omission
- CGS units for astrophysical quantities; geometrized units (c=G=1) where paper uses them
- Each translation agent produces its own .tex and .bib files
- Each agent commits individually
- Progress documented in markdown files in the `progress/` folder

**When to seek human feedback:**
- When you are unsure about your choice
- If you are confident but the choice involves subjectivity (no clear "best" criterion): proceed with your choice, but mention it to the human for feedback afterward

---

## Technical Notes

### Project Structure
```
NT disk/
  NT-Disk.pdf              # Original paper (53 PDF pages, rotated left, 2 subpages/page)
  input-1.md               # Task specification
  templates/               # CLAUDE.md and RESEARCH_NOTE.md templates
  progress/                # Stage progress reports and research diaries
  translate/
    agents/                # Individual agent .tex/.bib files (agent_01.tex, etc.)
    merged/                # Final merged document
  check/
    round1/               # First verification round (10 agents)
    round2/               # Second verification round (10 agents)
  conventions.md           # Converged math expression conventions
```

### Paper Structure
- **Title:** Astrophysics of Black Holes
- **Authors:** Igor D. Novikov (Moscow) and Kip S. Thorne (Caltech)
- **Pages:** 345--450 (106 book pages, 53 PDF pages)
- **Sections:** 6 main sections + references
- **PDF format:** Each page rotated left; each contains 2 book pages side-by-side

### Agent Page Assignments (28 agents, ~2 PDF pages each)
See `progress/agent_assignments.md` for detailed mapping.

### Compilation
```bash
pdflatex NT-Disk-translated.tex
bibtex NT-Disk-translated
pdflatex NT-Disk-translated.tex
pdflatex NT-Disk-translated.tex
```
