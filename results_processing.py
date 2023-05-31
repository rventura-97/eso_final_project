# -*- coding: utf-8 -*-
import os
import numpy as np
import pandas as pd

def compute_death_rate(file_dir):
    file = np.load(file_dir)
    return np.sum(file)

def compute_positive_diagnoses(file_dir):
    file = np.load(file_dir)
    return np.sum(file)

def compute_health_metrics():
    metrics_table = []
    for sim_batch in os.listdir("OUTPUTS"):
        batch_params = pd.read_csv("OUTPUTS/"+sim_batch+"/sim_params.csv")
        for batch_dir in os.listdir("OUTPUTS/"+sim_batch):
            if os.path.isdir("OUTPUTS/"+sim_batch+"/"+batch_dir):
                crit_evol_matrix = np.load("OUTPUTS/"+sim_batch+"/"+batch_dir+"/"+"crit_evol_markers.npy")
                crit_revs_matrix = np.load("OUTPUTS/"+sim_batch+"/"+batch_dir+"/"+"crit_reversals.npy")
                deaths_matrix = np.load("OUTPUTS/"+sim_batch+"/"+batch_dir+"/"+"deaths.npy")
                icu_occup_matrix = np.load("OUTPUTS/"+sim_batch+"/"+batch_dir+"/"+"icu_occupancy.npy")
                pos_digns_matrix = np.load("OUTPUTS/"+sim_batch+"/"+batch_dir+"/"+"positive_diagnoses.npy")
                
                num_of_deaths = np.sum(deaths_matrix)
                num_of_patients = num_of_deaths+deaths_matrix.shape[1]
                num_of_icu_entries = np.sum(np.floor(np.sum(np.diff(icu_occup_matrix,axis=0),axis=0)/2))
                num_of_crit_reversals = np.sum(crit_revs_matrix)
                num_of_pos_digns = np.sum(pos_digns_matrix)
                num_of_crit_evols = np.sum(np.floor(np.sum(crit_evol_matrix,axis=0)/2))
                
                # mean num of patients in icu
                # mean icu stay length
                # mean crit state at diagnose
                
                pop_death_rate = num_of_deaths/num_of_patients
                icu_death_rate = num_of_deaths/num_of_icu_entries
                
                metrics_table.append(pd.DataFrame(data = np.mat(np.concatenate((batch_params.iloc[[10,11,12],1].values,\
                                                  [pop_death_rate, icu_death_rate]))),\
                                                  columns = ["Type of Monitoring", "Appointments Interval",\
                                                             "RPM Recall", "Population Death Rate",\
                                                             "ICU Death Rate"]))
                    
                metrics_table = pd.concat(metrics_table).reset_index(drop=True)
                metrics_table[["Population Death Rate","ICU Death Rate"]] = metrics_table[["Population Death Rate","ICU Death Rate"]].apply(pd.to_numeric)
                metrics_table = metrics_table.groupby(["Type of Monitoring", "Appointments Interval","RPM Recall"]).mean()
                
    return metrics_table