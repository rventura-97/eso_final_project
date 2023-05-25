# -*- coding: utf-8 -*-
from simulation import Simulation

# %% Simulation parameters
t_sim = 25*365
num_patients = 1#25000
crit_trans_prob = 0.0005
t_crit_mean = 56 # days
t_crit_min = 7 # days
t_crit_max = 105 # days

# %% Initialize simulation
sim = Simulation(t_sim, num_patients, crit_trans_prob, t_crit_mean, t_crit_min, t_crit_max,"LOCAL",28)
sim.init()

# %% Run simulation
sim.run()
