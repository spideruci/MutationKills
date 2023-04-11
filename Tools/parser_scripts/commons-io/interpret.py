#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import pickle
import time
import numpy as np
import matplotlib.pyplot as plt
import csv
from matplotlib_venn import venn3


# In[2]:


# there exists a line that violate the text rule
# we separate it manually, it should've been two lines
# stderr  : Exception in thread "ThreadMonitor" start: [engine:junit-jupiter]/[class:org.apache.commons.io.FileSystemUtilsTestCase]/[method:testGetFreeSpaceWindows_String_ParseCommaFormatBytes()]
base = "info.txt"
def Lines():
    with open(base, encoding='utf-8',errors = "ignore") as inf:
        for line in inf:
            yield line
def get_killed(info):
    return [m for m in info if m["status"]=="killed"]
def get_survive(info):
    return [m for m in info if m["status"]=="survive"]
def get_abnormal(info):
    return [m for m in info if m["status"]=="abnormal"]


# In[3]:


def read_mutation_detail(detail_str):
    """
    extract info from "Running mutation ……"
    """
    mutation_class = re.findall("clazz=.*?,",detail_str)[0][6:-1]
    mutation_method = re.findall("method=.*?,",detail_str)[0][7:-1]
    mutator = re.findall("mutator=.*?]",detail_str)[0][8:-1]
    result = {}
    file_name = re.findall("filename=[a-zA-Z0-9_.\$]+", detail_str)[0][9:]
    line_number = re.findall("lineNumber=[0-9]+", detail_str)[0][11:]
    test_cases = re.findall("testsInOrder=.*]",detail_str)[0][14:-2]
    #since some test methods include arguments
    test_cases = test_cases.split("], ")
    for i in range(len(test_cases)-1):
        test_cases[i]+="]"
    result["mutation_class"] = mutation_class
    result["mutation_method"]= mutation_method
    result["mutator"]=mutator
    result["file_name"]= file_name
    result["line_number"] = line_number
    return result, test_cases


# In[6]:


flag = False #skip abnormal mutants(runerror, memoryerror, nonviable)
# ideally there would be no nonviable and runerror mutants
mutated_info = []
records = []
first = True
f = True
temp = None
further_analysis = []
for line_num, line in enumerate(Lines()):
    
    detected = len(re.findall("detected = ",line))!=0 and len(re.findall("detected = NON_VIABLE",line))==0
    mutation_details = re.findall("Running mutation MutationDetails \[.*\]",line)
    start = len(re.findall(" start: ", line))!=0
    
    EX = len(re.findall(" sourcethrow ",line))!=0 or len(re.findall(" testthrow ",line))!=0
    fail = len(re.findall("stderr  : exception ",line))!=0  
    
    if start:
        test_start = line.split(" start: ")[1]
        records.append([test_start[:-1]])

    if EX:
        if len(records) > 0 and not isinstance(records[-1][-1],list):
            if isinstance(records[-1][-1],list):
                continue
            if " sourcethrow " in line:
                records[-1].append("EXSource " + line.split(" sourcethrow ")[1])  
            else:
                records[-1].append("EXTest " + line.split(" testthrow ")[1])
            
    if fail:
        exception_record = re.split("stderr  : exception ",line)[1].split(" ")
        exception_record[-1] = exception_record[-1][:-1]
        records[-1].append(exception_record)
        
    if len(mutation_details)!=0:
        if not first:
            if flag:
                for i in range(len(mutated_info[-1]["test_cases"])):
                    try:
                        mutated_info[-1]["test_cases"][i]["record"] = records[i]       
                    except:
                        print(len(mutated_info))
                        rs = records
                        m = mutated_info[-1]
            else:
                mutated_info[-1]["status"]="abnormal"
        first = False
        flag = False

        records = []
        new_mutation = {}
        mutation_info,test_cases = read_mutation_detail(mutation_details[0])
        des = re.findall("description=.*?,",line)[0][12:-1]
        mutation_info["des"]=des
        new_mutation["mutation_info"] = mutation_info
        new_mutation["status"] = "survive"
        new_mutation["test_cases"] =[]
        for t in test_cases:
            new_mutation["test_cases"].append({"test_id":t,
                                               "Exception":None,"defensive":None, "state":None, "record":None})
        mutated_info.append(new_mutation)
    
    if(detected):
        flag=True 

