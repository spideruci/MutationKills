#!/usr/bin/env python
# coding: utf-8

import re
import pickle
import time
import numpy as np
import matplotlib.pyplot as plt
import csv
from matplotlib_venn import venn3

base = "info.txt"
def Lines():
    with open(base, encoding='utf-8',errors = "ignore") as inf:
        for line in inf:
            yield line

def read_mutation_detail(detail_str):
    mutation_class = re.findall("clazz=.*?,",detail_str)[0][6:-1]
    mutation_method = re.findall("method=.*?,",detail_str)[0][7:-1]
    mutator = re.findall("mutator=.*?]",detail_str)[0][8:-1]
    result = {}
    file_name = re.findall("filename=[a-zA-Z0-9_.\$]+", detail_str)[0][9:]
    line_number = re.findall("lineNumber=[0-9]+", detail_str)[0][11:]
    test_cases = re.findall("testsInOrder=.*]",detail_str)[0][14:-2]
    #since some test methods include arguments
    test_cases = test_cases.split("), ")
    for i in range(len(test_cases)-1):
        test_cases[i]+=")"
        
    result["mutation_class"] = mutation_class
    result["mutation_method"]= mutation_method
    result["mutator"]=mutator

    result["file_name"]= file_name
    result["line_number"] = line_number

    return result, test_cases

flag = False #skip abnormal mutants(runerror, memoryerror, nonviable)
mutated_info = []
records = []
first = True
further_analysis = []
for line_num, line in enumerate(Lines()):
    detected = len(re.findall("detected = ",line))!=0 and len(re.findall("detected = NON_VIABLE",line))==0
    mutation_details = re.findall("Running mutation MutationDetails \[.*\]",line)
    
    start = len(re.findall("stderr  : start: ", line))!=0
    EX = len(re.findall("stderr  : sourcethrow ",line))!=0 or len(re.findall("stderr  : testthrow ",line))!=0
    fail = len(re.findall("stderr  : exception ",line))!=0
    
    if start:
        
        test_start = line.split("stderr  : start: ")[1]
        records.append([test_start[:-1]])
    if EX:
        if len(records) > 0 and not isinstance(records[-1][-1],list):
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
                    mutated_info[-1]["test_cases"][i]["record"] = records[i]           
                        
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

def read_killed_mutation_detail(detail_str):
    mutation_class = re.findall("clazz=.*?,",detail_str)[0][6:-1]
    mutation_method = re.findall("method=.*?,",detail_str)[0][7:-1]
    mutator = re.findall("mutator=.*?]",detail_str)[0][8:-1]
    result = {}

    test_cases = re.findall("detected = KILLED by .*]",detail_str)[0][22:-2]
    #since some test methods include arguments
    test_cases = test_cases.split("), ")
    # some test methods in different classes have the same name
    for test_case in test_cases:
        if (len(re.findall('.*\(',test_case))==0):
            print(test_case)
            raise AssertionError("there are something wrong in test methods")
    test_cases = [re.findall('.*\(',test_case)[0][:-1] for test_case in test_cases]
    test_cases = [ test_case if '[' not in test_case else test_case[0:test_case.index('[')] for test_case in test_cases]
    #check if test_methods have same method names
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

counts=[]
for mutation in mutated_info:
    if mutation["status"]=="abnormal":
        continue
    count = 0
    for test_case in mutation["test_cases"]:
        if test_case["record"]==None:
            print("Attention: there is None record")
            count+=1

            continue
        for record in test_case["record"]:
            if isinstance(record,list):
               
                count+=1
    counts.append(count)

print("failing test runs: " + str(sum(result2)))
assert(sum(result2) == sum(counts))

#further process

for mutation in mutated_info:
    if mutation["status"]=="abnormal":
        continue
    for test_case in mutation["test_cases"]:
        test_case["state"] = "pass"
        test_case["Exception"]=[]
        for record in test_case["record"]:
            # a list means the detailed exception info
            if isinstance(record,list):
                test_case["state"] = "fail"
                test_case["Exception"].append(record[0])
                mutation["status"]="killed"


