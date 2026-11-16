# IG-Lab: Information Geometry for the Impatient

**Mirco A. Mannucci · HoloMathics, LLC · working research edition 0.2 (November 2026)**

A small executable laboratory accompanying *Information Geometry: When Probability Becomes Geometry*, in the **Higher Math for the Impatient** series. The central purpose is not to illustrate already-made claims but to make the mathematical assertions independently checkable.

## Get the book

- [`book/Information_Geometry_for_the_Impatient_v0.2_RESEARCH.pdf`](book/Information_Geometry_for_the_Impatient_v0.2_RESEARCH.pdf): **42-page research compilation**, preserving the original 27-page edition 0.1 and appending a 14-page mathematical extension, preceded by an editorial cover.
- [`book/Information_Geometry_v0.2_mathematical_extension.tex`](book/Information_Geometry_v0.2_mathematical_extension.tex): **editable LaTeX source of all new material**.
- [`book/Information_Geometry_v0.1_original.pdf`](book/Information_Geometry_v0.1_original.pdf): the recovered original. Its editable source was not available, so this is **not yet a single-source typeset v0.2**; the edition-0.1 pages are included as a PDF facsimile and remain unchanged.

### Mathematical core: what is proved rather than asserted

1. **Finite-simplex Čencov uniqueness:** compatible metrics across positive finite simplexes invariant under stochastic embeddings admitting recovery are exactly scalar multiples of Fisher. The proof uses permutation symmetry at uniform measures, common uniform refinements, rational distributions and continuity. **Ordinary reparametrization invariance is not enough.**
2. **Fisher monotonicity under any finite stochastic channel:** prove the metric contraction inequality by conditional expectation of scores, including the equality criterion.
3. **Divergences as generators:** second derivatives give a metric, third derivatives two dual connections; derive Bregman–KL orientation for minimal exponential families and distinguish mixture and exponential flatness from Levi–Civita curvature.
4. **Projection with actual hypotheses:** exact Bregman three-point identity; KL projection Pythagorean **inequality** generally, equality for appropriate affine/interior projections.
5. **Natural gradients as geometric dynamics:** KL trust-region local derivation, Bernoulli logit/probability coordinate invariance, categorical replicator dynamics and Gaussian examples. Fisher and Wasserstein are not interchangeable.

Mathematical scope and boundary conditions are recorded explicitly in the extension's **rigour ledger**. This is a rigorous finite classical treatment, not a proof for quantum, infinite-dimensional, singular, or all transport settings.

## Run the code

Python 3.10+; NumPy, SciPy and SymPy. Matplotlib is needed only for figures.

```bash
python -m venv .venv
# On Windows PowerShell: .\.venv\Scripts\Activate.ps1
# On macOS/Linux: source .venv/bin/activate
python -m pip install -e '.[test,visual]'
python -m pytest -q
python examples/quickstart.py
python examples/make_figures.py
```

Or, from an already provisioned Python environment, `PYTHONPATH=src python -m pytest -q` works without installation on macOS/Linux; on PowerShell: `$env:PYTHONPATH="src"; python -m pytest -q`.

### Code map

| Source | Mathematical object | Independent tests |
|---|---|---|
| `categorical.py` | Fisher simplex geometry, geodesics, KL, stochastic channels, congruent refinements, contraction | `test_categorical.py` |
| `gaussian.py` | Gaussian Fisher metric/distance, e/m/Fisher curves | `test_gaussian.py` |
| `duality.py` | Bregman identity, negative entropy and exact KL projection | `test_duality.py` |
| `learning.py` | Bernoulli natural gradients and replicator equation | `test_learning_symbolic.py` |
| `symbolic.py` | SymPy checks of two Fisher metrics | `test_learning_symbolic.py` |

There are four small runnable notebooks in `notebooks/`, three reproducible figures in `figures/`, and a CI workflow in `.github/workflows/tests.yml`.

**Do not confuse tests with proofs.** Finite numeric examples check implementation, while the written theorem quantifies over all eligible finite dimensions, all interior positive distributions, and all eligible channels.

## Rebuild the PDF

From the repository root (requires a standard LaTeX installation with `pdflatex` and Python `pypdf`):

```bash
cd book
pdflatex -interaction=nonstopmode -halt-on-error research_compilation_cover.tex
pdflatex -interaction=nonstopmode -halt-on-error Information_Geometry_v0.2_mathematical_extension.tex
pdflatex -interaction=nonstopmode -halt-on-error Information_Geometry_v0.2_mathematical_extension.tex
cd ..
python book/build_compilation.py
```

The original v0.1 text is preserved as a PDF, and `build_compilation.py` combines cover + original + new extension with PDF outline bookmarks. Note: LaTeX files use `../figures/` relative to the `book/` directory.

## Publish to GitHub

Create an empty GitHub repository named **IG-Lab** under `Mircus`, then extract this package (do **not** upload the `.zip` as a single GitHub file). In the extracted `IG-Lab` folder, use:

```powershell
.\publish_to_github.ps1
```

The script checks `origin`, initializes Git if needed, adds/commits, and pushes `main` without force. It will not overwrite a remote pointing elsewhere. Alternatively, ordinary `git init`, `git add`, `git commit`, and `git push` commands work.

## Editorial next steps

1. Recover the original v0.1 editable LaTeX, or re-typeset the first four chapters to make **one coherent source edition**.
2. Expand exercises and examples specifically around the Chentsov proof and statistical sufficient transformations.
3. Add machine-checkable symbolic Christoffel/curvature calculations for additional models; distinguish exact geometry from numeric approximation.
4. Once fully integrated, trim/expand to the desired concise series format (~40 pages), and run mathematical and editorial review before labeling it final.

**Repository status:** local reproducible research release prepared. Not represented as pushed or publicly available.
