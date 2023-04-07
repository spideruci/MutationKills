# OracleTracker

This project place probes after the instantiation of exceptions in source code and test code.

To generate the jar file, run

```
mvn clean compile assembly:single test-compile
```

change the probe info in visitMethodInsn method in Oraclevisitor to distinguish probes for source code from probes for test code.

To instrument the project source code's bytecode

```
java -jar "source-throw.jar" target/classes
java -jar "test-throw.jar" target/test-classes
```


