# Contributing to IG-Lab

IG-Lab serves two overlapping communities: readers exploring information geometry and collaborators checking and extending the mathematics. Contributions are welcome when they make the book **more intelligible, more rigorous, or more reproducible**.

## What makes a useful contribution?

- **Mathematics:** a corrected proof, a missing assumption, a precise counterexample, or a new worked derivation. Please cite the theorem/section and distinguish a claim valid for finite positive simplexes from one about general statistical manifolds.
- **Exposition:** an example that clarifies why Fisher, KL, mixture/exponential connections, and Levi–Civita geodesics are different objects; terminology or notation fixes that prevent confusion.
- **Experiments:** a short, reproducible script or notebook illustrating a specific statement. State whether it is a symbolic identity, an exact calculation, or a numerical approximation.
- **Tests:** add boundary-sensitive and coordinate-invariance checks, not merely golden-number assertions.

## Workflow

1. Open an issue describing the gap or proposed improvement, especially for significant new mathematics.
2. Fork or create a branch; make a focused change.
3. For Python contributions, use `python -m pip install -e ".[test,visual]"` and run `python -m pytest`.
4. In a pull request, include **claim, assumptions, evidence, tests**, and impact on the book or notebooks. Link the corresponding issue when possible.
5. Do not place draft artifacts in `book/`. That folder contains **only the current complete PDF**. Editorial sources and inputs belong in `manuscript/`; historical notes belong in `docs/` or Git history.

## Mathematical standards

State precise dimensions and positivity assumptions, distinguish stochastic embeddings with recovery from arbitrary stochastic channels, and identify the direction of every KL divergence. Equality conditions matter—especially for contraction and projection statements. Where a result requires affine constraints, strict positivity, smoothness, or an interior minimizer, say so explicitly.

Please do not represent numerical evidence as a proof, or extrapolate a finite classical result to singular, quantum, or infinite-dimensional models without a separate argument.

## Editorial status and licensing

The v0.2 book is a working research edition; its early typesetting source has not been fully recovered. Please coordinate structural manuscript changes rather than editing the output PDF directly.

No LICENSE file has yet been selected. Until one is added by the maintainer, do not assume that source code or manuscript text is licensed for unrestricted redistribution or modification. Proposed external contributions should be discussed with the maintainer on an issue.
