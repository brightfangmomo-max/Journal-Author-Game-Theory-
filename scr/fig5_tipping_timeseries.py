"""
Figure 5: Tipping dynamics under rising AI adoption

Panel (a) — Shrinking safety margin + shock asymmetry
  The tipping threshold x*(a_t) rises silently toward the population.
  An identical shock applied early (large safety margin) vs late (small
  margin) produces opposite outcomes: recovery vs collapse.

Panel (b) — Path dependence
  At fixed a=0.45 (bistable regime), two trajectories starting just above /
  just below x*(0.45) diverge to opposite absorbing states.

Set A: N=1000, alpha=0.2, K_rev=300, K=400, r=100, c=25, lam0=0.1, eps=0.05
AI:   gamma=0.5, delta=0.1, phi=0.4, mu=0.2

Output: fig5_tipping_timeseries.pdf in doc/tex/
"""

import os
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

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
C_THRESHOLD = '#EE6677'   # tipping threshold (red)
C_RECOVER   = '#228833'   # recovery trajectory / above threshold (green)
C_COLLAPSE  = '#4477AA'   # collapse trajectory / below threshold (blue)
C_AI        = '#EE7733'   # AI adoption curve (orange)
C_THRESH_PD = '#111111'   # threshold line in panel b

# ── Parameters ────────────────────────────────────────────────────────────────
N      = 1000
alpha  = 0.2
K_rev0 = 300.0
K      = 400.0
r      = 100.0
c0     = 25.0
lam0   = 0.10
eps    = 0.05
gamma  = 0.50
delta  = 0.10
phi    = 0.40
mu     = 0.20

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'doc', 'tex', 'fig5_tipping_timeseries.pdf')
DATA_PATH   = os.path.join(DATA_DIR, 'fig5_data.json')


def Pi_bad(x, a):
    K_rev = K_rev0 * (1 + delta * a)
    lam   = lam0 + mu * a
    c     = c0 * (1 - phi * a)
    V     = N * (1 - (1 - alpha) * x) * (1 + gamma * a)
    eta   = min(1.0, K_rev / V) if V > 0 else 1.0
    pi0   = 1 - eta * (1 - lam)
    pi1   = 1 - eta * eps
    M     = (1 + gamma * a) * (N * alpha * pi1 + N * (1 - alpha) * (1 - x) * pi0)
    rho   = min(1.0, K / M) if M > 0 else 1.0
    return r * rho * pi0 - c


def dx_step(x, a, dt=0.02):
    return float(np.clip(x - x*(1-x)*(1-alpha)*Pi_bad(x, a)*dt, 0.0, 1.0))


def find_threshold(a, tol=1e-5):
    if not (Pi_bad(1.0, a) < 0 and Pi_bad(0.0, a) > 0):
        return None
    lo, hi = 1e-4, 1-1e-4
    for _ in range(80):
        mid = (lo+hi)/2
        if Pi_bad(mid, a) > 0:
            lo = mid
        else:
            hi = mid
        if hi-lo < tol:
            break
    return (lo+hi)/2


# ── Simulation parameters ────────────────────────────────────────────────────
T_total     = 3000
a_max       = 0.80
dt_sim      = 0.02
SHOCK_SIZE  = 0.18
SHOCK_EARLY = 300
SHOCK_LATE  = 2000
a_pd        = 0.45
T2          = 1200
dt2         = 0.05


# ── Compute ──────────────────────────────────────────────────────────────────

def compute_data():
    a_series    = np.linspace(0.0, a_max, T_total)
    thresh_at_t = np.array([find_threshold(a) or np.nan for a in a_series])

    def simulate(shock_step):
        x = 1.0
        xs = []
        for t in range(T_total):
            if t == shock_step:
                x = max(0.0, x - SHOCK_SIZE)
            xs.append(x)
            x = dx_step(x, a_series[t], dt=dt_sim)
        return np.array(xs)

    traj_early = simulate(SHOCK_EARLY)
    traj_late  = simulate(SHOCK_LATE)

    x_pd = find_threshold(a_pd)
    if x_pd is None:
        x_pd = 0.85

    def run_pd(x0):
        traj = []
        x = x0
        for _ in range(T2):
            traj.append(x)
            x = dx_step(x, a_pd, dt=dt2)
        return np.array(traj)

    traj_above = run_pd(x_pd + 0.04)
    traj_below = run_pd(x_pd - 0.04)

    return {
        'a_series':    a_series,
        'thresh_at_t': thresh_at_t,
        'traj_early':  traj_early,
        'traj_late':   traj_late,
        'a_pd':        float(a_pd),
        'x_pd':        float(x_pd),
        'traj_above':  traj_above,
        'traj_below':  traj_below,
        'SHOCK_SIZE':  float(SHOCK_SIZE),
        'SHOCK_EARLY': int(SHOCK_EARLY),
        'SHOCK_LATE':  int(SHOCK_LATE),
        'T_total':     int(T_total),
        'T2':          int(T2),
    }


# ── Plot ─────────────────────────────────────────────────────────────────────

