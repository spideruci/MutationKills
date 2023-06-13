# MutationKills
This project provides an experimental replication setup and explanation for **To Kill a Mutant: An Empirical Study of Mutation Testing Kills**

# Table of Contents
- [Directory structure](#directory-structure)
  - [data-csvs](#data-csvs)
    - [interpret csv file](#rows-in-csv-file)
  - [subject programs](#subject-programs)
  - [Tools](#tools)
    - [Oracle Tracker](#tools-oracletracker)
    - [modified PIT](#tools-pit)
    - [parsing scripts](#tools-parser_scripts)
    - [RQs](#tools-rqs)

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

- [General Logics](#general-experimental-setups)


# Directory structure:
## data-csvs:  
detailed csv data for mutation kills presented in the paper.  

data2.zip contains 5 csv files for xmlgraphics, jsoup, joda-time, gson, commons-validator. 

data1.zip contains 5 csv files for commons-csv, commons-io, commons-jexl, commons-lang, commons-text. 

### rows in csv file:  
Each row in the csv file has these fields:  

| Field               | Description                                                 |
|---------------------|-------------------------------------------------------------|
| mutation_id         | Uniquely identifies a mutation                              |
| mutated_file        | The file where the mutation lives                           |
| mutated_line_number | The line number of the mutation                              |
| mutator             | Mutation operator                                           |
| mutation_state      | Killed/survived/killed(noResource). "killed(noResource)" means the mutation got killed due to running out of memory or time. |
| test_id             | Uniquely identifies a test case                             |
| test_state          | Pass/fail                                                   |
| exception           | The first exception that makes the test case fail           |
| cause               | Source oracle/test oracle/exogenous crash                   |
| loc                 | The location of the exception (first line of the stack trace)|


## subject programs
We included the subject programs under this directory. All programs have already been configured to run the experiment. 

## Tools

### Tools-OracleTracker
This project aims at instrumenting the project's code for the instantiation of Exceptions or Errors. 

We placed the generated jar files, **source-throw.jar** and **test-throw.jar** in subject programs.

### Tools-PIT
This project is based on PIT 1.9.5 for running mutation testing.

We choose to print each failing test's exception type, lineNumber, FileName, and MethodName on the scene. 
We also print the start of each test case.

### Tools-parser_scripts
To parse the text report from PIT. All output from System Standard Error would be directed to the file **info.txt**.   
Place info.txt and interpret.py under the same directory
A csv file and a Venn Graph will be generated.

### Tools-RQs
These are Python scripts that take a csv file as input and generate data for research questions presented in the paper.

# Getting Started 

# Requirement
Requirement: 
1. Docker must be installed on your system.
2. Python 3 is required, with the following packages installed: matplotlib, pandas, and numpy. (Please note, some systems may have both Python 2 and Python 3 installed; be sure to use Python 3 in the command line for this project.)
3. To illustrate the experimental procedure, we have prepared 10 distinct Docker images, each corresponding to the 10 subject programs discussed in the study. The time required to run the experiment varies across different subject projects, as estimated in the table provided below.

To demonstrate how the experiment was run, we configured 10 separate Docker images for all 10 subject programs in the paper. Different subject projects' experiment requires a different amount of time to run, which is estimated in the table below.

Upon completion of these steps, two types of outputs will be generated in the current directory: a **data file** (named as 'ProjectName.csv') and a **Venn diagram** (named as 'ProjectName.png').

## Estimated Time

Please be aware that these time estimations are based on machines utilizing **ARM architecture**, as the experiment is expected to run **significantly faster** on such systems with the provided linux-amd docker imageS. These estimates are derived from trials conducted in a Docker container on a **2021 MacBook Pro** utilizing the M1 Pro chip. 

If you're using other machines using amd architecture, such as a 2016 MacBook Pro equipped with an Intel chip or windows machine, you could run still run the provided 10 linux-amd dockers with the latest version of Docker. However, you may find that the required time to run the experiment can be considerably longer. For instance, it may take approximately 80 minutes to run the experiment for 'commons-validator'.

Alternatively, we also configured one linux-amd-based docker image for amd-based machines. Detailed instructions for building docker images for other subject programs are provided in [General Logics](#general-experimental-setups) section.



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
| commons-validator                 |  4min      |

## commons-validator

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

For amd-based machines that use intel chips:

pull the image: 
```
docker pull qinfendeheichi/validator-replication-amd:latest
```
run the container with a name (exp_container)
``` 
docker run --name exp_container_amd qinfendeheichi/validator-replication
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

From [Getting Started](#getting-started) section, we get a **csv file** (details explained [here](#rows-in-csv-file)) and a **venn graph**. 
Now we are going to extract relevant data from the csv file to replicate claims we made in the research paper. (The original data presented in the paper are [here](#data-csvs))

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

# General experimental setups
This is the general logics to run the experiment

## Install PIT

Go to PIT_modified, run:
```
mvn clean install -Dmaven.test.skip
```

## generate jar files to instrument source code/test code
go to Oracle Tracker, then run: 
```
mvn clean compile assembly:single
```
to distinguish the jar file for source code and test code, simply replace "testthrow " with "sourcethrow " in OracleVisitor.java at line 47.
We already placed both two jar files for the subject programs.

## Run mutation testing
go to subject program's directory, run

```
mvn clean compile test-compile
java -jar "source-throw.jar" target/classes
java -jar "test-throw.jar" target/test-classes
mvn -Dmaven.main.skip pitest:mutationCoverage >info.txt 2>result.txt
```

For a multi-module project like gson, instrument all source code/test code compiled files separtely. Then install it with bypassing recompilation. 

## generate csv file and a venn graph

put the appropriate interpret.py file under the subject project's directory, and run:

```
python interpret.py
```

# Special Situations

## Classifying test assertions

We classify that a test fails due to test code oracles based on exceptional information.  
For example, if a test fails with **org.opentest4j.AssertionFailedError**, we know exactly that the test fails due to a test code oracle.   
Sometimes, a single exception cannot help determine the cause. For example, a test could fail with "java.lang.AssertionError", it could either be from a source code oracle (by using Assert keyword or throwing new AssertionError), or from test code oracle(by using Assert keyword in test code, throwing new AssertionError in test code, or from testing frameworks).  

Thus we use information from the stack trace(only the first line). For example, 
```
Exception in thread "main" java.lang.AssertionError:
    at org.junit.Assert.fail(Assert.java:91)
```
We know that it is from junit api. 
However, textually search "truth.", "assertj", "junit", "mockito", etc in the stack trace does not always prove it's from a testing framework. For example, commons-text uses AssertJ assertions. The exceptions can sometimes be "java.lang.AssertionError". The top line in the stack trace would locate the closest exception context to the test code:
```
java.lang.AssertionError: 
Expecting code to raise a throwable.

	at org.apache.commons.text.AlphabetConverterTest.missingDoNotEncodeLettersFromEncodingTest(AlphabetConverterTest.java:120)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
```

However, in this case, we would know it fails due to a test code oracle because it's from test code.
