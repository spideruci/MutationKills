#!/usr/bin/env python
# coding: utf-8

# In[2]:


import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import pandas as pd
import csv
import sys

def fetch(data):
    """
    multiply the value by 100, round 2, then keep 4 digits
    get percentage data
    """
    data = f'{round(data * 100,2):05.2f}'
    return data

def commas(data):
    formatted_number = '{:,}'.format(data)
    return formatted_number

if len(sys.argv) < 2:
    print("A csv file should be provided as the only argument")
    sys.exit(1)
name = sys.argv[1]
df = pd.read_csv(name )
df = df[df["mutation_state"]!="killed(noResource)"] # filter timed_out/runerror

fail_MRs = len(df[df["test_state"]=="fail"])

T_MRs = len(df[df["cause"]=="test_oracle"])
T_test = len(set(df[df["cause"]=="test_oracle"]["test_id"]))

S_MRs = len(df[df["cause"]=="source_oracle"])
S_test = len(set(df[df["cause"]=="source_oracle"]["test_id"]))

crash_MRs = len(df[df["cause"]=="exogenous crash"])
crash_test = len(set(df[df["cause"]=="exogenous crash"]["test_id"]))

print("Number of all failed test runs:" + str(commas(fail_MRs)))
print("Failing due to Test Oracles: ")
print("\t" + "number of tests:" + str(commas(T_test)))
print("\t" + "test runs:" + str(commas(T_MRs)) + " (" + fetch(T_MRs/fail_MRs) + "%) ")
print("Failing due to Source oracles: " + str(commas(S_test)))
print("\t" + "test runs:" + str(commas(S_MRs)) + " (" + fetch(S_MRs/fail_MRs) + "%) ")
print("Failing due to Crashes: " + str(commas(S_test)))
print("\t" + "test runs:" + str(commas(crash_MRs)) + " (" + fetch(crash_MRs/fail_MRs) + "%) ")


# In[10]:




