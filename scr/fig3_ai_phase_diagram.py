"""
Figure 3: Baseline vs High-AI Adoption Phase Diagram (K_rev vs K)

Shows how AI adoption (a) shifts regime boundaries in the (K_rev, K) parameter
space.  Left panel: baseline (a=0).  Right panel: high AI adoption (a=0.8).
The comparison makes visible that the GH region shrinks and the BS/GC region
expands as AI lowers submission cost, raises submission volume, and degrades
screening accuracy faster than it raises review capacity.

Output: fig3_ai_phase_diagram.pdf  →  doc/tex/
"""

import os
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_io import save_data, load_data, DATA_DIR

# ─────────────────────────────────────────────────────────────────────────────
# 0.  Publication rcParams
# ─────────────────────────────────────────────────────────────────────────────

mpl.rcParams.update({
    'font.family':        'serif',
    'text.usetex':        True,
    'pdf.fonttype':       42,
    'savefig.dpi':        300,
    'axes.spines.top':    False,
    'axes.spines.right':  False,
    'axes.linewidth':     0.6,
    'xtick.major.width':  0.6,
    'ytick.major.width':  0.6,
    'xtick.direction':    'out',
    'ytick.direction':    'out',
})

# Paul Tol Bright palette — regime colours
# 0=GH, 1=GC, 2=BS, 3=SC, 4=NS
REGIME_COLORS = ['#228833', '#EE6677', '#CCBB44', '#4477AA', '#BBBBBB']
REGIME_NAMES  = ['Global Honesty (GH)', 'Global Corruption (GC)',
                 'Bistability (BS)', 'Stable Coexistence (SC)',
                 'No Submission (NS)']

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

    Regime codes: 0=GH, 1=GC, 2=BS, 3=SC, 4=NS
    """
    p   = base_params
    k   = p.get('smoothness', 15)
    a   = ai_level

    c_eff   = p['c']   * (1.0 - phi * a)
    lam_eff = min(p['lam'] + mu * a, 0.99)

    vol_mult  = 1.0 + gamma * a
    krev_mult = 1.0 + delta * a

    KR = K_rev_vals[np.newaxis, :]
    KS = K_store_vals[:, np.newaxis]

    def boundary_states(x_val):
        V_raw    = p['N'] * (1.0 - (1.0 - p['alpha']) * x_val)
        V_eff    = V_raw  * vol_mult
        K_r_eff  = KR     * krev_mult

        ratio_eta = K_r_eff / V_eff
        eta = np.clip(soft_min(1.0, ratio_eta, k), 0.0, 1.0)

        pi_0 = 1.0 - eta * (1.0 - lam_eff)
        pi_1 = 1.0 - eta * p['epsilon']

        V_G  = p['N'] * p['alpha']                             * vol_mult
        V_B  = p['N'] * (1.0 - p['alpha']) * (1.0 - x_val)   * vol_mult
        M    = V_G * pi_1 + V_B * pi_0

        ratio_rho = KS / M
        rho_bar   = np.clip(soft_min(1.0, ratio_rho, k), 0.0, 1.0)

        Pi_bad  = p['r'] * rho_bar * pi_0 - c_eff
        Pi_good = p['r'] * rho_bar * pi_1 - c_eff
        return Pi_bad, Pi_good

    Pi_bad_1, Pi_good_1 = boundary_states(0.999)
    Pi_bad_0, _         = boundary_states(0.001)

    ns         = Pi_good_1 < 0
    one_stable = Pi_bad_1  < 0
    zero_stable= Pi_bad_0  > 0
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

GAMMA = 0.5
DELTA = 0.1
PHI   = 0.4
MU    = 0.2

RES          = 180
K_rev_vals   = np.linspace(10, 600, RES)
K_store_vals = np.linspace(10, 700, RES)

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'doc', 'tex', 'fig3_ai_phase_diagram.pdf')
DATA_PATH   = os.path.join(DATA_DIR, 'fig3_data.json')

# ─────────────────────────────────────────────────────────────────────────────
# 3.  Compute
# ─────────────────────────────────────────────────────────────────────────────

def compute_data():
    print("Computing baseline phase map  (a = 0.0) ...")
    map_base = classify_regime_grid(K_rev_vals, K_store_vals, BASE,
                                     ai_level=0.0,
                                     gamma=GAMMA, delta=DELTA, phi=PHI, mu=MU)

    print("Computing high-AI phase map   (a = 0.8) ...")
    map_ai   = classify_regime_grid(K_rev_vals, K_store_vals, BASE,
                                     ai_level=0.8,
                                     gamma=GAMMA, delta=DELTA, phi=PHI, mu=MU)
    print("Done.")

    return {
        'map_base':    map_base,
        'map_ai':      map_ai,
        'K_rev_vals':  K_rev_vals,
        'K_store_vals': K_store_vals,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 4.  Plot
# ─────────────────────────────────────────────────────────────────────────────

def plot(data):
    map_base     = data['map_base']
    map_ai       = data['map_ai']
    K_rev_vals_  = data['K_rev_vals']
    K_store_vals_= data['K_store_vals']

    CMAP   = ListedColormap(REGIME_COLORS)
    EXTENT = [K_rev_vals_.min(), K_rev_vals_.max(),
              K_store_vals_.min(), K_store_vals_.max()]

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.2), sharey=True)
    fig.subplots_adjust(wspace=0.08)

    panel_data = [
        (map_base, r'Baseline ($a = 0$)'),
        (map_ai,   r'High AI adoption ($a = 0.8$)'),
    ]
    panel_labels = ['(a)', '(b)']

    for col, (grid, subtitle) in enumerate(panel_data):
        ax = axes[col]
        ax.imshow(grid, origin='lower', extent=EXTENT,
                  aspect='auto', cmap=CMAP, vmin=0, vmax=4)

        ax.set_xlabel(r'Verification capacity $K_{rev}$', fontsize=10)
        if col == 0:
            ax.set_ylabel(r'Allocation capacity $K$', fontsize=10)

        # Panel label — bold, upper-left
        ax.text(0.04, 0.96, r'\textbf{' + panel_labels[col] + '}',
                transform=ax.transAxes, fontsize=11, va='top')

        # Subtitle below panel label
        ax.text(0.04, 0.87, subtitle,
                transform=ax.transAxes, fontsize=9, va='top')

        # Mark the Set-A calibration point
        ax.plot(300, 400, marker='*', markersize=10,
                color='black', zorder=10)
        if col == 0:
            ax.annotate(r'Set A', xy=(300, 400), xytext=(350, 510),
                        fontsize=8, color='black',
                        arrowprops=dict(arrowstyle='->', color='black', lw=0.8))

        # Direct regime labels inside regions
        if col == 0:
            ax.text(0.70, 0.25, 'GH', transform=ax.transAxes,
                    fontsize=8, color='white', fontweight='bold',
                    ha='center', va='center')
            ax.text(0.25, 0.80, 'GC', transform=ax.transAxes,
                    fontsize=8, color='white', fontweight='bold',
                    ha='center', va='center')
            ax.text(0.60, 0.65, 'BS', transform=ax.transAxes,
                    fontsize=8, color='black', fontweight='bold',
                    ha='center', va='center', alpha=0.7)
        else:
            ax.text(0.82, 0.15, 'GH', transform=ax.transAxes,
                    fontsize=8, color='white', fontweight='bold',
                    ha='center', va='center')
            ax.text(0.35, 0.70, 'GC', transform=ax.transAxes,
                    fontsize=8, color='white', fontweight='bold',
                    ha='center', va='center')
            ax.text(0.55, 0.35, 'BS', transform=ax.transAxes,
                    fontsize=8, color='black', fontweight='bold',
                    ha='center', va='center', alpha=0.7)
            ax.annotate(r'Set A', xy=(300, 400), xytext=(360, 510),
                        fontsize=8, color='black',
                        arrowprops=dict(arrowstyle='->', color='black', lw=0.8))

        ax.tick_params(labelsize=9)

    # ── Shared legend ───────────────────────────────────────────────────────
    legend_handles = [
        Patch(facecolor=REGIME_COLORS[0], edgecolor='#555555', label='GH'),
        Patch(facecolor=REGIME_COLORS[2], edgecolor='#555555', label='BS'),
        Patch(facecolor=REGIME_COLORS[3], edgecolor='#555555', label='SC'),
        Patch(facecolor=REGIME_COLORS[1], edgecolor='#555555', label='GC'),
        Patch(facecolor=REGIME_COLORS[4], edgecolor='#555555', label='NS'),
    ]
    fig.legend(handles=legend_handles, loc='lower center',
               ncol=5, framealpha=0.95,
               bbox_to_anchor=(0.5, -0.06),
               fontsize=9)

    # ─────────────────────────────────────────────────────────────────────────
    # 5.  Save
    # ─────────────────────────────────────────────────────────────────────────
    plt.savefig(OUTPUT_PATH, bbox_inches='tight')
    print(f"Saved: {os.path.normpath(OUTPUT_PATH)}")


# ─────────────────────────────────────────────────────────────────────────────
# 6.  Main
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    recompute = '--recompute' in sys.argv
    if recompute or not os.path.exists(DATA_PATH):
        data = compute_data()
        save_data(data, DATA_PATH)
        print(f"Data saved: {DATA_PATH}")
    else:
        print(f"Loading cached data from {DATA_PATH}")
        data = load_data(DATA_PATH)
    plot(data)
