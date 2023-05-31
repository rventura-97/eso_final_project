# -*- coding: utf-8 -*-
# %% Import required modules
import ray
from simulation import ParallelSimulator

# %% Batch simulations parameters
num_batches = 1
sims_per_batch = 10

# %% Simulation parameters (fixed)
t_sim = 25*365
num_patients = 25000
crit_trans_prob = 0.0005
t_crit_mean = 4*28 # days
t_crit_min = 1*28 # days
t_crit_max = 7*28 # days
max_crit_reversal_prob = 0.3
icu_surv_base_prob = 0.8
icu_t_max = 28 # days
icu_t_min = 7 # days

# %% Base results without patient monitoring
type_of_monitoring = "NONE"
appointments_interval = 28 # not used
remote_detection_prob = 0.7 # not used

ray.init()
for _ in range(0, num_batches):
    parallel_sim = ParallelSimulator(sims_per_batch, t_sim, num_patients, crit_trans_prob,\
                                     t_crit_mean, t_crit_min, t_crit_max, max_crit_reversal_prob,\
                                     icu_surv_base_prob, icu_t_max, icu_t_min, type_of_monitoring,\
                                     appointments_interval, remote_detection_prob) 
    sims = parallel_sim.run_simulations()
ray.shutdown()


# %% Local patient monitoring (28 days)
type_of_monitoring = "LOCAL"
appointments_interval = [1*28, 2*28, 3*28, 4*28, 5*28, 6*28, 7*28, 8*28, 9*28, 10*28]
remote_detection_prob = 0.7 # not used

ray.init()
for i in range(0, len(appointments_interval)):
    for _ in range(0, num_batches):
        parallel_sim = ParallelSimulator(sims_per_batch, t_sim, num_patients, crit_trans_prob,\
                                         t_crit_mean, t_crit_min, t_crit_max, max_crit_reversal_prob,\
                                         icu_surv_base_prob, icu_t_max, icu_t_min, type_of_monitoring,\
                                         appointments_interval[i], remote_detection_prob) 
        sims = parallel_sim.run_simulations()
ray.shutdown()


# %% Remote patient monitoring (0.7)
type_of_monitoring = "REMOTE"
appointments_interval = 28 # not used
remote_detection_prob = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]

ray.init()
for i in range(0, len(remote_detection_prob)):
    for _ in range(0, num_batches):
        parallel_sim = ParallelSimulator(sims_per_batch, t_sim, num_patients, crit_trans_prob,\
                                         t_crit_mean, t_crit_min, t_crit_max, max_crit_reversal_prob,\
                                         icu_surv_base_prob, icu_t_max, icu_t_min, type_of_monitoring,\
                                         appointments_interval, remote_detection_prob[i]) 
        sims = parallel_sim.run_simulations()
ray.shutdown()