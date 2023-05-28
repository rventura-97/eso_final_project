# -*- coding: utf-8 -*-
import numpy as np

class Patient:
    
    def __init__(self, pat_id):
        self.pat_id = pat_id
        self.crit_rate = 0
        self.crit_state = 0
        self.alive = True
        self.crit_state_at_detection = None
        self.icu_surv_prob = None
        self.icu_surv_prob_rate = None
        self.remote_detect_prob = None
        self.remote_detect_prob_rate = None
        
    def update(self, t, t_crit_mean, t_crit_min, t_crit_max, t_appoint,\
               max_crit_reversal_prob, surv_state, crit_trans_prob,\
               icu_surv_prob_map, remote_detection_prob_map):
        
        update_msg = np.zeros(5)
        
        if self.alive == True:
            # Update criticality state
            self.crit_state += self.crit_rate
            if self.crit_rate > 0 and np.abs(1-self.crit_state) < 1/1000000:
                self.crit_state = 1
            elif self.crit_rate < 0 and np.abs(self.crit_state) < 1/1000000: 
                self.crit_state = 0
            
            # Random chance of starting transition to critical state
            if self.crit_state == 0 and self.crit_rate == 0:
                if np.random.rand() < crit_trans_prob:
                   self.crit_rate = 1/np.round(np.random.triangular(t_crit_min, t_crit_mean, t_crit_max))
                   update_msg[0] = 1
            
                   
            # Patient resets criticality state, becomes stable
            if self.crit_state == 0 and self.crit_rate < 0:
                self.crit_rate = 0
                
            # Patient reaches fully critical state
            if self.crit_state == 1 and self.crit_rate > 0:
                self.crit_rate = 0
                update_msg[0] = 1
                if self.crit_state_at_detection is None:
                    self.icu_surv_prob = icu_surv_prob_map.loc[icu_surv_prob_map.index[-1],"init_surv_prob"]
                    self.icu_surv_prob_rate = icu_surv_prob_map.loc[icu_surv_prob_map.index[-1],"surv_prob_inc_rate"]
                else:
                    days_at_icu = np.floor((icu_surv_prob_map.index[-1]-icu_surv_prob_map.index[0])*\
                                  self.crit_state_at_detection+icu_surv_prob_map.index[0])
                    self.icu_surv_prob = icu_surv_prob_map.loc[days_at_icu,"init_surv_prob"]
                    self.icu_surv_prob_rate = icu_surv_prob_map.loc[days_at_icu,"surv_prob_inc_rate"]
                    self.crit_state_at_detection = None
                    
                
            # Try to diagnose criticality state if there is an appointment at current time
            if surv_state == "LOCAL" and t_appoint == True and \
               self.crit_rate > 0 and self.crit_state < 1 and\
               self.crit_state_at_detection == None:
               # Random chance of correct positive diagnosis
               if np.random.rand() < self.crit_state:   
                    update_msg[1] = 1
                    self.crit_state_at_detection = self.crit_state
                    # Random chance of reversing transition to critical state
                    if np.random.rand() < -max_crit_reversal_prob*self.crit_state + max_crit_reversal_prob:
                        self.crit_rate = -self.crit_rate
                        self.crit_state_at_detection = None
                        update_msg[2] = 1
                        
            # Trigger remote diagnose
            if surv_state == "REMOTE" and self.crit_rate > 0 and\
                self.crit_state < 1 and self.remote_detect_prob == None: # self.crit_state > 0 (?)
                crit_days = np.round(1/self.crit_rate)
                self.remote_detect_prob = 0
                self.remote_detect_prob_rate = remote_detection_prob_map.loc[crit_days,"detect_prob_inc_rate"]
                
            # Try to diagnose criticality state if there is remote patient monitoring
            if surv_state == "REMOTE" and self.crit_rate > 0 and\
                self.crit_state < 1 and self.crit_state_at_detection == None and\
                self.remote_detect_prob != None: # self.crit_state > 0 (?)
                # Random chance of correct positive diagnosis
                if np.random.rand() < self.remote_detect_prob:   
                    update_msg[1] = 1
                    self.crit_state_at_detection = self.crit_state
                    # Random chance of reversing transition to critical state
                    if np.random.rand() < -max_crit_reversal_prob*self.crit_state + max_crit_reversal_prob:
                        self.crit_rate = -self.crit_rate
                        self.crit_state_at_detection = None
                        update_msg[2] = 1      
                # Update remote detection probability
                self.remote_detect_prob += self.remote_detect_prob_rate
                    
            # Update state at ICU
            if self.crit_state == 1 and self.crit_rate == 0 and self.icu_surv_prob < 1:
                # Random chance of death
                if np.random.rand() > self.icu_surv_prob:
                    self.alive = False
                    update_msg[4] = 1
                else:
                    # Update survival probability
                    self.icu_surv_prob += self.icu_surv_prob_rate
                    if np.abs(1-self.icu_surv_prob) < 1/1000000:
                        self.icu_surv_prob = 1
                    update_msg[3] = 1
            
            # Patient survived ICU, starts reversing critical state
            if self.crit_state == 1 and self.crit_rate == 0 and self.icu_surv_prob == 1:
                self.crit_state_at_detection = None
                self.icu_surv_prob = None
                self.icu_surv_prob_rate = None
                self.remote_detect_prob = None
                self.remote_detect_prob_rate = None
                self.crit_rate = -1/np.round(np.random.triangular(t_crit_min, t_crit_mean, t_crit_max))

        
        return update_msg

        


        
        