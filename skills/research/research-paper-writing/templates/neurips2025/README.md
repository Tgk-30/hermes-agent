# NeurIPS 2025 Template

This directory contains the NeurIPS 2025 LaTeX template files used by the research-paper-writing skill.

## Files

- `main.tex` — starter paper file
- `neurips.sty` — NeurIPS style file
- `extra_pkgs.tex` — extra package imports shared by the template
- `Makefile` — basic build helper

## Quick start

```bash
cd skills/research/research-paper-writing/templates/neurips2025
pdflatex main.tex
```

If you add a bibliography, use the normal LaTeX/BibTeX cycle:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Notes

- `main.tex` currently ships as a minimal skeleton and should be edited before use.
- The style file includes checklist/TODO commands that are part of the upstream template; they are not unfinished code.
- If you want a cloud workflow, upload this folder to Overleaf and compile `main.tex` there.
