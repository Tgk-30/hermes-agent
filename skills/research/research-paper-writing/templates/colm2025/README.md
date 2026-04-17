# CoLM 2025 Template

Template and style files for CoLM 2025.

## Files in this directory

- `colm2025_conference.tex` — main paper template
- `colm2025_conference.sty` — conference style file
- `colm2025_conference.bst` — bibliography style
- `colm2025_conference.bib` — sample bibliography entries
- `math_commands.tex` — reusable math macros
- `natbib.sty`, `fancyhdr.sty` — bundled style dependencies
- `colm2025_conference.pdf` — rendered reference copy of the template

## Quick start

```bash
cd skills/research/research-paper-writing/templates/colm2025
pdflatex colm2025_conference.tex
bibtex colm2025_conference
pdflatex colm2025_conference.tex
pdflatex colm2025_conference.tex
```

## Submission vs camera-ready

The template defaults to submission mode:

```latex
\usepackage[submission]{colm2025_conference}
```

When preparing the final version, switch to the mode required by the official CoLM instructions instead of editing the style internals directly.

## Notes

- Keep author names hidden while in submission mode.
- Use `colm2025_conference.pdf` as the visual reference if you want to compare formatting.
- Prefer editing the sample template rather than modifying the `.sty` file unless you are intentionally maintaining the template itself.
