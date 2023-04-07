#!/usr/bin/env python
# coding: utf-8

# In[29]:


import re
import pickle
import time
import numpy as np
import matplotlib.pyplot as plt
import csv
from matplotlib_venn import venn3


# In[4]:


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


# In[5]:


def read_mutation_detail(detail_str):
    mutation_class = re.findall("clazz=.*?,",detail_str)[0][6:-1]
    mutation_method = re.findall("method=.*?,",detail_str)[0][7:-1]
    mutator = re.findall("mutator=.*?]",detail_str)[0][8:-1]
    result = {}
    file_name = re.findall("filename=[a-zA-Z0-9_.\$]+", detail_str)[0][9:]
    line_number = re.findall("lineNumber=[0-9]+", detail_str)[0][11:]
    test_cases = re.findall("testsInOrder=.*]",detail_str)[0][14:-2]

    #since some test methods include arguments
    test_cases = test_cases.split(", ") # change here
    test_ids = test_cases# add here
    
    result["mutation_class"] = mutation_class
    result["mutation_method"]= mutation_method
    result["mutator"]=mutator

    result["file_name"]= file_name
    result["line_number"] = line_number
    return result, test_ids


# In[6]:


flag = False #skip abnormal mutants(runerror, memoryerror, nonviable) false means normal
mutated_info = []
records = []
first = True # first mutation result
further_analysis = []
for line_num, line in enumerate(Lines()):

    detected = len(re.findall("detected = ",line))!=0 and len(re.findall("detected = NON_VIABLE",line))==0
    mutation_details = re.findall("Running mutation MutationDetails \[.*\]",line)
    
    start = len(re.findall("stderr  : start: ", line))!=0
    EX = len(re.findall("stderr  : sourcethrow ",line))!=0
    fail = len(re.findall("stderr  : exception ",line))!=0
    
    if start:
        test_start = line.split("stderr  : start: ")[1]
        records.append([test_start[:-1]])
    if EX:
        # if records is empty it means PIT is collecting coverage in original run without mutations
        # it's possible that when PIT is installing (static blocks are loaded), there is sourcethrow
        # it might make the "seen" new exceptions not correct for a single test case, but the interpreted result is not influenced
        if len(records) > 0 and not isinstance(records[-1][-1],list):
            if " sourcethrow " in line:
                records[-1].append("EXSource " + line.split(" sourcethrow ")[1])   

    if fail:
        exception_record = re.split("stderr  : exception ",line)[1].split(" ")
        exception_record[-1] = exception_record[-1][:-1]
        records[-1].append(exception_record)
        if len(exception_record) == 1:
            print(line)
    if len(mutation_details)!=0:
        if not first:
            if flag:
                for i in range(len(mutated_info[-1]["test_cases"])):
                    mutated_info[-1]["test_cases"][i]["record"] = records[i]                 
            else:
                # mutation labeled as "TIMED_OUT","RUN_ERROR"
                mutated_info[-1]["status"]="abnormal"
        first = False
        flag = False
        
        # collect results from the last mutation
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
    mutation_class = re.findall("clazz=.*?,",detail_str)[0][6:-1]
    mutation_method = re.findall("method=.*?,",detail_str)[0][7:-1]
    mutator = re.findall("mutator=.*?]",detail_str)[0][8:-1]
    result = {}

    test_cases = re.findall("detected = KILLED by .*]",detail_str)[0][22:-2]

    test_cases = test_cases.split("], ")
    test_cases[-1]=re.findall(".*\(",test_cases[-1])[0]

    temp1 = [re.findall("\[class:.*?\]", _)[0][7:-1] for _ in test_cases]
    temp2=[]
    for _ in test_cases:

        _1 = re.findall("\[method:.*\(", _)
        _2 = re.findall("test-template:.*\(",_)
        if len(_1)!=0:
            temp2.append(_1[0][8:-1])
        else:
            temp2.append(_2[0][14:-1])
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


# In[8]:


counts=[]
for mutation in mutated_info:
    if mutation["status"]=="abnormal":
        continue
    count = 0
    for test_case in mutation["test_cases"]:
        if test_case["record"]==None:
            print(mutation["mutation_info"])
            print("Attention: there is None record")
            count+=1

            continue
        for record in test_case["record"]:
            if isinstance(record,list):
               
                count+=1
    counts.append(count)


# In[10]:


print("failing tests: " + str(sum(result2)))
assert(sum(result2) == sum(counts))


# In[11]:


#further process


# In[12]:


for mutation in mutated_info:
    if mutation["status"]=="abnormal":
        continue
    for test_case in mutation["test_cases"]:
        test_case["state"] = "pass"
        for record in test_case["record"]:
            # sanity check
            if isinstance(record[0], list):
                print(record)
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


# In[21]:


exceptions
# no double exceptions
# org.opentest4j.AssertionFailedError
# java.lang.AssertionError:
# AssertionErrors are from hamcrest
# org.mockito


# In[20]:


record_set = set()
for mutation in mutated_info:
    if mutation["status"]=="killed":
        for test_case in mutation["test_cases"]:
            if test_case["state"]=="fail" and test_case["Exception"]=="java.lang.AssertionError":
                record_set.add(" ".join(test_case["record"][-1]))
print(record_set)


# ## who will be labeled as test failure?

# org.opentest4j.AssertionFailedError  
# org.mockito  
# org.hamcrest.

# ## are there any throwables not ending with exception or error?

# # label defensive stuff

# In[24]:


for mutation in mutated_info:
    if mutation["status"]=="killed":
        for test_case in mutation["test_cases"]:
            if test_case["state"]=="fail":
                test_case["assertion_failure"]=False
                # fail;hamcrest;assertionError
                if len(test_case["record"][-1])>1 and test_case["record"][-1][1].startswith("org.hamcrest") and test_case["Exception"]=="java.lang.AssertionError":
                    test_case["assertion_failure"]=True
                if  "AssertionFailedError" in test_case["Exception"] or "mockito" in test_case["Exception"]:
                    test_case["assertion_failure"]=True
                # sanity check, shouldn't print
                if test_case["Exception"]=="java.lang.AssertionError" and test_case["assertion_failure"]==False:
                    print(test_case)
                record = test_case["record"]
                stack_trace = record[-1]
                # see no exceptions - exogenous crash
                if not record[-2].startswith("EX"):
                    continue
                    
                # memory error/stack overflow
                if len(stack_trace)==1:
                    # sanity check
                    print(record)
                    continue
                
                stack_line_num = stack_trace[4]
                stack_file = stack_trace[2]
                stack_exception = stack_trace[0]

                # matching
                for r in record[1:-1]:
                    throw_source = r
                    _, throw_exception, throw_line_num, throw_file = throw_source.split(" ")
                    throw_file = throw_file[:-1]
                    throw_exception = throw_exception.replace("/",'.')
                    if stack_line_num==throw_line_num and stack_file == throw_file and throw_exception ==stack_exception: 
                        if not _.startswith("EXTest"):
                            test_case["defensive"] = True
                        else:
                            test_case["assertion_failure"]=True      
                    


# In[26]:


with open('mutations.pickle', 'wb') as handle:
    pickle.dump(mutated_info, handle)    


# In[31]:


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
plt.savefig("commons-csv" +".png")
#     plt.tight_layout()
plt.clf()


# In[32]:


header = ['mutation_id','mutated_file','mutated_line_number',"mutator","mutation_state",
          'test_id',"test_state","exception","cause","loc"]
with open("commons-csv.csv", 'w', encoding='UTF8') as f:
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

