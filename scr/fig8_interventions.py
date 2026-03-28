"""
Figure 8: Intervention levers in the (K_rev, K) parameter space at a=0.8

Left panel:  base parameters — GC dominates, Set A deep in GC.
             Arrow shows K_rev expansion alone fails.
Right panel: after interventions (lambda=0.05, c=35) — GC eliminated.
             Combined arrow (K_rev + lambda + c) restores GH.

Output: fig8_interventions.pdf in doc/tex/
"""

import os
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
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

# Paul Tol Bright
REGIME_COLORS = ['#228833', '#EE6677', '#CCBB44', '#4477AA', '#BBBBBB']
REGIME_CMAP   = ListedColormap(REGIME_COLORS)

# ─────────────────────────────────────────────────────────────────────────────
# 1.  Model core (same as fig3)
# ─────────────────────────────────────────────────────────────────────────────

def soft_min(a, b, k=15):
    return -np.log(np.exp(-k * a) + np.exp(-k * b)) / k


def classify_regime_grid(K_rev_vals, K_store_vals, base_params, ai_level=0.0,
                          gamma=0.5, delta=0.1, phi=0.4, mu=0.2):
    p = base_params
    k = p.get('smoothness', 15)
    a = ai_level

    c_eff   = p['c']   * (1.0 - phi * a)
    lam_eff = min(p['lam'] + mu * a, 0.99)
    vol_mult  = 1.0 + gamma * a
    krev_mult = 1.0 + delta * a

    KR = K_rev_vals[np.newaxis, :]
    KS = K_store_vals[:, np.newaxis]

    def boundary_states(x_val):
        V_raw   = p['N'] * (1.0 - (1.0 - p['alpha']) * x_val)
        V_eff   = V_raw  * vol_mult
        K_r_eff = KR     * krev_mult
        eta = np.clip(soft_min(1.0, K_r_eff / V_eff, k), 0.0, 1.0)
        pi_0 = 1.0 - eta * (1.0 - lam_eff)
        pi_1 = 1.0 - eta * p['epsilon']
        V_G = p['N'] * p['alpha']                           * vol_mult
        V_B = p['N'] * (1.0 - p['alpha']) * (1.0 - x_val)  * vol_mult
        M   = V_G * pi_1 + V_B * pi_0
        rho_bar = np.clip(soft_min(1.0, KS / M, k), 0.0, 1.0)
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
    grid[not_ns &  one_stable &  zero_stable] = 2
    grid[not_ns &  one_stable & ~zero_stable] = 0
    grid[not_ns & ~one_stable &  zero_stable] = 1
    grid[not_ns & ~one_stable & ~zero_stable] = 3
    return grid


# ─────────────────────────────────────────────────────────────────────────────
# 2.  Parameters
# ─────────────────────────────────────────────────────────────────────────────

BASE = {
    'N': 1000, 'alpha': 0.2,
    'r': 100,  'c': 25,
    'lam': 0.1, 'epsilon': 0.05,
    'smoothness': 15,
}

BASE_INT = {
    'N': 1000, 'alpha': 0.2,
    'r': 100,  'c': 35,
    'lam': 0.05, 'epsilon': 0.05,
    'smoothness': 15,
}

GAMMA    = 0.5
DELTA    = 0.1
PHI      = 0.4
MU       = 0.2
AI_LEVEL = 0.8

RES          = 200
K_rev_vals   = np.linspace(10, 700, RES)
K_store_vals = np.linspace(10, 700, RES)

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'doc', 'tex', 'fig8_interventions.pdf')
DATA_PATH   = os.path.join(DATA_DIR, 'fig8_data.json')

# ─────────────────────────────────────────────────────────────────────────────
# 3.  Compute
# ─────────────────────────────────────────────────────────────────────────────

