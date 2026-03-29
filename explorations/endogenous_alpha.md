# Endogenous α: Modelling Ideas for Student Exploration

**Date:** 2026-03-29
**Context:** The current model holds α (the probability that a manuscript is genuinely good) fixed as AI adoption *a* rises. The paper frames this as a neutral assumption between an optimistic scenario (AI raises α) and a pessimistic one (AI lowers it). This document explores how α(a) could be made endogenous and what each specification would do to the results.

---

## Current Model Recap

In the baseline model:
- α is fixed at 0.2 (Set A) or 0.2 (Set B)
- α enters the replicator dynamics through the prefactor (1−α) and through the submission volume V(x,a) = N[1−(1−α)x]·(1+γa)
- α enters the quality measure Q(x) = α·π₁ / [α·π₁ + (1−α)(1−x)·π₀]
- **Crucially, α does NOT enter the collapse threshold** a* = (c₀ − rλ₀)/(rμ + c₀φ), which is determined at x=1 where only good papers are submitted

This last point is the key structural fact: α affects the *severity* of collapse (how bad the accepted pool gets) but not the *threshold* at which collapse occurs.

---

## Five Candidate Specifications

### Specification 1: Linear Quality Uplift

**Functional form:** α(a) = α₀(1 + ξa), where ξ ≥ 0 governs the quality-uplift sensitivity.

**Interpretation:** AI helps researchers execute better work at a rate proportional to adoption. This is the simplest possible specification and mirrors the structure of the other four channels (c, λ, V, K_rev are all linear in *a*).

**Mechanism:** Higher α means more of each author's submissions are genuinely good. For selective authors, this raises their submission rate (they submit when q=1, which happens more often). For universal authors, it doesn't change their behaviour (they submit everything regardless). The net effect is to increase V slightly and to improve the composition of the accepted pool.

**Where α enters the model:**
- V(x,a) = N[1−(1−α(a))x]·(1+γa) — volume rises slightly because selective authors have more good papers to submit
- M(x,a) — the peer-accepted pool shifts because the mix of good/bad papers changes
- Q(x,a) — quality improves at every x
- The replicator prefactor (1−α(a)) shrinks, slightly slowing the dynamics
- **a* at x=1:** With η=1 at the honest boundary, Π_bad(1,a) = r·λ(a) − c(a). This does NOT involve α. So a* is unchanged.

**Key prediction:** The collapse threshold is identical to the fixed-α model. The only difference is that the quality of the accepted pool is better at every population state, so the *welfare cost* of collapse is smaller (but collapse still happens at the same a*).

---

### Specification 2: Pool-Composition Effect (Entry of Non-Researchers)

**Functional form:** α(a) = α₀ / (1 + ψa), where ψ ≥ 0 governs the entry-dilution sensitivity.

**Interpretation:** AI lowers the barrier to producing a submission-ready manuscript, attracting individuals who do not have active research programmes. These entrants have no genuine findings to report (their personal α is effectively 0), diluting the average α in the population. This is a population-composition effect, not an individual-quality effect.

**Mechanism:** As *a* rises, the effective α falls because the "author" population now includes non-researchers. This is distinct from the universal-submission strategy: even a universal submitter in the current model has probability α of producing a good paper. Under this specification, new entrants have α ≈ 0, pulling the population average down.

**Where α enters the model:**
- All the same places as Specification 1, but in the opposite direction
- V rises faster (more bad papers in the pool)
- Q falls faster at every x
- **a* at x=1:** Still unchanged (same argument — α drops out at the honest boundary)
- **But:** The corrupt boundary Π_bad(0,a) is affected. Lower α means fewer good papers in the pool, which changes M(0,a) and therefore ρ̄(0,a). The defence-by-congestion mechanism may weaken (because the pool is more dominated by bad papers, rationing is tighter, which could either help or hurt depending on the magnitude).

**Key prediction:** Collapse threshold unchanged, but the *severity* of collapse is worse and the *recovery threshold* may shift. The welfare gap between GH and GC widens.

---

### Specification 3: Heterogeneous α Across Author Types

**Functional form:** Each author *i* has their own α_i drawn from a distribution (e.g., Beta(a_shape, b_shape)). AI adoption shifts the distribution — perhaps by adding mass at the lower end (entry of non-researchers) while also shifting the upper end rightward (existing researchers get better tools).

**Interpretation:** This captures the reality that AI doesn't affect all researchers equally. A senior researcher with a mature programme may see α increase (AI helps with execution); a junior researcher without established methods may see no change; a non-researcher entering the system contributes α ≈ 0.

**Mechanism:** The mean-field dynamics now depend on the *distribution* of α, not just the mean. The replicator equation becomes strategy-dependent: authors with high α_i have less to gain from universal submission (their good papers are already profitable), while authors with low α_i gain more from flooding. This could produce a sorting effect where low-α authors adopt universal submission first.

