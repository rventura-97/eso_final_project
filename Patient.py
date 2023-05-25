# -*- coding: utf-8 -*-
import numpy as np
from math import factorial

class Patient:
    
    def __init__(self, pat_id, surv_state, crit_trans_prob):
        self.pat_id = pat_id
        self.surv_state = surv_state
        self.crit_trans_prob = crit_trans_prob
        self.crit_rate = 0
        self.crit_state = 0
        self.alive = True
        self.crit_state_at_detection = None
        self.t_icu_entry = None
        self.icu_death_prob = None
        self.icu_death_prob_rate = None
        
    def update(self, t, t_crit_mean, t_crit_min, t_crit_max, t_appoint, max_crit_reversal_prob, icu_death_base_prob, icu_t_max, icu_t_min):
        update_msg = ""
        
        if self.alive == True:
            # Update criticality state
            if self.crit_rate > 0:
                self.crit_state = np.min([self.crit_state + self.crit_rate, 1])
            elif self.crit_rate < 0:
                self.crit_state = np.max([0, self.crit_state + self.crit_rate])
            
            # Random chance of starting transition to critical state
            if self.crit_state == 0 and self.crit_rate == 0:
                if np.random.rand() < self.crit_trans_prob:
                   self.crit_rate = 1/np.round(np.random.triangular(t_crit_min, t_crit_mean, t_crit_max))
                   
            # Patient resets criticality state, becomes stable
            if self.crit_state == 0 and self.crit_rate < 0:
                self.crit_rate = 0
                
            # Patients reaches fully critical state
            if self.crit_state == 1 and self.crit_rate > 0:
                self.crit_rate = 0
                update_msg = "REACHED_FULLY_CRITICAL"
                self.t_icu_entry = t
                if self.crit_state_at_detection is None:
                    self.icu_death_prob_rate = np.power((1-icu_death_base_prob)/factorial(icu_t_max),1/icu_t_max)
                    self.icu_death_prob = self.icu_death_prob_rate
                
            # Try to diagnose criticality state if there is an appointment at current time
            if self.surv_state == "LOCAL" and t_appoint == True and \
               self.crit_rate > 0 and self.crit_state < 1:
                # Random chance of correct positive diagnosis
                if np.random.rand() < self.crit_state:   
                    update_msg = "LOCAL_DIAGNOSE_BEFORE_CRITICAL"
                    self.crit_state_at_detection = self.crit_state
                    # Random chance of reversing transition to critical state
                    if np.random.rand() < -max_crit_reversal_prob*self.crit_state + max_crit_reversal_prob:
                        self.crit_rate = -self.crit_rate
                        self.crit_state_at_detection = None
                    
            # Update alive state at ICU
            if self.crit_state == 1 and self.crit_rate == 0:
                update_msg = "PATIENT_AT_ICU"
            
                
        else:
            update_msg = "DEAD"
            
        return update_msg

        


        
        