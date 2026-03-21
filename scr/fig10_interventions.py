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
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch, FancyArrowPatch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_io import save_data, load_data, DATA_DIR


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

    Regime codes: 0=GH(green), 1=GC(red), 2=BS(yellow), 3=SC(blue), 4=NS(gray)
    """
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

    ns          = Pi_good_1 < 0
    one_stable  = Pi_bad_1  < 0
    zero_stable = Pi_bad_0  > 0
    not_ns      = ~ns

    grid = np.full(Pi_bad_1.shape, -1, dtype=np.int8)
    grid[ns] = 4
    grid[not_ns &  one_stable &  zero_stable] = 2
    grid[not_ns &  one_stable & ~zero_stable] = 0
    grid[not_ns & ~one_stable &  zero_stable] = 1
    grid[not_ns & ~one_stable & ~zero_stable] = 3
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

BASE_INT = {
    'N': 1000, 'alpha': 0.2,
    'r': 100,  'c': 35,
    'lam': 0.05, 'epsilon': 0.05,
    'smoothness': 15,
}

GAMMA = 0.5
DELTA = 0.1
PHI   = 0.4
MU    = 0.2

AI_LEVEL = 0.8

RES          = 200
K_rev_vals   = np.linspace(10, 700, RES)
K_store_vals = np.linspace(10, 700, RES)

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'doc', 'tex', 'fig10_interventions.pdf')
DATA_PATH   = os.path.join(DATA_DIR, 'fig10_data.json')


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

    COLORS = ['#98FB98', '#FFB6C1', '#FFE4B5', '#ADD8E6', '#D3D3D3']
    CMAP   = ListedColormap(COLORS)
    EXTENT = [K_rev_vals_.min(), K_rev_vals_.max(),
              K_store_vals_.min(), K_store_vals_.max()]

    fig = plt.figure(figsize=(16, 7.0))
    gs  = gridspec.GridSpec(1, 2, figure=fig, wspace=0.12)

    FS_LABEL  = 15
    FS_TITLE  = 14
    FS_ANNOT  = 13
    FS_SMALL  = 12
    FS_LEGEND = 12

    # ── Left panel ─────────────────────────────────────────────────────────────
    ax0 = fig.add_subplot(gs[0, 0])
    ax0.imshow(map_base, origin='lower', extent=EXTENT,
               aspect='auto', cmap=CMAP, vmin=0, vmax=4)

    ax0.set_xlabel(r'Review capacity  $K_{rev}$', fontsize=FS_LABEL, fontweight='bold')
    ax0.set_ylabel(r'Slot capacity  $K$', fontsize=FS_LABEL, fontweight='bold')
    ax0.set_title(r'(a)  Current state: $a=0.8$, base parameters',
                  fontsize=FS_TITLE, pad=10, fontweight='bold')
    ax0.tick_params(labelsize=12)

    ax0.plot(300, 400, marker='*', markersize=16, color='black', zorder=10)
    ax0.annotate('Set A', xy=(300, 400), xytext=(220, 480),
                 fontsize=FS_ANNOT, color='black', fontweight='bold',
                 arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

    ax0.annotate('',
                 xy=(560, 400), xytext=(340, 400),
                 arrowprops=dict(arrowstyle='->', color='navy',
                                 lw=2.5, mutation_scale=22))
    ax0.text(450, 450, r'Principle 1: $K_{rev}\uparrow$' + '\n(remains in GC)',
             ha='center', va='bottom', fontsize=FS_ANNOT, color='navy',
             fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.35', facecolor='white',
                       edgecolor='navy', alpha=0.90))

    ax0.text(18, 80,
             r'GH only below $K \approx 124$',
             fontsize=FS_SMALL, color='#2e6b2e', style='italic', fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.30', facecolor='white',
                       edgecolor='#2e6b2e', alpha=0.88))

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

    ax1.plot(300, 400, marker='*', markersize=16, color='black', zorder=10)
    ax1.annotate('Set A\n(BS)', xy=(300, 400), xytext=(180, 500),
                 fontsize=FS_ANNOT, color='black', fontweight='bold',
                 arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

    ax1.annotate('',
                 xy=(620, 400), xytext=(340, 400),
                 arrowprops=dict(arrowstyle='->', color='darkgreen',
                                 lw=2.5, mutation_scale=22))
    ax1.text(480, 450, 'Principles 1+2+3\ncombined \u2192 GH',
             ha='center', va='bottom', fontsize=FS_ANNOT, color='darkgreen',
             fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.35', facecolor='white',
                       edgecolor='darkgreen', alpha=0.90))

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
    plt.savefig(OUTPUT_PATH, dpi=300, bbox_inches='tight')
    print(f"Saved -> {os.path.normpath(OUTPUT_PATH)}")
    plt.show()


# ─────────────────────────────────────────────────────────────────────────────
# 6.  Main
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    recompute = '--recompute' in sys.argv
    if recompute or not os.path.exists(DATA_PATH):
        data = compute_data()
        save_data(data, DATA_PATH)
        print(f"Data saved → {DATA_PATH}")
    else:
        print(f"Loading cached data from {DATA_PATH}")
        data = load_data(DATA_PATH)
    plot(data)
