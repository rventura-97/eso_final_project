# -*- coding: utf-8 -*-
import os
import ray
import numpy as np
import pandas as pd


def compute_health_metrics_table(method="single"):
    # Initialize metrics table
    num_of_sims = 0
    for sim_batch in os.listdir("OUTPUTS"):
        for batch_dir in os.listdir("OUTPUTS/"+sim_batch):
            if os.path.isdir("OUTPUTS/"+sim_batch+"/"+batch_dir):
                num_of_sims += 1    
                
    metrics_table = pd.DataFrame(data=np.zeros((num_of_sims, 9130)),
                                 columns = ["Sim Batch",\
                                            "Sim Number",\
                                            "Crit Evol File",\
                                            "Crit Revs File",\
                                            "Deaths File",\
                                            "ICU Occup File",\
                                            "Pos Digns File",\
                                            "Type of Monitoring",\
                                            "Appointments Interval",\
                                            "RPM Recall",\
                                            "Critical Death Rate",\
                                            "ICU Death Rate",\
                                            "Early Diagnoses Rate",\
                                            "Criticality Reversal Rate",\
                                            "Mean ICU Occupancy",\
                                            "Max ICU Occupacy",\
                                            "Mean ICU Stay",\
                                            "Max Number of Early Diagnoses"])
        
    sim_count = 0
    for sim_batch in os.listdir("OUTPUTS"):
        batch_params = pd.read_csv("OUTPUTS/"+sim_batch+"/sim_params.csv")
        for batch_dir in os.listdir("OUTPUTS/"+sim_batch):
            if os.path.isdir("OUTPUTS/"+sim_batch+"/"+batch_dir):
                metrics_table.loc[sim_count,"Sim Batch"] = sim_batch
                metrics_table.loc[sim_count,"Sim Number"] = batch_dir
                metrics_table.loc[sim_count,"Crit Evol File"] = "OUTPUTS/"+sim_batch+"/"+batch_dir+"/"+"crit_evol_markers.npy"
                metrics_table.loc[sim_count,"Crit Revs File"] = "OUTPUTS/"+sim_batch+"/"+batch_dir+"/"+"crit_reversals.npy"
                metrics_table.loc[sim_count,"Deaths File"] = "OUTPUTS/"+sim_batch+"/"+batch_dir+"/"+"deaths.npy"
                metrics_table.loc[sim_count,"ICU Occup File"] = "OUTPUTS/"+sim_batch+"/"+batch_dir+"/"+"icu_occupancy.npy"
                metrics_table.loc[sim_count,"Pos Digns File"] = "OUTPUTS/"+sim_batch+"/"+batch_dir+"/"+"positive_diagnoses.npy"
                
                type_of_monitoring = batch_params.iloc[10,1]
                if type_of_monitoring == "NONE":
                    metrics_table.loc[sim_count,"Type of Monitoring"] = type_of_monitoring
                    metrics_table.loc[sim_count,"Appointments Interval"] = "NONE"
                    metrics_table.loc[sim_count,"RPM Recall"] = "NONE"
                elif type_of_monitoring == "LOCAL":
                    metrics_table.loc[sim_count,"Type of Monitoring"] = type_of_monitoring
                    metrics_table.loc[sim_count,"Appointments Interval"] = batch_params.iloc[11,1]
                    metrics_table.loc[sim_count,"RPM Recall"] = "NONE"
                elif type_of_monitoring == "REMOTE":
                    metrics_table.loc[sim_count,"Type of Monitoring"] = type_of_monitoring
                    metrics_table.loc[sim_count,"Appointments Interval"] = "NONE"
                    metrics_table.loc[sim_count,"RPM Recall"] = batch_params.iloc[12,1]
                      
                sim_count += 1
          
                
    # Compute metrics  
    if method == "single":
        for s in range(0, metrics_table.shape[0]):
            s_metrics = single_compute_health_metrics(metrics_table.iloc[s,:])   
            metrics_table.iloc[np.logical_and(metrics_table["Sim Batch"].values==s_metrics["Sim Batch"].values,\
                               metrics_table["Sim Number"].values==s_metrics["Sim Number"].values),10:] = s_metrics.values[0,2:]
            print("Processed simulation {} / {}".format(s+1, metrics_table.shape[0]))
    elif method == "ray":
        s_metrics = []
        for s in range(0, metrics_table.shape[0]):
            s_metrics.append(ray_compute_health_metrics.remote(metrics_table.iloc[s,:]))
        metrics_list = ray.get(s_metrics)  

        for metrics in metrics_list:
            metrics_table.iloc[np.logical_and(metrics_table["Sim Batch"].values==metrics["Sim Batch"].values,\
                               metrics_table["Sim Number"].values==metrics["Sim Number"].values),10:] = metrics.values[0,2:]
    
    
    metrics_table_summary = metrics_table.iloc[:,7:].groupby(["Type of Monitoring","Appointments Interval","RPM Recall"]).mean()
                
    return metrics_table, metrics_table_summary


