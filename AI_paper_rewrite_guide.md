# Guide for rewriting the paper with an AI-asymmetry extension

**Goal:** Rework the existing congestion/tipping-point model of publishing into a new paper where **AI is an asymmetric shock**: it increases *production/submission pressure* faster than it increases *verification/review capacity* (and may also raise “polished-but-wrong” false positives). The punchline is that **AI requires different publication institutions**—focused on verification and incentive design, not simply “more slots.”

---

## 0) What you should deliver (concrete outputs)

### Primary deliverables
1. **Rewritten paper draft** (LaTeX/Word—whatever the team uses) with the new AI framing and extension.
2. **Figures (vector preferred)**: mechanism diagram, phase diagrams (baseline vs AI), hysteresis visualization, interventions overlay.
3. **Appendix**: derivations and any simulation/ABM details.

### Intermediate deliverables (for quick feedback)
- **1-page “model + AI extension” box** (equations + plain-language interpretation).
- **1-page “institution menu” box** (table mapping interventions → model parameters).
- **Rewritten Introduction** (1.5–2 pages) that sells the new paper to a broad audience.

---

## 1) The core story (keep this straight)

### One-sentence mechanism
> AI makes it cheaper and faster to generate and submit papers than it is to verify them, so review becomes congested, screening degrades, and “always submit” becomes a profitable strategy—creating tipping points and hysteresis.

### The three “sellable” one-liners (must appear in intro + discussion)
- **Why slot expansion can backfire:** More slots raise the expected payoff of submitting marginal/low-quality papers unless verification scales too.
- **Why elite journals can be stable due to scarcity:** When acceptance is extremely rare, spamming isn’t worth the cost; scarcity acts as a deterrent.
- **Why recovery is hard:** After tipping, the low-quality state sustains itself (hysteresis), so small reforms won’t restore quality; you need a big push to cross a recovery threshold.

---

## 2) Map AI channels to model parameters (your “translation layer”)

You are extending an existing model with:
- Submission volume: **V**
- Review capacity: **K_rev**
- Slot capacity: **K** (or K_store)
- False positive/negative rates: **λ, ε**
- Publication reward: **r**
- Submission cost: **c**
- “Spam profitability”: **Π_bad = r · ρ̄ · π0 − c**
- Dynamics over honesty/self-restraint share: **x**

### AI adoption parameter
Introduce **a ∈ [0,1]** = AI adoption intensity (or share of AI-enabled authors).

Then specify the asymmetry using simple “elasticity” forms:
- **Production / submission shock:**  
  V(x, a) = V(x) · (1 + γ a)
- **Verification scaling (slower):**  
  K_rev(a) = K_rev(0) · (1 + δ a), with **δ < γ**
- **Lower friction:**  
  c(a) decreasing in a (AI reduces drafting + resubmission effort)
- **Screening vulnerability:**  
  λ(a) increasing in a (polished-but-wrong manuscripts more likely to pass unless countered)

> You do *not* need perfect empirical calibration—this can be presented as a stylized, testable assumption.

---

## 3) Paper structure (section-by-section plan)

Below, each bullet is roughly **one paragraph**.

### Abstract (1 paragraph)
- Frame AI as a productivity shock that increases submission pressure and may degrade screening; show this creates tipping points/hysteresis and motivates verification-centric institutions.

### 1. Introduction (5–7 paragraphs)
- Hook: “AI can write papers faster than we can verify them.”
- Explain why this is a **system-level** problem, not just individual ethics.
- Two bottlenecks: verification (review) and allocation (slots).
- Contribution: extend congestion model with AI adoption parameter shifting productivity/cost/screening asymmetrically.
- Headline results: tipping points; slot expansion paradox; scarcity stability; hysteresis.
- Policy punchline: AI requires **new institutions** (verification packages, audits, submission tokens).
- Roadmap.

**Figure:** *Fig 1 (end of intro)* Mechanism diagram (AI → V up, c down, λ up, K_rev slow) → Π_bad up → tipping.

### 2. Stylized facts / motivation: “AI is an asymmetric shock” (3–5 paragraphs)
- Why AI scales production: low marginal cost drafting, iterative editing, templates, translation.
- Why verification scales poorly: deep reading, data/code checks, expertise constraints.
- Review-side AI constraints: confidentiality + policy + quality concerns (so K_rev doesn’t rise as fast).
- State the asymmetry hypothesis clearly: **production elasticity > verification elasticity**.
- Translate to model dials you will turn: α up, c down, λ up, K_rev slow.

