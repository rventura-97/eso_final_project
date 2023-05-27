# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import sympy
from scipy.optimize import bisect


def generate_appointments_schedule(num_patients, appointments_interval, t_sim):
    appoints_per_day = np.ceil(num_patients/appointments_interval)
    appoints_sched = np.tile(np.arange(0,num_patients),np.int(np.ceil(appoints_per_day*t_sim/num_patients)))
    appoints_sched = appoints_sched[0:np.int(appoints_per_day*t_sim)]
    appoints_sched = appoints_sched.reshape(-1,np.int(appoints_per_day))
    
    return appoints_sched


def compute_icu_surv_prob_map(base_surv_prob, max_icu_days, min_icu_days):
    icu_surv_prob_map = pd.DataFrame(data=np.zeros((max_icu_days-min_icu_days+1,3)),\
                                     columns=["init_surv_prob","surv_prob_inc_rate","surv_prob"],\
                                     index=np.arange(min_icu_days,max_icu_days+1))
    icu_surv_prob_map.index.name = "days_in_icu"
        
    x = sympy.Symbol('x')
    f = 1
    for t in range(1,max_icu_days+1):
        f = f*(1-t*x)
    f = f - base_surv_prob
    f = sympy.lambdify(x,f)
    f_sol = bisect(f,0,0.1)
    
    icu_surv_prob_map["init_surv_prob"] = np.ones(max_icu_days-min_icu_days+1)-\
                                          f_sol*np.arange(min_icu_days,max_icu_days+1)
    icu_surv_prob_map["surv_prob_inc_rate"] = f_sol
    
    for d in icu_surv_prob_map.index:
        icu_surv_prob_map.loc[d,"surv_prob"] = np.prod(np.arange(0,d)*f_sol +\
                                               icu_surv_prob_map.loc[d,"init_surv_prob"])

    return icu_surv_prob_map