def single_compute_health_metrics(sim_params):
    crit_evol_matrix = np.load(sim_params["Crit Evol File"])
    crit_revs_matrix = np.load(sim_params["Crit Revs File"])
    deaths_matrix = np.load(sim_params["Deaths File"])
    icu_occup_matrix = np.load(sim_params["ICU Occup File"])
    pos_digns_matrix = np.load(sim_params["Pos Digns File"])
    
    num_of_deaths = np.sum(deaths_matrix)
    num_of_icu_entries = np.sum(np.ceil(np.sum(np.diff(icu_occup_matrix,axis=0),axis=0)/2))
    num_of_crit_reversals = np.sum(crit_revs_matrix)
    num_of_pos_digns = np.sum(pos_digns_matrix)
    num_of_crit_evols = np.sum(np.ceil(np.sum(crit_evol_matrix,axis=0)/2))
    
    crit_death_rate = num_of_deaths/num_of_crit_evols
    icu_death_rate = num_of_deaths/num_of_icu_entries
    pos_digns_rate = num_of_pos_digns/num_of_crit_evols
    crit_rev_rate = num_of_crit_reversals/num_of_crit_evols
    
    mean_icu_occup = np.mean(np.sum(icu_occup_matrix,axis=1))
    max_icu_occup = np.max(np.sum(icu_occup_matrix,axis=1))
    mean_icu_time = compute_mean_icu_time(icu_occup_matrix)
    max_num_pos_digns_day = np.max(np.sum(pos_digns_matrix,axis=1))
    
    metrics = pd.DataFrame(data=[sim_params["Sim Batch"],sim_params["Sim Number"],\
                                 crit_death_rate, icu_death_rate, pos_digns_rate,\
                                 crit_rev_rate, mean_icu_occup, max_icu_occup,\
                                 mean_icu_time, max_num_pos_digns_day]).transpose()
    
    metrics.columns = ["Sim Batch","Sim Number","Critical Death Rate","ICU Death Rate",\
                       "Early Diagnoses Rate", "Criticality Reversal Rate",\
                       "Mean ICU Occupancy", "Max ICU Occupacy", "Mean ICU Stay",\
                       "Max Number of Early Diagnoses"]

    
    return metrics

@ray.remote
def ray_compute_health_metrics(sim_params):
    crit_evol_matrix = np.load(sim_params["Crit Evol File"])
    crit_revs_matrix = np.load(sim_params["Crit Revs File"])
    deaths_matrix = np.load(sim_params["Deaths File"])
    icu_occup_matrix = np.load(sim_params["ICU Occup File"])
    pos_digns_matrix = np.load(sim_params["Pos Digns File"])
    
    num_of_deaths = np.sum(deaths_matrix)
    num_of_icu_entries = np.sum(np.ceil(np.sum(np.diff(icu_occup_matrix,axis=0),axis=0)/2))
    num_of_crit_reversals = np.sum(crit_revs_matrix)
    num_of_pos_digns = np.sum(pos_digns_matrix)
    num_of_crit_evols = np.sum(np.ceil(np.sum(crit_evol_matrix,axis=0)/2))
    
    crit_death_rate = num_of_deaths/num_of_crit_evols
    icu_death_rate = num_of_deaths/num_of_icu_entries
    pos_digns_rate = num_of_pos_digns/num_of_crit_evols
    crit_rev_rate = num_of_crit_reversals/num_of_crit_evols
    
    mean_icu_occup = np.mean(np.sum(icu_occup_matrix,axis=1))
    max_icu_occup = np.max(np.sum(icu_occup_matrix,axis=1))
    mean_icu_time = compute_mean_icu_time(icu_occup_matrix)
    max_num_pos_digns_day = np.max(np.sum(pos_digns_matrix,axis=1))
    
    metrics = pd.DataFrame(data=[sim_params["Sim Batch"],sim_params["Sim Number"],\
                                 crit_death_rate, icu_death_rate, pos_digns_rate,\
                                 crit_rev_rate, mean_icu_occup, max_icu_occup,\
                                 mean_icu_time, max_num_pos_digns_day]).transpose()
    
    metrics.columns = ["Sim Batch","Sim Number","Critical Death Rate","ICU Death Rate",\
                       "Early Diagnoses Rate", "Criticality Reversal Rate",\
                       "Mean ICU Occupancy", "Max ICU Occupacy", "Mean ICU Stay",\
                       "Max Number of Early Diagnoses"]

    
    return metrics
    

