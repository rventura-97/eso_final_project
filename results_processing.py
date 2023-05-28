# -*- coding: utf-8 -*-
import numpy as np

def compute_death_rate(sim):
    return np.sum(sim.deaths)/(sim.num_patients+np.sum(sim.deaths))