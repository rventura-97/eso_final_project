# -*- coding: utf-8 -*-
# %% Import required modules
import ray
from results_processing import compute_health_metrics_table, compute_economic_metrics_table

# %% Compute health metrics
ray.init()
health_metrics, health_metrics_mean = compute_health_metrics_table(method="ray")
ray.shutdown()

# %% Save health metrics
health_metrics.to_csv("REPORTS/health_metrics.csv")
health_metrics_mean.to_csv("REPORTS/health_metrics_mean.csv")

# %% Compute economic metrics
econ_params = {"Cardiologist salary per day": 10000/28,
               "Appointments per doctor per day": 4,
               "ICU cost per patient per day": 1000,
               "Remote monitoring cost per patient per day": 50/28,
               "Initial remote monitoring cost per patient": 10000,
               "Num of patients": 25000,
               "Simulation time in days": 9125}

ray.init()
econ_metrics, econ_metrics_mean = compute_economic_metrics_table(econ_params, method="ray")
ray.shutdown()

# %% 
econ_metrics.to_csv("REPORTS/econ_metrics.csv")
econ_metrics_mean.to_csv("REPORTS/econ_metrics_mean.csv")