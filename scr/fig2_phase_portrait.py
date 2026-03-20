"""
Figure 2: Baseline phase portrait (bistability)

Plots the spam payoff Π_bad(x) against the honest-author share x under
Set-A parameters (the bistability-prone calibration).  The curve crosses
zero at an interior tipping threshold x* ≈ 0.82.

  Red shading  : Π_bad(x) > 0 → AS strategy spreads, x falls toward 0.
  Green shading: Π_bad(x) < 0 → OG strategy spreads, x rises toward 1.

Both x = 0 (full corruption) and x = 1 (full honesty) are absorbing states.
Which one prevails depends on whether the initial share of honest authors
sits above or below x*.

Output: polynomial_graph_1.pdf  →  doc/tex/
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

# ─────────────────────────────────────────────────────────────────────────────
# 1.  Model core
# ─────────────────────────────────────────────────────────────────────────────

def soft_min(a, b, k=15):
    """Smooth differentiable approximation of min(a, b)."""
    return -np.log(np.exp(-k * a) + np.exp(-k * b)) / k


def spam_payoff(x, p):
    """
    Spam payoff  Π_bad(x) = r · ρ̄(x) · π₀(x) − c.

    Parameters
    ----------
    x : array-like
        Honest-author share, in (0, 1).
    p : dict
        Model parameters (N, alpha, K_rev, K_store, r, c, lam, epsilon).

    Returns
    -------
    ndarray of same shape as x.
    """
    k       = p.get('smoothness', 15)
    V_total = p['N'] * (1.0 - (1.0 - p['alpha']) * x)
    eta     = np.clip(soft_min(1.0, p['K_rev'] / V_total, k), 0.0, 1.0)
    pi_0    = 1.0 - eta * (1.0 - p['lam'])
    pi_1    = 1.0 - eta * p['epsilon']
    V_G     = p['N'] * p['alpha']
    V_B     = p['N'] * (1.0 - p['alpha']) * (1.0 - x)
    M       = V_G * pi_1 + V_B * pi_0
    rho_bar = np.clip(soft_min(1.0, p['K_store'] / M, k), 0.0, 1.0)
    return p['r'] * rho_bar * pi_0 - p['c']


# ─────────────────────────────────────────────────────────────────────────────
# 2.  Parameters  (Set A — bistability)
# ─────────────────────────────────────────────────────────────────────────────

PARAMS = {
    'N': 1000, 'alpha': 0.2,
    'K_rev': 300, 'K_store': 400,
    'r': 100,  'c': 25,
    'lam': 0.1, 'epsilon': 0.05,
    'smoothness': 15,
}

# ─────────────────────────────────────────────────────────────────────────────
# 3.  Compute curve and tipping threshold
# ─────────────────────────────────────────────────────────────────────────────

x_grid  = np.linspace(0.001, 0.999, 600)
y_curve = spam_payoff(x_grid, PARAMS)

# Locate the interior zero crossing (tipping threshold x*)
x_star = None
for idx in np.where(np.diff(np.sign(y_curve)))[0]:
    x1, x2 = x_grid[idx], x_grid[idx + 1]
    y1, y2 = y_curve[idx], y_curve[idx + 1]
    if y2 != y1:
        x_star = x1 - y1 * (x2 - x1) / (y2 - y1)
        break   # take the first (and only expected) interior crossing

# ─────────────────────────────────────────────────────────────────────────────
# 4.  Plot
# ─────────────────────────────────────────────────────────────────────────────

# Colour palette — consistent with the phase-diagram figures (fig4–fig10)
C_GREEN = '#98FB98'   # Π_bad < 0  →  honesty region   (matches GH colour)
C_RED   = '#FFB6C1'   # Π_bad > 0  →  corruption region (matches GC colour)
C_CURVE = '#1a1a2e'   # main curve

fig, ax = plt.subplots(figsize=(7.5, 4.8))

# ── Shaded regions ────────────────────────────────────────────────────────────
ax.fill_between(x_grid, -1e6, 1e6,
                where=(y_curve < 0), color=C_GREEN, alpha=0.55,
                interpolate=True, zorder=0)
ax.fill_between(x_grid, -1e6, 1e6,
                where=(y_curve > 0), color=C_RED, alpha=0.55,
                interpolate=True, zorder=0)

# ── Π_bad(x) curve ───────────────────────────────────────────────────────────
ax.plot(x_grid, y_curve, color=C_CURVE, lw=2.2, zorder=3)

# ── Zero line ────────────────────────────────────────────────────────────────
ax.axhline(0, color='#444444', lw=0.9, linestyle='--', zorder=2)

# ── Stable fixed-point markers at x = 0 and x = 1 ───────────────────────────
MSIZE = 10
ax.scatter([0, 1], [0, 0],
           s=MSIZE**2, color='black', zorder=6, clip_on=False)

# ── Tipping-threshold marker (orange, consistent with paper caption) ──────────
if x_star is not None:
    y_abs_max = float(np.max(np.abs(y_curve)))
    ax.scatter([x_star], [0],
               s=(MSIZE + 2)**2, color='#FF8C00',
               edgecolors='black', linewidths=0.8, zorder=7)
    ax.annotate(
        rf'$x^* \approx {x_star:.2f}$',
        xy=(x_star, 0),
        xytext=(x_star - 0.18, y_abs_max * 0.38),
        fontsize=10.5,
        arrowprops=dict(arrowstyle='->', color='#333333', lw=1.0),
        color='#333333',
    )

# ── Axis limits and labels ────────────────────────────────────────────────────
y_abs_max = float(np.max(np.abs(y_curve)))
ax.set_xlim(0, 1)
ax.set_ylim(-y_abs_max * 1.4, y_abs_max * 1.4)
ax.set_xlabel(r'Honest-author share  $x$', fontsize=12)
ax.set_ylabel(r'Spam payoff  $\Pi_{\mathrm{bad}}(x)$', fontsize=12)
ax.tick_params(labelsize=10)
ax.grid(True, alpha=0.25, linestyle='--', linewidth=0.7)

# ── Parameter annotation box — style matches fig4–fig10 ──────────────────────
param_str = (
    r'$N=1000,\;\alpha=0.2$' '\n'
    r'$K_{rev}=300,\;K=400$' '\n'
    r'$r=100,\;c=25,\;\lambda=0.10,\;\varepsilon=0.05$'
)
ax.text(0.03, 0.97, param_str,
        transform=ax.transAxes, fontsize=9.5,
        verticalalignment='top',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                  edgecolor='#aaaaaa', alpha=0.90))

# ── Legend ────────────────────────────────────────────────────────────────────
legend_handles = [
    Patch(facecolor=C_RED,   alpha=0.7,
          label=r'$\Pi_{\mathrm{bad}}>0$: AS spreads, $x$ falls'),
    Patch(facecolor=C_GREEN, alpha=0.7,
          label=r'$\Pi_{\mathrm{bad}}<0$: OG spreads, $x$ rises'),
    Line2D([0], [0], color=C_CURVE, lw=2.2,
           label=r'$\Pi_{\mathrm{bad}}(x)$'),
    Line2D([0], [0], marker='o', color='w', lw=0,
           markerfacecolor='black', markersize=9,
           label='Absorbing state ($x=0$ or $x=1$)'),
    Line2D([0], [0], marker='o', color='w', lw=0,
           markerfacecolor='#FF8C00', markeredgecolor='black', markersize=9,
           label=r'Tipping threshold $x^*$'),
]
ax.legend(handles=legend_handles, loc='lower right',
          fontsize=9, framealpha=0.92, edgecolor='#cccccc')

# ─────────────────────────────────────────────────────────────────────────────
# 5.  Save
# ─────────────────────────────────────────────────────────────────────────────
plt.tight_layout()
OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'doc', 'tex')
OUT_PATH = os.path.join(OUT_DIR, 'polynomial_graph_1.pdf')
plt.savefig(OUT_PATH, dpi=150, bbox_inches='tight')
print(f"Saved: {OUT_PATH}")
