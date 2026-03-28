"""
Figure 7: Regime map in (N, a) space -- AI erodes the stability window

Single-panel figure showing how the collapse threshold N_up(a) falls as AI
adoption rises. The regime map in (N, a) space makes visible that the
GH and BS regions shrink and vanish at a ~ 0.5.

Set A parameters: K_rev=300, K=400, r=100, c=25, lam0=0.1, eps=0.05
AI parameters:    gamma=0.5, delta=0.1, phi=0.4, mu=0.2

Output: fig7_hysteresis_widening.pdf in doc/tex/
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_io import save_data, load_data, DATA_DIR
from fig_style import apply_style, REGIME_CMAP, regime_legend

apply_style()

# ─────────────────────────────────────────────────────────────────────────────
# 1.  Model core
# ─────────────────────────────────────────────────────────────────────────────

def soft_min(u, v, k=15):
    return -np.log(np.exp(-k * u) + np.exp(-k * v)) / k


def payoffs(x, N, K_rev, K_store, p, a,
            gamma=0.5, delta=0.1, phi=0.4, mu=0.2):
    k       = p.get('smoothness', 15)
    c_eff   = p['c']   * (1.0 - phi * a)
    lam_eff = min(p['lam'] + mu * a, 0.99)
    vol_m   = 1.0 + gamma * a
    krev_m  = 1.0 + delta * a

    V   = N * (1.0 - (1.0 - p['alpha']) * x) * vol_m
    Kr  = K_rev * krev_m
    eta = np.clip(soft_min(1.0, Kr / V, k), 0.0, 1.0)
    p0  = 1.0 - eta * (1.0 - lam_eff)
    p1  = 1.0 - eta * p['epsilon']

    VG  = N * p['alpha']                        * vol_m
    VB  = N * (1.0 - p['alpha']) * (1.0 - x)   * vol_m
    M   = VG * p1 + VB * p0
    rho = np.clip(soft_min(1.0, K_store / M, k), 0.0, 1.0)
    return p['r'] * rho * p0 - c_eff, p['r'] * rho * p1 - c_eff


def classify(N, K_rev, K_store, p, a, gamma, delta, phi, mu):
    kw = dict(N=N, K_rev=K_rev, K_store=K_store, p=p, a=a,
              gamma=gamma, delta=delta, phi=phi, mu=mu)
    Pb1, Pg1 = payoffs(0.999, **kw)
    Pb0, _   = payoffs(0.001, **kw)
    if Pg1 < 0:
        return 4
    one_s  = Pb1 < 0
    zero_s = Pb0 > 0
    if   one_s and     zero_s: return 2
    elif one_s and not zero_s: return 0
    elif not one_s and zero_s: return 1
    else:                      return 3


# ─────────────────────────────────────────────────────────────────────────────
# 2.  Parameters
# ─────────────────────────────────────────────────────────────────────────────

BASE = {
    'N': 1000, 'alpha': 0.2,
    'r': 100,  'c': 25,
    'lam': 0.1, 'epsilon': 0.05,
    'smoothness': 15,
}
KR, KS = 300, 400
AI     = dict(gamma=0.5, delta=0.1, phi=0.4, mu=0.2)

N_grid = np.linspace(50, 2500, 220)
A_grid = np.linspace(0.0, 1.0, 150)

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'doc', 'tex', 'fig7_hysteresis_widening.pdf')
DATA_PATH   = os.path.join(DATA_DIR, 'fig7_data.json')

# ─────────────────────────────────────────────────────────────────────────────
# 3.  Compute
# ─────────────────────────────────────────────────────────────────────────────

def compute_data():
    print("Computing (N, a) phase map ...")
    phase_map = np.zeros((len(A_grid), len(N_grid)), dtype=np.int8)
    for i, a_v in enumerate(A_grid):
        for j, N_v in enumerate(N_grid):
            phase_map[i, j] = classify(N_v, KR, KS, BASE, a_v, **AI)
    print("Done.")

    N_up_curve = np.full(len(A_grid), np.nan)
    N_lo_curve = np.full(len(A_grid), np.nan)

    for i in range(len(A_grid)):
        row = phase_map[i, :]
        stable_honest = np.where((row == 0) | (row == 2))[0]
        if len(stable_honest) > 0:
            N_up_curve[i] = N_grid[stable_honest[-1]]
        bs_idx = np.where(row == 2)[0]
        if len(bs_idx) > 0:
            N_lo_curve[i] = N_grid[bs_idx[0]]

    return {
        'phase_map':  phase_map,
        'N_up_curve': N_up_curve,
        'N_lo_curve': N_lo_curve,
        'N_grid':     N_grid,
        'A_grid':     A_grid,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 4.  Plot (single panel)
# ─────────────────────────────────────────────────────────────────────────────

def plot(data):
    phase_map  = data['phase_map']
    N_up_curve = data['N_up_curve']
    N_lo_curve = data['N_lo_curve']
    N_grid_    = data['N_grid']
    A_grid_    = data['A_grid']

    fig, ax = plt.subplots(figsize=(5.0, 3.5))

    ax.imshow(phase_map, origin='lower', aspect='auto', cmap=REGIME_CMAP,
              vmin=0, vmax=4,
              extent=[N_grid_.min(), N_grid_.max(), A_grid_.min(), A_grid_.max()])

    # Contour lines at regime boundaries
    ax.contour(N_grid_, A_grid_, phase_map.astype(float),
               levels=[0.5, 1.5, 2.5, 3.5],
               colors='#333333', linewidths=0.5, alpha=0.6)

    # Collapse boundary
    valid = ~np.isnan(N_up_curve)
    ax.plot(N_up_curve[valid], A_grid_[valid],
            color='#CC3311', lw=2.0, label=r'Collapse boundary $N_\uparrow(a)$')

    # Lower BS boundary
    valid2 = ~np.isnan(N_lo_curve)
    ax.plot(N_lo_curve[valid2], A_grid_[valid2],
            color='#004488', lw=1.5, ls='--', label=r'Lower BS boundary')

    ax.set_xlabel(r'Population size $N$', fontsize=10)
    ax.set_ylabel(r'AI adoption $a$', fontsize=10)
    ax.tick_params(labelsize=9)

    ax.legend(loc='upper right', framealpha=0.92, fontsize=8)

    # Regime legend below panel
    present = sorted(set(np.unique(phase_map).tolist()))
    regime_legend(fig, present_codes=present,
                  loc='lower center', bbox_to_anchor=(0.5, -0.02),
                  ncol=len(present))

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
