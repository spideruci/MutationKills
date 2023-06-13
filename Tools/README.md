This page provides an explanation of the tools and data structure for the experiment

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
 - [General Logics](#general-experimental-setups)
 - [Docker Images](#docker-images)



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
We included the subject programs under this directory. All programs have already been configured with jar files for instrumentation and maven dependencies to run the experiment. 

## Tools

### Tools-OracleTracker
This project aims at instrumenting the project's code for the instantiation of Exceptions or Errors. 

We placed the generated jar files, **source-throw.jar** and **test-throw.jar** in subject programs.

### Tools-PIT
This project is based on PIT 1.9.5 for running mutation testing.

We choose to print each failing test's exception type, lineNumber, FileName, and MethodName on the scene to standard error output. 
We also print the start of each test case.

### Tools-parser_scripts
We did a post-analysis of the output of PIT. All output from System Standard Error would be directed to the file **info.txt**.   
To parse the text report from PIT, place info.txt and interpret.py under the same directory. Each script is uniquely customized for the subject program. 
A csv file and a Venn Graph will then be generated.

### Tools-RQs
These are Python scripts that take a csv file as input and generate data for individual research questions presented in the paper.


# General experimental setups
This is the general logic to run the experiment

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

# Docker Images:

Here are options to run the experiment in a docker container. We provided all arm-based docker images and 1 x86-based docker image for commons-validator. Here, we provided additional information to help create docker files for other subject programs.

This is an example of the instructions of a docker file for commons-valdiator. Four files, including pitest-1.9.5, interpret.py, and the pom.xml for the subject project, together with Dockerfile, should be placed under the same root directory.
The logics are as follows in the following four code blocks: making interpret.py an executable and installing Python dependencies, installing PIT dependency, installing the subject project's dependencies, running the experiment and parsing the results.

```
FROM python:3.9-slim-buster
COPY interpret.py /
RUN pip install numpy
RUN pip install matplotlib
RUN pip install matplotlib-venn
RUN pip install pyinstaller
RUN apt-get update && apt-get install -y binutils
RUN pyinstaller --onefile interpret.py
RUN ls -la

FROM maven:3.8.6-jdk-8 AS build
WORKDIR /commons-validator
COPY pom.xml /commons-validator/project/
COPY source-throw.jar /commons-validator/project/
COPY test-throw.jar /commons-validator/project/
COPY src/ /commons-validator/project/src/
COPY pitest-1.9.5/ /commons-validator/pitest-1.9.5/
COPY --from=0 /dist/interpret /commons-validator/project/
WORKDIR /commons-validator/pitest-1.9.5
RUN mvn clean install -Dmaven.test.skip

WORKDIR /commons-validator/project
RUN mvn dependency:go-offline

CMD cd /commons-validator/project\
    && mvn clean compile test-compile \
    && java -jar "source-throw.jar" target/classes \
    && java -jar "test-throw.jar" target/test-classes \
    && mvn "-Dmaven.main.skip" pitest:mutationCoverage >info.txt 2>result.txt \
    && ./interpret
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