exceptions = dict()

for mutation in mutated_info:
    if mutation["status"]=="killed":
        for test_case in mutation["test_cases"]:
            if len(test_case["Exception"])>0:
                e = test_case["Exception"][0]
                if e not in exceptions:
                    exceptions[e]=1
                else:
                    exceptions[e]+=1



# check AssertionError
# temp_assert = set()
# for mutation in mutated_info:
#     if mutation["status"]=="killed":
#         for test_case in mutation["test_cases"]:
#             if test_case["state"]=="fail":
#                 if test_case["Exception"][0]=="java.lang.AssertionError":
#                     temp_assert.add(" ".join(test_case["record"][-1]))
# temp_assert

# test failure
# junit
# com.google.common.truth.
# some of the java.lang.AssertionError are from junit
exceptions


# # label assertion failure

for mutation in mutated_info:
    if mutation["status"] =="survive":
        for test_case in mutation["test_cases"]:
            test_case["assertion_failure"] = False
    if mutation["status"]=="killed":
        for test_case in mutation["test_cases"]:
            if test_case["state"]=="fail":
                test_case["assertion_failure"]=None
                # defined in the project
                if test_case["Exception"][0].startswith("com.google.gson"):
                    test_case["defensive"]=True
                    continue
                # junit/truth
                if "junit" in test_case["Exception"][0] or ".truth." in test_case["Exception"][0]:
                    test_case["assertion_failure"]=True
                    continue
                
                if test_case["Exception"][0]=="java.lang.AssertionError" and test_case["record"][-1][1]=="org.junit.Assert":
                    test_case["assertion_failure"]=True
                    continue

                stack_trace = test_case["record"][-1]
                if len(stack_trace)==1:
                    continue
                stack_line_num = stack_trace[4]
                stack_file = stack_trace[2]
                stack_exception = stack_trace[0]
                for r in test_case["record"][1:-1]:
                    if isinstance(r, list):
                        continue
                    throw_source = r
                    _, throw_exception, throw_line_num, throw_file = throw_source.split(" ")
                    throw_file = throw_file[:-1]
                    throw_exception = throw_exception.replace("/",'.')
                    
                    if stack_line_num ==throw_line_num and stack_file == throw_file and throw_exception ==stack_exception:
                        if not _.startswith("EXTest"):
                            test_case["defensive"] = True
                        else:
                            test_case["assertion_failure"]=True     
                        continue
                if test_case["Exception"][0]=="java.lang.AssertionError" and test_case["defensive"]!=True:
                    # sanity check
                    print(test_case)
                

fail_num  =0
defensive_num = 0
for mutation in mutated_info:
    if mutation["status"] =="killed":
        for test_case in mutation["test_cases"]:
            if test_case["state"] =="fail":
                fail_num +=1
                if test_case["defensive"]:
                    defensive_num +=1
                    


# # denfensive failing  tests percetage


print("source code oracle: " + str(defensive_num))


with open('mutations.pickle', 'wb') as handle:
    pickle.dump(mutated_info, handle)
    
def get_killed(info):
    return [m for m in info if m["status"]=="killed"]
def get_survive(info):
    return [m for m in info if m["status"]=="survive"]
def get_abnormal(info):
    return [m for m in info if m["status"]=="abnormal"]

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

plt.title("killed mutants", fontdict={'fontsize': 14})
#     plt.legend(bbox_to_anchor=(0.8,0.8))
plt.savefig("gson" +".png")
#     plt.tight_layout()
plt.clf()


header = ['mutation_id','mutated_file','mutated_line_number',"mutator","mutation_state",
          'test_id',"test_state","exception","cause","loc"]
with open("gson.csv", 'w', encoding='UTF8') as f:
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
                        assert len(EX)==1
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
                row[4]="killed"
                row[5]=test_case["test_id"]
                row[6]="pass"
                writer.writerow(row)