def plot(data):
    a_series     = data['a_series']
    thresh_at_t  = data['thresh_at_t']
    traj_early   = data['traj_early']
    traj_late    = data['traj_late']
    a_pd_        = data['a_pd']
    x_pd_        = data['x_pd']
    traj_above   = data['traj_above']
    traj_below   = data['traj_below']
    SHOCK_SIZE_  = data['SHOCK_SIZE']
    SHOCK_EARLY_ = data['SHOCK_EARLY']
    SHOCK_LATE_  = data['SHOCK_LATE']
    T_total_     = data['T_total']
    T2_          = data['T2']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.2))
    fig.subplots_adjust(wspace=0.35)

    steps = np.arange(T_total_)

    # ─── Panel A: shock asymmetry ─────────────────────────────────────────────
    ax1.plot(steps, thresh_at_t, color=C_THRESHOLD, linewidth=1.8,
             linestyle='--', label=r'Tipping threshold $x^*(a_t)$', zorder=3)

    ax1.plot(steps, traj_early, color=C_RECOVER, linewidth=1.5, alpha=0.9,
             label=r'Early shock $\to$ recovers')
    ax1.plot(steps, traj_late, color=C_COLLAPSE, linewidth=1.5, alpha=0.9,
             label=r'Late shock $\to$ collapses')

    # Shock arrows
    for t_shock, color, traj in [(SHOCK_EARLY_, C_RECOVER, traj_early),
                                  (SHOCK_LATE_,  C_COLLAPSE, traj_late)]:
        ax1.annotate('', xy=(t_shock, traj[t_shock]),
                     xytext=(t_shock, traj[t_shock] + SHOCK_SIZE_),
                     arrowprops=dict(arrowstyle='->', color=color, lw=1.3))

    # AI adoption on secondary axis (kept minimal)
    ax1b = ax1.twinx()
    ax1b.plot(steps, a_series, color=C_AI, linewidth=1.0,
              linestyle=':', alpha=0.6, label=r'$a_t$')
    ax1b.set_ylabel(r'AI adoption $a_t$', fontsize=9, color=C_AI, alpha=0.7)
    ax1b.set_ylim(-0.05, 1.05)
    ax1b.tick_params(axis='y', labelcolor=C_AI, labelsize=8, colors=C_AI)
    ax1b.spines['right'].set_visible(True)
    ax1b.spines['right'].set_color(C_AI)
    ax1b.spines['right'].set_alpha(0.4)

    # Safety margin annotation
    ann_t = int(T_total_ * 0.55)
    ann_y = thresh_at_t[ann_t]
    if not np.isnan(ann_y):
        ax1.annotate(
            'Safety margin\nnarrows',
            xy=(ann_t, ann_y),
            xytext=(ann_t + 400, ann_y - 0.25),
            fontsize=7.5, color=C_THRESHOLD, ha='left',
            arrowprops=dict(arrowstyle='->', color=C_THRESHOLD, lw=0.9)
        )

    ax1.set_xlabel('Time step', fontsize=10)
    ax1.set_ylabel(r'Honest-author share $x_t$', fontsize=10)
    ax1.set_ylim(-0.05, 1.08)
    ax1.tick_params(labelsize=9)

    # Combined legend
    lines1, lab1 = ax1.get_legend_handles_labels()
    lines2, lab2 = ax1b.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, lab1 + lab2, fontsize=7.5, framealpha=0.92,
               loc='lower left')

    ax1.text(0.03, 0.97, r'\textbf{(a)}', transform=ax1.transAxes,
             fontsize=11, va='top')

    # ─── Panel B: path dependence ─────────────────────────────────────────────
    pd_steps = np.arange(T2_)

    ax2.plot(pd_steps, traj_above, color=C_RECOVER, linewidth=2.0,
             label=rf'$x_0={x_pd_+0.04:.2f}$ (above $x^*$)')
    ax2.plot(pd_steps, traj_below, color=C_COLLAPSE, linewidth=2.0,
             label=rf'$x_0={x_pd_-0.04:.2f}$ (below $x^*$)')
    ax2.axhline(x_pd_, color=C_THRESH_PD, linestyle='--', linewidth=1.2,
                alpha=0.6, label=rf'$x^*\approx{x_pd_:.2f}$')

    ax2.set_xlabel('Time step', fontsize=10)
    ax2.set_ylabel(r'Honest-author share $x_t$', fontsize=10)
    ax2.set_ylim(-0.05, 1.08)
    ax2.tick_params(labelsize=9)
    ax2.legend(fontsize=7.5, loc='center right', framealpha=0.92)

    ax2.text(0.03, 0.97, r'\textbf{(b)}', transform=ax2.transAxes,
             fontsize=11, va='top')
    ax2.text(0.03, 0.78, rf'Path dependence at $a={a_pd_}$',
             transform=ax2.transAxes, fontsize=7.5, color='#444444', va='top')

    # ─────────────────────────────────────────────────────────────────────────
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, bbox_inches='tight')
    print(f"Saved: {os.path.normpath(OUTPUT_PATH)}")


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
