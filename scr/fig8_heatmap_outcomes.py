"""
Fig 8: Heatmap of long-run outcomes over (delta/gamma ratio, mu = d_lambda/d_a).

x-axis: delta/gamma  in [0, 1]   — how fast review capacity keeps pace with production
y-axis: mu           in [0, 0.4] — how fast AI raises the false-positive rate

For each (delta/gamma, mu) pair, we run the ODE to convergence at a=0.8
and record the long-run honest-author share x*.
A second panel shows the regime classification (GH / BS / SC / GC).
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_io import save_data, load_data, DATA_DIR

# ── Fixed baseline parameters (Set A) ────────────────────────────────────────
N      = 1000
alpha  = 0.2
K_rev0 = 300.0
K      = 400.0
r      = 100.0
c0     = 25.0
lam0   = 0.10
eps    = 0.05
gamma  = 0.50   # production elasticity (fixed)
phi    = 0.40   # cost-reduction slope  (fixed)
a_val  = 0.80   # AI adoption level at which we evaluate

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '..', 'doc', 'tex', 'fig8_heatmap_outcomes.pdf')
DATA_PATH   = os.path.join(DATA_DIR, 'fig8_data.json')


# ── AI-extended model at fixed a ─────────────────────────────────────────────
def compute_Pi_bad(x, K_rev_eff, lam_eff, c_eff):
    V   = N * (1 - (1 - alpha) * x)  # base volume (1+gamma*a factor absorbed into K_rev_eff)
    eta = min(1.0, K_rev_eff / V) if V > 0 else 1.0
    pi0 = 1 - eta * (1 - lam_eff)
    pi1 = 1 - eta * eps
    M   = (1 + gamma * a_val) * (N * alpha * pi1 + N * (1 - alpha) * (1 - x) * pi0)
    rho = min(1.0, K / M) if M > 0 else 1.0
    return r * rho * pi0 - c_eff

def run_ode(K_rev_eff, lam_eff, c_eff, x0=0.90, steps=6000, dt=0.01):
    x = x0
    for _ in range(steps):
        pb = compute_Pi_bad(x, K_rev_eff, lam_eff, c_eff)
        dx = -x * (1 - x) * (1 - alpha) * pb * dt
        x  = float(np.clip(x + dx, 0.0, 1.0))
    return x

def classify_regime(K_rev_eff, lam_eff, c_eff):
    """
    Classify by signs of Pi_bad at boundaries.
    GH: both <0;  GC: both >0;  BS: Pi_bad(1)<0, Pi_bad(0)>0;  SC: Pi_bad(1)>0, Pi_bad(0)<0
    """
    p1 = compute_Pi_bad(1.0, K_rev_eff, lam_eff, c_eff)
    p0 = compute_Pi_bad(0.0, K_rev_eff, lam_eff, c_eff)
    if p1 < 0 and p0 < 0:
        return 'GH'
    elif p1 > 0 and p0 > 0:
        return 'GC'
    elif p1 < 0 and p0 > 0:
        return 'BS'
    else:
        return 'SC'


# ── Parameter grid ────────────────────────────────────────────────────────────
n_pts     = 60
dg_ratios = np.linspace(0.0, 1.0,  n_pts)   # delta/gamma
mu_vals   = np.linspace(0.0, 0.40, n_pts)   # dλ/da


# ── Compute ───────────────────────────────────────────────────────────────────

def compute_data():
    xstar_grid  = np.zeros((n_pts, n_pts))
    regime_grid = np.empty((n_pts, n_pts), dtype=object)

    print("Computing heatmap grid (this may take ~30 s)…")
    for i, mu in enumerate(mu_vals):
        for j, dg in enumerate(dg_ratios):
            delta_eff = dg * gamma
            K_rev_eff = K_rev0 * (1 + delta_eff * a_val)
            K_rev_norm = K_rev_eff / (1 + gamma * a_val)
            lam_eff   = lam0 + mu * a_val
            c_eff     = c0 * (1 - phi * a_val)

            regime = classify_regime(K_rev_norm, lam_eff, c_eff)
            regime_grid[i, j] = regime

            xstar_grid[i, j] = run_ode(K_rev_norm, lam_eff, c_eff, x0=0.90)

    print("Grid complete.")

    # Convert object array to list of lists for JSON serialisation
    regime_list = regime_grid.tolist()

    return {
        'xstar_grid':  xstar_grid,
        'regime_list': regime_list,
        'dg_ratios':   dg_ratios,
        'mu_vals':     mu_vals,
    }


# ── Plot ──────────────────────────────────────────────────────────────────────

def plot(data):
    xstar_grid  = data['xstar_grid']
    regime_list = data['regime_list']
    dg_ratios_  = data['dg_ratios']
    mu_vals_    = data['mu_vals']

    regime_to_int = {'GH': 0, 'SC': 1, 'BS': 2, 'GC': 3}
    regime_grid = np.array(regime_list)
    regime_int  = np.vectorize(regime_to_int.get)(regime_grid).astype(float)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), gridspec_kw={'wspace': 0.45})

    # --- Panel A: long-run x* heatmap ---
    ax = axes[0]
    im = ax.imshow(
        xstar_grid,
        origin='lower',
        aspect='auto',
        extent=[dg_ratios_[0], dg_ratios_[-1], mu_vals_[0], mu_vals_[-1]],
        cmap='RdYlGn',
        vmin=0, vmax=1
    )
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label(r'Long-run honest-author share $x^*$', fontsize=11)

    cs = ax.contour(
        dg_ratios_, mu_vals_, xstar_grid,
        levels=[0.50],
        colors=['black'], linewidths=1.8, linestyles='--'
    )
    ax.clabel(cs, fmt={0.50: r'$x^*=0.5$'}, fontsize=9)

    ax.set_xlabel(r'Verification elasticity ratio $\delta/\gamma$', fontsize=11)
    ax.set_ylabel(r'False-positive slope $\mu = \mathrm{d}\lambda/\mathrm{d}a$', fontsize=11)
    ax.set_title(r'(a) Long-run honest-author share $x^*$'
                 '\n'
                 r'at $a=0.8$', fontsize=10)

    ax.text(0.85, 0.35, 'Collapse\nzone', color='black',   fontsize=9,
            ha='center', va='center', fontweight='bold',
            transform=ax.transAxes)
    ax.text(0.15, 0.10, 'Stable\nzone',  color='darkgreen',  fontsize=9,
            ha='center', va='center', fontweight='bold',
            transform=ax.transAxes)

    # --- Panel B: regime classification heatmap ---
    ax2 = axes[1]
    cmap4 = mcolors.ListedColormap(['#2ca02c', '#1f77b4', '#ffdd57', '#d62728'])
    bounds = [-0.5, 0.5, 1.5, 2.5, 3.5]
    norm4  = mcolors.BoundaryNorm(bounds, cmap4.N)

    im2 = ax2.imshow(
        regime_int,
        origin='lower',
        aspect='auto',
        extent=[dg_ratios_[0], dg_ratios_[-1], mu_vals_[0], mu_vals_[-1]],
        cmap=cmap4,
        norm=norm4
    )

    legend_elements = [
        Patch(facecolor='#2ca02c', label='GH — Global Honesty'),
        Patch(facecolor='#1f77b4', label='SC — Stable Coexistence'),
        Patch(facecolor='#ffdd57', label='BS — Bistability'),
        Patch(facecolor='#d62728', label='GC — Global Corruption'),
    ]
    ax2.legend(handles=legend_elements, loc='upper right', fontsize=8.5,
               framealpha=0.9)

    ax2.set_xlabel(r'Verification elasticity ratio $\delta/\gamma$', fontsize=11)
    ax2.set_ylabel(r'False-positive slope $\mu = \mathrm{d}\lambda/\mathrm{d}a$', fontsize=11)
    ax2.set_title(r'(b) Regime classification at $a=0.8$', fontsize=10)

    ax2.axhline(0.20, color='white', linestyle=':', linewidth=1.2, alpha=0.8)
    ax2.text(0.50, 0.21, r'Baseline $\mu=0.2$', color='black',
             fontsize=10, fontweight='bold', ha='center', transform=ax2.get_xaxis_transform())
    ax2.axvline(0.20, color='white', linestyle=':', linewidth=1.2, alpha=0.8)
    ax2.text(0.21, 0.85, r'Baseline $\delta/\gamma=0.2$', color='white',
             fontsize=8, va='center', rotation=90, transform=ax2.get_yaxis_transform())

    fig.suptitle(
        r'Fig. 8 — Outcome sensitivity to verification investment ($\delta/\gamma$) and'
        '\n'
        r'screening vulnerability ($\mu$) at AI adoption $a=0.8$'
        r'  ($\gamma=0.5,\;\phi=0.4$; Set A)',
        fontsize=11, y=1.02
    )

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, bbox_inches='tight')
    print("fig8 saved.")


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
