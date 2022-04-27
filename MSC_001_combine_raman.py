# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 16:06:05 2022

@author: s4142554

Aim: Script to combine all raman data into a single .csv file 
"""
#load modules
import re
import os
import pandas as pd


###############################################################################
script = os.path.basename(__file__).split('.',1)[0]
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
cwd = os.getcwd()
###############################################################################

#Input and Output folders
InputFolder = "//uq.edu.au/UQ-Research/BIOMARKERS-I0885/Methylation/MISC/MISC_001/MSC_001_Raman/"
ResultFolder = "//uq.edu.au/UQ-Research/BIOMARKERS-I0885/Methylation/MISC/MISC_001/MSC_001_Results"




def RamanRead(InputRamanFolder, ResultFolder):
    
    ramanfiles = os.listdir(InputFolder)

    #summary and results folder
    sumFile = os.path.join(script, ResultFolder, "summary.csv")
    raman_file = os.path.join(script, ResultFolder, "raman.csv")
    
    summary = [["sample", "date", "time"]]
    
    df_list = []
    
    for file in ramanfiles:
        
        name = file.split("_")[0]
        
        file = os.path.join(script, InputRamanFolder, file)
        
        df = []
        
        with open(file, 'r') as file:
            
            for line in file:
                if line.startswith("process"):
                    line = line.rstrip("\n").rsplit(' ')[6:]
                    date, time, am_pm = line
                    time = " ".join([time, am_pm])
                    summary.append([name, date, time])
                    
                else:
                    line = line.rstrip().split("\t")
                    if len(line) != 1:
                        df.append(line)
                    
            df = pd.DataFrame(df).set_index(0)
            df.columns = [name]
            
            df_list.append(df)
                    
    #merge all dfs in df_list according to index
    df = pd.concat(df_list, axis=1, join="inner")

    #turn summary into dataframe
    summary_df = pd.DataFrame(summary)

    #write to file
    df.to_csv(sumFile, sep=",", header=True, index=True)
    summary_df.to_csv(raman_file, sep=",", header=False, index=False)
                    
    
    return summary_df

###############################################################################

result = RamanRead(InputFolder, ResultFolder)


