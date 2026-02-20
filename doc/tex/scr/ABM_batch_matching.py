import numpy as np
import matplotlib.pyplot as plt

# =====================================================================
# Theoretical ODE Calculation (Mean-Field Approximation)
# =====================================================================
def theoretical_delta_x(x, params, beta=1.0):
    """
    Calculates the expected evolutionary velocity (Delta x) based on the 
    infinite-population mean-field approximation (ODE).
    """
    N, alpha = params['N'], params['alpha']
    K_rev, K_store = params['K_rev'], params['K_store']
    r, c, lam, eps = params['r'], params['c'], params['lam'], params['eps']
    
    # Stage 1: Global Submission Volume
    V = N * alpha + N * (1 - alpha) * (1 - x)
    
    # Stage 2: Global Peer Review Screening Intensity
    eta = min(1.0, K_rev / V) if V > 0 else 1.0
    
    # Probabilities of passing review
    pi_1 = 1 - eta * eps
    pi_0 = 1 - eta * (1 - lam)
    
    # Expected volume of peer-accepted papers
    M = N * alpha * pi_1 + N * (1 - alpha) * (1 - x) * pi_0
    
    # Stage 3: Global Rationing Probability (Congestion)
    rho = min(1.0, K_store / M) if M > 0 else 1.0
    
    # Expected net payoff of a bad paper
    Pi_bad = r * rho * pi_0 - c
    
    # Fitness difference between strategies (OG vs AS)
    payoff_diff = - (1 - alpha) * Pi_bad
    
    # Fermi transition probabilities
    prob_AS_to_OG = 1 / (1 + np.exp(-beta * payoff_diff))
    prob_OG_to_AS = 1 / (1 + np.exp(-beta * (-payoff_diff)))
    
    # Expected rate of change (scaled by the 2% revision rate per step)
    rate = 0.02 * ( (1 - x) * prob_AS_to_OG - x * prob_OG_to_AS )
    return rate


# =====================================================================
# Agent-Based Model with Local Batch-Matching
# =====================================================================
def run_batch_abm(params, initial_x, batch_size=50, steps=2000, noise_beta=1.0):
    """
    Runs the Agent-Based Model where authors are randomly divided into 
    local batches (sub-markets) to compete for a fraction of journal slots.
    """
    N = params['N']
    alpha = params['alpha']
    r, c = params['r'], params['c']
    lam, eps = params['lam'], params['eps']
    
    # Scale journal capacities proportionally to match the local batch size
    scale_factor = batch_size / N
    K_rev_local = params['K_rev'] * scale_factor
    K_store_local = params['K_store'] * scale_factor
    
    # Initialize population: 1 for Only Good (OG), 0 for Always Submit (AS)
    num_OG = int(initial_x * N)
    population = np.array([1]*num_OG + [0]*(N - num_OG))
    
    # Data recording lists
    history_x = []
    recorded_rhos = []
    scatter_dx = []
    
    for t in range(steps):
        # Record current macro state
        n_og_global = np.sum(population)
        current_x = n_og_global / N
        history_x.append(current_x)
        
        # Shuffle population to assign to random local rooms (batches)
        indices = np.random.permutation(N)
        payoffs = np.zeros(N)
        
        # Loop through each batch (sub-market)
        for i in range(0, N, batch_size):
            batch_idx = indices[i:i+batch_size]
            batch_pop = population[batch_idx]
            
            n_og_local = np.sum(batch_pop)
            n_as_local = batch_size - n_og_local
            
            # Stage 1: Local Submission Volume
            V_local = n_og_local * alpha + n_as_local * 1.0
            
            # Stage 2: Local Peer Review
            eta_local = min(1.0, K_rev_local / V_local) if V_local > 0 else 1.0
            pi_1 = 1 - eta_local * eps
            pi_0 = 1 - eta_local * (1 - lam)
            
            # Local Peer-Accepted Volume
            M_local = n_og_local * alpha * pi_1 + n_as_local * (alpha * pi_1 + (1 - alpha) * pi_0)
            
            # Stage 3: Local Congestion and Rationing Probability
            rho_local = min(1.0, K_store_local / M_local) if M_local > 0 else 1.0
            
            # Record local congestion during the second half of the simulation (steady state)
            if t > int(steps/2): 
                recorded_rhos.append(rho_local)
                
            # Stage 4: Local Payoff Calculation
            Pi_good = r * rho_local * pi_1 - c
            Pi_bad = r * rho_local * pi_0 - c
            
            u_og = alpha * Pi_good
            u_as = alpha * Pi_good + (1 - alpha) * Pi_bad
            
            # Assign realized payoffs to agents in the current batch
            for idx, strat in zip(batch_idx, batch_pop):
                payoffs[idx] = u_og if strat == 1 else u_as
                
        # Stage 5: Global Social Learning (Pairwise Comparison)
        # Agents randomly select a peer from the entire population to imitate
        num_revise = int(0.02 * N)
        rev_indices = np.random.choice(N, num_revise, replace=False)
        opp_indices = np.random.choice(N, num_revise, replace=True)
        
        for idx, opp in zip(rev_indices, opp_indices):
            s_i = population[idx]
            s_j = population[opp]
            
            if s_i != s_j:
                payoff_diff = payoffs[s_j] - payoffs[idx]
                prob_switch = 1 / (1 + np.exp(-noise_beta * payoff_diff))
                if np.random.random() < prob_switch:
                    population[idx] = s_j
                    
        # Record evolutionary velocity (Delta x) for phase scatter plot
        new_x = np.sum(population) / N
        if t % 5 == 0: # Sample every 5 steps to avoid overcrowding the scatter plot
            scatter_dx.append((current_x, new_x - current_x))
            
    return history_x, recorded_rhos, scatter_dx

