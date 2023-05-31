# -*- coding: utf-8 -*-
# %% Import required modules
from simulation import Simulation
from aux_functions import compute_icu_surv_prob_map
from aux_functions import generate_appointments_schedule
from aux_functions import compute_remote_detect_prob_map

# %% Simulation parameters (fixed)
t_sim = 25*365
num_patients = 25000
crit_trans_prob = 0.0005
t_crit_mean = 6*28 # days
t_crit_min = 3*28 # days
t_crit_max = 9*28 # days
max_crit_reversal_prob = 0.3
icu_surv_base_prob = 0.8
icu_t_max = 28 # days
icu_t_min = 7 # days
icu_surv_prob_map = compute_icu_surv_prob_map(icu_surv_base_prob,icu_t_max,icu_t_min)

# %% Simulation parameters (variable)
type_of_monitoring = "NONE"
appointments_interval = 6*28 # days
appointments_schedule = generate_appointments_schedule(num_patients, appointments_interval, t_sim)
remote_detection_prob = 0.7
remote_detection_prob_map = compute_remote_detect_prob_map(remote_detection_prob, t_crit_max, t_crit_min)

# %% Initialize simulation
sim = Simulation(t_sim, num_patients, crit_trans_prob,\
                 t_crit_mean, t_crit_min, t_crit_max,\
                 type_of_monitoring, max_crit_reversal_prob,\
                 icu_t_max, icu_t_min, appointments_schedule,\
                 icu_surv_prob_map, remote_detection_prob_map)
sim.init()

# %% Run simulation
sim.run()



