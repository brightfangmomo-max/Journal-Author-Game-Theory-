
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

# ==========================================
# 1. Core Mathematical Model
# ==========================================
def soft_min(a, b, k):
    return -np.log(np.exp(-k * a) + np.exp(-k * b)) / k

def get_dxdt_curve(x_arr, p):
    k = p.get('smoothness', 15)
    y_vals = []

    for x in x_arr:
        # 1. Volume calculation
        V_total = p['N'] * (1 - (1 - p['alpha']) * x)

        # 2. Review Stage
        eta = np.clip(soft_min(1.0, p['K_rev'] / V_total, k), 0.0, 1.0)
        pi_0 = 1 - eta * (1 - p['lam'])
        pi_1 = 1 - eta * p['epsilon']

        # 3. Storage Stage
        V_G = p['N'] * p['alpha']
        V_B = p['N'] * (1 - p['alpha']) * (1 - x)
        M = V_G * pi_1 + V_B * pi_0
        rho_bar = np.clip(soft_min(1.0, p['K_store'] / M, k), 0.0, 1.0)

        # 4. Payoff
        Pi_bad = p['r'] * rho_bar * pi_0 - p['c']

        # 5. Velocity: dx/dt = -x(1-x)(1-alpha) * Pi_bad
        dxdt = -x * (1 - x) * (1 - p['alpha']) * Pi_bad
        y_vals.append(dxdt)

    return np.array(y_vals)

