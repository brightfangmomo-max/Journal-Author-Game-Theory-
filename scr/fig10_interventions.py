"""
Figure 10: Intervention Levers — Phase Maps Showing How Policy Restores GH
===========================================================================

Left panel:  a=0.8 with BASE parameters.  Set A (K_rev=300, K=400) is deep in GC.
             A navy arrow shows K_rev↑ alone stays in GC.

Right panel: a=0.8 with intervention parameters (lambda=0.05, c=35, phi=0, mu=0).
             GC is eliminated everywhere.  Set A is in BS.  Combined K_rev↑ arrow
             pushes Set A into GH.

Output: saves fig10_interventions.pdf to doc/tex/ (relative to this script).
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch, FancyArrowPatch


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
    p = base_params
    k = p.get('smoothness', 15)
    a = ai_level

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

        # Screening intensity eta = min(1, K_rev_eff / V_eff)  →  shape (1, J)
        ratio_eta = K_r_eff / V_eff
        eta = np.clip(soft_min(1.0, ratio_eta, k), 0.0, 1.0)

        pi_0 = 1.0 - eta * (1.0 - lam_eff)   # bad-paper pass rate
        pi_1 = 1.0 - eta * p['epsilon']       # good-paper pass rate

        # Peer-accepted pool M (with AI-driven volume)
        V_G  = p['N'] * p['alpha']                             * vol_mult
        V_B  = p['N'] * (1.0 - p['alpha']) * (1.0 - x_val)   * vol_mult
        M    = V_G * pi_1 + V_B * pi_0         # shape (1, J)

        # Rationing probability rho_bar = min(1, K / M)  →  broadcast to (I, J)
        ratio_rho = KS / M
        rho_bar   = np.clip(soft_min(1.0, ratio_rho, k), 0.0, 1.0)

        Pi_bad  = p['r'] * rho_bar * pi_0 - c_eff   # shape (I, J)
        Pi_good = p['r'] * rho_bar * pi_1 - c_eff
        return Pi_bad, Pi_good

    Pi_bad_1, Pi_good_1 = boundary_states(0.999)
    Pi_bad_0, _         = boundary_states(0.001)

    # ── Classification ─────────────────────────────────────────────────────────
    ns          = Pi_good_1 < 0              # No Submission (Gray)
    one_stable  = Pi_bad_1  < 0             # x=1 is stable
    zero_stable = Pi_bad_0  > 0             # x=0 is stable
    not_ns      = ~ns

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

# Base parameters (Set A, no intervention)
BASE = {
    'N': 1000, 'alpha': 0.2,
    'r': 100,  'c': 25,
    'lam': 0.1, 'epsilon': 0.05,
    'smoothness': 15,
}

# Intervention parameters: lambda lowered, c raised, phi=0 and mu=0 lock
# these improvements in (AI no longer degrades lambda or c after the reforms)
BASE_INT = {
    'N': 1000, 'alpha': 0.2,
    'r': 100,  'c': 35,
    'lam': 0.05, 'epsilon': 0.05,
    'smoothness': 15,
}

# AI elasticity parameters
GAMMA = 0.5   # production elasticity  (gamma)
DELTA = 0.1   # verification elasticity (delta < gamma)
PHI   = 0.4   # submission-cost slope   (phi)
MU    = 0.2   # false-positive slope    (mu)

AI_LEVEL = 0.8

# Grid resolution and axis ranges
RES          = 200
K_rev_vals   = np.linspace(10, 700, RES)
K_store_vals = np.linspace(10, 700, RES)

# ─────────────────────────────────────────────────────────────────────────────
# 3.  Compute regime maps
# ─────────────────────────────────────────────────────────────────────────────
print("Computing left panel:  a=0.8, base parameters ...")
map_base = classify_regime_grid(K_rev_vals, K_store_vals, BASE,
                                 ai_level=AI_LEVEL,
                                 gamma=GAMMA, delta=DELTA, phi=PHI, mu=MU)

print("Computing right panel: a=0.8, intervention parameters ...")
map_int  = classify_regime_grid(K_rev_vals, K_store_vals, BASE_INT,
                                 ai_level=AI_LEVEL,
                                 gamma=GAMMA, delta=DELTA, phi=0.0, mu=0.0)
print("Done.")

# ─────────────────────────────────────────────────────────────────────────────
# 4.  Plot
# ─────────────────────────────────────────────────────────────────────────────
# Regime colours: GH=0 green, GC=1 red, BS=2 yellow, SC=3 blue, NS=4 gray
COLORS = ['#98FB98', '#FFB6C1', '#FFE4B5', '#ADD8E6', '#D3D3D3']
CMAP   = ListedColormap(COLORS)
EXTENT = [K_rev_vals.min(), K_rev_vals.max(),
          K_store_vals.min(), K_store_vals.max()]

fig = plt.figure(figsize=(16, 7.0))
gs  = gridspec.GridSpec(1, 2, figure=fig, wspace=0.12)

FS_LABEL  = 15   # axis labels
FS_TITLE  = 14   # panel titles
FS_ANNOT  = 13   # annotation text inside panels
FS_SMALL  = 12   # secondary annotations
FS_LEGEND = 12   # legend

# ── Left panel ─────────────────────────────────────────────────────────────
ax0 = fig.add_subplot(gs[0, 0])
ax0.imshow(map_base, origin='lower', extent=EXTENT,
           aspect='auto', cmap=CMAP, vmin=0, vmax=4)

ax0.set_xlabel(r'Review capacity  $K_{rev}$', fontsize=FS_LABEL, fontweight='bold')
ax0.set_ylabel(r'Slot capacity  $K$', fontsize=FS_LABEL, fontweight='bold')
ax0.set_title(r'(a)  Current state: $a=0.8$, base parameters',
              fontsize=FS_TITLE, pad=10, fontweight='bold')
ax0.tick_params(labelsize=12)

# Set A star
ax0.plot(300, 400, marker='*', markersize=16, color='black', zorder=10)
ax0.annotate('Set A', xy=(300, 400), xytext=(220, 480),
             fontsize=FS_ANNOT, color='black', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

# Navy arrow: Principle 1 K_rev↑ alone — stays in GC
# Arrow starts well to the right of Set A to avoid overlap
ax0.annotate('',
             xy=(560, 400), xytext=(340, 400),
             arrowprops=dict(arrowstyle='->', color='navy',
                             lw=2.5, mutation_scale=22))
# Label box placed above the arrow, shifted right so it clears the star
ax0.text(450, 450, r'Principle 1: $K_{rev}\uparrow$' + '\n(remains in GC)',
         ha='center', va='bottom', fontsize=FS_ANNOT, color='navy',
         fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.35', facecolor='white',
                   edgecolor='navy', alpha=0.90))

# Annotation: GH only below K≈124
ax0.text(18, 80,
         r'GH only below $K \approx 124$',
         fontsize=FS_SMALL, color='#2e6b2e', style='italic', fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.30', facecolor='white',
                   edgecolor='#2e6b2e', alpha=0.88))

# Subtitle box
ax0.text(0.02, 0.98,
         r'$\lambda=0.26,\; c=17 \;\Rightarrow\; \lambda > c/r$:' + '\nGH impossible at $K=400$',
         transform=ax0.transAxes, fontsize=FS_SMALL, fontweight='bold',
         verticalalignment='top',
         bbox=dict(boxstyle='round,pad=0.40', facecolor='white',
                   edgecolor='gray', alpha=0.92))

# ── Right panel ─────────────────────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0, 1])
ax1.imshow(map_int, origin='lower', extent=EXTENT,
           aspect='auto', cmap=CMAP, vmin=0, vmax=4)

ax1.set_xlabel(r'Review capacity  $K_{rev}$', fontsize=FS_LABEL, fontweight='bold')
ax1.set_yticklabels([])
ax1.set_title(r'(b)  After Principles 2+3: $\lambda=0.05$, $c=35$',
              fontsize=FS_TITLE, pad=10, fontweight='bold')
ax1.tick_params(labelsize=12)

# Set A star — now in BS
ax1.plot(300, 400, marker='*', markersize=16, color='black', zorder=10)
ax1.annotate('Set A\n(BS)', xy=(300, 400), xytext=(180, 500),
             fontsize=FS_ANNOT, color='black', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

# Dark green arrow: combined → GH (K_rev up to 620)
ax1.annotate('',
             xy=(620, 400), xytext=(340, 400),
             arrowprops=dict(arrowstyle='->', color='darkgreen',
                             lw=2.5, mutation_scale=22))
ax1.text(480, 450, 'Principles 1+2+3\ncombined \u2192 GH',
         ha='center', va='bottom', fontsize=FS_ANNOT, color='darkgreen',
         fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.35', facecolor='white',
                   edgecolor='darkgreen', alpha=0.90))

# Annotation box: what each principle does
ax1.text(690, 175,
         'Principles 2+3:\n'
         r'  $\lambda\downarrow$, $c\uparrow$' + '\n'
         r'$\Rightarrow$ GC eliminated' + '\n\n'
         'Principle 1:\n'
         r'  $K_{rev}\uparrow$' + '\n'
         'BS \u2192 GH',
         ha='right', va='center', fontsize=FS_SMALL, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.40', facecolor='#f0fff0',
                   edgecolor='darkgreen', alpha=0.94))

# Subtitle box
ax1.text(0.02, 0.98,
         r'$\lambda=0.05 < c/r=0.35$:' + '\nGH condition restored',
         transform=ax1.transAxes, fontsize=FS_SMALL, fontweight='bold',
         verticalalignment='top',
         bbox=dict(boxstyle='round,pad=0.40', facecolor='white',
                   edgecolor='gray', alpha=0.92))

# ── Shared legend ─────────────────────────────────────────────────────────────
legend_handles = [
    Patch(facecolor='#98FB98', edgecolor='#555',
          label='Global Honesty (GH)  —  $x \\to 1$ from anywhere'),
    Patch(facecolor='#FFE4B5', edgecolor='#555',
          label='Bistability (BS)       —  history-dependent'),
    Patch(facecolor='#ADD8E6', edgecolor='#555',
          label='Stable Coexistence (SC) — interior long-run outcome'),
    Patch(facecolor='#FFB6C1', edgecolor='#555',
          label='Global Corruption (GC) —  $x \\to 0$ from anywhere'),
    Patch(facecolor='#D3D3D3', edgecolor='#555',
          label='No Submission (NS)      —  participation fails'),
]
fig.legend(handles=legend_handles, loc='lower center',
           ncol=3, framealpha=0.95,
           bbox_to_anchor=(0.5, -0.11),
           prop={'size': FS_LEGEND, 'weight': 'bold'},
           title=(r'Regime legend  |  Base: $N=1000,\ \alpha=0.2,\ r=100,\ \varepsilon=0.05$;'
                  r'  AI: $\gamma=0.5,\ \delta=0.1$'),
           title_fontsize=11)

fig.suptitle(
    r'Fig.~10  $\cdot$  Intervention levers in the $(K_{rev},\,K)$ space at $a=0.8$:'
    '\nPrinciples 2+3 eliminate GC; Principle 1 converts BS into GH',
    fontsize=14, fontweight='bold', y=1.03
)

# ─────────────────────────────────────────────────────────────────────────────
# 5.  Save
# ─────────────────────────────────────────────────────────────────────────────
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR  = os.path.join(SCRIPT_DIR, '..', 'doc', 'tex')
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'fig10_interventions.pdf')

plt.savefig(OUTPUT_PATH, dpi=300, bbox_inches='tight')
print(f"Saved -> {os.path.normpath(OUTPUT_PATH)}")
plt.show()
