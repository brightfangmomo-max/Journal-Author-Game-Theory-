import numpy as np

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from matplotlib.lines import Line2D 



# ==========================================
# 1. Core Model Functions (Rigorous)
# ==========================================
def soft_min(a, b, k):
    return -np.log(np.exp(-k * a) + np.exp(-k * b)) / k

def get_model_states(x, p):
    k = p.get('smoothness', 15)
    # Volume
    V_total = p['N'] * (1 - (1 - p['alpha']) * x)
    # Review
    eta = np.clip(soft_min(1.0, p['K_rev'] / V_total, k), 0.0, 1.0)
    pi_0 = 1 - eta * (1 - p['lam'])
    pi_1 = 1 - eta * p['epsilon']
    # Storage
    V_G = p['N'] * p['alpha']
    V_B = p['N'] * (1 - p['alpha']) * (1 - x)
    M = V_G * pi_1 + V_B * pi_0
    rho_bar = np.clip(soft_min(1.0, p['K_store'] / M, k), 0.0, 1.0)
    # Payoffs
    Pi_bad = p['r'] * rho_bar * pi_0 - p['c']
    Pi_good = p['r'] * rho_bar * pi_1 - p['c']
    return Pi_bad, Pi_good, rho_bar, eta, pi_0, pi_1

def classify_regime_point(p):
    """
    Returns regime code:
    0: GH (Green), 1: GC (Red), 2: BS (Yellow), 3: SC (Blue), 4: NS (Gray)
    """
    # 1. Check Viability (Participation Constraint at Honest Equilibrium)
    Pi_bad_1, Pi_good_1, _, _, _, _ = get_model_states(0.999, p)
    if Pi_good_1 < 0:
        return 4 # NS

    # 2. Check Stability Boundaries
    one_stable = (Pi_bad_1 < 0)
    Pi_bad_0, _, _, _, _, _ = get_model_states(0.001, p)
    zero_stable = (Pi_bad_0 > 0)

    if one_stable and zero_stable: return 2 # BS
    if one_stable and not zero_stable: return 0 # GH
    if not one_stable and zero_stable: return 1 # GC
    if not one_stable and not zero_stable: return 3 # SC
    return 4 # Fallback

def get_quality_at_equilibrium(p):
    x_grid = np.linspace(0, 1, 500)
    dxdt = -x_grid * (1 - x_grid) * (1 - p['alpha']) * get_model_states(x_grid, p)[0]

    roots = []
    # Check boundaries
    pb0, _, _, _, _, _ = get_model_states(0.001, p)
    if pb0 > 0: roots.append(0.0)
    pb1, _, _, _, _, _ = get_model_states(0.999, p)
    if pb1 < 0: roots.append(1.0)
    # Internal
    signs = np.sign(dxdt)
    sign_changes = np.where(np.diff(signs))[0]
    for idx in sign_changes:
        if dxdt[idx] > 0 and dxdt[idx+1] < 0:
            roots.append(x_grid[idx])

    if not roots: return 0.0 # Should be covered by NS
    x_star = max(roots)

    # Calculate Q
    _, _, _, _, pi_0, pi_1 = get_model_states(x_star, p)
    pass_G = p['N'] * p['alpha'] * pi_1
    pass_B = p['N'] * (1 - p['alpha']) * (1 - x_star) * pi_0
    if (pass_G + pass_B) < 1e-9: return 0.0
    return pass_G / (pass_G + pass_B)

# ==========================================
# 2. Scanning Setup
# ==========================================
base_params = {
    'N': 1000, 'alpha': 0.2,
    'K_rev': 300, 'K_store': 400,
    'r': 100, 'c': 25,
    'lam': 0.1, 'epsilon': 0.05,
    'smoothness': 15
}

sweeps = [
    ('lam', r'(a) False Positive Rate ($\lambda$)', np.linspace(0, 0.5, 200)),
    ('epsilon', r'(b) Friction ($\epsilon$)', np.linspace(0, 0.5, 200)),
    ('r', r'(c) Reward ($r$)', np.linspace(0, 300, 200)),
    ('c', r'(d) Submission Cost ($c$)', np.linspace(0, 100, 200)),
    ('alpha', r'(e) Productivity ($\alpha$)', np.linspace(0.05, 0.95, 200))
]

# Splitting the sweeps into 3 parts (2, 2, 1)
sweeps_part1 = sweeps[:2] # a, b
sweeps_part2 = sweeps[2:4] # c, d
sweeps_part3 = sweeps[4:] # e

# ==========================================
# 3. Plotting Helper Function
# ==========================================
def plot_regime_strips(sweep_list, filename, figsize):
    fig, axes = plt.subplots(len(sweep_list), 1, figsize=figsize, sharey=True)
    # Ensure axes is iterable even if only 1 plot
    if len(sweep_list) == 1: axes = [axes]

    colors = ['#98FB98', '#FFB6C1', '#FFE4B5', '#ADD8E6', '#D3D3D3']
    cmap = ListedColormap(colors)

    for i, (param, label, vals) in enumerate(sweep_list):
        ax = axes[i]
        regime_strip = []
        quality_line = []

        for val in vals:
            p = base_params.copy()
            p[param] = val
            reg = classify_regime_point(p)
            regime_strip.append(reg)
            if reg == 4:
                quality_line.append(np.nan)
            else:
                quality_line.append(get_quality_at_equilibrium(p))

        regime_arr = np.array(regime_strip)[np.newaxis, :]
        ax.imshow(regime_arr, aspect='auto', cmap=cmap, vmin=0, vmax=4,
                  extent=[vals.min(), vals.max(), 0, 1.1], alpha=0.6)
        ax.plot(vals, quality_line, 'k-', lw=2, label='Avg. Quality ($Q$)')

        ax.set_xlabel(label, fontsize=12)
        ax.set_ylabel('Quality ($Q$)', fontsize=12)
        ax.set_ylim(0, 1.1)
        ax.grid(True, alpha=0.2, linestyle='--')

    # Legend (same for all)
    legend_elements = [
        Patch(facecolor='#98FB98', label='Global Honesty', alpha=0.6),
        Patch(facecolor='#FFE4B5', label='Bistability', alpha=0.6),
        Patch(facecolor='#ADD8E6', label='Stable Coexistence', alpha=0.6),
        Patch(facecolor='#FFB6C1', label='Global Corruption', alpha=0.6),
        Patch(facecolor='#D3D3D3', label='Collapse (NS)', alpha=0.6),
        plt.Line2D([0], [0], color='k', lw=2, label='Quality Level')
    ]
    # Adjust legend position based on number of subplots
    bbox_y = 1.05 if len(sweep_list) > 1 else 1.15
    fig.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, bbox_y), ncol=3, fontsize=10)

    plt.tight_layout()
    # Adjust top margin to accommodate legend
    top_margin = 0.85 if len(sweep_list) > 1 else 0.80
    plt.subplots_adjust(top=top_margin)
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()

# ==========================================
# 4. Generate Plots
# ==========================================
# Part 1: lambda, epsilon (2 plots)
plot_regime_strips(sweeps_part1, 'strategic_regimes_scan_part1.pdf', figsize=(8, 5.5))

# Part 2: r, c (2 plots)
plot_regime_strips(sweeps_part2, 'strategic_regimes_scan_part2.pdf', figsize=(8, 5.5))

# Part 3: alpha (1 plot)
plot_regime_strips(sweeps_part3, 'strategic_regimes_scan_part3.pdf', figsize=(8, 3.5))