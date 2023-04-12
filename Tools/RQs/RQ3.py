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


# In[11]:


name = "commons-io.csv"
mutators = ['PrimitiveReturns',"Math","ConditionalsBoundary","NullReturnVals",
            "BooleanFalseReturnVals","VoidMethodCall","BooleanTrueReturnVals",
           "NegateConditionals","EmptyObjectReturnVals","Increments"]
print("Percentages of 3rd Party Crashes among all failing tests for different mutation operators")
text = ""
for mutator in mutators:
    text += mutator
    df = pd.read_csv(name)
    df = df[df["mutation_state"]!="killed(noResource)"]
    n1 = len(df[(df["mutator"] == mutator) & (df["cause"]=="exogenous crash")])
    n2 = len(df[(df["mutator"]== mutator) & (df["test_state"]=="fail")])
    text += ": "
    if n2 == 0:
        text += fetch(0)
    else:
        text += fetch(n1/n2) + "%"
    text += "\n"
print(text)


# In[ ]:




