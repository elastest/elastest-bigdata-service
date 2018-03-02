# User documentation of the ElasTest Big data Service (EBS)

## Features
The current version of ElasTest Big data Service, provides the following features:

- Spark API to launch tasks (using lang clients / shell)
- Integration with Alluxio in EDM for importing/exporting data to/from HDFS


## How to run
Elastest Big-Data Service (EBS) is integrated in ElasTest TORM. To execute EBS follow the [instructions to execute ElasTest](https://github.com/elastest/elastest-torm/blob/master/docs/index.md).


### Using EBS from a TJob

In order to use EBS from a TJob, you need to use the ElasTest\ebs-spark image. Anything executed inside that image, can directly access the whole ElasTest Big Data stack, both from EBS and EDM provided components. A demo Spark project is inside [ElasTest demo projects](https://github.com/elastest/demo-projects/tree/master/ebs-test) and the TJob code to use it is given below: 

```bash
git clone https://github.com/elastest/demo-projects.git


cd demo-projects/ebs-test

mvn package
rm -f big.txt
wget https://norvig.com/big.txt


#clean the pre-existing file
hadoop fs  -rmr /out.txt
hadoop fs -rmr /big.txt
hadoop fs -copyFromLocal big.txt /big.txt


spark-submit --class org.sparkexample.WordCountTask --master spark://spark:7077 /demo-projects/ebs-test/target/hadoopWordCount-1.0-SNAPSHOT.jar /big.txt

hadoop fs -getmerge /out.txt ./out.txt
head -10 out.txt
```

## Docker Images

The EBS docker images are the following:

	# ElasTest\ebs-spark: It contains the Apache spark open source cluster-computing framework and a git/maven toolset to build projects.
	# ElasTest\ebs: It contains the REST API which is responsible for the EBS health check.