# =====================================================================
# Configuration and Execution
# =====================================================================

# Parameter Sets (Scenario A: Bistability, Scenario B: Stable Coexistence)
params_A = {'N': 1000, 'alpha': 0.2, 'K_rev': 300, 'K_store': 400, 'r': 100, 'c': 25, 'lam': 0.1, 'eps': 0.05}
params_B = {'N': 1000, 'alpha': 0.2, 'K_rev': 1200, 'K_store': 180, 'r': 150, 'c': 30, 'lam': 0.4, 'eps': 0.01}

print("Running Local Batch-Matching ABM Simulations...")
sim_steps = 2000

# Run Scenario B (Stable Coexistence) simulations
traj_B_local_low, rhos_B, _ = run_batch_abm(params_B, initial_x=0.1, steps=sim_steps)
traj_B_local_high, _, _ = run_batch_abm(params_B, initial_x=0.9, steps=sim_steps)

# Run Scenario A (Bistability) simulations
traj_A_local_low, _, _ = run_batch_abm(params_A, initial_x=0.1, steps=sim_steps)
traj_A_local_high, _, _ = run_batch_abm(params_A, initial_x=0.9, steps=sim_steps)
# Run a specific run starting near the tipping point (0.82) to capture stochastic drift
_, _, scatter_A_tip = run_batch_abm(params_A, initial_x=0.81, steps=sim_steps)

# Generate Theoretical ODE Trajectories for comparison
traj_B_ode_low, traj_B_ode_high = [0.1], [0.9]
traj_A_ode_low, traj_A_ode_high = [0.1], [0.9]

for _ in range(sim_steps - 1):
    traj_B_ode_low.append(max(0, min(1, traj_B_ode_low[-1] + theoretical_delta_x(traj_B_ode_low[-1], params_B))))
    traj_B_ode_high.append(max(0, min(1, traj_B_ode_high[-1] + theoretical_delta_x(traj_B_ode_high[-1], params_B))))
    
    traj_A_ode_low.append(max(0, min(1, traj_A_ode_low[-1] + theoretical_delta_x(traj_A_ode_low[-1], params_A))))
    traj_A_ode_high.append(max(0, min(1, traj_A_ode_high[-1] + theoretical_delta_x(traj_A_ode_high[-1], params_A))))


# =====================================================================
# Plotting and PDF Export
# =====================================================================

