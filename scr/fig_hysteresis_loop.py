"""
fig_hysteresis_loop.py

Classic fold-bifurcation (hysteresis loop) diagram.

Two panels contrast:
  (a) N = 300  -- low submission pressure.  Full GH → BS → GC transition
      visible in a-space; a clear recovery threshold exists.
  (b) N = 600  -- high submission pressure.  System starts in Bistability
      at a = 0; no recovery is possible by reducing a alone.

Each panel shows:
  - Upper stable branch  x* = 1  (honest norm self-sustaining)
  - Lower stable branch  x* = 0  (corrupt norm self-sustaining)
  - Unstable tipping threshold  x*_tip(a)  (dashed)
  - Forward path arrow  (increasing a → collapse at a_col)
  - Backward path arrow (decreasing a → recovery at a_rec, or absent)
  - Regime-coloured background (GH green, BS yellow, GC red)

Output: doc/tex/fig_hysteresis_loop.pdf

Parameters follow Set A baseline with AI-extension (gamma, delta, phi, mu).
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_io import save_data, load_data, DATA_DIR

# ── Base parameters (Set A) ──────────────────────────────────────────────────
ALPHA = 0.2
K_REV = 300.0
K     = 400.0
R     = 100.0
C0    = 25.0
LAM0  = 0.1
EPS   = 0.05

# AI-extension elasticities
GAMMA = 0.5   # production elasticity   (γ)
DELTA = 0.1   # verification elasticity (δ < γ)
PHI   = 0.4   # cost-reduction slope    (φ)
MU    = 0.2   # false-positive slope    (μ)

K_SMOOTH = 60  # soft-min sharpness (higher → closer to hard min)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'doc', 'tex', 'fig_hysteresis_loop.pdf')
DATA_PATH   = os.path.join(DATA_DIR, 'fig_hysteresis_loop_data.json')


# ── Model functions ───────────────────────────────────────────────────────────

def soft_min(a, b):
    """Numerically stable smooth approximation of min(a, b)."""
    with np.errstate(over='ignore', invalid='ignore'):
        return -np.log(np.exp(-K_SMOOTH * a) + np.exp(-K_SMOOTH * b)) / K_SMOOTH


def pibad(x, a_ai, N):
    """
    Spam payoff Π_bad(x, a, N) under the AI extension.

    Parameters
    ----------
    x    : float or ndarray  -- honest-author share in [0, 1]
    a_ai : float             -- AI adoption level in [0, 1]
    N    : float             -- author population
    """
    K_rev_a = K_REV * (1.0 + DELTA * a_ai)
    c_a     = C0   * (1.0 - PHI   * a_ai)
    lam_a   = LAM0 + MU    * a_ai

    V   = N * (1.0 - (1.0 - ALPHA) * x) * (1.0 + GAMMA * a_ai)
    eta = np.clip(soft_min(1.0, K_rev_a / V), 0.0, 1.0)
    pi0 = 1.0 - eta * (1.0 - lam_a)
    pi1 = 1.0 - eta * EPS

    M   = (1.0 + GAMMA * a_ai) * (N * ALPHA * pi1 + N * (1.0 - ALPHA) * (1.0 - x) * pi0)
    rho = np.clip(soft_min(1.0, K / M), 0.0, 1.0)
    return R * rho * pi0 - c_a


def compute_branches(N, a_vals, n_pts=5000):
    """
    For every a in a_vals return three arrays:
      uppers   -- 1.0 where x=1 is stable, else nan
      lowers   -- 0.0 where x=0 is stable, else nan
      tippings -- interior unstable x* where it exists, else nan
    """
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

        # Interior roots: scan for sign changes in Π_bad(x)
        pb = pibad(x_grid, a, N)
        sc = np.where(np.diff(np.sign(pb)))[0]
        for idx in sc:
            p1, p2 = pb[idx], pb[idx + 1]
            if p2 == p1:
                continue
            x_root = x_grid[idx] - p1 * (x_grid[idx + 1] - x_grid[idx]) / (p2 - p1)
            # Unstable if Π_bad goes + → − as x rises
            if p1 > 0 and p2 < 0:
                tippings[i] = x_root

    return uppers, lowers, tippings


def find_threshold_a(N, a_vals, boundary):
    """
    Return the first a at which a boundary equilibrium changes stability.
      boundary = 'upper' → first a where x=1 loses stability (Π_bad(1) ≥ 0)
      boundary = 'lower' → first a where x=0 becomes stable  (Π_bad(0) ≥ 0)
    """
    for a in a_vals:
        if boundary == 'upper':
            if pibad(0.999, a, N) >= 0.0:
                return float(a)
        else:
            if pibad(0.001, a, N) >= 0.0:
                return float(a)
    return np.nan


# ── Compute ───────────────────────────────────────────────────────────────────

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


# ── Plotting ──────────────────────────────────────────────────────────────────

def draw_panel(ax, panel):
    """Draw one bifurcation panel."""
    N        = panel['N']
    a_vals   = panel['a_vals']
    uppers   = panel['uppers']
    lowers   = panel['lowers']
    tippings = panel['tippings']
    a_col    = panel['a_col']
    a_rec    = panel['a_rec']

    # ── Colour scheme ──
    C_UP  = '#2166ac'   # blue  – honest stable branch
    C_LO  = '#c0392b'   # red   – corrupt stable branch
    C_TIP = '#e67e22'   # orange – unstable tipping threshold
    C_GH  = '#91cf60'
    C_BS  = '#fee08b'
    C_GC  = '#fc8d59'
    ALPHA_BG = 0.18

    # ── Background regime shading ──
    a_min, a_max = a_vals[0], a_vals[-1]
    if not np.isnan(a_rec) and not np.isnan(a_col):
        ax.axvspan(a_min, a_rec, alpha=ALPHA_BG, color=C_GH, zorder=0)
        ax.axvspan(a_rec, a_col, alpha=ALPHA_BG, color=C_BS, zorder=0)
        ax.axvspan(a_col, a_max, alpha=ALPHA_BG, color=C_GC, zorder=0)
    elif np.isnan(a_rec) and not np.isnan(a_col):
        ax.axvspan(a_min, a_col, alpha=ALPHA_BG, color=C_BS, zorder=0)
        ax.axvspan(a_col, a_max, alpha=ALPHA_BG, color=C_GC, zorder=0)
    else:
        ax.axvspan(a_min, a_max, alpha=ALPHA_BG, color=C_GC, zorder=0)

    # ── Stable branches ──
    ax.plot(a_vals, uppers,   color=C_UP,  lw=2.6, solid_capstyle='round', zorder=3)
    ax.plot(a_vals, lowers,   color=C_LO,  lw=2.6, solid_capstyle='round', zorder=3)

    # ── Unstable tipping branch ──
    ax.plot(a_vals, tippings, color=C_TIP, lw=2.0, ls='--', zorder=4)

    # ── Vertical threshold reference lines ──
    if not np.isnan(a_col):
        ax.axvline(a_col, color=C_UP, lw=0.9, ls=':', alpha=0.65, zorder=2)
    if not np.isnan(a_rec):
        ax.axvline(a_rec, color=C_LO, lw=0.9, ls=':', alpha=0.65, zorder=2)

    # ── Collapse jump arrow (forward path hits a_col → drops) ──
    if not np.isnan(a_col):
        ax.annotate('',
                    xy=(a_col, 0.05), xytext=(a_col, 0.93),
                    arrowprops=dict(arrowstyle='->', color=C_UP,
                                   lw=1.6, mutation_scale=14),
                    zorder=5)

    # ── Recovery jump arrow (backward path hits a_rec → rises) ──
    if not np.isnan(a_rec):
        ax.annotate('',
                    xy=(a_rec, 0.95), xytext=(a_rec, 0.05),
                    arrowprops=dict(arrowstyle='->', color=C_LO,
                                   lw=1.6, mutation_scale=14),
                    zorder=5)

    # ── Horizontal path-direction arrows ──
    if not np.isnan(a_col):
        mid_fwd = min(a_col * 0.55, a_col - 0.05)
        ax.annotate('', xy=(mid_fwd + 0.07, 1.0), xytext=(mid_fwd, 1.0),
                    arrowprops=dict(arrowstyle='->', color='#333333', lw=1.3),
                    zorder=5)
        ax.text(mid_fwd + 0.035, 1.035, 'forward $\\to$',
                fontsize=7.5, color='#333333', ha='center', va='bottom')

    if not np.isnan(a_rec):
        mid_bwd = a_rec + (a_col - a_rec) * 0.5
        ax.annotate('', xy=(mid_bwd - 0.07, 0.0), xytext=(mid_bwd, 0.0),
                    arrowprops=dict(arrowstyle='->', color='#333333', lw=1.3),
                    zorder=5)
        ax.text(mid_bwd - 0.035, -0.055, '$\\leftarrow$ backward',
                fontsize=7.5, color='#333333', ha='center', va='top')

    # ── Threshold labels ──
    if not np.isnan(a_col):
        ax.text(a_col + 0.012, 0.50,
                f'$a_{{\\rm col}}={a_col:.2f}$',
                fontsize=8.5, color=C_UP, va='center', style='italic')
    if not np.isnan(a_rec):
        ax.text(a_rec + 0.012, 0.50,
                f'$a_{{\\rm rec}}={a_rec:.2f}$',
                fontsize=8.5, color=C_LO, va='center', style='italic')

    # ── Hysteresis gap bracket for panel (a) ──
    if not np.isnan(a_rec) and not np.isnan(a_col):
        gap = a_col - a_rec
        y_brk = -0.14
        ax.annotate('', xy=(a_col, y_brk), xytext=(a_rec, y_brk),
                    arrowprops=dict(arrowstyle='<->', color='#555555',
                                   lw=1.3, mutation_scale=10),
                    zorder=5)
        ax.text((a_rec + a_col) / 2, y_brk - 0.07,
                f'hysteresis gap $\\Delta a = {gap:.2f}$',
                fontsize=8.5, ha='center', color='#444444')

    # ── No-recovery annotation for panel (b) ──
    if np.isnan(a_rec):
        ax.text(0.20, -0.14,
                'No GH phase: reducing $a$ alone cannot restore honesty.',
                fontsize=8.2, ha='center', color='#8b0000',
                style='italic', zorder=5)

    # ── Axes formatting ──
    ax.set_xlim(a_vals[0], a_vals[-1])
    ax.set_ylim(-0.25, 1.18)
    ax.set_xlabel('AI adoption $a$', fontsize=11)
    ax.set_ylabel('Long-run honest-author share $x^*$', fontsize=11)
    ax.set_yticks([0.0, 0.25, 0.50, 0.75, 1.0])
    ax.set_yticklabels(['0\n(corrupt)', '0.25', '0.50', '0.75', '1.0\n(honest)'],
                       fontsize=8.5)
    ax.grid(True, alpha=0.20, ls='--')
    ax.tick_params(axis='x', labelsize=9)


def plot(data):
    panels = data['panels']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 5.6),
                                    gridspec_kw={'wspace': 0.30})

    draw_panel(ax1, panels[0])
    ax1.set_title(f'(a) Low-pressure field ($N={panels[0]["N"]}$)', fontsize=11, pad=12)
    ax1.set_ylabel('Long-run honest-author share $x^*$', fontsize=11)

    draw_panel(ax2, panels[1])
    ax2.set_title(f'(b) High-pressure field ($N={panels[1]["N"]}$)', fontsize=11, pad=12)
    ax2.set_ylabel('')

    # ── Shared legend ──
    legend_handles = [
        Line2D([0], [0], color='#2166ac', lw=2.6,
               label='Stable: honest ($x^*=1$)'),
        Line2D([0], [0], color='#c0392b', lw=2.6,
               label='Stable: corrupt ($x^*=0$)'),
        Line2D([0], [0], color='#e67e22', lw=2.0, ls='--',
               label='Unstable tipping threshold $x^*_{\\rm tip}$'),
        mpatches.Patch(facecolor='#91cf60', alpha=0.55,
                       label='GH: honesty self-restoring'),
        mpatches.Patch(facecolor='#fee08b', alpha=0.55,
                       label='BS: history determines outcome'),
        mpatches.Patch(facecolor='#fc8d59', alpha=0.55,
                       label='GC: corruption self-sustaining'),
    ]
    fig.legend(handles=legend_handles,
               loc='lower center', bbox_to_anchor=(0.5, -0.08),
               ncol=3, fontsize=9.5, framealpha=0.95,
               columnspacing=1.2, handlelength=2.0)

    plt.tight_layout(rect=[0, 0.08, 1, 1])

    # ── Save ──
    plt.savefig(OUTPUT_PATH, bbox_inches='tight')
    print(f'Saved: {os.path.normpath(OUTPUT_PATH)}')
    plt.show()


# ── Main ──────────────────────────────────────────────────────────────────────

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