**Table:** *Table 1 (end of section)* AI channel → model parameter mapping.

### 3. Related literature (4–6 paragraphs)
- Congestion/public goods in peer review.
- Strategic submission and evolutionary dynamics.
- Publication inflation and quality dilution.
- AI in science: productivity + evaluation constraints.
- Institutional design for scientific verification.
- Gap: no unified model connecting AI shocks to tipping + institutional design.

### 4. Baseline model recap (4–6 paragraphs)
- Players/strategies (selective vs always submit).
- Two bottlenecks: η = min(1, K_rev / V) and ρ̄ = min(1, K / M).
- Screening errors: π0, π1 via λ, ε; congestion weakens screening.
- Payoff for marginal bad submission Π_bad = r ρ̄ π0 − c.
- Replicator dynamics and equilibrium regimes.
- Intuition: screening collapse vs rationing deterrence.

**Figure:** *Fig 2* Baseline phase portrait (show bistability threshold).

### 5. AI extension (6–9 paragraphs) — *main new model*
- Define AI adoption a and explain interpretation.
- Production channel: V increases with a (γ).
- Friction channel: c decreases with a.
- Vulnerability channel: λ increases with a unless mitigated.
- Review-assistance channel: K_rev increases with a but slower (δ < γ).
- Combine into Π_bad(x, a) and show why it rises with a.
- Interpret: AI is not “one thing”; separate creation vs verification.
- Special cases: if δ ≈ γ and λ falls, stability can be preserved.
- Preview testable predictions.

**Figure:** *Fig 3* “Parameter-shift diagram” (arrows from a to α, c, λ, K_rev).  
**Table:** *Table 2* Scenario matrix: (δ/γ high vs low) × (λ rising vs stable/falling).

### 6. Analysis: equilibria, tipping, hysteresis under AI (6–10 paragraphs)
- Equilibrium condition Π_bad = 0 and boundary stability.
- Comparative statics: increasing a shifts Π_bad upward; bistability region expands.
- Slot expansion revisited: increasing K alone raises ρ̄ → boosts spam incentive, especially when λ rises and c falls.
- Scarcity stability: defense by congestion; show how cheap submission (low c) erodes this protection.
- Hysteresis: collapse vs recovery thresholds diverge more as a rises.
- λ is the critical destabilizer: motivates verification institutions.
- Policy levers move phase boundaries: raise K_rev, reduce λ, add friction (raise c), reshape rewards r.
- Early warning signals + summary propositions (proofs to appendix).

**Figures:**  
- *Fig 4* Baseline vs high-a phase diagram (K_rev vs K).  
- *Fig 5* Stable equilibrium x*(a).  
- *Fig 6* Hysteresis loop widening with a (collapse vs recovery thresholds).

### 7. Simulations / ABM (optional but strong) (5–8 paragraphs)
- Why ABM: heterogeneity + diffusion of AI adoption.
- Agents: strategies + AI-enabled status.
- Adoption dynamics: exogenous trend or payoff-driven imitation.
- Review/slots implemented with K_rev(a), λ(a), K.
- Results: tipping as a rises; path dependence.
- Robustness: vary δ/γ, slope of λ(a), c(a).
- Optional: field subcommunities; stochastic near-threshold flips.

**Figures:**  
- *Fig 7* Time series of x_t and a_t (tipping).  
- *Fig 8* Heatmap outcomes over (δ/γ, dλ/da).

### 8. Institutional design for the AI era (6–9 paragraphs) — *the punchline*
- Goal: keep the system in the “honesty basin” by stabilizing Π_bad.
- Principle 1: scale verification (raise effective K_rev) without raising λ.
- Principle 2: reduce false positives (lower λ) via audits, code/data requirements, structured checks.
- Principle 3: add smart friction (raise effective c for low-effort submissions): tokens/quotas, triage, escalating resubmission costs.
- Principle 4: decouple dissemination from certification: preprints + certification layers.
- Mapping: each institution corresponds to parameter shifts.
- Transition policy: hysteresis implies “reset” interventions may be needed after collapse.
- Equity: friction can hurt under-resourced authors; propose waivers/tokens grants.
- Summarize a policy menu: quick wins vs deep redesign.

