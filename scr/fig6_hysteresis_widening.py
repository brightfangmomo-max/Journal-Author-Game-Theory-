"""
Figure 6: How AI adoption erodes the stability window and shifts collapse thresholds

Two-panel figure:

Left panel — Regime map in (N, a) space
    X-axis: population size N (external submission pressure)
    Y-axis: AI adoption intensity a ∈ [0, 1]
    Color:  regime (GH/BS/SC/GC/NS)
    Overlaid curves:
        Red solid:  N_up(a)  — largest N where GH or BS holds (collapse boundary)
        Blue dashed: N_lo(a) — smallest N where BS begins (lower BS boundary)
    Key result: as a rises, N_up(a) falls (collapse arrives sooner) and the
    bistable window [N_lo, N_up] shrinks and vanishes.

Right panel — Collapse threshold N_up(a) and quality at equilibrium
    X-axis: AI adoption a
    Y-axis (left): N_up(a) — collapse threshold
    Y-axis (right, twin): equilibrium quality Q* at N=500 (moderate pressure)
    Shows the continuous erosion of resilience as a increases, even before
    the system reaches the tipping point.

Set A parameters: K_rev=300, K=400, r=100, c=25, λ₀=0.1, ε=0.05
AI parameters:    γ=0.5, δ=0.1, φ=0.4, μ=0.2
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

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


def equilibrium_quality(N, K_rev, K_store, p, a,
                         gamma=0.5, delta=0.1, phi=0.4, mu=0.2):
    """
    Compute equilibrium quality Q* on the FORWARD (honest-start) path.
    Use the highest stable x:
      GH → x=1, BS → x=1 (forward), SC → interior root, GC → x=0, NS → NaN
    """
    kw = dict(N=N, K_rev=K_rev, K_store=K_store, p=p, a=a,
              gamma=gamma, delta=delta, phi=phi, mu=mu)
    reg = classify(**kw)

    if reg == 4:
        return np.nan
    elif reg == 0 or reg == 2:   # GH or BS: forward path stays at x=1
        x_eq = 1.0
    elif reg == 1:                # GC
        x_eq = 0.0
    else:                         # SC: find interior root
        xs   = np.linspace(0.005, 0.995, 600)
        vals = np.array([payoffs(x, **kw)[0] for x in xs])
        sc   = np.where(np.diff(np.sign(vals)))[0]
        if len(sc) == 0:
            x_eq = 0.5
        else:
            xl, xh = xs[sc[0]], xs[sc[0]+1]
            for _ in range(35):
                xm = 0.5*(xl+xh)
                if payoffs(xm, **kw)[0] * payoffs(xl, **kw)[0] < 0:
                    xh = xm
                else:
                    xl = xm
            x_eq = 0.5*(xl+xh)

    # Quality Q = fraction of good papers in the accepted pool
    pb, _  = payoffs(x_eq, **kw)
    c_eff  = p['c'] * (1.0 - phi * a)
    lam_e  = min(p['lam'] + mu * a, 0.99)
    vol_m  = 1.0 + gamma * a
    krev_m = 1.0 + delta * a
    k_     = p.get('smoothness', 15)
    V      = N * (1.0 - (1.0 - p['alpha']) * x_eq) * vol_m
    Kr     = K_rev * krev_m
    eta    = np.clip(soft_min(1.0, Kr / V, k_), 0.0, 1.0)
    p0     = 1.0 - eta * (1.0 - lam_e)
    p1     = 1.0 - eta * p['epsilon']
    VG     = N * p['alpha'] * vol_m
    VB     = N * (1.0 - p['alpha']) * (1.0 - x_eq) * vol_m
    pass_G = VG * p1
    pass_B = VB * p0
    denom  = pass_G + pass_B
    if denom < 1e-9:
        return np.nan
    return pass_G / denom


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

# ─────────────────────────────────────────────────────────────────────────────
# 3.  Build (N, a) phase map
# ─────────────────────────────────────────────────────────────────────────────
N_grid = np.linspace(50, 2500, 220)
A_grid = np.linspace(0.0, 1.0, 150)

print("Computing (N, a) phase map …")
phase_map = np.zeros((len(A_grid), len(N_grid)), dtype=np.int8)
for i, a_v in enumerate(A_grid):
    for j, N_v in enumerate(N_grid):
        phase_map[i, j] = classify(N_v, KR, KS, BASE, a_v, **AI)
print("Done.")

# ─────────────────────────────────────────────────────────────────────────────
# 4.  Compute N_up(a) and N_lo(a) from phase map
#     N_up(a): upper edge of GH-or-BS (last N where forward path is x=1)
#     N_lo(a): lower edge of BS zone (smallest N where BS appears)
# ─────────────────────────────────────────────────────────────────────────────
N_up_curve = np.full(len(A_grid), np.nan)
N_lo_curve = np.full(len(A_grid), np.nan)

for i in range(len(A_grid)):
    row = phase_map[i, :]
    # N_up: largest N where regime is 0 (GH) or 2 (BS)
    stable_honest = np.where((row == 0) | (row == 2))[0]
    if len(stable_honest) > 0:
        N_up_curve[i] = N_grid[stable_honest[-1]]
    # N_lo: smallest N where regime is 2 (BS)
    bs_idx = np.where(row == 2)[0]
    if len(bs_idx) > 0:
        N_lo_curve[i] = N_grid[bs_idx[0]]

# ─────────────────────────────────────────────────────────────────────────────
# 5.  Compute Q*(a) at fixed N=500 (quality erosion with AI)
# ─────────────────────────────────────────────────────────────────────────────
A_line  = np.linspace(0.0, 1.0, 80)
N_fixed = 500

print("Computing equilibrium quality Q*(a) at N=500 …")
Q_curve = np.array([
    equilibrium_quality(N_fixed, KR, KS, BASE, a_v, **AI)
    for a_v in A_line
])
print("Done.")

# Also compute x*(a) at N=500 for reference
print("Computing regime at N=500 across a …")
reg_at_N500 = np.array([classify(N_fixed, KR, KS, BASE, a_v, **AI)
                         for a_v in A_line])
print("Done.")

# ─────────────────────────────────────────────────────────────────────────────
# 6.  Plot
# ─────────────────────────────────────────────────────────────────────────────
COLORS = ['#98FB98', '#FFB6C1', '#FFE4B5', '#ADD8E6', '#D3D3D3']
CMAP   = ListedColormap(COLORS)

fig = plt.figure(figsize=(15, 6.0))
gs  = gridspec.GridSpec(1, 2, figure=fig, wspace=0.30, width_ratios=[1.2, 1])

# ── Left: (N, a) phase map ────────────────────────────────────────────────────
ax_map = fig.add_subplot(gs[0, 0])
ax_map.imshow(phase_map, origin='lower', aspect='auto', cmap=CMAP,
              vmin=0, vmax=4,
              extent=[N_grid.min(), N_grid.max(), A_grid.min(), A_grid.max()])

# N_up(a) boundary
valid = ~np.isnan(N_up_curve)
ax_map.plot(N_up_curve[valid], A_grid[valid],
            'r-', lw=2.4, label=r'$N_\uparrow(a)$: collapse boundary')

# N_lo(a) boundary (lower BS edge)
valid2 = ~np.isnan(N_lo_curve)
ax_map.plot(N_lo_curve[valid2], A_grid[valid2],
            'b--', lw=1.8, label=r'$N_{lo}(a)$: lower BS boundary')

# Regime labels
ax_map.text(150,  0.05, 'GH', fontsize=12, color='#1A6B22', fontweight='bold')
ax_map.text(950,  0.10, 'BS', fontsize=12, color='#6B5000', fontweight='bold')
ax_map.text(1900, 0.07, 'SC', fontsize=12, color='#1A4080', fontweight='bold')
ax_map.text(800,  0.78, 'GC', fontsize=12, color='#8B0000', fontweight='bold')

# Annotate N_up shrinkage
a0_up = N_up_curve[0]  if not np.isnan(N_up_curve[0])  else np.nan
a5_up = N_up_curve[int(0.5*len(A_grid))] if len(A_grid) > int(0.5*len(A_grid)) else np.nan
if not np.isnan(a0_up):
    ax_map.annotate(f'$N_\\uparrow(0)\\approx{a0_up:.0f}$',
                    xy=(a0_up, 0.0), xytext=(a0_up-300, 0.12),
                    fontsize=9, color='darkred',
                    arrowprops=dict(arrowstyle='->', color='darkred', lw=1.2))

ax_map.set_xlabel('Population size  $N$', fontsize=12)
ax_map.set_ylabel('AI adoption  $a$', fontsize=12)
ax_map.set_title('(a)  Regime map in $(N,\\,a)$ space\n'
                 r'Red curve: collapse boundary $N_\uparrow(a)$ falls as $a$ rises',
                 fontsize=11, pad=8, fontweight='bold')
ax_map.legend(fontsize=9.5, loc='upper right', framealpha=0.92)

# ── Right: N_up(a) and Q*(a) ──────────────────────────────────────────────────
ax_r = fig.add_subplot(gs[0, 1])

# --- N_up(a) on primary axis ---
ax_r.plot(A_grid[valid], N_up_curve[valid],
          'r-', lw=2.5, label=r'$N_\uparrow(a)$: collapse threshold')

# Shade the area below N_up(a) = "safe zone"
ax_r.fill_between(A_grid[valid], 0, N_up_curve[valid],
                   color='#98FB98', alpha=0.22,
                   label='Stable-honesty region (forward path)')

ax_r.set_xlabel('AI adoption  $a$', fontsize=12)
ax_r.set_ylabel(r'Collapse threshold  $N_\uparrow(a)$', fontsize=12, color='darkred')
ax_r.tick_params(axis='y', labelcolor='darkred')
ax_r.set_xlim(0, 1)
ax_r.set_ylim(0, N_grid.max() * 1.05)
ax_r.grid(True, alpha=0.22, ls='--')

# --- Q*(a) at N=500 on twin axis ---
ax_q = ax_r.twinx()
# Color segments by regime
REGIME_CLR = {0:'#2E8B57', 2:'#DAA520', 3:'#3A7EC8', 1:'#C83A3A', 4:'gray'}
for i in range(len(A_line)-1):
    rc = REGIME_CLR.get(reg_at_N500[i], 'gray')
    ax_q.plot(A_line[i:i+2], Q_curve[i:i+2],
              color=rc, lw=2.0, alpha=0.85)

ax_q.set_ylabel(r'Equilibrium quality  $Q^*(a)$  at $N=500$',
                fontsize=11, color='#444')
ax_q.set_ylim(0, 1.12)
ax_q.tick_params(axis='y', labelcolor='#444')

# Combined legend
handles = [
    Line2D([0],[0], color='r',      lw=2.5, label=r'$N_\uparrow(a)$: collapse threshold'),
    Patch(facecolor='#98FB98', alpha=0.4, label='Stable-honesty region'),
    Line2D([0],[0], color='#2E8B57',lw=2.0, label=r'$Q^*(a)$ in GH (green)'),
    Line2D([0],[0], color='#DAA520',lw=2.0, label=r'$Q^*(a)$ in BS (yellow)'),
    Line2D([0],[0], color='#3A7EC8',lw=2.0, label=r'$Q^*(a)$ in SC (blue)'),
    Line2D([0],[0], color='#C83A3A',lw=2.0, label=r'$Q^*(a)$ in GC (red)'),
]
ax_r.legend(handles=handles, fontsize=8.5, loc='upper right', framealpha=0.93)

# Parameter box
param_txt = (r'$K_{rev}=300,\ K=400,\ N_{eval}=500$' '\n'
             r'$r=100,\ c=25,\ \lambda_0=0.1,\ \varepsilon=0.05$' '\n'
             r'$\gamma=0.5,\ \delta=0.1,\ \phi=0.4,\ \mu=0.2$')
ax_r.text(0.02, 0.38, param_txt, transform=ax_r.transAxes,
          fontsize=8, va='bottom',
          bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                    edgecolor='gray', alpha=0.88))

ax_r.set_title(r'(b)  $N_\uparrow(a)$ falls as AI rises; quality $Q^*$ degrades'
               '\n'
               r'At $a\gtrsim0.5$,  $N_\uparrow$ vanishes — no stable-honesty region remains',
               fontsize=11, pad=8, fontweight='bold')

# ── Shared legend for regime colors ──────────────────────────────────────────
legend_patches = [
    Patch(facecolor='#98FB98', edgecolor='gray', label='Global Honesty (GH)'),
    Patch(facecolor='#FFE4B5', edgecolor='gray', label='Bistability (BS)'),
    Patch(facecolor='#ADD8E6', edgecolor='gray', label='Stable Coexistence (SC)'),
    Patch(facecolor='#FFB6C1', edgecolor='gray', label='Global Corruption (GC)'),
    Patch(facecolor='#D3D3D3', edgecolor='gray', label='No Submission (NS)'),
]
fig.legend(handles=legend_patches, loc='lower center', ncol=5,
           fontsize=9, framealpha=0.95, bbox_to_anchor=(0.5, -0.08))

fig.suptitle(
    'Fig. 6  ·  AI adoption erodes the stable-honesty window and lowers the collapse threshold\n'
    r'$N_\uparrow(a)$ falls continuously; at $a \gtrsim 0.5$ the GH/BS region disappears '
    r'and the system defaults to GC or SC',
    fontsize=12, fontweight='bold', y=1.02
)

# ─────────────────────────────────────────────────────────────────────────────
# 7.  Save
# ─────────────────────────────────────────────────────────────────────────────
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'doc', 'tex',
                            'fig6_hysteresis_widening.pdf')
plt.savefig(OUTPUT_PATH, dpi=300, bbox_inches='tight')
print(f"Saved → {os.path.normpath(OUTPUT_PATH)}")
plt.show()