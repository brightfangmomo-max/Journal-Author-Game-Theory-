"""
Figure 5: Stable equilibrium x*(a) as AI adoption rises

For each level of AI adoption a ∈ [0, 1], we trace the stable long-run
outcome for the share of honest authors x*.

Three scenario tracks are shown:
  Track A  — Set A parameters (K_rev=300, K=400): prone to bistability.
             x* = 1 while GH holds; once the system crosses into BS the
             reported value is the UNSTABLE tipping threshold x*_tip (dashed),
             because the stable outcome is the absorbing state x=1 on the high
             side and x=0 on the low side.  We show both:
               – the tipping threshold x*_tip (marks how fragile the system is)
               – the collapse point (a at which GH → BS, marked by a vertical line)

  Track B  — Set B parameters (K_rev=1200, K=180): prone to stable coexistence.
             x* is the interior stable equilibrium (blue region).

  Track C  — Intermediate (K_rev=500, K=300): shows transition from GH through
             BS to GC as a rises, with the tipping threshold x*_tip traced.

For each a value:
  • The regime is classified from the boundary payoffs.
  • If regime == GH: stable x* = 1.
  • If regime == SC: find interior root of Π_bad(x,a)=0 (stable one).
  • If regime == BS: find interior root of Π_bad(x,a)=0 (unstable tipping
    threshold x*_tip).  The stable outcomes are x=1 and x=0.
  • If regime == GC: stable x* = 0.
  • If regime == NS: x* = NaN.

Output: fig5_equilibrium_vs_a.pdf in doc/tex/
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_io import save_data, load_data, DATA_DIR

# ─────────────────────────────────────────────────────────────────────────────
# 1.  Model core
# ─────────────────────────────────────────────────────────────────────────────
def soft_min(u, v, k=15):
    return -np.log(np.exp(-k * u) + np.exp(-k * v)) / k


def pi_bad(x, K_rev, K_store, p, a,
           gamma=0.5, delta=0.1, phi=0.4, mu=0.2):
    """Spam payoff Π_bad(x, a) — scalar or array in x."""
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
    Return (regime, x_stable, x_tip) where:
      regime   : 0=GH, 1=GC, 2=BS, 3=SC, 4=NS
      x_stable : the stable x* (1 for GH, 0 for GC, interior for SC, NaN for NS)
      x_tip    : interior zero of Π_bad (unstable in BS, stable in SC), NaN otherwise
    """
    kw = dict(K_rev=K_rev, K_store=K_store, p=p, a=a,
              gamma=gamma, delta=delta, phi=phi, mu=mu)

    Pb1  = pi_bad(0.999, **kw)
    Pb0  = pi_bad(0.001, **kw)

    # Participation constraint
    k_     = p.get('smoothness', 15)
    c_eff  = p['c'] * (1.0 - phi * a)
    lam_e  = min(p['lam'] + mu * a, 0.99)
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
        return 4, np.nan, np.nan    # NS

    one_stable  = Pb1 < 0
    zero_stable = Pb0 > 0

    if   one_stable and not zero_stable:
        regime = 0   # GH
    elif not one_stable and zero_stable:
        regime = 1   # GC
    elif one_stable and zero_stable:
        regime = 2   # BS
    else:
        regime = 3   # SC

    # ── Find interior root of Π_bad(x)=0 by bisection ────────────────────────
    x_tip = np.nan
    x_grid = np.linspace(0.005, 0.995, 2000)
    vals   = pi_bad(x_grid, **kw)
    sign_c = np.where(np.diff(np.sign(vals)))[0]

    if len(sign_c) > 0:
        for idx in sign_c:
            x_lo, x_hi = x_grid[idx], x_grid[idx + 1]
            for _ in range(40):
                x_mid = 0.5 * (x_lo + x_hi)
                if pi_bad(x_mid, **kw) * pi_bad(x_lo, **kw) < 0:
                    x_hi = x_mid
                else:
                    x_lo = x_mid
            candidate = 0.5 * (x_lo + x_hi)
            x_tip = candidate
            break   # first (lowest-x) root

    # Stable x*
    if   regime == 0: x_stable = 1.0
    elif regime == 1: x_stable = 0.0
    elif regime == 3: x_stable = x_tip   # SC: interior is stable
    else:             x_stable = np.nan  # BS: both boundaries stable; show x_tip separately

    return regime, x_stable, x_tip


# ─────────────────────────────────────────────────────────────────────────────
# 2.  Scenario definitions
# ─────────────────────────────────────────────────────────────────────────────
BASE = {
    'N': 1000, 'alpha': 0.2,
    'r': 100,  'c': 25,
    'lam': 0.1, 'epsilon': 0.05,
    'smoothness': 15,
}

AI_KW = dict(gamma=0.5, delta=0.1, phi=0.4, mu=0.2)

SCENARIOS = [
    # (label, K_rev, K_store, color_regime, marker)
    ('Set A  ($K_{rev}=300,\\ K=400$)\nBistability-prone',
     300, 400, '#E8733A', 's'),
    ('Set B  ($K_{rev}=1200,\\ K=180$)\nCoexistence-prone',
     1200, 180, '#3A7EC8', 'o'),
    ('Intermediate  ($K_{rev}=500,\\ K=300$)',
     500, 300, '#6A3AC8', '^'),
]

A_VALS = np.linspace(0.0, 1.0, 120)

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'doc', 'tex', 'fig5_equilibrium_vs_a.pdf')
DATA_PATH   = os.path.join(DATA_DIR, 'fig5_data.json')