# Plot 1: Scenario B Trajectory Comparison
plt.figure(figsize=(8, 5))
plt.plot(range(sim_steps), traj_B_ode_low, color='darkblue', linestyle='--', linewidth=2, label='Theoretical ODE (Start 0.1)')
plt.plot(range(sim_steps), traj_B_local_low, color='blue', alpha=0.6, linewidth=1.5, label='Batch ABM (Start 0.1)')
plt.plot(range(sim_steps), traj_B_ode_high, color='darkorange', linestyle='--', linewidth=2, label='Theoretical ODE (Start 0.9)')
plt.plot(range(sim_steps), traj_B_local_high, color='orange', alpha=0.6, linewidth=1.5, label='Batch ABM (Start 0.9)')
plt.title('Plot 1: Scenario B (Stable Coexistence) under Local Matching', fontsize=13)
plt.xlabel('Time Steps', fontsize=12)
plt.ylabel('Proportion of Honest Authors (x)', fontsize=12)
plt.ylim(-0.05, 1.05)
plt.legend(loc='lower right', fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('Plot1_ScenarioB_Trajectory.pdf')

# Plot 2: Scenario A Trajectory Comparison
plt.figure(figsize=(8, 5))
plt.plot(range(sim_steps), traj_A_ode_low, color='darkred', linestyle='--', linewidth=2, label='Theoretical ODE (Start 0.1)')
plt.plot(range(sim_steps), traj_A_local_low, color='red', alpha=0.6, linewidth=1.5, label='Batch ABM (Start 0.1)')
plt.plot(range(sim_steps), traj_A_ode_high, color='darkgreen', linestyle='--', linewidth=2, label='Theoretical ODE (Start 0.9)')
plt.plot(range(sim_steps), traj_A_local_high, color='green', alpha=0.6, linewidth=1.5, label='Batch ABM (Start 0.9)')
plt.title('Plot 2: Scenario A (Bistability) under Local Matching', fontsize=13)
plt.xlabel('Time Steps', fontsize=12)
plt.ylabel('Proportion of Honest Authors (x)', fontsize=12)
plt.ylim(-0.05, 1.05)
plt.legend(loc='center right', fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('Plot2_ScenarioA_Trajectory.pdf')

# Plot 3: Distribution of Local Congestion (Histogram)
plt.figure(figsize=(8, 5))
# Filter out non-congested rooms (rho=1.0) to better visualize the bottleneck distribution
rhos_congested = [r for r in rhos_B if r < 1.0]
plt.hist(rhos_congested, bins=20, color='purple', edgecolor='black', alpha=0.6)
plt.axvline(np.mean(rhos_congested), color='red', linestyle='dashed', linewidth=2, label=f'Mean $\\rho$ = {np.mean(rhos_congested):.2f}')
plt.title('Plot 3: Distribution of Local Congestion $\\rho$ (Scenario B Steady State)', fontsize=13)
plt.xlabel('Realized Publication Probability ($\\rho$) in Local Batches', fontsize=12)
plt.ylabel('Frequency (Number of Batches)', fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('Plot3_Congestion_Histogram.pdf')

# Plot 4: Phase Portrait with Stochastic Drift
plt.figure(figsize=(8, 5))
# Generate Theoretical Curve
x_vals = np.linspace(0, 1, 100)
dx_vals = [theoretical_delta_x(x, params_A) for x in x_vals]
plt.plot(x_vals, dx_vals, color='black', linewidth=2, label='Theoretical Expected Velocity ($\\Delta x$)')
plt.axhline(0, color='gray', linestyle='--')

# Overlay Local ABM Scatter Drift
scatter_x = [pt[0] for pt in scatter_A_tip]
scatter_y = [pt[1] for pt in scatter_A_tip]
plt.scatter(scatter_x, scatter_y, color='orange', alpha=0.3, s=15, label='Batch ABM Realized $\\Delta x$ (Stochastic Drift)')

plt.title('Plot 4: Evolutionary Phase Portrait with Stochastic Drift (Scenario A)', fontsize=13)
plt.xlabel('Proportion of Honest Authors (x)', fontsize=12)
plt.ylabel('Evolutionary Velocity ($\\Delta x$)', fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('Plot4_Phase_Scatter.pdf')

print("All 4 plots successfully generated and saved as PDFs.")