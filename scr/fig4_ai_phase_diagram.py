"""
Figure 4: Baseline vs High-AI Adoption Phase Diagram (K_rev vs K)

Shows how AI adoption (a) shifts regime boundaries in the (K_rev, K) parameter
space.  Left panel: baseline (a=0).  Right panel: high AI adoption (a=0.8).
The comparison makes visible that the GH (green) region shrinks and the
BS/GC (yellow/red) region expands as AI lowers submission cost, raises
submission volume, and degrades screening accuracy faster than it raises
review capacity.

Output: saves fig4_ai_phase_diagram.pdf to the same directory as this script's
        parent (doc/tex/).
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

# ─────────────────────────────────────────────────────────────────────────────
# 1.  Model core
# ─────────────────────────────────────────────────────────────────────────────
def soft_min(a, b, k=15):
    """Smooth, differentiable approximation of min(a, b)."""
    return -np.log(np.exp(-k * a) + np.exp(-k * b)) / k


def classify_regime_grid(K_rev_vals, K_store_vals, base_params, ai_level=0.0,
                          gamma=0.5, delta=0.1, phi=0.4, mu=0.2):
    """
    Vectorised regime classification over a 2-D grid of (K_rev, K_store).

    AI channels (all as functions of a = ai_level):
        V(x,a)      = N[1-(1-alpha)x] * (1 + gamma*a)   production elasticity
        K_rev(a)    = K_rev * (1 + delta*a)             verification elasticity
        c(a)        = c_0 * (1 - phi*a)                 lower friction
        lambda(a)   = lambda_0 + mu*a                   weaker screening

    Regime codes: 0=GH(green), 1=GC(red), 2=BS(yellow), 3=SC(blue), 4=NS(gray)
    """
    p   = base_params
    k   = p.get('smoothness', 15)
    a   = ai_level

    # ── AI-adjusted scalar parameters ─────────────────────────────────────────
    c_eff   = p['c']   * (1.0 - phi * a)
    lam_eff = min(p['lam'] + mu * a, 0.99)

    # Volume multiplier (applies symmetrically to good and bad submissions)
    vol_mult  = 1.0 + gamma * a   # >1 → more submissions
    krev_mult = 1.0 + delta * a   # >1 but < vol_mult → lagging review

    # ── Build 2-D arrays: rows = K_store axis, cols = K_rev axis ──────────────
    KR = K_rev_vals[np.newaxis, :]    # shape (1, J)
    KS = K_store_vals[:, np.newaxis]  # shape (I, 1)

    def boundary_states(x_val):
        """Return Pi_bad and Pi_good at a single boundary value of x."""
        V_raw    = p['N'] * (1.0 - (1.0 - p['alpha']) * x_val)
        V_eff    = V_raw  * vol_mult          # effective submission volume
        K_r_eff  = KR     * krev_mult         # effective review capacity  (1, J)

        # Screening intensity η = min(1, K_rev_eff / V_eff)  →  shape (1, J)
        ratio_eta = K_r_eff / V_eff
        eta = np.clip(soft_min(1.0, ratio_eta, k), 0.0, 1.0)

        pi_0 = 1.0 - eta * (1.0 - lam_eff)   # bad-paper pass rate
        pi_1 = 1.0 - eta * p['epsilon']       # good-paper pass rate

        # Peer-accepted pool M (with AI-driven volume)
        V_G  = p['N'] * p['alpha']                             * vol_mult
        V_B  = p['N'] * (1.0 - p['alpha']) * (1.0 - x_val)   * vol_mult
        M    = V_G * pi_1 + V_B * pi_0         # shape (1, J)

        # Rationing probability ρ̄ = min(1, K / M)  →  broadcast to (I, J)
        ratio_rho = KS / M
        rho_bar   = np.clip(soft_min(1.0, ratio_rho, k), 0.0, 1.0)

        Pi_bad  = p['r'] * rho_bar * pi_0 - c_eff   # shape (I, J)
        Pi_good = p['r'] * rho_bar * pi_1 - c_eff
        return Pi_bad, Pi_good

    Pi_bad_1, Pi_good_1 = boundary_states(0.999)
    Pi_bad_0, _         = boundary_states(0.001)

    # ── Classification ─────────────────────────────────────────────────────────
    ns         = Pi_good_1 < 0              # No Submission (Gray)
    one_stable = Pi_bad_1  < 0             # x=1 is stable
    zero_stable= Pi_bad_0  > 0             # x=0 is stable
    not_ns     = ~ns

    grid = np.full(Pi_bad_1.shape, -1, dtype=np.int8)
    grid[ns] = 4
    grid[not_ns &  one_stable &  zero_stable] = 2   # Bistability
    grid[not_ns &  one_stable & ~zero_stable] = 0   # Global Honesty
    grid[not_ns & ~one_stable &  zero_stable] = 1   # Global Corruption
    grid[not_ns & ~one_stable & ~zero_stable] = 3   # Stable Coexistence
    return grid


# ─────────────────────────────────────────────────────────────────────────────
# 2.  Parameter setup
# ─────────────────────────────────────────────────────────────────────────────
BASE = {
    'N': 1000, 'alpha': 0.2,
    'r': 100,  'c': 25,
    'lam': 0.1, 'epsilon': 0.05,
    'smoothness': 15,
}

# AI elasticity parameters (constant across both panels)
GAMMA = 0.5   # production elasticity  (γ)
DELTA = 0.1   # verification elasticity (δ < γ)
PHI   = 0.4   # submission-cost slope   (φ)
MU    = 0.2   # false-positive slope    (μ)

# Grid resolution and axis ranges
RES         = 180
K_rev_vals   = np.linspace(10, 600, RES)
K_store_vals = np.linspace(10, 700, RES)

# ─────────────────────────────────────────────────────────────────────────────
# 3.  Compute regime maps
# ─────────────────────────────────────────────────────────────────────────────
print("Computing baseline phase map  (a = 0.0) …")
map_base = classify_regime_grid(K_rev_vals, K_store_vals, BASE,
                                 ai_level=0.0,
                                 gamma=GAMMA, delta=DELTA, phi=PHI, mu=MU)

print("Computing high-AI phase map   (a = 0.8) …")
map_ai   = classify_regime_grid(K_rev_vals, K_store_vals, BASE,
                                 ai_level=0.8,
                                 gamma=GAMMA, delta=DELTA, phi=PHI, mu=MU)
print("Done.")

# ─────────────────────────────────────────────────────────────────────────────
# 4.  Plot
# ─────────────────────────────────────────────────────────────────────────────
COLORS = ['#98FB98', '#FFB6C1', '#FFE4B5', '#ADD8E6', '#D3D3D3']
CMAP   = ListedColormap(COLORS)
EXTENT = [K_rev_vals.min(), K_rev_vals.max(),
          K_store_vals.min(), K_store_vals.max()]

fig = plt.figure(figsize=(14, 5.8))
gs  = gridspec.GridSpec(1, 2, figure=fig, wspace=0.10)

PANEL_SPECS = [
    (map_base, r'(a)  Baseline  ($a = 0$)',
     r'$N=1000,\ \alpha=0.2,\ r=100,\ c=25,\ \lambda=0.10,\ \varepsilon=0.05$'),
    (map_ai,   r'(b)  High AI adoption  ($a = 0.8$)',
     (r'$c\!\downarrow\!{=}25{\times}0.68,\;'
      r'\lambda\!\uparrow\!{=}0.10{+}0.16,\;'
      r'V\!\uparrow\!{\times}1.40,\;'
      r'K_{rev}\!\uparrow\!{\times}1.08$'
      r'$\quad(\gamma{=}0.5>\delta{=}0.1)$')),
]

axes = []
for col, (grid, title, subtitle) in enumerate(PANEL_SPECS):
    ax = fig.add_subplot(gs[0, col])
    ax.imshow(grid, origin='lower', extent=EXTENT,
              aspect='auto', cmap=CMAP, vmin=0, vmax=4)

    ax.set_xlabel(r'Review capacity  $K_{rev}$', fontsize=12)
    if col == 0:
        ax.set_ylabel(r'Slot capacity  $K$', fontsize=12)
    else:
        ax.set_yticklabels([])

    ax.set_title(title, fontsize=13, pad=8, fontweight='bold')

    # Parameter annotation box
    ax.text(0.02, 0.98, subtitle,
            transform=ax.transAxes, fontsize=8.5,
            verticalalignment='top',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='white',
                      edgecolor='gray', alpha=0.88))

    # Mark the Set-A calibration point
    ax.plot(300, 400, marker='*', markersize=11,
            color='black', zorder=10,
            label='Set A calibration' if col == 0 else '')
    if col == 0:
        ax.annotate('Set A', xy=(300, 400), xytext=(340, 490),
                    fontsize=9, color='black',
                    arrowprops=dict(arrowstyle='->', color='black', lw=1.2))
    axes.append(ax)

# ── Directional arrows between panels ────────────────────────────────────────
# Use figure-level annotation to draw a broad arrow between the two subplots
fig.text(0.508, 0.52, r'$a\!\uparrow$', ha='center', va='center',
         fontsize=15, color='#8B0000', fontweight='bold')
fig.text(0.508, 0.44, r'AI adoption', ha='center', va='center',
         fontsize=8.5, color='#8B0000')
ax_arrow = fig.add_axes([0.498, 0.47, 0.020, 0.06])
ax_arrow.annotate('', xy=(0.5, 0.0), xytext=(0.5, 1.0),
                  xycoords='axes fraction', textcoords='axes fraction',
                  arrowprops=dict(arrowstyle='->', color='#8B0000', lw=2.0))
ax_arrow.axis('off')

# ── Shared legend ─────────────────────────────────────────────────────────────
legend_handles = [
    Patch(facecolor='#98FB98', edgecolor='#555', label='Global Honesty (GH)  —  x→1 from anywhere'),
    Patch(facecolor='#FFE4B5', edgecolor='#555', label='Bistability (BS)       —  history-dependent'),
    Patch(facecolor='#ADD8E6', edgecolor='#555', label='Stable Coexistence (SC) — interior equilibrium'),
    Patch(facecolor='#FFB6C1', edgecolor='#555', label='Global Corruption (GC) —  x→0 from anywhere'),
    Patch(facecolor='#D3D3D3', edgecolor='#555', label='No Submission (NS)      —  participation fails'),
]
fig.legend(handles=legend_handles, loc='lower center',
           ncol=3, framealpha=0.95,
           bbox_to_anchor=(0.5, -0.10),
           prop={'size': 11, 'weight': 'bold'},
           title=(r'Regime legend  |  AI parameters: $\gamma=0.5,\ \delta=0.1,\ \phi=0.4,\ \mu=0.2$'),
           title_fontsize=10)

fig.suptitle(
    'Fig. 4  ·  AI adoption shifts regime boundaries in the '
    r'$(K_{rev},\, K)$ parameter space',
    fontsize=13, fontweight='bold', y=1.01
)

# ─────────────────────────────────────────────────────────────────────────────
# 5.  Save
# ─────────────────────────────────────────────────────────────────────────────
# Resolve output path relative to this script's location
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR  = os.path.join(SCRIPT_DIR, '..', 'doc', 'tex')
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'fig4_ai_phase_diagram.pdf')

plt.savefig(OUTPUT_PATH, dpi=300, bbox_inches='tight')
print(f"Saved → {os.path.normpath(OUTPUT_PATH)}")
plt.show()