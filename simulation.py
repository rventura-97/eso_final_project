# -*- coding: utf-8 -*-
import numpy as np
from time import time
from patient import Patient

class Simulation:
    def __init__(self, t_sim, num_patients, crit_trans_prob, t_crit_mean, t_crit_min, t_crit_max, surv_state, appointments_interval,max_crit_reversal_prob,icu_death_base_prob, icu_t_max, icu_t_min):
        # Simulation variables
        self.t_sim = t_sim
        self.num_patients = num_patients
        self.patients = [None]*self.num_patients
        self.crit_trans_prob = crit_trans_prob
        self.t_crit_mean = t_crit_mean
        self.t_crit_min = t_crit_min
        self.t_crit_max = t_crit_max
        self.surv_state = surv_state
        self.appointments_interval = appointments_interval
        self.appoints_sched = []
        self.max_crit_reversal_prob = max_crit_reversal_prob
        self.icu_death_base_prob = icu_death_base_prob
        self.icu_t_max = icu_t_max
        self.icu_t_min = icu_t_min
        self.sim_time = 0
        
        # Report variables
        self.icu_admissions = np.zeros(self.t_sim)
        
    def init(self):
        # Generate appointments scheduling if using local patitent monitoring
        if self.surv_state == "LOCAL":
            self.appoints_sched = self.__gen_appoints_sched()
        
        for i in range(0, self.num_patients):
            self.patients[i] = Patient(pat_id=i,\
                                       surv_state=self.surv_state,\
                                       crit_trans_prob=self.crit_trans_prob)
                
    def run(self):
        t_start = time()
        for t in range(0, self.t_sim):
            for p in range(0, self.num_patients):
                # Update each patient
                if self.surv_state == "LOCAL":
                    if np.isin(p,self.appoints_sched[t,0]):
                        t_appoint = True
                    else:
                        t_appoint = False
                else:
                    t_appoint = False
                    
                msg = self.patients[p].update(t, self.t_crit_mean,\
                                              self.t_crit_min, self.t_crit_max,\
                                              t_appoint, self.max_crit_reversal_prob,\
                                              self.icu_death_base_prob,\
                                              self.icu_t_max,\
                                              self.icu_t_min)
                
                # Record each patient's state at current time
                if msg == "REACHED_FULLY_CRITICAL":
                    self.icu_admissions[t] += 1
                
            print(t)
            
        t_end = time()
        self.sim_time = t_end - t_start
        
        
    def __gen_appoints_sched(self):
        appoints_per_day = np.ceil(self.num_patients/self.appointments_interval)
        appoints_sched = np.tile(np.arange(0,self.num_patients),np.int(np.ceil(appoints_per_day*self.t_sim/self.num_patients)))
        appoints_sched = appoints_sched[0:np.int(appoints_per_day*self.t_sim)]
        appoints_sched = appoints_sched.reshape(-1,np.int(appoints_per_day))
        
        return appoints_sched
        
            