**Where α enters the model:** Everywhere, but the honest-boundary analysis becomes more complex because the "first deviator" is now the author with the lowest α (who gains most from spamming). The collapse threshold may become α-dependent because it's no longer a representative-agent model.

**Key prediction:** Potentially changes the collapse threshold. The system may tip earlier because the marginal deviator has lower α than the population mean, making deviation more profitable at the margin.

---

### Specification 4: Endogenous α Through Research-Quality Feedback

**Functional form:** α depends on x (the honest-author share) as well as a: α(x, a) = α₀ · g(x) · (1 + ξa), where g(x) is increasing in x (a more honest field produces better science, which raises the probability of genuine findings for everyone).

**Interpretation:** When the field is honest (x ≈ 1), the published literature is reliable, researchers build on solid foundations, and the probability of genuine findings is high. When the field is corrupt (x ≈ 0), the literature is polluted, researchers waste effort on false leads, and α falls. This creates a positive feedback loop: corruption breeds more corruption through the research-quality channel.

**Mechanism:** This is the most structurally interesting specification because it creates an additional self-reinforcing dynamic. In the current model, corruption is self-reinforcing only through the screening channel (more bad papers → more congestion → worse screening → more bad papers). Adding a quality-feedback loop means corruption also degrades the underlying research landscape, making recovery even harder.

**Where α enters the model:** The replicator dynamics now have an additional feedback term. The collapse threshold may shift because α(1,a) ≠ α(0,a), and the honest-boundary condition could become α-dependent if g(1) ≠ 1.

**Key prediction:** Amplifies the asymmetric recovery result. The recovery gap widens because restoring x to 1 requires not just fixing the incentive structure but also waiting for the research base to rebuild. Could turn the current fold bifurcation into a more complex structure.

---

### Specification 5: Task-Dependent α (Decomposed Quality)

**Functional form:** Decompose manuscript quality into components: α = α_idea · α_execution · α_reporting. AI affects each component differently: α_idea is unchanged (nature determines ideas), α_execution(a) = α_exec,0(1 + ξ_exec · a) rises with AI (better tools), α_reporting(a) = α_rep,0(1 + ξ_rep · a) rises with AI (better writing). The overall α(a) = α_idea · α_execution(a) · α_reporting(a).

**Interpretation:** Quality is multi-dimensional. AI raises the execution and reporting components but not the ideation component. This connects directly to the production-verification asymmetry table (Table S6 in the supplement). A manuscript is "genuinely good" only if all three components are adequate.

**Mechanism:** Even if AI raises α_execution and α_reporting substantially, the overall α is bounded by α_idea (the weakest link if ideas are scarce). In fields with abundant research opportunities (high α_idea), AI genuinely raises α. In fields where good ideas are scarce, α barely moves because the binding constraint is ideation, not execution.

**Where α enters the model:** Same as Specification 1, but with field-heterogeneous effects. Fields with high α_idea see α rise; fields with low α_idea see almost no change.

**Key prediction:** Field-heterogeneous outcomes. Some fields benefit from AI (α rises, quality improves), while others see the pure negative effects of the baseline model. The collapse threshold is still α-independent, but the welfare consequences differ across fields.

---

## Comparative Evaluation

| Specification | Analytical tractability | Changes a*? | Changes recovery gap? | Changes welfare? | Empirical testability | Complexity added | Recommendation |
|---|---|---|---|---|---|---|---|
| **1. Linear uplift** α₀(1+ξa) | High — same structure as other channels | **No** — α drops out at x=1 | No — same fold bifurcation structure | Yes — Q improves at every x, partially offsets damage | Low — hard to measure α directly | Minimal — one new parameter ξ | **Good first extension.** Shows robustness of a*. Easy to implement. |
| **2. Pool dilution** α₀/(1+ψa) | High — same structure | **No** — same argument | Possibly — corrupt boundary shifts | Yes — Q worsens, amplifies damage | Medium — could proxy via author demographics | Minimal — one new parameter ψ | **Good complement to Spec 1.** Shows the pessimistic case. |
| **3. Heterogeneous α_i** | Low — requires distributional assumptions, possibly simulation-only | **Possibly** — marginal deviator has lowest α | Possibly — depends on distribution shape | Yes — sorting effects | Low — requires individual-level data | High — distribution parameters, sorting dynamics | **Interesting but hard.** Best explored via ABM. Not analytically tractable. |
| **4. Quality feedback** α(x,a) | Medium — adds a feedback loop to ODE | **Possibly** — if g(1) ≠ g(0) affects the boundary condition | **Yes — amplifies** — corruption degrades the research base, making recovery harder | Yes — strongly | Medium — could test via citation-chain quality | Medium — one new function g(x) | **Most novel contribution.** Amplifies the paper's key message. Worth pursuing if tractable. |
| **5. Task-decomposed** α = α_idea·α_exec·α_rep | Medium — product structure is clean | **No** — same α-independence at x=1 | No — same structure | Yes — field-heterogeneous | High — could compare across fields with different α_idea | Medium — three sub-parameters, field variation | **Good for empirical predictions.** Connects to Table S6. Less novel theoretically. |

