# -*- coding: utf-8 -*-
import numpy as np
from time import time
from patient import Patient

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
                    self.icu_occupancy[t,p] = True
                if msg[3] == 1:
                    self.deaths[t,p] = True                    
                    
                
            print(t)
            
        t_end = time()
        self.sim_time = t_end - t_start
        
            