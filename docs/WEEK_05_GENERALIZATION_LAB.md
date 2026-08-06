# Week 5 paper anchor: hypothesis choice and generalization

> A bounded critical-reading and experiment brief. The generated Week 5 journal
> is the execution surface; this document preserves the rationale and lab.

Before the curriculum introduces formal model training, Week 5 uses Michael
Timothy Bennett's [*The Optimal Choice of Hypothesis Is the Weakest, Not the
Shortest*](https://arxiv.org/abs/2301.12987v4) as a critical reading on
induction, generalization, and inductive bias.

The paper argues—under its finite-language and uniformly distributed task
assumptions—that maximizing a hypothesis's **weakness** (the size of the set of
possibilities it leaves open) can generalize better than minimizing description
length. Learners should treat this as a claim to examine, not a replacement for
MDL, regularization, or task-specific priors.

The bounded Week 5 paper lab is:

- define the paper's terms: task, model, extension, weakness, and description length;
- reproduce or critique the binary-arithmetic toy comparison on a small finite dataset;
- report generalization rate, extent of generalization, and the assumptions that make the comparison meaningful; and
- connect the result to later leakage checks, calibration, slice-based retrieval evaluation, and LLM behavior under distribution shift.

The evidence is one technical explanation plus a small reproducible experiment
or a falsifiable critique. It does not add another phase or change the 100-math-
module count; it gives the early diagnostic a stronger theory-of-generalization
anchor.

## Canonical resource entry

[The paper on arXiv](https://arxiv.org/abs/2301.12987v4) ·
[Resource catalog](https://sethuiyer.github.io/tensor-to-tenant/resources/)