---

## GAN-Style Assessment

### Generator: Why pursue endogenous α?

1. **Pre-empts the strongest referee objection.** "You assume AI only makes things worse" is the first thing a non-specialist reviewer will say. Having a formal extension that shows the results are robust (or even strengthened) closes this gap.

2. **Specification 4 (quality feedback) would genuinely strengthen the paper.** The current model has one self-reinforcing loop (screening degradation). Adding a second loop (research-quality degradation) makes the asymmetric recovery result even more dramatic and provides a mechanistic explanation for why collapsed fields are so hard to repair. This is a novel contribution beyond the current paper.

3. **Specification 5 connects to the new Table S6.** The production-verification asymmetry table already decomposes research into stages. A task-decomposed α would formally embed that table into the model, strengthening internal coherence.

4. **Specifications 1 and 2 together provide a clean sensitivity analysis.** Running both as a bracket (optimistic vs pessimistic) and showing a* is unchanged in both cases is a powerful robustness argument that could go in the supplement as a new appendix.

### Discriminator: Why NOT pursue endogenous α?

1. **The main result is already α-independent.** The collapse threshold a* doesn't involve α. Adding endogenous α confirms this but doesn't change the core finding. The marginal contribution may be small.

2. **Specifications 3 and 4 break analytical tractability.** The paper's strength is its closed-form results. Moving to simulation-only extensions weakens the theoretical contribution and may not fit the PNAS format.

3. **More parameters without more data.** ξ, ψ, g(x) are all free parameters with no empirical calibration. Adding them without grounding them in data opens the model to the critique that it can be tuned to produce any result.

4. **Scope creep risk.** The paper already has a clear message. Adding a fifth channel (α) with multiple sub-specifications could dilute the narrative. The Discussion already handles the fixed-α assumption with the two-sided framing; a full extension may be better suited to a follow-up paper.

### Resolution: Recommended Path

**For the current paper (supplement extension):**
- Implement **Specifications 1 + 2** as a paired sensitivity analysis in a new appendix (e.g., Appendix H). Show that a* is unchanged under both α₀(1+ξa) and α₀/(1+ψa). Plot Q(x,a) under the three scenarios (fixed, optimistic, pessimistic) to show the welfare effects. This takes ~2 pages and one figure. It directly pre-empts the referee critique.

**For a follow-up paper or deeper exploration:**
- Explore **Specification 4** (quality feedback) as a standalone contribution. The idea that corruption degrades the research base, which further degrades quality, which further incentivises corruption, is a genuinely new feedback loop that current models of academic publishing do not capture. This could be a self-contained theory paper.
- Explore **Specification 3** (heterogeneous α) via ABM. This connects to the empirical literature on AI adoption heterogeneity (early adopters vs late adopters) and could generate testable predictions about which sub-populations drive the collapse.

---

## Implementation Notes for Student

### Specification 1 (Linear Uplift) — Easiest Starting Point

```python
# In the existing model code, replace fixed alpha with:
def alpha_endogenous(a, alpha0=0.2, xi=0.1):
    return alpha0 * (1 + xi * a)

# Then re-run:
# 1. The a* calculation — verify it's unchanged
# 2. The regime map (fig3) — compare fixed vs endogenous alpha
# 3. The quality Q(x) under GC — show the partial offset
# 4. The welfare analysis — quantify the offset
```

### Specification 2 (Pool Dilution) — Same Difficulty

```python
def alpha_diluted(a, alpha0=0.2, psi=0.3):
    return alpha0 / (1 + psi * a)

# Same re-runs as above, but Q worsens instead of improving
```

### Specification 4 (Quality Feedback) — Harder

```python
def alpha_feedback(x, a, alpha0=0.2, xi=0.1, g_slope=0.5):
    # g(x) = 1 - g_slope*(1-x): quality degrades as x falls
    g = 1 - g_slope * (1 - x)
    return alpha0 * g * (1 + xi * a)

# This changes the ODE because alpha now depends on x
# The replicator equation must be re-derived with d(alpha)/dx terms
# Best explored numerically first, then check if closed-form results survive
```

### Key Quantities to Report

For each specification, compute and compare:
1. **a\* (collapse threshold)** — does it change? By how much?
2. **Recovery gap** Δa = a_col − a_rec — does it widen or narrow?
3. **Quality at GC** Q(0, a) — how much worse/better is the accepted pool?
4. **Regime map** in (K_rev, K) space — do the boundaries shift?
5. **Welfare** W(x, a) — does the normative ranking of levers change?
