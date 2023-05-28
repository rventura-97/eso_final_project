# -*- coding: utf-8 -*-
import ray
import numpy as np
from time import time
from patient import Patient
from aux_functions import compute_icu_surv_prob_map
from aux_functions import generate_appointments_schedule
from aux_functions import compute_remote_detect_prob_map

class Simulation:
    def __init__(self, t_sim, num_patients, crit_trans_prob, t_crit_mean, t_crit_min, t_crit_max,\
                 surv_state, max_crit_reversal_prob,\
                 icu_t_max, icu_t_min, appointments_schedule,\
                 icu_surv_prob_map, remote_detection_prob_map):
        
        # Simulation variables
        self.t_sim = t_sim
        self.num_patients = num_patients
        self.patients = [None]*self.num_patients
        self.crit_trans_prob = crit_trans_prob
        self.t_crit_mean = t_crit_mean
        self.t_crit_min = t_crit_min
        self.t_crit_max = t_crit_max
        self.surv_state = surv_state
        self.max_crit_reversal_prob = max_crit_reversal_prob
        self.icu_t_max = icu_t_max
        self.icu_t_min = icu_t_min
        self.sim_time = 0
        self.appointments_schedule = appointments_schedule
        self.icu_surv_prob_map = icu_surv_prob_map
        self.remote_detection_prob_map = remote_detection_prob_map
        
        # Report variables
        self.crit_evol_markers = np.zeros((self.t_sim, self.num_patients),dtype=bool)
        self.positive_diagnoses = np.zeros((self.t_sim, self.num_patients),dtype=bool)
        self.crit_reversals = np.zeros((self.t_sim, self.num_patients),dtype=bool)
        self.icu_occupancy = np.zeros((self.t_sim, self.num_patients),dtype=bool)
        self.deaths = np.zeros((self.t_sim, self.num_patients),dtype=bool)
        
        
        
        
    def init(self):
        for i in range(0, self.num_patients):
            self.patients[i] = Patient(pat_id=i)
                
    def run(self):
        t_start = time()
        for t in range(0, self.t_sim):
            for p in range(0, self.num_patients):
                # Update each patient
                if self.surv_state == "LOCAL":
                    if np.isin(self.patients[p].pat_id, self.appointments_schedule[t,0]):
                        t_appoint = True
                    else:
                        t_appoint = False
                else:
                    t_appoint = False
                    
                msg = self.patients[p].update(t, self.t_crit_mean,\
                                              self.t_crit_min, self.t_crit_max,\
                                              t_appoint, self.max_crit_reversal_prob,\
                                              self.surv_state, self.crit_trans_prob,\
                                              self.icu_surv_prob_map, self.remote_detection_prob_map)
                
                if msg[0] == 1:
                    self.crit_evol_markers[t,p] = True
                if msg[1] == 1:
                    self.positive_diagnoses[t,p] = True
                if msg[2] == 1:
                    self.crit_reversals[t,p] = True
                if msg[3] == 1:
                    self.icu_occupancy[t,p] = True 
                if msg[4] == 1:
                    self.deaths[t,p] = True  
                    
                
            print(t)
            
        t_end = time()
        self.sim_time = t_end - t_start
        
class ParallelSimulator:
    def __init__(self, num_simulations, t_sim, num_patients, crit_trans_prob,\
                 t_crit_mean, t_crit_min, t_crit_max, max_crit_reversal_prob,\
                 icu_surv_base_prob, icu_t_max, icu_t_min, type_of_monitoring,\
                 appointments_interval, remote_detection_prob):
        
        self.num_simulations = num_simulations
        self.output_dir = ""
        
        self.t_sim = t_sim
        self.num_patients = num_patients
        self.crit_trans_prob = crit_trans_prob
        self.t_crit_mean = t_crit_mean
        self.t_crit_min = t_crit_min
        self.t_crit_max = t_crit_max
        self.max_crit_reversal_prob = max_crit_reversal_prob
        self.icu_surv_base_prob = icu_surv_base_prob
        self.icu_t_max = icu_t_max
        self.icu_t_min = icu_t_min
        self.type_of_monitoring = type_of_monitoring
        self.appointments_interval = appointments_interval
        self.remote_detection_prob = remote_detection_prob
        
        self.icu_surv_prob_map = compute_icu_surv_prob_map(icu_surv_base_prob,icu_t_max,icu_t_min)
        self.appointments_schedule = generate_appointments_schedule(num_patients, appointments_interval, t_sim)
        self.remote_detection_prob_map = compute_remote_detect_prob_map(remote_detection_prob, t_crit_max, t_crit_min)
        
    def run_simulations(self):
        # create folder and write simulation parameters file and schedule
        sims = []
        for _ in range(0, self.num_simulations):
            sims.append(launch_simulation.remote(self.t_sim, self.num_patients, self.crit_trans_prob,\
                                                 self.t_crit_mean, self.t_crit_min, self.t_crit_max,\
                                                 self.type_of_monitoring, self.max_crit_reversal_prob,\
                                                 self.icu_t_max, self.icu_t_min, self.appointments_schedule,\
                                                 self.icu_surv_prob_map, self.remote_detection_prob_map))
        
        outputs = ray.get(sims)
        
        return outputs
        
@ray.remote            
def launch_simulation(t_sim, num_patients, crit_trans_prob, t_crit_mean, t_crit_min, t_crit_max,\
                      surv_state, max_crit_reversal_prob,\
                      icu_t_max, icu_t_min, appointments_schedule,\
                      icu_surv_prob_map, remote_detection_prob_map):
    
    sim = Simulation(t_sim, num_patients, crit_trans_prob, t_crit_mean, t_crit_min, t_crit_max,\
                     surv_state, max_crit_reversal_prob,\
                     icu_t_max, icu_t_min, appointments_schedule,\
                     icu_surv_prob_map, remote_detection_prob_map)
        
    sim.run()
    
    return sim            