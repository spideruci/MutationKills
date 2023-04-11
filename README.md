# MutationKills
This project includes the experiment setUp for **To kIll a Mutant: An Empirical Study of Mutation Testing Kills**

# Table of Contents
- [Directory structure](#directory-structure)
  - [data-csvs](#data-csvs)
    - [interpret csv file](#rows-in-csv-file)
  - [subject programs](#subject-programs)
  - [Tools](#tools)
    - [Oracle Tracker](#tools-oracletracker)
    - [modified PIT](#tools-pit)
    - [parsing scripts](#tools-parser_scripts)

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
- [General Logics](#general-experimental-setups)


# Directory structure:
## data-csvs:  
detailed csv data for mutation kills.  

data2.zip contain 5 csv files for xmlgraphics, jsoup, joda-time, gson, commons-validator. 

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
This project aims at instrumenting the project's code for the instantation of Exception or Error. 

We placed the generated jar files, **source-throw.jar** and **test-throw.jar** in subject programs.

### Tools-PIT
This project is based on PIT 1.9.5 for running mutation testing.

We choose to print the each failing test's exception type, lineNumber, FileName, and MethodName on the scene. 
We also print the start of each test case.

### Tools-parser_scripts
To parse the text report from PIT. All output from System Standard Error would be directed to the file **info.txt**.   
Place info.txt and interpret.py under the same directory
A csv file and a Venn Graph will be generated.



# Getting Started

# Requirement
Requirement: Docker installed

To demonstrate how the experiment was run, we configured 10 separate Docker images for all 10 subject programs in the paper. Different subject project's experiment requires different amount of time to run, which is estimated in the table below.

After finishing this step, a **data file**(ProjectName.csv) and a **venn graph** (ProjectName.png) are expected to be generated in the current directory. 

## Estimated Time
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
| commons-jexl               |   2h 40min          |
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

# General experimental setups
This is the general logics to to run the experiment

## install PIT

Go to PIT_modified, run:
```
mvn clean install -Dmaven.test.skip
```

## generate jar files to instrument source code/test code
go to oracle tracker, then run: 
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

for multi-module project like gson, instrument all source code/test code compiled files separtely. Then install it with bypassing recompilation. 

## generate csv file and a venn graph

put the appropriate interpret.py file under subject project's directory, and run:

```
python interpret.py
```