def compute_data():
    print("Computing left panel:  a=0.8, base parameters ...")
    map_base = classify_regime_grid(K_rev_vals, K_store_vals, BASE,
                                     ai_level=AI_LEVEL,
                                     gamma=GAMMA, delta=DELTA, phi=PHI, mu=MU)

    print("Computing right panel: a=0.8, intervention parameters ...")
    map_int  = classify_regime_grid(K_rev_vals, K_store_vals, BASE_INT,
                                     ai_level=AI_LEVEL,
                                     gamma=GAMMA, delta=DELTA, phi=0.0, mu=0.0)
    print("Done.")

    return {
        'map_base':     map_base,
        'map_int':      map_int,
        'K_rev_vals':   K_rev_vals,
        'K_store_vals': K_store_vals,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 4.  Plot
# ─────────────────────────────────────────────────────────────────────────────

def plot(data):
    map_base      = data['map_base']
    map_int       = data['map_int']
    K_rev_vals_   = data['K_rev_vals']
    K_store_vals_ = data['K_store_vals']

    EXTENT = [K_rev_vals_.min(), K_rev_vals_.max(),
              K_store_vals_.min(), K_store_vals_.max()]

    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(7.0, 3.2), sharey=True)
    fig.subplots_adjust(wspace=0.08)

    # ── Left panel: base parameters ──────────────────────────────────────────
    ax0.imshow(map_base, origin='lower', extent=EXTENT,
               aspect='auto', cmap=REGIME_CMAP, vmin=0, vmax=4)

    ax0.set_xlabel(r'Verification capacity $K_{rev}$', fontsize=10)
    ax0.set_ylabel(r'Allocation capacity $K$', fontsize=10)
    ax0.tick_params(labelsize=9)

    ax0.text(0.04, 0.96, r'\textbf{(a)}', transform=ax0.transAxes,
             fontsize=11, va='top')
    ax0.text(0.04, 0.87, r'Base parameters at $a=0.8$',
             transform=ax0.transAxes, fontsize=8, va='top', color='#444444')

    # Set A marker + arrow
    ax0.plot(300, 400, marker='*', markersize=12, color='black', zorder=10)
    ax0.annotate('Set A', xy=(300, 400), xytext=(220, 510),
                 fontsize=8, color='black',
                 arrowprops=dict(arrowstyle='->', color='black', lw=0.8))

    ax0.annotate('',
                 xy=(550, 400), xytext=(330, 400),
                 arrowprops=dict(arrowstyle='->', color='#004488',
                                 lw=2.0, mutation_scale=16))
    ax0.text(440, 435, r'$K_{rev}\!\uparrow$ alone',
             ha='center', fontsize=7.5, color='#004488')

    # Direct regime labels
    ax0.text(0.75, 0.12, 'GH', transform=ax0.transAxes,
             fontsize=8, color='white', fontweight='bold', ha='center')
    ax0.text(0.30, 0.70, 'GC', transform=ax0.transAxes,
             fontsize=8, color='white', fontweight='bold', ha='center')

    # ── Right panel: after interventions ─────────────────────────────────────
    ax1.imshow(map_int, origin='lower', extent=EXTENT,
               aspect='auto', cmap=REGIME_CMAP, vmin=0, vmax=4)

    ax1.set_xlabel(r'Verification capacity $K_{rev}$', fontsize=10)
    ax1.tick_params(labelsize=9)

    ax1.text(0.04, 0.96, r'\textbf{(b)}', transform=ax1.transAxes,
             fontsize=11, va='top')
    ax1.text(0.04, 0.87, r'After $\lambda\!\downarrow$, $c\!\uparrow$',
             transform=ax1.transAxes, fontsize=8, va='top', color='#444444')

    # Set A marker + combined arrow
    ax1.plot(300, 400, marker='*', markersize=12, color='black', zorder=10)
    ax1.annotate('Set A', xy=(300, 400), xytext=(200, 510),
                 fontsize=8, color='black',
                 arrowprops=dict(arrowstyle='->', color='black', lw=0.8))

    ax1.annotate('',
                 xy=(600, 400), xytext=(330, 400),
                 arrowprops=dict(arrowstyle='->', color='#228833',
                                 lw=2.0, mutation_scale=16))
    ax1.text(465, 435, r'$+\; K_{rev}\!\uparrow \to$ GH',
             ha='center', fontsize=7.5, color='#228833')

    # Direct regime labels
    ax1.text(0.80, 0.12, 'GH', transform=ax1.transAxes,
             fontsize=8, color='white', fontweight='bold', ha='center')
    ax1.text(0.35, 0.50, 'BS', transform=ax1.transAxes,
             fontsize=8, color='black', fontweight='bold', ha='center', alpha=0.7)

    # ── Shared legend ────────────────────────────────────────────────────────
    legend_handles = [
        Patch(facecolor=REGIME_COLORS[0], edgecolor='#555555', label='GH'),
        Patch(facecolor=REGIME_COLORS[2], edgecolor='#555555', label='BS'),
        Patch(facecolor=REGIME_COLORS[3], edgecolor='#555555', label='SC'),
        Patch(facecolor=REGIME_COLORS[1], edgecolor='#555555', label='GC'),
        Patch(facecolor=REGIME_COLORS[4], edgecolor='#555555', label='NS'),
    ]
    fig.legend(handles=legend_handles, loc='lower center',
               ncol=5, framealpha=0.95,
               bbox_to_anchor=(0.5, -0.06), fontsize=9)

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, bbox_inches='tight')
    print(f"Saved: {os.path.normpath(OUTPUT_PATH)}")


# ─────────────────────────────────────────────────────────────────────────────
# 5.  Main
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