def compute_mean_icu_time(icu_occup_matrix):
    mean_icu_time = np.diff(np.nonzero(np.diff(icu_occup_matrix.flatten('F')))[0])
    mean_icu_time = mean_icu_time[mean_icu_time<=28]
    mean_icu_time = np.mean(mean_icu_time)
    return mean_icu_time
    

def compute_economic_metrics_table(econ_params, method="single"):
    # Initialize metrics table
    num_of_sims = 0
    for sim_batch in os.listdir("OUTPUTS"):
        for batch_dir in os.listdir("OUTPUTS/"+sim_batch):
            if os.path.isdir("OUTPUTS/"+sim_batch+"/"+batch_dir):
                num_of_sims += 1    
       
    cols = np.arange(0,econ_params["Simulation time in days"]+1).astype(str)
    cols = ["Cum cost at "+cols[i] for i in range(0,len(cols))]    
    cols = np.concatenate((["Sim Batch",\
                            "Sim Number",\
                            "Crit Evol File",\
                            "Crit Revs File",\
                            "Deaths File",\
                            "ICU Occup File",\
                            "Pos Digns File",\
                            "Type of Monitoring",\
                            "Appointments Interval",\
                            "RPM Recall",\
                            "Number of Doctors",\
                            "Total Cost",\
                            "ICU Cost Fraction",\
                            "Doctors Cost Fraction",\
                            "RPM Cost Fraction"],cols))         
       
    metrics_table = pd.DataFrame(data = np.zeros((num_of_sims, len(cols))),
                                 columns = cols)
        
    sim_count = 0
    for sim_batch in os.listdir("OUTPUTS"):
        batch_params = pd.read_csv("OUTPUTS/"+sim_batch+"/sim_params.csv")
        for batch_dir in os.listdir("OUTPUTS/"+sim_batch):
            if os.path.isdir("OUTPUTS/"+sim_batch+"/"+batch_dir):
                metrics_table.loc[sim_count,"Sim Batch"] = sim_batch
                metrics_table.loc[sim_count,"Sim Number"] = batch_dir
                metrics_table.loc[sim_count,"Crit Evol File"] = "OUTPUTS/"+sim_batch+"/"+batch_dir+"/"+"crit_evol_markers.npy"
                metrics_table.loc[sim_count,"Crit Revs File"] = "OUTPUTS/"+sim_batch+"/"+batch_dir+"/"+"crit_reversals.npy"
                metrics_table.loc[sim_count,"Deaths File"] = "OUTPUTS/"+sim_batch+"/"+batch_dir+"/"+"deaths.npy"
                metrics_table.loc[sim_count,"ICU Occup File"] = "OUTPUTS/"+sim_batch+"/"+batch_dir+"/"+"icu_occupancy.npy"
                metrics_table.loc[sim_count,"Pos Digns File"] = "OUTPUTS/"+sim_batch+"/"+batch_dir+"/"+"positive_diagnoses.npy"
                
                type_of_monitoring = batch_params.iloc[10,1]
                if type_of_monitoring == "NONE":
                    metrics_table.loc[sim_count,"Type of Monitoring"] = type_of_monitoring
                    metrics_table.loc[sim_count,"Appointments Interval"] = "NONE"
                    metrics_table.loc[sim_count,"RPM Recall"] = "NONE"
                elif type_of_monitoring == "LOCAL":
                    metrics_table.loc[sim_count,"Type of Monitoring"] = type_of_monitoring
                    metrics_table.loc[sim_count,"Appointments Interval"] = batch_params.iloc[11,1]
                    metrics_table.loc[sim_count,"RPM Recall"] = "NONE"
                elif type_of_monitoring == "REMOTE":
                    metrics_table.loc[sim_count,"Type of Monitoring"] = type_of_monitoring
                    metrics_table.loc[sim_count,"Appointments Interval"] = "NONE"
                    metrics_table.loc[sim_count,"RPM Recall"] = batch_params.iloc[12,1]
                      
                sim_count += 1
          
                
    # Compute metrics  
    if method == "single":
        for s in range(0, metrics_table.shape[0]):
            s_metrics = single_compute_econ_metrics(econ_params, metrics_table.iloc[s,:])
            
            metrics_table.iloc[np.logical_and(metrics_table["Sim Batch"].values==s_metrics["Sim Batch"].values,
                               metrics_table["Sim Number"].values==s_metrics["Sim Number"].values),10:] = s_metrics.values[0,2:].astype('float')
            print("Processed simulation {} / {}".format(s+1, metrics_table.shape[0]))
    elif method == "ray":
        s_metrics = []
        for s in range(0, metrics_table.shape[0]):
            s_metrics.append(ray_compute_econ_metrics.remote(econ_params, metrics_table.iloc[s,:]))
        metrics_list = ray.get(s_metrics)  

        for metrics in metrics_list:
            metrics_table.iloc[np.logical_and(metrics_table["Sim Batch"].values==metrics["Sim Batch"].values,\
                               metrics_table["Sim Number"].values==metrics["Sim Number"].values),10:] = metrics.values[0,2:].astype('float')
    
    
    metrics_table_summary = metrics_table.iloc[:,7:].groupby(["Type of Monitoring","Appointments Interval","RPM Recall"]).mean()
                
    return metrics_table, metrics_table_summary

