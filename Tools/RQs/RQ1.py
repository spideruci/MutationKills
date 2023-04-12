#!/usr/bin/env python
# coding: utf-8

# In[5]:


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


# In[8]:


if len(sys.argv) < 2:
    print("A csv file should be provided as the only argument")
    sys.exit(1)

name = sys.argv[1]
df = pd.read_csv(name )
# all mutants
df = df[df["mutation_state"]!="killed(noResource)"] # filter timed_out/runerror
all_mutants = len(df.groupby('mutation_id'))

# multi_test_mutants
mutation_counts = df.groupby('mutation_id')['test_id'].nunique()
mutation_ids = mutation_counts[mutation_counts >= 2].index.tolist()
df_selected = df[df['mutation_id'].isin(mutation_ids)]
multi_test_mutants = len(set(df_selected["mutation_id"]))

# survived multi_test_mutants
df_survive = df_selected[df_selected["mutation_state"]=="survive"]
multi_test_survived = len(set(df_survive["mutation_id"]))

# multi_test_wholly_killed
mutation_counts = df.groupby('mutation_id').agg({'test_id': 'nunique', 'test_state': lambda x: (x == 'fail').all()})
filtered_df = df[df['mutation_id'].isin(mutation_counts[(mutation_counts['test_id'] >= 2) & mutation_counts['test_state']].index)]
multi_test_wholly_killed = len(set(filtered_df["mutation_id"]))
partially_killed = multi_test_mutants-multi_test_wholly_killed- multi_test_survived

print("All Mutants: " +  str(commas(all_mutants))) 
print("Multi-Test Mutants: " +  str(commas(multi_test_mutants)) + " (" + fetch(multi_test_mutants/all_mutants) + "%)")
print("Survived: " + str(commas(multi_test_survived)) + " (" + fetch(multi_test_survived/all_mutants) + "%)")
print("Wholly Killed: " + str(commas(multi_test_wholly_killed)) + " (" + fetch(multi_test_wholly_killed/all_mutants) + "%) " )
print("Partially Killed: " + str(commas(partially_killed)) + " (" + fetch(partially_killed/all_mutants) + "%) " )