if flag:
    for i in range(len(mutated_info[-1]["test_cases"])):
        mutated_info[-1]["test_cases"][i]["record"] = records[i]
else:
    mutated_info[-1]["status"]="abnormal"


# # Verify the number of killing tests the same as PIT

# In[7]:


def read_killed_mutation_detail(detail_str):
    """
    extract info from mutation result
    """
    mutation_class = re.findall("clazz=.*?,",detail_str)[0][6:-1]
    mutation_method = re.findall("method=.*?,",detail_str)[0][7:-1]
    mutator = re.findall("mutator=.*?]",detail_str)[0][8:-1]
    result = {}

    test_cases = re.findall("detected = KILLED by .*]",detail_str)[0][22:-2]

    test_cases = test_cases.split("], ")

    temp1 = [re.findall("\[class:.*?\]", _)[0][7:-1] for _ in test_cases]
    temp2=[]
    for _ in test_cases:

        _1 = re.findall("\[method:.*\(", _)
        _2 = re.findall("test-template:.*\(",_)
        _3 = re.findall("test-factory.*",_)
        if len(_1)!=0:
            temp2.append(_1[0][8:-1])
        elif len(_2)!=0:
            temp2.append(_2[0][14:-1])
        else:

            temp2.append(_3[0])
            
    test_cases = [temp1[i]+"."+temp2[i] for i in range(len(temp1))]
    result["mutation_class"] = mutation_class
    result["mutation_method"]= mutation_method
    result["mutator"]=mutator

    return result, test_cases
        
result2 = []
for line in Lines():
    detected_killed_info = re.findall("detected = KILLED by .*]",line)

    if len(detected_killed_info)!=0:
        mutation_info,test_cases = read_killed_mutation_detail(line)
        result2.append(len(test_cases))
        
        


# fix variation in the same line

# In[8]:


temp =0
counts=[]
flag=False
t =0
haha = 0
for mutation in mutated_info:
    flag=False
    if mutation["status"]=="abnormal":
        continue
    count = 0
    for test_case in mutation["test_cases"]:
        if test_case["record"]==None:
            print(mutation["mutation_info"])
            print("Attention: there is None record")
            temp = mutation
            count+=1
            continue
        for record in test_case["record"]:
            if isinstance(record,list):
                flag=True
                count+=1

    counts.append(count)
     


# In[11]:


print("failing test runs: " + str(sum(counts)))
# Attention, this script needs to be tuned, as there are anomalies in the output.
# needs to modify it manually!
assert(sum(result2) == sum(counts))


# In[12]:


for mutation in mutated_info:
    if mutation["status"]=="abnormal":
        continue
    for test_case in mutation["test_cases"]:
        test_case["state"] = "pass"
        for record in test_case["record"]:
            # a list means the detailed exception info
            if isinstance(record,list):
                test_case["state"] = "fail"
                test_case["Exception"] = record[0]
                mutation["status"]="killed"
                


# In[13]:


exceptions = dict()

for mutation in mutated_info:
    if mutation["status"]=="killed":
        for test_case in mutation["test_cases"]:
            if test_case["Exception"]!=None:
                e = test_case["Exception"]
                if e not in exceptions:
                    exceptions[e]=1
                else:
                    exceptions[e]+=1


# In[56]:


# org.opentest4j.AssertionFailedError
#mockito
# CHECK java.lang.AssertionError all are from source code
# no double exceptions

# for mutation in mutated_info:
#     if mutation["status"]=="killed":
#         for test_case in mutation["test_cases"]:
#             if test_case["state"]=="fail":
#                 if test_case["Exception"]=="java.lang.AssertionError":
#                     print(test_case["record"])


# In[14]:


exceptions


# In[15]:


