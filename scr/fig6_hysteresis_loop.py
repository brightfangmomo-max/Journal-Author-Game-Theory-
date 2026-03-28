"""
Figure 6: Hysteresis loop -- collapse and recovery thresholds

Classic fold-bifurcation diagram showing that collapse (increasing a) happens
at a higher threshold than recovery (decreasing a), creating a hysteresis gap.

Two panels contrast:
  (a) N = 300  -- low pressure.  Full GH -> BS -> GC transition;
      clear recovery threshold exists.
  (b) N = 600  -- high pressure.  System starts in BS at a = 0;
      no recovery is possible by reducing a alone.

Output: fig6_hysteresis_loop.pdf in doc/tex/
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
C_UP  = '#4477AA'   # honest stable branch (blue)
C_LO  = '#EE6677'   # corrupt stable branch (red)
C_TIP = '#EE7733'   # unstable tipping threshold (orange)
C_GH  = '#44BB99'   # GH background (Paul Tol Light)
C_BS  = '#EEDD88'   # BS background
C_GC  = '#EE8866'   # GC background
ALPHA_BG = 0.15

# ── Base parameters (Set A) ──────────────────────────────────────────────────
ALPHA = 0.2
K_REV = 300.0
K     = 400.0
R     = 100.0
C0    = 25.0
LAM0  = 0.1
EPS   = 0.05
GAMMA = 0.5
DELTA = 0.1
PHI   = 0.4
MU    = 0.2
K_SMOOTH = 60

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'doc', 'tex', 'fig6_hysteresis_loop.pdf')
DATA_PATH   = os.path.join(DATA_DIR, 'fig6_data.json')


# ── Model functions ──────────────────────────────────────────────────────────

def soft_min(a, b):
    with np.errstate(over='ignore', invalid='ignore'):
        return -np.log(np.exp(-K_SMOOTH * a) + np.exp(-K_SMOOTH * b)) / K_SMOOTH


def pibad(x, a_ai, N):
    """Weak-paper payoff Pi_bad(x, a, N)."""
    K_rev_a = K_REV * (1.0 + DELTA * a_ai)
    c_a     = C0   * (1.0 - PHI   * a_ai)
    lam_a   = LAM0 + MU * a_ai

    V   = N * (1.0 - (1.0 - ALPHA) * x) * (1.0 + GAMMA * a_ai)
    eta = np.clip(soft_min(1.0, K_rev_a / V), 0.0, 1.0)
    pi0 = 1.0 - eta * (1.0 - lam_a)
    pi1 = 1.0 - eta * EPS

    M   = (1.0 + GAMMA * a_ai) * (N * ALPHA * pi1 + N * (1.0 - ALPHA) * (1.0 - x) * pi0)
    rho = np.clip(soft_min(1.0, K / M), 0.0, 1.0)
    return R * rho * pi0 - c_a


def compute_branches(N, a_vals, n_pts=5000):
    uppers   = np.full(len(a_vals), np.nan)
    lowers   = np.full(len(a_vals), np.nan)
    tippings = np.full(len(a_vals), np.nan)

    x_grid = np.linspace(0.005, 0.995, n_pts)

    for i, a in enumerate(a_vals):
        pb1 = float(pibad(0.999, a, N))
        pb0 = float(pibad(0.001, a, N))

        if pb1 < 0.0:
            uppers[i] = 1.0
        if pb0 > 0.0:
            lowers[i] = 0.0

        pb = pibad(x_grid, a, N)
        sc = np.where(np.diff(np.sign(pb)))[0]
        for idx in sc:
            p1, p2 = pb[idx], pb[idx + 1]
            if p2 == p1:
                continue
            x_root = x_grid[idx] - p1 * (x_grid[idx + 1] - x_grid[idx]) / (p2 - p1)
            if p1 > 0 and p2 < 0:
                tippings[i] = x_root

    return uppers, lowers, tippings


def find_threshold_a(N, a_vals, boundary):
    """
    Find stability thresholds.
      boundary = 'upper' -> first a where x=1 loses stability (collapse threshold a_col)
      boundary = 'lower' -> recovery threshold a_rec: scan from HIGH a downward
                             to find the first a where x=0 loses stability.
                             If x=0 is stable at all a (including a=0), return NaN.
    """
    if boundary == 'upper':
        for a in a_vals:
            if pibad(0.999, a, N) >= 0.0:
                return float(a)
        return np.nan
    else:
        if pibad(0.001, a_vals[0], N) >= 0.0:
            for a in a_vals:
                if pibad(0.001, a, N) < 0.0:
                    for a2 in a_vals:
                        if pibad(0.001, a2, N) >= 0.0:
                            return float(a2)
            return np.nan
        else:
            for a in a_vals:
                if pibad(0.001, a, N) >= 0.0:
                    return float(a)
            return np.nan


# ── Compute ──────────────────────────────────────────────────────────────────

def compute_data():
    a_vals = np.linspace(0.0, 0.70, 700)
    panels = []
    for N in [300, 600]:
        uppers, lowers, tippings = compute_branches(N, a_vals)
        a_col = find_threshold_a(N, a_vals, boundary='upper')
        a_rec = find_threshold_a(N, a_vals, boundary='lower')
        panels.append({
            'N':        N,
            'a_vals':   a_vals,
            'uppers':   uppers,
            'lowers':   lowers,
            'tippings': tippings,
            'a_col':    a_col,
            'a_rec':    a_rec,
        })
    return {'panels': panels}


# ── Drawing ──────────────────────────────────────────────────────────────────

def draw_panel(ax, panel):
    N        = panel['N']
    a_vals   = panel['a_vals']
    uppers   = panel['uppers']
    lowers   = panel['lowers']
    tippings = panel['tippings']
    a_col    = panel['a_col']
    a_rec    = panel['a_rec']

    a_min, a_max = a_vals[0], a_vals[-1]

    # ── Background regime shading ──
    has_rec = not np.isnan(a_rec)
    has_col = not np.isnan(a_col)

    if has_rec and has_col:
        ax.axvspan(a_min, a_rec, alpha=ALPHA_BG, color=C_GH, zorder=0)
        ax.axvspan(a_rec, a_col, alpha=ALPHA_BG, color=C_BS, zorder=0)
        ax.axvspan(a_col, a_max, alpha=ALPHA_BG, color=C_GC, zorder=0)
        ax.text((a_min + a_rec) / 2, 1.05, 'GH', ha='center', fontsize=7,
                color='#666666', transform=ax.get_xaxis_transform())
        ax.text((a_rec + a_col) / 2, 1.05, 'BS', ha='center', fontsize=7,
                color='#666666', transform=ax.get_xaxis_transform())
        ax.text((a_col + a_max) / 2, 1.05, 'GC', ha='center', fontsize=7,
                color='#666666', transform=ax.get_xaxis_transform())
    elif not has_rec and has_col:
        ax.axvspan(a_min, a_col, alpha=ALPHA_BG, color=C_BS, zorder=0)
        ax.axvspan(a_col, a_max, alpha=ALPHA_BG, color=C_GC, zorder=0)
        ax.text((a_min + a_col) / 2, 1.05, 'BS', ha='center', fontsize=7,
                color='#666666', transform=ax.get_xaxis_transform())
        ax.text((a_col + a_max) / 2, 1.05, 'GC', ha='center', fontsize=7,
                color='#666666', transform=ax.get_xaxis_transform())
    else:
        ax.axvspan(a_min, a_max, alpha=ALPHA_BG, color=C_GC, zorder=0)
        ax.text(0.5, 1.05, 'GC', ha='center', fontsize=7,
                color='#666666', transform=ax.get_xaxis_transform())

    # ── Stable branches ──
    ax.plot(a_vals, uppers, color=C_UP, lw=2.2, solid_capstyle='round', zorder=3)
    ax.plot(a_vals, lowers, color=C_LO, lw=2.2, solid_capstyle='round', zorder=3)

    # ── Unstable tipping branch ──
    ax.plot(a_vals, tippings, color=C_TIP, lw=1.8, ls='--', zorder=4)

    # ── Vertical threshold reference lines ──
    if has_col:
        ax.axvline(a_col, color=C_UP, lw=0.7, ls=':', alpha=0.5, zorder=2)
    if has_rec:
        ax.axvline(a_rec, color=C_LO, lw=0.7, ls=':', alpha=0.5, zorder=2)

    # ── Collapse jump arrow (shortened, thin) ──
    if has_col:
        # Find the tipping value at a_col for arrow start
        idx_col = np.argmin(np.abs(a_vals - a_col))
        tip_val = tippings[idx_col] if not np.isnan(tippings[idx_col]) else 0.85
        ax.annotate('',
                    xy=(a_col, 0.03), xytext=(a_col, tip_val),
                    arrowprops=dict(arrowstyle='->', color=C_UP,
                                   lw=0.8, mutation_scale=8),
                    zorder=5)

    # ── Recovery jump arrow (shortened, thin; only if recovery exists) ──
    if has_rec:
        idx_rec = np.argmin(np.abs(a_vals - a_rec))
        tip_val = tippings[idx_rec] if not np.isnan(tippings[idx_rec]) else 0.15
        ax.annotate('',
                    xy=(a_rec, 0.97), xytext=(a_rec, tip_val),
                    arrowprops=dict(arrowstyle='->', color=C_LO,
                                   lw=0.8, mutation_scale=8),
                    zorder=5)

    # ── Threshold labels ──
    if has_col:
        ax.text(a_col + 0.01, 0.50,
                rf'$a_{{\rm col}}={a_col:.2f}$',
                fontsize=8, color=C_UP, va='center')
    if has_rec:
        ax.text(a_rec + 0.01, 0.50,
                rf'$a_{{\rm rec}}={a_rec:.2f}$',
                fontsize=8, color=C_LO, va='center')

    # ── Axes formatting ──
    ax.set_xlim(a_vals[0], a_vals[-1])
    ax.set_ylim(-0.05, 1.12)
    ax.set_xlabel(r'AI adoption $a$', fontsize=10)
    ax.set_yticks([0.0, 0.25, 0.50, 0.75, 1.0])
    ax.tick_params(labelsize=9)


def plot(data):
    panels = data['panels']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.4),
                                    gridspec_kw={'wspace': 0.28})

    draw_panel(ax1, panels[0])
    ax1.set_ylabel(r'Honest-author share $x^*$', fontsize=10)
    ax1.text(0.04, 0.96, r'\textbf{(a)}', transform=ax1.transAxes,
             fontsize=11, va='top')
    ax1.text(0.04, 0.87, rf'Low pressure ($N={panels[0]["N"]}$)',
             transform=ax1.transAxes, fontsize=8, va='top', color='#444444')

    draw_panel(ax2, panels[1])
    ax2.set_ylabel('')
    ax2.text(0.04, 0.96, r'\textbf{(b)}', transform=ax2.transAxes,
             fontsize=11, va='top')
    ax2.text(0.04, 0.87, rf'High pressure ($N={panels[1]["N"]}$)',
             transform=ax2.transAxes, fontsize=8, va='top', color='#444444')

    # ── Legend inside panel (a) ──
    legend_handles = [
        Line2D([0], [0], color=C_UP, lw=2.2,
               label=r'Stable: honest ($x^*\!=1$)'),
        Line2D([0], [0], color=C_LO, lw=2.2,
               label=r'Stable: corrupt ($x^*\!=0$)'),
        Line2D([0], [0], color=C_TIP, lw=1.8, ls='--',
               label=r'Unstable threshold'),
    ]
    ax1.legend(handles=legend_handles, loc='lower left',
               fontsize=7.5, framealpha=0.92)

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, bbox_inches='tight')
    print(f'Saved: {os.path.normpath(OUTPUT_PATH)}')


# ── Main ─────────────────────────────────────────────────────────────────────

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