# ─────────────────────────────────────────────────────────────────────────────
# 3.  Compute
# ─────────────────────────────────────────────────────────────────────────────

def compute_data():
    results = []
    for (label, kr, ks, color, marker) in SCENARIOS:
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
            'color':    color,
            'marker':   marker,
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

    REGIME_COLORS = {0: '#98FB98', 1: '#FFB6C1', 2: '#FFE4B5', 3: '#ADD8E6', 4: '#D3D3D3'}
    REGIME_NAMES  = {0: 'GH', 1: 'GC', 2: 'BS', 3: 'SC', 4: 'NS'}

    fig, axes = plt.subplots(1, 3, figsize=(15, 5.2), sharey=True,
                              constrained_layout=True)

    for ax, rec in zip(axes, results):
        label    = rec['label']
        regimes  = rec['regimes']
        x_stables= rec['x_stables']
        x_tips   = rec['x_tips']

        # ── Regime background strip ───────────────────────────────────────────────
        prev_reg = regimes[0]
        seg_start = A_VALS_[0]
        for i in range(1, len(A_VALS_)):
            if regimes[i] != prev_reg or i == len(A_VALS_) - 1:
                seg_end = A_VALS_[i]
                rc = REGIME_COLORS.get(int(prev_reg), 'white')
                ax.axvspan(seg_start, seg_end, color=rc, alpha=0.25, zorder=0)
                ax.text(0.5 * (seg_start + seg_end), 0.03,
                        REGIME_NAMES.get(int(prev_reg), '?'),
                        ha='center', va='bottom', fontsize=8,
                        color='gray', transform=ax.get_xaxis_transform())
                seg_start = A_VALS_[i]
                prev_reg  = regimes[i]

        # ── Stable x* line ────────────────────────────────────────────────────────
        mask_gh = (regimes == 0)
        mask_gc = (regimes == 1)
        mask_sc = (regimes == 3)

        if mask_gh.any():
            ax.plot(A_VALS_[mask_gh], x_stables[mask_gh],
                    color='#2E8B57', lw=2.5, label=r'$x^*=1$ (GH stable)')
        if mask_sc.any():
            ax.plot(A_VALS_[mask_sc], x_stables[mask_sc],
                    color='#3A7EC8', lw=2.5, label=r'$x^*$ interior (SC stable)')
        if mask_gc.any():
            ax.plot(A_VALS_[mask_gc], x_stables[mask_gc],
                    color='#C83A3A', lw=2.5, label=r'$x^*=0$ (GC stable)')

        # ── Tipping-point / BS interior x*_tip ───────────────────────────────────
        mask_bs   = (regimes == 2)
        tips_plot = x_tips.copy()
        tips_plot[~(mask_bs | mask_sc)] = np.nan
        tips_bs   = tips_plot.copy()
        tips_bs[~mask_bs] = np.nan

        if not np.all(np.isnan(tips_bs)):
            ax.plot(A_VALS_, tips_bs,
                    color='#FF8C00', lw=2.0, ls='--',
                    label=r'$x^*_{tip}$ (BS tipping threshold)')

        # ── Vertical marker at regime-transition points ───────────────────────────
        for i in range(1, len(regimes)):
            if regimes[i] != regimes[i - 1]:
                a_tr = 0.5 * (A_VALS_[i - 1] + A_VALS_[i])
                ax.axvline(a_tr, color='gray', lw=1.0, ls=':', alpha=0.8)
                ax.text(a_tr + 0.01, 0.55,
                        f'{regimes[i - 1]}→{regimes[i]}',
                        fontsize=7.5, color='gray',
                        transform=ax.get_xaxis_transform(),
                        rotation=90, va='center')

        # ── Decorations ───────────────────────────────────────────────────────────
        ax.set_xlim(0, 1)
        ax.set_ylim(-0.05, 1.10)
        ax.set_xlabel(r'AI adoption intensity  $a$', fontsize=11)
        if ax is axes[0]:
            ax.set_ylabel(r'Honest-author share at long-run outcome  $x^*$', fontsize=11)
        ax.set_title(label, fontsize=10.5, pad=7)
        ax.grid(True, alpha=0.25, ls='--')
        ax.legend(loc='lower left', framealpha=0.92, prop={'size': 11, 'weight': 'bold'})

        box_txt = (r'$\gamma=0.5,\ \delta=0.1$' '\n'
                   r'$\phi=0.4,\ \mu=0.2$')
        ax.text(0.97, 0.97, box_txt, transform=ax.transAxes,
                fontsize=8, va='top', ha='right',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor='gray', alpha=0.85))

    fig.suptitle(
        r'Fig. 5  ·  Long-run honest-author share $x^*(a)$ as AI adoption rises',
        fontsize=13, fontweight='bold'
    )

    # ─────────────────────────────────────────────────────────────────────────────
    # 5.  Save
    # ─────────────────────────────────────────────────────────────────────────────
    plt.savefig(OUTPUT_PATH, dpi=300, bbox_inches='tight')
    print(f"Saved → {os.path.normpath(OUTPUT_PATH)}")
    plt.show()


# ─────────────────────────────────────────────────────────────────────────────
# 6.  Main
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    recompute = '--recompute' in sys.argv
    if recompute or not os.path.exists(DATA_PATH):
        print("Computing data...")
        data = compute_data()
        save_data(data, DATA_PATH)
        print(f"Data saved → {DATA_PATH}")
    else:
        print(f"Loading cached data from {DATA_PATH}")
        data = load_data(DATA_PATH)
    plot(data)