def single_compute_econ_metrics(econ_params, sim_params):
    icu_occup_matrix = np.load(sim_params["ICU Occup File"])
    pos_digns_matrix = np.load(sim_params["Pos Digns File"])
    
    icu_days_cumcost = np.concatenate(([0],(econ_params["ICU cost per patient per day"]*\
                       np.int64(np.sum(np.cumsum(icu_occup_matrix,axis=0),axis=1)))/1000000))
    icu_days_totalcost = icu_days_cumcost[-1]
    
    if sim_params["Type of Monitoring"] == "NONE":
        num_of_doctors = 0
        cumcost = icu_days_cumcost
        totalcost = icu_days_totalcost
        icu_cost_fraction = 1
        doctors_cost_fraction = 0
        rpm_cost_fraction = 0
    elif sim_params["Type of Monitoring"] == "LOCAL":
        num_of_doctors = int(np.ceil(np.ceil(econ_params["Num of patients"]/int(\
                         sim_params["Appointments Interval"]))/econ_params[\
                         "Appointments per doctor per day"]))
        doctors_cumcost = (np.int64(np.arange(0,econ_params["Simulation time in days"]+1))*\
                          num_of_doctors*econ_params["Cardiologist salary per day"])/1000000    
        doctors_totalcost = doctors_cumcost[-1] 
                                                           
        cumcost = icu_days_cumcost + doctors_cumcost
        totalcost = icu_days_totalcost + doctors_totalcost
        
        icu_cost_fraction = icu_days_totalcost/totalcost
        doctors_cost_fraction = doctors_totalcost/totalcost
        rpm_cost_fraction = 0
        
    elif sim_params["Type of Monitoring"] == "REMOTE":
        num_of_doctors = int(np.ceil(np.max(np.sum(pos_digns_matrix,axis=1))/\
                         econ_params["Appointments per doctor per day"]))
        doctors_cumcost = (np.int64(np.arange(0,econ_params["Simulation time in days"]+1))*\
                          num_of_doctors*econ_params["Cardiologist salary per day"])/1000000    
        doctors_totalcost = doctors_cumcost[-1]  
        
        rpm_cumcost = (np.int64(np.arange(0,econ_params["Simulation time in days"]+1))*\
                      econ_params["Num of patients"]*\
                      econ_params["Remote monitoring cost per patient per day"]+\
                      econ_params["Num of patients"]*\
                      econ_params["Initial remote monitoring cost per patient"])/1000000    
        rpm_totalcost = rpm_cumcost[-1]  
        
        cumcost = icu_days_cumcost + doctors_cumcost + rpm_cumcost
        totalcost = icu_days_totalcost + doctors_totalcost + rpm_totalcost
        
        icu_cost_fraction = icu_days_totalcost/totalcost
        doctors_cost_fraction = doctors_totalcost/totalcost
        rpm_cost_fraction = rpm_totalcost/totalcost

        
    cols = np.arange(0,econ_params["Simulation time in days"]+1).astype(str)
    cols = ["Cum cost at "+cols[i] for i in range(0,len(cols))]    
    cols = np.concatenate((["Sim Batch",\
                            "Sim Number",\
                            "Number of Doctors",\
                            "Total Cost",\
                            "ICU Cost Fraction",\
                            "Doctors Cost Fraction",\
                            "RPM Cost Fraction"],cols))
    
    metrics = pd.DataFrame(data=np.concatenate(([sim_params["Sim Batch"],\
                                                 sim_params["Sim Number"],\
                                                 num_of_doctors,\
                                                 totalcost,\
                                                 icu_cost_fraction,\
                                                 doctors_cost_fraction,\
                                                 rpm_cost_fraction],   
                                                 cumcost))).transpose()
    metrics.columns = cols

    return metrics

