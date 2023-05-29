# -*- coding: utf-8 -*-
# %% Import required modules
import ray
from simulation import ParallelSimulator

# %% Batch simulations parameters
num_batches = 4
sims_per_batch = 25

# %% Simulation parameters (fixed)
t_sim = 25*365
num_patients = 25000
crit_trans_prob = 0.0005
t_crit_mean = 56 # days
t_crit_min = 7 # days
t_crit_max = 105 # days
max_crit_reversal_prob = 0.3
icu_surv_base_prob = 0.8
icu_t_max = 28 # days
icu_t_min = 7 # days

# %% Base results without patient monitoring
type_of_monitoring = "NONE"
appointments_interval = 28 # days
remote_detection_prob = 0.7

ray.init()

for _ in range(0, num_batches):
    parallel_sim = ParallelSimulator(sims_per_batch, t_sim, num_patients, crit_trans_prob,\
                                     t_crit_mean, t_crit_min, t_crit_max, max_crit_reversal_prob,\
                                     icu_surv_base_prob, icu_t_max, icu_t_min, type_of_monitoring,\
                                     appointments_interval, remote_detection_prob) 
        
    sims = parallel_sim.run_simulations()

ray.shutdown()