**Table:** *Table 3* Institution → parameter mapping (K_rev, λ, c, r, K).  
**Figure:** *Fig 9* Interventions overlay arrows on phase diagram.

### 9. Empirical predictions & measurement (4–7 paragraphs)
- Nonlinear degradation as a rises (quiet then cliff).
- Wider hysteresis with AI.
- Proxies for λ rising: polish/format improvements without robustness.
- Proxies for K_rev stress: reviewer decline rates, desk rejects, turnaround time.
- Data sources and identification ideas.
- What would falsify asymmetry: review automation scales as fast as submissions *and* lowers λ.

### 10. Discussion / limitations / extensions (4–6 paragraphs)
- Simplified strategies and single-field; AI as scalar.
- Not “AI bad,” but “institutions must match scaling laws.”
- Extensions: multi-journal competition; endogenous rewards; reviewer incentives; reputation systems.

### 11. Conclusion (2–3 paragraphs)
- Restate asymmetry and tipping-point risk.
- Emphasize institutional redesign toward verification.

---

## 4) Writing guidelines (to improve readability)

### Style rules
- Use short sentences; define every symbol once; minimize acronyms.
- Replace dynamical-systems jargon with plain language:
  - “attractor” → “long-run outcome”
  - “basin of attraction” → “region where the system moves toward…”
  - “repeller” → “unstable tipping threshold”
- Avoid slogan repetition; define terms once then use plain phrasing.

### “Show, don’t tell”
- Introduce each technical step with a 1–2 sentence intuition.
- Every result should connect to an institutional lever.

### Use boxes
- **Box 1:** “Model in one page” (equations + interpretation).
- **Box 2:** “What AI changes” (parameter mapping + asymmetry assumption).
- **Box 3:** “Policy menu” (institution mapping table).

---

## 5) A practical task plan (what to do next)

### Day 1–2: Extract and compress baseline model
- Create a 1-page baseline summary:
  - list parameters, key equations, regime definitions, and 2–3 headline findings.
- Identify which baseline figures you can reuse (phase diagram, hysteresis).

### Day 3–4: Write the AI extension cleanly
- Define a and the functional forms (γ, δ, λ(a), c(a)).
- Write 2–3 propositions/claims (even informal) about how equilibria shift with a.
- Draft Fig 1 (mechanism diagram) and Fig 3 (AI parameter arrows).

### Day 5–7: Draft new Introduction + Institutional Design section
- Intro must lead with AI asymmetry + tipping points.
- Institutional section must map each proposal to parameter shifts.

### Day 8+: Add analysis/simulations and polish
- Produce baseline vs AI phase diagrams.
- Add hysteresis figure showing widening under AI.
- Tighten text; add boxes; reduce jargon.

---

## 6) Checklist before sending a draft to the PI

- [ ] Intro contains the three one-liner “whys” (slots, scarcity stability, hysteresis).
- [ ] AI adoption parameter a is defined and tied to **at least** V and K_rev with **δ < γ**.
- [ ] You explain *why* K_rev doesn’t scale symmetrically (institutional/policy constraints + human expertise).
- [ ] At least one figure shows baseline vs AI-shifted regime boundaries.
- [ ] Policy section maps institutions → (K_rev ↑, λ ↓, c ↑, r reshaped, K adjusted).
- [ ] Text is readable: jargon minimized, symbols introduced once, strong intuitions.

---

## 7) Notes on “how to phrase the pitch” (useful sentences)

- “AI is a productivity shock that scales text generation faster than verification.”
- “Peer review is a scarce attention resource; congestion changes incentives.”
- “If publishing capacity expands without verification scaling, the expected payoff of spamming rises.”
- “Scarcity can deter spamming, but AI can erode that deterrence by collapsing the cost of submission.”
- “After a collapse, recovery is hard because the low-quality equilibrium is self-sustaining.”

---

## 8) File organization (suggested)

- `/drafts/` paper versions
- `/figures/` SVG/PDF sources + exports
- `/notes/` baseline extraction, parameter mapping, proposition sketches
- `/code/` if you simulate or generate figures

---

### Quick questions for the team (ask early, don’t block writing)
- Are we targeting a theory journal, science policy audience, or general interest?
- Do we want ABM simulations in the main text or appendix?
- Which empirical “stylized facts” are safe to cite vs keep as conjecture?

---

**If you get stuck:** write the **Intro + Box 1 + Institutional table** first. Those three pieces will clarify the rest.