# ==========================================
# 2. Plotting Function with Full Coverage
# ==========================================
def plot_styled_regions(ax, x, y, title, regime_type, params):

    # 1. Background Regions
    # We use axvspan for Global cases to ensure 100% coverage including endpoints
    if regime_type == 'Corruption':
        ax.axvspan(0, 1, color='#F08080', alpha=0.2, label='Collapse to Corruption')
    elif regime_type == 'Honesty':
        ax.axvspan(0, 1, color='#90EE90', alpha=0.2, label='Growth to Honesty')
    else:
        # For mixed regimes, we rely on the sign of y
        # We use a large Y extent to ensure full vertical coverage
        ax.fill_between(x, -1000, 1000, where=(y > 0), color='#90EE90', alpha=0.2, interpolate=True, label='Growth to Honesty')
        ax.fill_between(x, -1000, 1000, where=(y < 0), color='#F08080', alpha=0.2, interpolate=True, label='Collapse to Corruption')

    # 2. Plot the Curve
    ax.plot(x, y, color='#2F4F4F', lw=2.5, label=r'$\dot{x}$')
    ax.axhline(0, color='black', lw=1, linestyle='--')
    ax.set_xlim(0, 1)

    # Dynamic Y-limit
    y_abs_max = max(np.max(np.abs(y)), 0.05)
    ax.set_ylim(-y_abs_max*1.3, y_abs_max*1.3)

    # 3. Markers logic
    sign_changes = np.where(np.diff(np.sign(y)))[0]
    roots = []
    roots.append((0, y[0]))
    roots.append((1, y[-1]))
    for idx in sign_changes:
        x1, x2 = x[idx], x[idx+1]
        y1, y2 = y[idx], y[idx+1]
        if y2 != y1:
            root_x = x1 - y1 * (x2 - x1) / (y2 - y1)
            roots.append((root_x, 0))

    marker_size = 10

    if regime_type == 'Bistability':
        ax.plot(0, 0, 'o', color='black', markersize=marker_size, zorder=5)
        ax.plot(1, 0, 'o', color='black', markersize=marker_size, zorder=5)
        internal_roots = [r for r in roots if 0.01 < r[0] < 0.99]
        if internal_roots:
            rx = internal_roots[0][0]
            ax.plot(rx, 0, 'o', color='#FF8C00', markersize=marker_size+2, markeredgecolor='black', zorder=10)
            ax.annotate(f'$x^* \\approx {rx:.2f}$', (rx, 0), xytext=(rx, y_abs_max*0.3), arrowprops=dict(facecolor='black', arrowstyle='->'), ha='center')

    elif regime_type == 'Coexistence':
        ax.plot(0, 0, 'o', color='white', markeredgecolor='black', markersize=marker_size, zorder=5)
        ax.plot(1, 0, 'o', color='white', markeredgecolor='black', markersize=marker_size, zorder=5)
        internal_roots = [r for r in roots if 0.01 < r[0] < 0.99]
        if internal_roots:
            rx = internal_roots[0][0]
            ax.plot(rx, 0, 'o', color='#1E90FF', markersize=marker_size+2, markeredgecolor='black', zorder=10)
            ax.annotate(f'$x^* \\approx {rx:.2f}$', (rx, 0), xytext=(rx, -y_abs_max*0.3), arrowprops=dict(facecolor='black', arrowstyle='->'), ha='center')

    elif regime_type == 'Honesty':
        ax.plot(0, 0, 'o', color='white', markeredgecolor='black', markersize=marker_size, zorder=5)
        ax.plot(1, 0, 'o', color='black', markersize=marker_size, zorder=5)

    elif regime_type == 'Corruption':
        # x=0 Stable, x=1 Unstable
        ax.plot(0, 0, 'o', color='black', markersize=marker_size, zorder=5)
        ax.plot(1, 0, 'o', color='white', markeredgecolor='black', markersize=marker_size, zorder=5)

    # 4. Styling
    ax.set_xlabel('Proportion of Honest Authors ($x$)', fontsize=12)
    ax.set_ylabel(r'Evolutionary Velocity ($\dot{x}$)', fontsize=12)
    ax.set_title(title, fontsize=14, pad=12)
    ax.grid(True, alpha=0.3, linestyle='--')

    # 5. Legend
    legend_elements = [
        Patch(facecolor='#90EE90', alpha=0.3, label='Honesty Region'),
        Patch(facecolor='#F08080', alpha=0.3, label='Corruption Region'),
        Line2D([0], [0], color='#2F4F4F', lw=2.5, label='Dynamics'),
        Line2D([0], [0], marker='o', color='w', label='Stable', markerfacecolor='black', markersize=8),
        Line2D([0], [0], marker='o', color='w', label='Unstable', markerfacecolor='white', markeredgecolor='black', markersize=8)
    ]
    if regime_type == 'Bistability':
        legend_elements.append(Line2D([0], [0], marker='o', color='w', label='Tipping Point', markerfacecolor='#FF8C00', markeredgecolor='black', markersize=10))
    elif regime_type == 'Coexistence':
        legend_elements.append(Line2D([0], [0], marker='o', color='w', label='Stable Coexistence', markerfacecolor='#1E90FF', markeredgecolor='black', markersize=10))

    ax.legend(handles=legend_elements, loc='lower right', fontsize=8, framealpha=0.9)

    # 6. Parameter Box
    param_str = (
        f"$r={params['r']}, c={params['c']}$\n"
        f"$\\lambda={params['lam']}, K_{{rev}}={params['K_rev']}$\n"
        f"$K_{{store}}={params['K_store']}$"
    )
    ax.text(0.05, 0.95, param_str, transform=ax.transAxes, fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

# ==========================================
# 3. Generate
# ==========================================
x_grid = np.linspace(0, 1, 200)

params_1 = {'N': 1000, 'alpha': 0.2, 'smoothness': 15, 'K_rev': 300, 'K_store': 400, 'r': 100, 'c': 25, 'lam': 0.1, 'epsilon': 0.05}
params_2 = {'N': 1000, 'alpha': 0.2, 'smoothness': 15, 'K_rev': 1200, 'K_store': 180, 'r': 150, 'c': 30, 'lam': 0.4, 'epsilon': 0.01}
params_3 = {'N': 1000, 'alpha': 0.2, 'smoothness': 15, 'K_rev': 800, 'K_store': 400, 'r': 100, 'c': 35, 'lam': 0.1, 'epsilon': 0.05}
params_4 = {'N': 1000, 'alpha': 0.2, 'smoothness': 15, 'K_rev': 200, 'K_store': 1500, 'r': 150, 'c': 5, 'lam': 0.3, 'epsilon': 0.05}

cases = [
    (params_1, 'Bistability (Tipping Point)', 'Bistability', 'polynomial_graph_1.pdf'),
    (params_2, 'Stable Coexistence (Attractor)', 'Coexistence', 'polynomial_graph_2.pdf'),
    (params_3, 'Global Honesty (Convergence)', 'Honesty', 'polynomial_graph_3.pdf'),
    (params_4, 'Global Corruption (Collapse)', 'Corruption', 'polynomial_graph_4.pdf')
]

for p, title, r_type, fname in cases:
    y = get_dxdt_curve(x_grid, p)
    plt.figure(figsize=(7, 5))
    plot_styled_regions(plt.gca(), x_grid, y, title, r_type, p)
    plt.tight_layout()
    plt.show() # To display as requested
    plt.savefig(fname, dpi=300)