#!/usr/bin/env python
# coding: utf-8

# In[20]:


import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import pandas as pd
import csv
import sys
import matplotlib.patches as mpatches

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


# In[37]:


labels = set()
df = pd.read_csv(name)
df = df[df["mutation_state"]!="killed(noResource)"]
df = df[df["cause"]=="exogenous crash"]

n = len(df)
d = {}
for index, row in df.iterrows():
    key = row["exception"] + " " +row["mutator"]
    if key in d:
        d[key]+=1
    else:
        d[key]=1

top3_pairs = sorted(d.items(), key=lambda x: x[1], reverse=True)[:3]
labels.add(top3_pairs[0][0])
labels.add(top3_pairs[1][0])
labels.add(top3_pairs[2][0])


# In[38]:


labels


# In[39]:


colors = ["#FF0000","#FF8000","#FFFF00","#80FF00","#00FFFF","#0080FF","#0000FF","#7F00FF","#FF00FF","#808080"]
hatches = ['/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*']
hatch_map ={}
color_map = {}
for index,label in enumerate(labels):
    color_map[label] = colors[index]
    hatch_map[label]=hatches[index]
color_map


# In[41]:


fig = plt.figure(figsize=(3,3),dpi = 100)
df = pd.read_csv(name)
df = df[df["mutation_state"]!="killed(noResource)"]
df = df[df["cause"]=="exogenous crash"]

n = len(df)
d = {}
for index, row in df.iterrows():
    key = row["exception"] + " " +row["mutator"]
    if key in d:
        d[key]+=1
    else:
        d[key]=1

top3_pairs = sorted(d.items(), key=lambda x: x[1], reverse=True)[:3]

base = 0
plt.bar([name],int(top3_pairs[0][1])/n,bottom = base, edgecolor = "black",color = color_map[top3_pairs[0][0]],hatch = hatch_map[top3_pairs[0][0]],label = top3_pairs[0][0])
base = base +int(top3_pairs[0][1])/n
plt.bar([name],int(top3_pairs[1][1])/n,bottom = base,edgecolor = "black",color = color_map[top3_pairs[1][0]],hatch = hatch_map[top3_pairs[1][0]],label = top3_pairs[1][0])
base = base +int(top3_pairs[1][1])/n
plt.bar([name],int(top3_pairs[2][1])/n,bottom = base,edgecolor = "black",color = color_map[top3_pairs[2][0]],hatch = hatch_map[top3_pairs[2][0]],label = top3_pairs[2][0])
base = base +int(top3_pairs[2][1])/n
plt.bar([name],1-base, bottom = base, color = 'white')
plt.xticks(rotation=60)
    
patches = []
for label, color in color_map.items():
    patches.append(mpatches.Patch(edgecolor="black",facecolor=color,hatch = hatch_map[label],label=label,fill=True))
# patches[9],patches[8]=patches[8],patches[9]

plt.legend(handles=patches)
# plt.legend()
plt.ylabel("proportion of exception-mutator pair")
plt.show()
    


# ## RQ4-2

# In[46]:


print(name + ": top 5 categories of 3rd party crash")
df = pd.read_csv(name)
df = df[df["mutation_state"]!="killed(noResource)"]
df = df[df["cause"]=="exogenous crash"]
d = dict()
for index, row in df.iterrows():
    key = row["exception"]
    if key in d:
        d[key]+=1
    else:
        d[key]=1
top3_pairs = sorted(d.items(), key=lambda x: x[1], reverse=True)[:5]
result = [(i[0],str(round(i[1]/len(df)*100,1))+"%") for i in top3_pairs]
for e, p in result:
    print(e + ": " + p)

