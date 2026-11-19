# Manuscript sources and reproducibility

**Readers should start with the single PDF in [`../book/`](../book/).** This directory contains build tools and the preserved material needed for a source-aware research edition.

- `Information_Geometry_v0.1_original.pdf` — the original 27-page typeset text. The editable source of Chapters 1–5 has not been recovered.
- `Information_Geometry_v0.2_integrated_part_II.tex` — editable LaTeX for the new mathematical Chapters 6–11.
- `simplex_emblem.png` — artwork used by the generated front matter.
- `build_full_edition.py` — assembles a unified reading PDF, using the preserved chapter pages and compiled Part II.

## Build

From the repository root, with a LaTeX distribution installed:

```bash
cd manuscript
pdflatex -interaction=nonstopmode -halt-on-error Information_Geometry_v0.2_integrated_part_II.tex
pdflatex -interaction=nonstopmode -halt-on-error Information_Geometry_v0.2_integrated_part_II.tex
cd ..
python manuscript/build_full_edition.py
```

Python dependencies for the assembler: `pypdf`, `reportlab`, and `Pillow`. For example: `python -m pip install pypdf reportlab Pillow`. The generated book is written to `book/Information_Geometry_for_the_Impatient_v0.2_COMPLETE.pdf`.

The script prefers fonts from the original Linux build when available and uses built-in PDF fonts elsewhere; typography can therefore differ slightly across systems. It is **not** a fully source-unified LaTeX book until Chapters 1–5 are recovered or retyped.

**Editorial rule:** commit only the current complete PDF under `book/`. Intermediate outputs must remain here and should not be committed.