@ray.remote
def ray_compute_econ_metrics(econ_params, sim_params):
    icu_occup_matrix = np.load(sim_params["ICU Occup File"])
    pos_digns_matrix = np.load(sim_params["Pos Digns File"])
    
    icu_days_cumcost = np.concatenate(([0],(econ_params["ICU cost per patient per day"]*\
                       np.int64(np.sum(np.cumsum(icu_occup_matrix,axis=0),axis=1)))/1000000))
    icu_days_totalcost = icu_days_cumcost[-1]
    
    if sim_params["Type of Monitoring"] == "NONE":
        num_of_doctors = 0
        cumcost = icu_days_cumcost
        totalcost = icu_days_totalcost
        icu_cost_fraction = 1
        doctors_cost_fraction = 0
        rpm_cost_fraction = 0
    elif sim_params["Type of Monitoring"] == "LOCAL":
        num_of_doctors = int(np.ceil(np.ceil(econ_params["Num of patients"]/int(\
                         sim_params["Appointments Interval"]))/econ_params[\
                         "Appointments per doctor per day"]))
        doctors_cumcost = (np.int64(np.arange(0,econ_params["Simulation time in days"]+1))*\
                          num_of_doctors*econ_params["Cardiologist salary per day"])/1000000    
        doctors_totalcost = doctors_cumcost[-1] 
                                                           
        cumcost = icu_days_cumcost + doctors_cumcost
        totalcost = icu_days_totalcost + doctors_totalcost
        
        icu_cost_fraction = icu_days_totalcost/totalcost
        doctors_cost_fraction = doctors_totalcost/totalcost
        rpm_cost_fraction = 0
        
    elif sim_params["Type of Monitoring"] == "REMOTE":
        num_of_doctors = int(np.ceil(np.max(np.sum(pos_digns_matrix,axis=1))/\
                         econ_params["Appointments per doctor per day"]))
        doctors_cumcost = (np.int64(np.arange(0,econ_params["Simulation time in days"]+1))*\
                          num_of_doctors*econ_params["Cardiologist salary per day"])/1000000    
        doctors_totalcost = doctors_cumcost[-1]  
        
        rpm_cumcost = (np.int64(np.arange(0,econ_params["Simulation time in days"]+1))*\
                      econ_params["Num of patients"]*\
                      econ_params["Remote monitoring cost per patient per day"]+\
                      econ_params["Num of patients"]*\
                      econ_params["Initial remote monitoring cost per patient"])/1000000    
        rpm_totalcost = rpm_cumcost[-1]  
        
        cumcost = icu_days_cumcost + doctors_cumcost + rpm_cumcost
        totalcost = icu_days_totalcost + doctors_totalcost + rpm_totalcost
        
        icu_cost_fraction = icu_days_totalcost/totalcost
        doctors_cost_fraction = doctors_totalcost/totalcost
        rpm_cost_fraction = rpm_totalcost/totalcost

        
    cols = np.arange(0,econ_params["Simulation time in days"]+1).astype(str)
    cols = ["Cum cost at "+cols[i] for i in range(0,len(cols))]    
    cols = np.concatenate((["Sim Batch",\
                            "Sim Number",\
                            "Number of Doctors",\
                            "Total Cost",\
                            "ICU Cost Fraction",\
                            "Doctors Cost Fraction",\
                            "RPM Cost Fraction"],cols))
    
    metrics = pd.DataFrame(data=np.concatenate(([sim_params["Sim Batch"],\
                                                 sim_params["Sim Number"],\
                                                 num_of_doctors,\
                                                 totalcost,\
                                                 icu_cost_fraction,\
                                                 doctors_cost_fraction,\
                                                 rpm_cost_fraction],   
                                                 cumcost))).transpose()
    metrics.columns = cols

    return metrics