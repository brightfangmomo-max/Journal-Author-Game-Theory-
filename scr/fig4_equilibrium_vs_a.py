"""
Figure 4: Stable equilibrium x*(a) as AI adoption rises

Two scenario tracks:
  Track A -- Set A (K_rev=300, K=400): bistability-prone.
            Shows the tipping threshold x*_tip rising silently toward x=1,
            then collapsing into GC.
  Track B -- Set B (K_rev=1200, K=180): coexistence-prone.
            Interior stable equilibrium x* falls smoothly as a rises.

Output: fig4_equilibrium_vs_a.pdf in doc/tex/
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_io import save_data, load_data, DATA_DIR
from fig_style import apply_style

apply_style()

# Paul Tol Bright
C_GH   = '#228833'   # Global Honesty stable branch
C_GC   = '#EE6677'   # Global Corruption stable branch
C_SC   = '#4477AA'   # Stable Coexistence branch
C_TIP  = '#EE7733'   # Tipping threshold (dashed)

# Regime background shading -- Paul Tol Light (softer for fills)
BG_GH  = '#44BB99'
BG_GC  = '#EE8866'
BG_BS  = '#EEDD88'
BG_SC  = '#77AADD'
BG_NS  = '#DDDDDD'
BG_MAP = {0: BG_GH, 1: BG_GC, 2: BG_BS, 3: BG_SC, 4: BG_NS}
NAME_MAP = {0: 'GH', 1: 'GC', 2: 'BS', 3: 'SC', 4: 'NS'}

# ─────────────────────────────────────────────────────────────────────────────
# 1.  Model core
# ─────────────────────────────────────────────────────────────────────────────

def soft_min(u, v, k=15):
    return -np.log(np.exp(-k * u) + np.exp(-k * v)) / k


def weak_paper_payoff(x, K_rev, K_store, p, a,
                      gamma=0.5, delta=0.1, phi=0.4, mu=0.2):
    """Weak-paper payoff Pi_bad(x, a)."""
    k       = p.get('smoothness', 15)
    c_eff   = p['c']   * (1.0 - phi * a)
    lam_eff = min(p['lam'] + mu * a, 0.99)
    vol_m   = 1.0 + gamma * a
    krev_m  = 1.0 + delta * a

    V_eff   = p['N'] * (1.0 - (1.0 - p['alpha']) * x) * vol_m
    Kr_eff  = K_rev * krev_m
    eta     = np.clip(soft_min(1.0, Kr_eff / V_eff, k), 0.0, 1.0)
    pi_0    = 1.0 - eta * (1.0 - lam_eff)
    pi_1    = 1.0 - eta * p['epsilon']

    V_G  = p['N'] * p['alpha']                        * vol_m
    V_B  = p['N'] * (1.0 - p['alpha']) * (1.0 - x)   * vol_m
    M    = V_G * pi_1 + V_B * pi_0
    rho  = np.clip(soft_min(1.0, K_store / M, k), 0.0, 1.0)

    return p['r'] * rho * pi_0 - c_eff


def classify_and_find_equilibria(K_rev, K_store, p, a,
                                  gamma=0.5, delta=0.1, phi=0.4, mu=0.2):
    """
    Return (regime, x_stable, x_tip).
      regime: 0=GH, 1=GC, 2=BS, 3=SC, 4=NS
    """
    kw = dict(K_rev=K_rev, K_store=K_store, p=p, a=a,
              gamma=gamma, delta=delta, phi=phi, mu=mu)

    Pb1  = weak_paper_payoff(0.999, **kw)
    Pb0  = weak_paper_payoff(0.001, **kw)

    # Participation constraint
    k_     = p.get('smoothness', 15)
    c_eff  = p['c'] * (1.0 - phi * a)
    vol_m  = 1.0 + gamma * a
    krev_m = 1.0 + delta * a
    V1     = p['N'] * p['alpha'] * vol_m
    Kr_e   = K_rev * krev_m
    eta1   = np.clip(soft_min(1.0, Kr_e / V1, k_), 0.0, 1.0)
    pi_1_  = 1.0 - eta1 * p['epsilon']
    M1     = p['N'] * p['alpha'] * vol_m * pi_1_
    rho1   = np.clip(soft_min(1.0, K_store / M1, k_), 0.0, 1.0)
    Pg1    = p['r'] * rho1 * pi_1_ - c_eff

    if Pg1 < 0:
        return 4, np.nan, np.nan

    one_stable  = Pb1 < 0
    zero_stable = Pb0 > 0

    if   one_stable and not zero_stable: regime = 0
    elif not one_stable and zero_stable: regime = 1
    elif one_stable and zero_stable:     regime = 2
    else:                                regime = 3

    # Find interior root of Pi_bad(x)=0 by bisection
    x_tip = np.nan
    x_grid = np.linspace(0.005, 0.995, 2000)
    vals   = weak_paper_payoff(x_grid, **kw)
    sign_c = np.where(np.diff(np.sign(vals)))[0]

    if len(sign_c) > 0:
        idx = sign_c[0]
        x_lo, x_hi = x_grid[idx], x_grid[idx + 1]
        for _ in range(40):
            x_mid = 0.5 * (x_lo + x_hi)
            if weak_paper_payoff(x_mid, **kw) * weak_paper_payoff(x_lo, **kw) < 0:
                x_hi = x_mid
            else:
                x_lo = x_mid
        x_tip = 0.5 * (x_lo + x_hi)

    if   regime == 0: x_stable = 1.0
    elif regime == 1: x_stable = 0.0
    elif regime == 3: x_stable = x_tip
    else:             x_stable = np.nan

    return regime, x_stable, x_tip


# ─────────────────────────────────────────────────────────────────────────────
# 2.  Scenario definitions (two panels only)
# ─────────────────────────────────────────────────────────────────────────────

BASE = {
    'N': 1000, 'alpha': 0.2,
    'r': 100,  'c': 25,
    'lam': 0.1, 'epsilon': 0.05,
    'smoothness': 15,
}

AI_KW = dict(gamma=0.5, delta=0.1, phi=0.4, mu=0.2)

SCENARIOS = [
    ('Set A', 300, 400),
    ('Set B', 1200, 180),
]

A_VALS = np.linspace(0.0, 1.0, 120)

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'doc', 'tex', 'fig4_equilibrium_vs_a.pdf')
DATA_PATH   = os.path.join(DATA_DIR, 'fig4_data.json')

# ─────────────────────────────────────────────────────────────────────────────
# 3.  Compute
# ─────────────────────────────────────────────────────────────────────────────

def compute_data():
    results = []
    for (label, kr, ks) in SCENARIOS:
        regimes   = []
        x_stables = []
        x_tips    = []
        for a_val in A_VALS:
            reg, xs, xt = classify_and_find_equilibria(kr, ks, BASE, a_val, **AI_KW)
            regimes.append(reg)
            x_stables.append(xs)
            x_tips.append(xt)
        results.append({
            'label':    label,
            'kr':       kr,
            'ks':       ks,
            'regimes':  np.array(regimes, dtype=np.int32),
            'x_stables': np.array(x_stables),
            'x_tips':   np.array(x_tips),
        })
    return {'A_VALS': A_VALS, 'results': results}


# ─────────────────────────────────────────────────────────────────────────────
# 4.  Plot
# ─────────────────────────────────────────────────────────────────────────────

def plot(data):
    A_VALS_  = data['A_VALS']
    results  = data['results']

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.2), sharey=True)
    fig.subplots_adjust(wspace=0.08)

    panel_labels = [r'\textbf{(a)}', r'\textbf{(b)}']
    subtitles = [
        r'Set A',
        r'Set B',
    ]

    for col, rec in enumerate(results):
        ax = axes[col]
        regimes   = rec['regimes']
        x_stables = rec['x_stables']
        x_tips    = rec['x_tips']

        # ── Regime background strips ────────────────────────────────────────
        prev_reg = regimes[0]
        seg_start = A_VALS_[0]
        for i in range(1, len(A_VALS_)):
            if regimes[i] != prev_reg or i == len(A_VALS_) - 1:
                seg_end = A_VALS_[i]
                rc = BG_MAP.get(int(prev_reg), 'white')
                ax.axvspan(seg_start, seg_end, color=rc, alpha=0.12, zorder=0)
                # Regime label at top of strip
                ax.text(0.5 * (seg_start + seg_end), 1.03,
                        NAME_MAP.get(int(prev_reg), ''),
                        ha='center', va='bottom', fontsize=7,
                        color='#666666', transform=ax.get_xaxis_transform())
                seg_start = A_VALS_[i]
                prev_reg  = regimes[i]

        # ── Stable x* lines ────────────────────────────────────────────────
        mask_gh = (regimes == 0)
        mask_gc = (regimes == 1)
        mask_sc = (regimes == 3)

        if mask_gh.any():
            ax.plot(A_VALS_[mask_gh], x_stables[mask_gh],
                    color=C_GH, lw=2.0, label=r'$x^*=1$ (GH)')
        if mask_sc.any():
            ax.plot(A_VALS_[mask_sc], x_stables[mask_sc],
                    color=C_SC, lw=2.0, label=r'$x^*$ interior (SC)')
        if mask_gc.any():
            ax.plot(A_VALS_[mask_gc], x_stables[mask_gc],
                    color=C_GC, lw=2.0, label=r'$x^*=0$ (GC)')

        # ── Tipping threshold (BS) ─────────────────────────────────────────
        mask_bs = (regimes == 2)
        tips_bs = x_tips.copy()
        tips_bs[~mask_bs] = np.nan

        if not np.all(np.isnan(tips_bs)):
            ax.plot(A_VALS_, tips_bs,
                    color=C_TIP, lw=1.8, ls='--',
                    label=r'$x^*_{tip}$ (tipping threshold)')

        # ── Regime transition markers ──────────────────────────────────────
        for i in range(1, len(regimes)):
            if regimes[i] != regimes[i - 1]:
                a_tr = 0.5 * (A_VALS_[i - 1] + A_VALS_[i])
                ax.axvline(a_tr, color='#888888', lw=0.8, ls=':', alpha=0.7)

        # ── Labels and formatting ──────────────────────────────────────────
        ax.set_xlim(0, 1)
        ax.set_ylim(-0.05, 1.10)
        ax.set_xlabel(r'AI adoption $a$', fontsize=10)
        if col == 0:
            ax.set_ylabel(r'Honest-author share $x^*$', fontsize=10)

        ax.text(0.04, 0.96, panel_labels[col],
                transform=ax.transAxes, fontsize=11, va='top')
        ax.text(0.04, 0.87, subtitles[col],
                transform=ax.transAxes, fontsize=7.5, va='top',
                color='#444444')

        ax.legend(loc='center right', framealpha=0.92, fontsize=8)
        ax.tick_params(labelsize=9)

    # ─────────────────────────────────────────────────────────────────────────
    # 5.  Save
    # ─────────────────────────────────────────────────────────────────────────
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, bbox_inches='tight')
    print(f"Saved: {os.path.normpath(OUTPUT_PATH)}")


# ─────────────────────────────────────────────────────────────────────────────
# 6.  Main
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    recompute = '--recompute' in sys.argv
    if recompute or not os.path.exists(DATA_PATH):
        print("Computing data...")
        data = compute_data()
        save_data(data, DATA_PATH)
        print(f"Data saved: {DATA_PATH}")
    else:
        print(f"Loading cached data from {DATA_PATH}")
        data = load_data(DATA_PATH)
    plot(data)
