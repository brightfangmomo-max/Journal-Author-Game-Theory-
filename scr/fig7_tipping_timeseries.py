"""
Fig 7: Two-panel figure illustrating the tipping dynamics under rising AI adoption.

Panel (a) — Shrinking safety margin + shock asymmetry
  x_t ≈ 1 throughout (honest norm holds), while the tipping threshold x*(a_t)
  rises silently toward the population. A sudden shock (a coordinated wave of
  low-quality submissions, modelled as a one-time drop in x) is applied TWICE:
    - Early shock  (low a, large safety margin) → system recovers
    - Late shock   (high a, small safety margin) → system collapses
  Identical shock magnitude; radically different long-run outcomes.

Panel (b) — Path dependence
  At a fixed a=0.45 (bistable regime), two trajectories starting just above /
  just below x*(0.45) diverge to opposite absorbing states.

Set A: N=1000, alpha=0.2, K_rev=300, K=400, r=100, c=25, lam0=0.1, eps=0.05
AI:   gamma=0.5, delta=0.1, phi=0.4, mu=0.2
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

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

def Pi_bad(x, a):
    K_rev = K_rev0 * (1 + delta * a)
    lam   = lam0 + mu * a
    c     = c0 * (1 - phi * a)
    V     = N * (1 - (1 - alpha) * x) * (1 + gamma * a)
    eta   = min(1.0, K_rev / V) if V > 0 else 1.0
    pi0   = 1 - eta * (1 - lam)
    pi1   = 1 - eta * eps
    M     = N * alpha * pi1 + N * (1 - alpha) * (1 - x) * pi0
    rho   = min(1.0, K / M) if M > 0 else 1.0
    return r * rho * pi0 - c

def dx_step(x, a, dt=0.02):
    return float(np.clip(x - x*(1-x)*(1-alpha)*Pi_bad(x,a)*dt, 0.0, 1.0))

def find_threshold(a, tol=1e-5):
    if not (Pi_bad(1.0, a) < 0 and Pi_bad(0.0, a) > 0):
        return None
    lo, hi = 1e-4, 1-1e-4
    for _ in range(80):
        mid = (lo+hi)/2
        (lo if Pi_bad(mid,a)>0 else hi).__class__  # dummy
        if Pi_bad(mid, a) > 0:
            lo = mid
        else:
            hi = mid
        if hi-lo < tol:
            break
    return (lo+hi)/2

# ── Pre-compute x*(a) curve ───────────────────────────────────────────────────
a_vals  = np.linspace(0.0, 0.80, 300)
x_star  = np.array([find_threshold(a) or np.nan for a in a_vals])

# ── Panel A simulation parameters ────────────────────────────────────────────
T_total  = 3000
a_max    = 0.80
dt_sim   = 0.02
a_series = np.linspace(0.0, a_max, T_total)

SHOCK_SIZE  = 0.18    # magnitude of x drop (same in both cases)
SHOCK_EARLY = 300     # time step of early shock (a ≈ 0.08)
SHOCK_LATE  = 2000    # time step of late shock  (a ≈ 0.53)

def simulate(shock_step, label):
    x = 1.0
    xs = []
    for t in range(T_total):
        if t == shock_step:
            x = max(0.0, x - SHOCK_SIZE)
        xs.append(x)
        x = dx_step(x, a_series[t], dt=dt_sim)
    return np.array(xs)

traj_early = simulate(SHOCK_EARLY, 'early')
traj_late  = simulate(SHOCK_LATE,  'late')

# Map a-values → time steps for threshold overlay
thresh_at_t = np.array([find_threshold(a) or np.nan for a in a_series])

# ── Panel B: path dependence ──────────────────────────────────────────────────
a_pd   = 0.45
x_pd   = find_threshold(a_pd)
if x_pd is None:
    x_pd = 0.85

T2 = 1200
dt2 = 0.05

def run_pd(x0):
    traj = []
    x = x0
    for _ in range(T2):
        traj.append(x)
        x = dx_step(x, a_pd, dt=dt2)
    return np.array(traj)

traj_above = run_pd(x_pd + 0.04)
traj_below = run_pd(x_pd - 0.04)

# ── Plotting ──────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(13, 6.2))
gs  = gridspec.GridSpec(1, 2, figure=fig, wspace=0.38)

# ─── Panel A ──────────────────────────────────────────────────────────────────
ax1  = fig.add_subplot(gs[0])
ax1b = ax1.twinx()

steps = np.arange(T_total)

ax1.plot(steps, thresh_at_t, color='crimson', linewidth=2.0,
         linestyle='--', label=r'Tipping threshold $x^*(a_t)$', zorder=3)

ax1.plot(steps, traj_early, color='forestgreen', linewidth=1.8, alpha=0.9,
         label=fr'Early shock (t={SHOCK_EARLY}, $a\approx{a_series[SHOCK_EARLY]:.2f}$) → recovers')
ax1.plot(steps, traj_late, color='steelblue', linewidth=1.8, alpha=0.9,
         label=fr'Late shock  (t={SHOCK_LATE},  $a\approx{a_series[SHOCK_LATE]:.2f}$) → collapses')

ax1b.plot(steps, a_series, color='darkorange', linewidth=1.3,
          linestyle=':', alpha=0.75, label=r'AI adoption $a_t$')

# Mark shock events
for t_shock, color, traj in [(SHOCK_EARLY,'forestgreen',traj_early),
                               (SHOCK_LATE, 'steelblue',  traj_late)]:
    ax1.annotate('', xy=(t_shock, traj[t_shock]),
                 xytext=(t_shock, traj[t_shock]+SHOCK_SIZE),
                 arrowprops=dict(arrowstyle='->', color=color, lw=1.5))

lines1, lab1 = ax1.get_legend_handles_labels()
lines2, lab2 = ax1b.get_legend_handles_labels()
ax1.legend(lines1+lines2, lab1+lab2, fontsize=8.2, framealpha=0.93,
           bbox_to_anchor=(0.5, -0.22), loc='upper center',
           bbox_transform=ax1.transAxes, ncol=2)

ax1.set_xlabel('Time step', fontsize=11)
ax1.set_ylabel(r'Honest-author share $x_t$', color='steelblue', fontsize=10)
ax1b.set_ylabel(r'AI adoption level $a_t$', color='darkorange', fontsize=10)
ax1.set_ylim(-0.05, 1.13)
ax1b.set_ylim(-0.05, 1.13)
ax1.tick_params(axis='y', labelcolor='steelblue')
ax1b.tick_params(axis='y', labelcolor='darkorange')
ax1.set_title(r'(a) Same shock, different timing: the system grows fragile silently',
              fontsize=10, pad=7)
ax1.grid(True, alpha=0.22)

# Safety-margin annotation — arrow tip lands exactly on the red dashed line
ann_t = int(T_total * 0.60)   # t=1800, a≈0.48, threshold clearly visible
ann_y = thresh_at_t[ann_t]
ax1.annotate(
    'Safety margin\nnarrows',
    xy=(ann_t, ann_y),
    xytext=(ann_t + 480, ann_y - 0.22),
    fontsize=8, color='crimson', ha='left',
    arrowprops=dict(arrowstyle='->', color='crimson', lw=1.1)
)

# ─── Panel B ──────────────────────────────────────────────────────────────────
ax2 = fig.add_subplot(gs[1])
pd_steps = np.arange(T2)

ax2.plot(pd_steps, traj_above, color='forestgreen', linewidth=2.2,
         label=fr'$x_0={x_pd+0.04:.2f}$ (above $x^*$) $\to$ full honesty')
ax2.plot(pd_steps, traj_below, color='crimson', linewidth=2.2,
         label=fr'$x_0={x_pd-0.04:.2f}$ (below $x^*$) $\to$ collapse')
ax2.axhline(x_pd, color='black', linestyle='--', linewidth=1.5, alpha=0.7,
            label=fr'Tipping threshold $x^*\approx{x_pd:.2f}$')

ax2.set_xlabel('Time step', fontsize=11)
ax2.set_ylabel(r'Honest-author share $x_t$', fontsize=11)
ax2.set_ylim(-0.05, 1.13)
ax2.legend(fontsize=8.5, loc='center right', framealpha=0.92)
ax2.set_title(fr'(b) Path dependence at $a={a_pd}$: identical shock size, opposite outcomes',
              fontsize=10, pad=7)
ax2.grid(True, alpha=0.22)

fig.suptitle(
    r'Fig. 7 — AI adoption silently erodes the stability window;'
    r' a fixed-size shock becomes irreversible once the tipping threshold rises'
    '\n'
    r'($\gamma=0.5,\;\delta=0.1,\;\phi=0.4,\;\mu=0.2$; Set A)',
    fontsize=10.5, y=1.02
)

plt.tight_layout()
plt.subplots_adjust(bottom=0.18)
plt.savefig('doc/tex/fig7_tipping_timeseries.pdf', bbox_inches='tight')
print("fig7 saved.")