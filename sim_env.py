# -*- coding: utf-8 -*-
import numpy as np

class sim_env:
    def __init__(self, num_pats, t_max):
        self.num_pats = num_pats
        self.t_max = t_max


    def init(self):
        # Initialize patients health level timeline
        self.pat_state = np.zeros((self.num_pats,self.t_max))
        self.pat_state[:] = np.nan
        
        for p in range(0,self.num_pats):
            crit_delta_t = int(np.random.normal(3*4*7, 4*7))
            crit_t_0 = np.random.randint(0,self.t_max-crit_delta_t)
            self.pat_state[p,0:crit_t_0] = 0
            self.pat_state[p,crit_t_0:crit_t_0+crit_delta_t] = np.arange(1,crit_delta_t+1)*(100/crit_delta_t)