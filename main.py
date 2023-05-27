# -*- coding: utf-8 -*-
from simulation import Simulation
from aux_functions import compute_icu_surv_prob_map

# %% Simulation parameters (fixed)
t_sim = 25*365
num_patients = 1#25000
crit_trans_prob = 0.0005
t_crit_mean = 56 # days
t_crit_min = 7 # days
t_crit_max = 105 # days
max_crit_reversal_prob = 0.3
icu_death_base_prob = 0.2
icu_surv_base_prob = 0.7
icu_t_max = 28 # days
icu_t_min = 7 # days

# %%
icu_surv_prob_map = compute_icu_surv_prob_map(icu_surv_base_prob,icu_t_max,icu_t_min)


# %% Simulation parameters (variable)
appointments_interval = 28 # days

# %% Initialize simulation
sim = Simulation(t_sim, num_patients, crit_trans_prob,\
                 t_crit_mean, t_crit_min, t_crit_max,"NONE",\
                 appointments_interval, max_crit_reversal_prob,\
                 icu_death_base_prob, icu_t_max, icu_t_min)
sim.init()

# %% Run simulation
sim.run()