for mutation in mutated_info:
    if mutation["status"]=="killed":
        for test_case in mutation["test_cases"]:
            if test_case["state"]=="fail":
                record = test_case["record"]
                stack_trace = record[-1]
                test_case["assertion_failure"]=False
                if "AssertionFailedError" in test_case["Exception"]:
                    test_case["assertion_failure"]=True
                    continue
                if "mockito" in test_case["Exception"]:
                    test_case["assertion_failure"]=True
                    continue
                if test_case["Exception"].startswith("org.apache.commons.io"):
                    test_case["defensive"]=True
                    continue
                if len(stack_trace)==1:
                    continue
                if not record[-2].startswith("EX"):
                    continue
                stack_line_num = stack_trace[4]
                stack_file = stack_trace[2]
                stack_exception = stack_trace[0]
                for r in record[1:-1]:
                    throw_source = r
                    _, throw_exception, throw_line_num, throw_file = throw_source.split(" ")
                    throw_file = throw_file[:-1]
                    throw_exception = throw_exception.replace("/",'.')
                
                    if stack_line_num ==throw_line_num and stack_file == throw_file and throw_exception ==stack_exception:
                        if not _.startswith("EXTest"):
                            test_case["defensive"] = True
                        else:
#                             print(test_case)
                            test_case["assertion_failure"]=True        
                    


# In[16]:


fail_num  =0
defensive_num = 0
for mutation in mutated_info:
    if mutation["status"] =="killed":
        for test_case in mutation["test_cases"]:
            if test_case["state"] =="fail":
                fail_num +=1
                if test_case["defensive"]:
                    defensive_num +=1


# In[17]:


with open('mutations.pickle', 'wb') as handle:
    pickle.dump(mutated_info, handle)


# In[18]:


with open('mutations.pickle', 'rb') as handle:
    data = pickle.load(handle)
a,b,c = set(),set(),set()
killed = get_killed(data)
survive = get_survive(data)
all_mutant = killed+survive
for index,mutant in enumerate(all_mutant):
    for test_case in mutant["test_cases"]:
        if test_case["state"]=="fail":
            if test_case["defensive"]==True:
                a.add(index)
            elif test_case["assertion_failure"]==True:
                b.add(index)
            else:
                c.add(index)
plt.figure(figsize=(10,10),dpi = 500)          
venn3(subsets = [a,b,c], set_labels = ('source code oracle', 'test code oracle',"trivial crash"))

plt.title("kiled mutants", fontdict={'fontsize': 14})
#     plt.legend(bbox_to_anchor=(0.8,0.8))
plt.savefig("commons-io" +".png")
#     plt.tight_layout()
plt.clf()


# In[19]:


header = ['mutation_id','mutated_file','mutated_line_number',"mutator","mutation_state",
          'test_id',"test_state","exception","cause","loc"]
with open("commons-io.csv", 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    row = [None]*9
    for index,mutation in enumerate(data):
        info = mutation["mutation_info"]
        if mutation["status"]=="abnormal":
            row = [None]*10
            row[0]=index
            row[1]= info["file_name"]
            row[2]=info["line_number"]
            row[3]=info["mutator"].split(".")[-1][:-7]
            row[4]="killed(noResource)"
            writer.writerow(row)
        if mutation["status"]=="killed":
            for test_case in mutation["test_cases"]:
                row = [None]*10
                row[0]=index
                row[1]= info["file_name"]
                row[2]=info["line_number"]
                row[3]=info["mutator"].split(".")[-1][:-7]
                row[4]="killed"
                row[5]=test_case["test_id"]

                if test_case["state"]=="pass":
                    row[6]="pass"
                else:
                    row[6]="fail"
                    EX = test_case["Exception"]
                    if isinstance(EX,list):
                        # shouldn't print here
                        print(EX)
                        EX = EX[0]
                    row[7]= EX
                    if test_case["assertion_failure"]==True:
                        row[8]="test_oracle"
                    elif test_case["defensive"]:
                        row[8]="source_oracle"
                    else:
                        row[8]="exogenous crash"
                    row[9]=test_case["record"][-1]
                writer.writerow(row)
                
        if mutation["status"]=="survive":
             for test_case in mutation["test_cases"]:
                row = [None]*9
                row[0]=index
                row[1]= info["file_name"]
                row[2]=info["line_number"]
                row[3]=info["mutator"].split(".")[-1][:-7]
                row[4]="survive"
                row[5]=test_case["test_id"]
                row[6]="pass"
                writer.writerow(row)

