# -*- coding: utf-8 -*-
import numpy as np

class Patient:
    
    def __init__(self, pat_id, surv_state, crit_trans_prob):
        self.pat_id = pat_id
        self.surv_state = surv_state
        self.appoints = []
        self.crit_trans_prob = crit_trans_prob
        self.crit_rate = 0
        self.crit_state = "STABLE"
        
    def update(self):
        if self.crit_state == "STABLE":
            if np.random.rand() < self.crit_trans_prob:
                self.crit_state = "INCREASING"
        