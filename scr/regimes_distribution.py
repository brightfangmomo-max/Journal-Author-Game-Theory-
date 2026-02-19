import numpy as np

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch



# ==========================================
# 1. Core Model Functions
# ==========================================
def soft_min(a, b, k):
    """Smooth approximation of min(a, b)"""
    return -np.log(np.exp(-k * a) + np.exp(-k * b)) / k

def get_model_states(x, p):
    k = p.get('smoothness', 15)

    # 1. Volume
    V_total = p['N'] * (1 - (1 - p['alpha']) * x)

    # 2. Review Bottleneck (Eta)
    # Clip to [0, 1] to avoid negative probabilities due to soft_min approximation
    eta_val = soft_min(1.0, p['K_rev'] / V_total, k)
    eta = np.clip(eta_val, 0.0, 1.0)

    pi_0 = 1 - eta * (1 - p['lam'])
    pi_1 = 1 - eta * p['epsilon']

    # 3. Storage Bottleneck (Rho)
    V_G = p['N'] * p['alpha']
    V_B = p['N'] * (1 - p['alpha']) * (1 - x)
    M = V_G * pi_1 + V_B * pi_0

    # Clip to [0, 1]
    rho_val = soft_min(1.0, p['K_store'] / M, k)
    rho_bar = np.clip(rho_val, 0.0, 1.0)

    # 4. Payoffs
    # Net Utility of Bad Paper
    Pi_bad = p['r'] * rho_bar * pi_0 - p['c']
    # Net Utility of Good Paper (for Participation Constraint)
    Pi_good = p['r'] * rho_bar * pi_1 - p['c']

    return Pi_bad, Pi_good, rho_bar, eta

def classify_regime_map(p):
    """
    Classify the regime for the Phase Diagram.
    0: GH, 1: GC, 2: BS, 3: SC, 4: NS
    """
    # Check Boundary Payoffs

    # x=1 (Honesty Boundary)
    Pi_bad_1, Pi_good_1, _, _ = get_model_states(0.999, p)

    # Check viability (Participation Constraint)
    # If honest authors expect negative utility even at x=1 (clean system),
    # the system is non-viable (No Submission).
    if Pi_good_1 < 0:
        return 4 # System Collapse (NS) - Gray

    # Stability of x=1
    # If Pi_bad(1) < 0, cheating is unprofitable -> x tends to 1 -> STABLE
    # If Pi_bad(1) > 0, cheating is profitable -> x tends to 0 -> UNSTABLE
    one_stable = (Pi_bad_1 < 0)

    # x=0 (Corruption Boundary)
    Pi_bad_0, _, _, _ = get_model_states(0.001, p)
    # Stability of x=0
    # If Pi_bad(0) > 0, cheating is profitable -> x tends to 0 -> STABLE
    # If Pi_bad(0) < 0, cheating is unprofitable -> x tends to 1 -> UNSTABLE
    zero_stable = (Pi_bad_0 > 0)

    # Determine Regime based on boundary stability
    if one_stable and zero_stable:
        return 2 # Bistability (Yellow)
    elif one_stable and not zero_stable:
        return 0 # Global Honesty (Green)
    elif not one_stable and zero_stable:
        return 1 # Global Corruption (Red)
    elif not one_stable and not zero_stable:
        return 3 # Stable Coexistence (Blue)

    return -1

# ==========================================
# 2. Generate Phase Diagram Data
# ==========================================
# Parameter Selection Logic:
# To see all 4 regimes, we need a setup where:
# 1. Uncongested cheating is NOT profitable (r*lam < c) -> Allows Green/Yellow
# 2. Review collapse is possible (K_rev < N*alpha) -> Allows Red/Blue
# 3. Storage collapse is possible -> Allows Blue/Green transition
#
# Selected Set: r=100, c=25, lam=0.1
# r*lam = 10 < 25 -> Pi_bad(1) < 0 if review is perfect.
# But if review fails (eta -> 0, pi0 -> 1), Pi_bad -> 100*1*1 - 25 = 75 > 0.
# So we can get 1 Unstable if K_rev is low.
map_params = {
    'N': 1000,
    'alpha': 0.2,
    'r': 100,
    'c': 25,
    'lam': 0.1,
    'epsilon': 0.05,
    'smoothness': 15
}

res = 200 # High resolution for clean boundaries
k_rev_vals = np.linspace(10, 200, res)
k_store_vals = np.linspace(10, 500, res)
regime_map = np.zeros((res, res))

for i, ks in enumerate(k_store_vals):
    for j, kr in enumerate(k_rev_vals):
        p = map_params.copy()
        p['K_rev'] = kr
        p['K_store'] = ks
        regime_map[i, j] = classify_regime_map(p)

# ==========================================
# 3. Plotting
# ==========================================
plt.figure(figsize=(9, 7))

# Colormap: 0=Green, 1=Red, 2=Yellow, 3=Blue, 4=Gray
# Order in map values: 0, 1, 2, 3, 4
# ListedColormap needs colors for integers 0, 1, 2, 3, 4
colors = ['#98FB98', '#FFB6C1', '#FFE4B5', '#ADD8E6', '#D3D3D3']
cmap = ListedColormap(colors)

plt.imshow(regime_map, origin='lower',
           extent=[k_rev_vals.min(), k_rev_vals.max(), k_store_vals.min(), k_store_vals.max()],
           aspect='auto', cmap=cmap)

plt.xlabel(r'Review Capacity ($K_{rev}$)', fontsize=12)
plt.ylabel(r'Slot Capacity ($K_{store}$)', fontsize=12)
plt.title('Phase Diagram: Decoupling the Dual Bottlenecks', fontsize=14)

# Custom Legend
legend_elements = [
    Patch(facecolor='#98FB98', label='Global Honesty (GH)'),
    Patch(facecolor='#FFE4B5', label='Bistability (BS)'),
    Patch(facecolor='#ADD8E6', label='Stable Coexistence (SC)'),
    Patch(facecolor='#FFB6C1', label='Global Corruption (GC)'),
    Patch(facecolor='#D3D3D3', label='System Collapse (NS)')
]
plt.legend(handles=legend_elements, loc='upper right', framealpha=0.95, fontsize=10)

plt.tight_layout()
plt.savefig('regime_map_final.pdf', dpi=300)
plt.show()