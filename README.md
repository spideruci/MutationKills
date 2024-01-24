# MutationKills
This is an artifact package for ISSTA 2023 paper "To Kill A Mutant — An Empirical Study of Mutation Testing Kills".

For reusability, general data structure and other documentation for the experiment are introduced [here](Tools/README.md).

# Table of Contents

- [Getting Started](#getting-started)
    - [commons-validator](#commons-validator)
    - [commons-io](#commons-io)
    - [commons-csv](#commons-csv)
    - [joda-time](#joda-time)
    - [jsoup](#jsoup)
    - [commons-jexl](#commons-jexl)
    - [xmlgraphics](#xmlgraphics)
    - [commons-lang](#commons-lang)
    - [gson](#gson)
    - [commons-text](#commons-text)
   
- [Detailed Instructions](#detailed-instructions)
  - [RQ1](#rq1)
  - [RQ2](#rq2)
  - [RQ3](#rq3)
  - [RQ4](#rq4)


# Getting Started 

# Requirement
Requirement: 
1. Docker must be installed on your system.
2. Python 3 is required, with the following packages installed: matplotlib, pandas, and numpy. (Please note, some systems may have both Python 2 and Python 3 installed; be sure to use Python 3 in the command line for this project.)
3. To illustrate the experimental procedure, we have prepared 10 distinct Docker images, each corresponding to the 10 subject programs discussed in the study. The time required to run the experiment varies across different subject projects, as estimated in the table provided below.

To demonstrate how the experiment was run, we configured 10 separate Docker images for all 10 subject programs in the paper. Different subject projects' experiment requires a different amount of time to run, which is estimated in the table below.

Upon completion of these steps, two types of outputs will be generated in the current directory: a **data file** (named as 'ProjectName.csv') and a **Venn diagram** (named as 'ProjectName.png').

## Estimated Time

Please be aware that these time estimations are based on machines utilizing **ARM architecture**, as the experiment is expected to run **significantly faster** on such systems with the provided arm-based docker images. These estimates are derived from trials conducted in an arm-based Docker container on a **2021 MacBook Pro** utilizing the M1 Pro chip. 

If you're using other machines using x86 architecture, such as a 2016 MacBook Pro equipped with an Intel chip or Windows machine, you could still run the provided 10 arm-based docker images with the latest version of Docker. However, you may find that the required time to run the experiment can be considerably longer, because docker runs these in an emulated mode. For instance, it may take approximately 80 minutes to run the experiment for 'commons-validator' on Macbook Pro 2021.

To demonstrate the experiment we conducted in not limited to arm-based machines, we also configured one x86-based docker image for x86-based machines in the Detailed Instructions section for commons-validator. Procedures of building docker images for other subject programs are provided in the [Data Structure](Tools/README.md) section.



| subject name        | estimated amount of time                                                |
|---------------------|-------------------------------------------------------------|
| gson        |             10min                |
| commons-io     | 1h 40min                         |
| commons-lang | 2h                             |
| commons-csv            |         7min                                 |
| joda-time      |  1h 2min |     
| jsoup            |             44min              |
| xmlgraphics          |          7min                                         |
| commons-text          |     35min   |
| commons-jexl               |   2h 40min   (30 GB memory are expected to be occupied)       |
| commons-validator                 |  4min  (8min for surface book 2 machine)  |

## commons-validator

### For arm-based machines:

pull the image: 
```
docker pull qinfendeheichi/validator-replication:latest
```
run the container with a name (exp_container)
``` 
docker run --name exp_container qinfendeheichi/validator-replication
```
get the csv file and venn graph from the container to the current directory
```
docker cp exp_container:/commons-validator/project/commons-validator.csv .
docker cp exp_container:/commons-validator/project/commons-validator.png .
```

### For amd-based machines that use intel chips:

pull the image: 
```
docker pull qinfendeheichi/validator-replication-amd:latest
```
run the container with a name (exp_container)
``` 
docker run --name exp_container_amd qinfendeheichi/validator-replication-amd
```
get the csv file and venn graph from the container to the current directory
```
docker cp exp_container_amd:/commons-validator/project/commons-validator.csv .
docker cp exp_container_amd:/commons-validator/project/commons-validator.png .
```


## gson

```
docker pull qinfendeheichi/gson-replication:latest
```
```
docker run --name gson qinfendeheichi/gson-replication
```
```
docker cp gson:/gson/gson.csv .
docker cp gson:/gson/gson.png .
```

## commons-io

```
docker pull qinfendeheichi/commons-io-replication:latest
```
```
docker run --name commons-io qinfendeheichi/commons-io-replication
```
```
docker cp commons-io:/commons-io/project/commons-io.csv .
docker cp commons-io:/commons-io/project/commons-io.png .
```

## commons-lang

```
docker pull qinfendeheichi/commons-lang-replication:latest
```
```
docker run --name commons-lang qinfendeheichi/commons-lang-replication
```
```
docker cp commons-lang:/commons-lang/project/commons-lang.csv .
docker cp commons-lang:/commons-lang/project/commons-lang.png .
```


## commons-csv

```
docker pull qinfendeheichi/commons-csv-replication:latest
```
```
docker run --name commons-csv qinfendeheichi/commons-csv-replication
```
```
docker cp commons-csv:/commons-csv/project/commons-csv.csv .
docker cp commons-csv:/commons-csv/project/commons-csv.png .
```



## joda-time

```
docker pull qinfendeheichi/joda-time-replication:latest
```
```
docker run --name joda-time qinfendeheichi/joda-time-replication
```
```
docker cp joda-time:/joda-time/project/joda-time.csv .
docker cp joda-time:/joda-time/project/joda-time.png .
```

## jsoup

```
docker pull qinfendeheichi/jsoup-replication:latest
```
```
docker run --name jsoup qinfendeheichi/jsoup-replication
```
```
docker cp jsoup:/jsoup/project/jsoup.csv .
docker cp jsoup:/jsoup/project/jsoup.png .
```

## xmlgraphics

```
docker pull qinfendeheichi/xmlgraphics:latest
```
```
docker run --name xmlgraphics qinfendeheichi/xmlgraphics-replication
```
```
docker cp xmlgraphics:/xmlgraphics/project/xmlgraphics.csv .
docker cp xmlgraphics:/xmlgraphics/project/xmlgraphics.png .
```


## commons-text

```
docker pull qinfendeheichi/commons-text:latest
```
```
docker run --name commons-text qinfendeheichi/commons-text-replication
```
```
docker cp commons-text:/commons-text/project/commons-text.csv .
docker cp commons-text:/commons-text/project/commons-text.png .
```

## commons-jexl

```
docker pull qinfendeheichi/commons-jexl:latest
```
```
docker run --name commons-jexl qinfendeheichi/commons-jexl-replication
```
```
docker cp commons-jexl:/commons-jexl/project/commons-jexl.csv .
docker cp commons-jexl:/commons-jexl/project/commons-jexl.png .
```



# Detailed Instructions

In this section, we use this artifact to back up key claims described in the paper.  

From [Getting Started](#getting-started) section, we get a **csv file** (details explained [here](Tools/README.md#rows-in-csv-file)) and a **venn graph**. 
Now we are going to extract relevant data from the csv file to replicate the claims we made in the research paper. (The original data presented in the paper are [here](Tools/README.md#data-csvs))

The essential Python scripts for this project can be found in the 'tools/RQs' directory. Please ensure that the CSV file and Python scripts are situated in the same directory.

It's important to note that the experimental process may exhibit some level of flakiness, which could be due to:
1. Flaky tests or tests that result in flaky coverage.
2. Constraints in PIT resources, leading to flakiness when labeling certain TIMED_OUT or MEMORY_ERROR mutants.
The results obtained from the data analysis, as detailed in the study, are anticipated to be **very similar**, but not necessarily identical, to those achieved in a separate experimental run. This consistency underscores the overall conclusions and assertions presented in the paper.

## RQ1

How many tests execute the mutation and what are their failure rates?  
to get such data per project, run   
```
python RQ1.py commons-csv.csv
```
Replace "commons-csv.csv" with another csv file's name for another subject project.  

Results are expected to be generated for the relevant subject program corresponding to **Table 2** in the paper.  
As stated above, due to test flakiness, some data differences are expected but they should not deviate too much from what we reported in the paper.  
## RQ2

How does a test kill a mutant?  
```
python RQ2.py commons-csv.csv
```
corresponding to **Table 3** in paper.  
The Venn Graph is generated in the previous section that corresponds to Figure 3 in the paper.  

## RQ3

Are certain mutation operators more prone to certain test failure causes?
```
python RQ3.py commons-csv.csv
```
corresponding to **Table 4** in paper.  
## RQ4

What types of uncaught exceptions kill mutants
```
python RQ4.py commons-csv.csv
```
A figure corresponding to **Figure 4** in the paper is expected to be first presented. After closing the graph, data are expected to be shown corresponding to **Table 5** in the paper.

