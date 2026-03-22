"""
Fig 9: Stochastic ABM validation of the ODE tipping result (Fig 7).

Built on ABM_batch_matching.py.  The key extension: at each time step t the
journal parameters are updated according to the current AI adoption level a_t,
so the ABM experiences the same rising-a trajectory shown in Fig 7(a).

At each step:
  K_rev_eff(a) = K_rev0 * (1 + delta*a) / (1 + gamma*a)   [net screening capacity]
  lambda_eff(a)= lam0 + mu * a                              [false-positive rate]
  c_eff(a)     = c0   * (1 - phi * a)                       [submission cost]

The volume scaling (1 + gamma*a) appears in the denominator of K_rev_eff because
AI raises submission volume faster than it raises review capacity; the effective
screening ratio therefore falls even if the absolute K_rev rises.

Panel (a): 30 ABM run-trajectories (thin, coloured by collapse outcome),
           mean ABM trajectory (bold blue), ODE prediction (bold black dashed),
           and tipping threshold x*(a_t) (red dashed).
           Stochastic fluctuations push some runs below the threshold before
           the ODE predicts collapse—earlier-than-expected tipping.

Panel (b): Fraction of the 30 runs that have collapsed (x < 0.3) as a function
           of a_t.  The ODE predicts a step function at the critical a; the ABM
           produces a smooth S-curve, showing that stochastic noise brings
           forward the effective tipping point.

N_RUNS = 30, N = 1000, batch_size = 50, beta = 1.0.
Set A: K_rev0=300, K=400, r=100, c0=25, lam0=0.1, eps=0.05.
AI:    gamma=0.5, delta=0.1, phi=0.4, mu=0.2.
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_io import save_data, load_data, DATA_DIR

# ── Fixed parameters ──────────────────────────────────────────────────────────
ALPHA      = 0.2
K_REV0     = 300.0
K_STORE    = 400.0
R          = 100.0
C0         = 25.0
LAM0       = 0.10
EPS        = 0.05
GAMMA      = 0.50
DELTA      = 0.10
PHI        = 0.40
MU         = 0.20

BETA       = 1.0
N_RUNS     = 30
T_TOTAL    = 3000
A_MAX      = 0.80
X0              = 0.82
COLLAPSE_THRESH = 0.30

N_LARGE     = 1000
N_SMALL     =  200
BATCH_LARGE =   50
BATCH_SMALL =   20

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'doc', 'tex', 'fig9_abm_validation.pdf')
DATA_PATH   = os.path.join(DATA_DIR, 'fig9_data.json')


# ── AI-extended effective parameters ─────────────────────────────────────────
def K_rev_eff(a):
    return K_REV0 * (1 + DELTA * a) / (1 + GAMMA * a)

def lam_eff(a):
    return LAM0 + MU * a

def c_eff(a):
    return C0 * (1 - PHI * a)


# ── ODE tipping-threshold finder ──────────────────────────────────────────────
def Pi_bad_ode(x, a):
    Krev = K_rev_eff(a)
    lam  = lam_eff(a)
    c    = c_eff(a)
    V    = N_LARGE * (1 - (1 - ALPHA) * x)
    eta  = min(1.0, Krev / V) if V > 0 else 1.0
    pi0  = 1 - eta * (1 - lam)
    pi1  = 1 - eta * EPS
    M    = (1 + GAMMA * a) * (N_LARGE * ALPHA * pi1 + N_LARGE * (1 - ALPHA) * (1 - x) * pi0)
    rho  = min(1.0, K_STORE / M) if M > 0 else 1.0
    return R * rho * pi0 - c

def find_threshold(a, tol=1e-5):
    if not (Pi_bad_ode(1.0, a) < 0 and Pi_bad_ode(0.0, a) > 0):
        return None
    lo, hi = 1e-4, 1 - 1e-4
    for _ in range(80):
        mid = (lo + hi) / 2
        if Pi_bad_ode(mid, a) > 0:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return (lo + hi) / 2


# ── ODE trajectory (mean-field prediction) ───────────────────────────────────
def ode_trajectory(a_series):
    x = X0
    traj = []
    dt_ode = 0.02
    for t in range(T_TOTAL):
        traj.append(x)
        pb = Pi_bad_ode(x, a_series[t])
        dx = -x * (1 - x) * (1 - ALPHA) * pb * dt_ode
        x  = float(np.clip(x + dx, 0.0, 1.0))
    return np.array(traj)


# ── AI-extended ABM ─────────────────────────────────────────────────────────
def run_abm_with_ai(a_schedule, x0=X0, N_pop=N_LARGE, batch_size=BATCH_LARGE, beta=BETA):
    n_steps = len(a_schedule)
    scale   = batch_size / N_pop

    K_rev_base = K_REV0 * (N_pop / N_LARGE)
    K_sto_base = K_STORE * (N_pop / N_LARGE)

    n_og     = int(x0 * N_pop)
    pop      = np.array([1] * n_og + [0] * (N_pop - n_og), dtype=np.int8)
    history  = []

    for t in range(n_steps):
        history.append(np.mean(pop))

        a_t = a_schedule[t]

        K_rev_loc = (K_rev_base * (1 + DELTA * a_t) / (1 + GAMMA * a_t)) * scale
        K_sto_loc = K_sto_base * scale
        lam       = lam_eff(a_t)
        c         = c_eff(a_t)

        payoffs = np.zeros(N_pop)

        idx_perm = np.random.permutation(N_pop)
        for i in range(0, N_pop, batch_size):
            b_idx = idx_perm[i:i + batch_size]
            b_pop = pop[b_idx]

            n_og_b = int(np.sum(b_pop))
            n_as_b = batch_size - n_og_b

            V_loc = n_og_b * ALPHA + n_as_b * 1.0
            eta   = min(1.0, K_rev_loc / V_loc) if V_loc > 0 else 1.0
            pi1   = 1 - eta * EPS
            pi0   = 1 - eta * (1 - lam)

            M_loc = (1 + GAMMA * a_t) * (
                n_og_b * ALPHA * pi1
                + n_as_b * (ALPHA * pi1 + (1 - ALPHA) * pi0)
            )
            rho   = min(1.0, K_sto_loc / M_loc) if M_loc > 0 else 1.0

            Pi_good = R * rho * pi1 - c
            Pi_bad_ = R * rho * pi0 - c
            u_og    = ALPHA * Pi_good
            u_as    = ALPHA * Pi_good + (1 - ALPHA) * Pi_bad_

            for agent, strat in zip(b_idx, b_pop):
                payoffs[agent] = u_og if strat == 1 else u_as

        n_rev  = max(1, int(0.02 * N_pop))
        focal  = np.random.choice(N_pop, n_rev, replace=False)
        models = np.random.choice(N_pop, n_rev, replace=True)

        for f, m in zip(focal, models):
            if pop[f] != pop[m]:
                diff  = payoffs[m] - payoffs[f]
                p_sw  = 1.0 / (1.0 + np.exp(-beta * diff))
                if np.random.random() < p_sw:
                    pop[f] = pop[m]

    return np.array(history)


# ── Compute ───────────────────────────────────────────────────────────────────

def compute_data():
    np.random.seed(42)
    a_series = np.linspace(0.0, A_MAX, T_TOTAL)

    print("Computing ODE trajectory…")
    ode_traj = ode_trajectory(a_series)
    thresh_curve = np.array([find_threshold(a) or np.nan for a in a_series])

    print(f"Running {N_RUNS} ABM replications — N={N_LARGE}…")
    runs_large = []
    for run_i in range(N_RUNS):
        traj = run_abm_with_ai(a_series, N_pop=N_LARGE, batch_size=BATCH_LARGE)
        runs_large.append(traj)
        if (run_i + 1) % 10 == 0:
            print(f"  {run_i + 1}/{N_RUNS}")
    runs_large = np.array(runs_large)

    print(f"Running {N_RUNS} ABM replications — N={N_SMALL}…")
    runs_small = []
    for run_i in range(N_RUNS):
        traj = run_abm_with_ai(a_series, N_pop=N_SMALL, batch_size=BATCH_SMALL)
        runs_small.append(traj)
        if (run_i + 1) % 10 == 0:
            print(f"  {run_i + 1}/{N_RUNS}")
    runs_small = np.array(runs_small)

    print("All ABM runs complete.")

    mean_large = runs_large.mean(axis=0)
    mean_small = runs_small.mean(axis=0)
    frac_large = (runs_large < COLLAPSE_THRESH).mean(axis=0)
    frac_small = (runs_small < COLLAPSE_THRESH).mean(axis=0)

    a_crit_ode = None
    for a_val in a_series:
        xt = find_threshold(a_val)
        if xt is not None and xt > X0:
            a_crit_ode = float(a_val)
            break

    return {
        'a_series':    a_series,
        'ode_traj':    ode_traj,
        'thresh_curve':thresh_curve,
        'runs_large':  runs_large,
        'runs_small':  runs_small,
        'mean_large':  mean_large,
        'mean_small':  mean_small,
        'frac_large':  frac_large,
        'frac_small':  frac_small,
        'a_crit_ode':  a_crit_ode,
    }


# ── Plot ──────────────────────────────────────────────────────────────────────

def plot(data):
    a_series    = data['a_series']
    ode_traj    = data['ode_traj']
    thresh_curve= data['thresh_curve']
    runs_large  = data['runs_large']
    runs_small  = data['runs_small']
    mean_large  = data['mean_large']
    mean_small  = data['mean_small']
    frac_large  = data['frac_large']
    frac_small  = data['frac_small']
    a_crit_ode  = data['a_crit_ode']

    fig = plt.figure(figsize=(13, 6.5))
    gs  = gridspec.GridSpec(1, 2, figure=fig, wspace=0.38)

    # ─── Panel A: trajectories for N=200 (small sub-field) ───────────────────────
    ax1  = fig.add_subplot(gs[0])
    ax1b = ax1.twinx()

    steps = np.arange(T_TOTAL)

    for run in runs_small:
        col = '#d62728' if run[-1] < COLLAPSE_THRESH else '#1f77b4'
        ax1.plot(steps, run, color=col, alpha=0.20, linewidth=0.7)

    ax1.plot(steps, mean_small, color='steelblue', linewidth=2.2,
             label=fr'Mean ABM ($N={N_SMALL}$, sub-field)', zorder=4)
    ax1.plot(steps, mean_large, color='forestgreen', linewidth=2.0,
             linestyle='--', label=fr'Mean ABM ($N={N_LARGE}$, full field)', zorder=4)

    ax1.plot(steps, ode_traj, color='black', linewidth=1.8, linestyle=':',
             label='ODE (mean-field, $N\\to\\infty$)', zorder=5)

    ax1.plot(steps, thresh_curve, color='crimson', linewidth=1.8, linestyle='-.',
             label=r'Tipping threshold $x^*(a_t)$', zorder=5)

    ax1b.plot(steps, a_series, color='darkorange', linewidth=1.2,
              linestyle=':', alpha=0.65, label=r'AI adoption $a_t$')

    custom = [Patch(color='#1f77b4', alpha=0.5, label=f'$N={N_SMALL}$ run → honesty'),
              Patch(color='#d62728', alpha=0.5, label=f'$N={N_SMALL}$ run → collapse')]
    lines1, lab1 = ax1.get_legend_handles_labels()
    lines2, lab2 = ax1b.get_legend_handles_labels()
    ax1.legend(handles=custom + lines1 + lines2,
               bbox_to_anchor=(0.5, -0.22), loc='upper center',
               bbox_transform=ax1.transAxes, ncol=3,
               fontsize=7.8, framealpha=0.93)

    ax1.set_xlabel('Time step', fontsize=11)
    ax1.set_ylabel(r'Honest-author share $x_t$', color='steelblue', fontsize=10)
    ax1b.set_ylabel(r'AI adoption level $a_t$', color='darkorange', fontsize=10)
    ax1.set_ylim(-0.05, 1.13)
    ax1b.set_ylim(-0.05, 1.13)
    ax1.tick_params(axis='y', labelcolor='steelblue')
    ax1b.tick_params(axis='y', labelcolor='darkorange')
    ax1.set_title(fr'(a) ABM trajectories vs ODE — starting at $x_0={X0}$'
                  '\n(30 runs per community size)',
                  fontsize=10, pad=7)
    ax1.grid(True, alpha=0.2)

    # ─── Panel B: collapse fraction — N=200 vs N=1000 ────────────────────────────
    ax2 = fig.add_subplot(gs[1])

    ax2.plot(a_series, frac_small, color='steelblue', linewidth=2.2,
             label=fr'$N={N_SMALL}$ (sub-field, 30 runs)')
    ax2.fill_between(a_series, frac_small, alpha=0.15, color='steelblue')

    ax2.plot(a_series, frac_large, color='forestgreen', linewidth=2.0,
             linestyle='--', label=fr'$N={N_LARGE}$ (full field, 30 runs)')
    ax2.fill_between(a_series, frac_large, alpha=0.12, color='forestgreen')

    if a_crit_ode is not None:
        ax2.axvline(a_crit_ode, color='black', linestyle='--', linewidth=1.8,
                    label=fr'ODE: $x^*(a)$ crosses $x_0$ at $a^*={a_crit_ode:.2f}$')
        ax2.text(a_crit_ode + 0.01, 0.50,
                 'ODE\npredicts\nvulnerability', fontsize=8, color='black', va='center')

    ax2.set_xlabel(r'AI adoption level $a$', fontsize=11)
    ax2.set_ylabel(f'Fraction of {N_RUNS} runs collapsed ($x < 0.3$)', fontsize=10)
    ax2.set_ylim(-0.03, 1.08)
    ax2.set_xlim(0.0, A_MAX)
    ax2.legend(fontsize=9, loc='upper left', framealpha=0.93)
    ax2.set_title('(b) Small communities collapse earlier:\n'
                  'stochastic noise advances the tipping point',
                  fontsize=10, pad=7)
    ax2.grid(True, alpha=0.2)

    fig.suptitle(
        fr'Fig. 9 — Stochastic ABM validation: $N={N_SMALL}$ sub-fields tip earlier than the'
        '\n'
        r'ODE predicts; $N=1000$ fields are more robust — both confirm the tipping mechanism'
        r'  ($\gamma=0.5$, $\delta=0.1$, $\phi=0.4$, $\mu=0.2$; Set A)',
        fontsize=10.5, y=1.02
    )

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.18)
    plt.savefig(OUTPUT_PATH, bbox_inches='tight')
    print("fig9 saved.")


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
