# MutationKills
This project includes the experiment setUp for **To kIll a Mutant: An Empirical Study of Mutation Testing Kills**

# 1. Directory structure:
## 1.1 data/csvs:  
detailed csv data for mutation kills.  

data1.zip contain 5 csv files for xmlgraphics, jsoup, joda-time, gson, commons-validator. 

data2.zip contains 5 csv files for commons-csv, commons-io, commons-jexl, commons-lang, commons-text. 

### 1.1.1 rows in csv file:  
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


## 1.2 subject programs
We included the subject programs under this directory. All programs have already been configured to run the experiment. 

## 1.3 Tools

### 1.3.1 Tools/OracleTracker
This project aims at instrumenting the project's code for the instantation of Exception or Error. 

We placed the generated jar files, **source-throw.jar** and **test-throw.jar** in subject programs.

### 1.3.2Tools/PIT
This project is based on PIT 1.9.5 for running mutation testing.

We choose to print the each failing test's exception type, lineNumber, FileName, and MethodName on the scene. 
We also print the start of each test case.

### 1.3.3 Tools/parser_scripts
To parse the text report from PIT. All output from System Standard Error would be directed to the file **info.txt**.   
Place info.txt and interpret.py under the same directory
A csv file and a Venn Graph will be generated.

# 2. How to run the experiment for each subject program?

## 2.1 install PIT

Go to PIT_modified, run:
```
mvn clean install -Dmaven.test.skip
```

## 2.2 generate jar files to instrument source code/test code
go to oracle tracker, then run: 
```
mvn clean compile assembly:single
```
to distinguish the jar file for source code and test code, simply replace "testthrow " with "sourcethrow " in OracleVisitor.java at line 47.
We already placed both two jar files for the subject programs.

## 2.3 Run mutation testing
go to subject program's directory, run

```
mvn clean compile test-compile
java -jar "source-throw.jar" target/classes
java -jar "test-throw.jar" target/test-classes
mvn -Dmaven.main.skip pitest:mutationCoverage >info.txt 2>result.txt
```

for multi-module project like gson, instrument all source code/test code compiled files separtely. Then install it with bypassing recompilation. 

## 2.4 generate csv file and a venn graph

put the appropriate interpret.py file under subject project's directory, and run:

```
python interpret.py
```

# 3. A fast real example with a Docker Container

To demonstrate how the experiment was run, we configured a Docker image for **commons-validator**. The whole experiment should cost around 5 minutes.  


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


