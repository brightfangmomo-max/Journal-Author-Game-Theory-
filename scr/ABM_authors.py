
import numpy as np
import matplotlib.pyplot as plt

def run_abm_simulation(params, initial_x, steps=3000, noise_beta=1.0):
    # read parameters from input dictionary
    N = params['N']
    alpha = params['alpha']
    K_rev = params['K_rev']
    K_store = params['K_store']
    r = params['r']
    c = params['c']
    lam = params['lam']
    eps = params['eps']

    # define the initial population
    num_OG = int(initial_x * N)
    population = np.array([1]*num_OG + [0]*(N - num_OG))

    #Two strategies only, OG and AS

    history_x = []

    for t in range(steps):
        n_og = np.sum(population)
        n_as = N - n_og
        
        # fraction of only good
        x = n_og / N
        history_x.append(x)

        # Total number of papers submitted
        V = n_og * alpha + n_as * 1.0

        # set eta, which is .,....
        if V <= 0: 
            eta = 1.0
        else: 
            eta = min(1.0, K_rev / V)

        # compute payoffs?
        pi_1 = 1 - eta * eps
        pi_0 = 1 - eta * (1 - lam)

        M = (N * alpha) * pi_1 + (n_as * (1 - alpha)) * pi_0

        if M <= 0: rho = 1.0
        else: rho = min(1.0, K_store / M)

        Pi_bad = r * rho * pi_0 - c
        payoff_diff = - (1 - alpha) * Pi_bad

        prob_AS_to_OG = 1 / (1 + np.exp(-noise_beta * payoff_diff))
        prob_OG_to_AS = 1 / (1 + np.exp(-noise_beta * (-payoff_diff)))

        num_revise = int(0.02 * N)
        indices = np.random.choice(N, num_revise, replace=False)

        for idx in indices:
            if population[idx] == 0:
                if np.random.random() < prob_AS_to_OG:
                    population[idx] = 1
            else:
                if np.random.random() < prob_OG_to_AS:
                    population[idx] = 0

    return history_x

params_A = {
    'N': 1000, 'alpha': 0.2, 'K_rev': 300, 'K_store': 400,
    'r': 100, 'c': 25, 'lam': 0.1, 'eps': 0.05
}

traj_A_low = run_abm_simulation(params_A, initial_x=0.1)
traj_A_high = run_abm_simulation(params_A, initial_x=0.9)

plt.figure(figsize=(7, 6))
plt.plot(traj_A_low, label='Start Low (x=0.1)', color='red', alpha=0.8, linewidth=2)
plt.plot(traj_A_high, label='Start High (x=0.9)', color='green', alpha=0.8, linewidth=2)
plt.title('Scenario A: Bistability', fontsize=14)
plt.xlabel('Time Steps', fontsize=12)
plt.ylabel('Proportion of Honest Authors (x)', fontsize=12)
plt.ylim(-0.05, 1.05)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

params_B = {
    'N': 1000, 'alpha': 0.2, 'K_rev': 1200, 'K_store': 180,
    'r': 150, 'c': 30, 'lam': 0.4, 'eps': 0.01
}

traj_B_low = run_abm_simulation(params_B, initial_x=0.1)
traj_B_high = run_abm_simulation(params_B, initial_x=0.9)

plt.figure(figsize=(7, 6))
plt.plot(traj_B_low, label='Start Low (x=0.1)', color='blue', alpha=0.8, linewidth=2)
plt.plot(traj_B_high, label='Start High (x=0.9)', color='orange', alpha=0.8, linewidth=2)
plt.title('Scenario B: Stable Coexistence', fontsize=14)
plt.xlabel('Time Steps', fontsize=12)
plt.ylabel('Proportion of Honest Authors (x)', fontsize=12)
plt.ylim(-0.05, 1.05)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()