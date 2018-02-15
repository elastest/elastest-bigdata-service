# Development documentation of the ElasTest Big data Service (EBS)

## Architecture

![](images/ebs_architecture_diagram.png) 

**Spark Master/Worker**: Spark uses a master/worker architecture. There is a driver that talks to a single coordinator called master that manages workers in which executors run.
	

**HDFS Client**: The native client for the HDFS filesystem.  The client is pre-configured with the details of the HDFS Cluster. It allows the communication of the Spark Master/Workers with the HDFS filesystem.

**Alluxio Client**: The native client for the Alluxio filesystem interface.  The client is pre-configured with the details of the Alluxio Cluster. It allows the communication of the Spark Master/Workers with the Alluxio filesystem interface which abstracts other filesystems (local/HDFS etc).

## Development procedure

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

## Continuous Integration

The ElasTest CI is served by the ElasTest Jenkins platform (https://ci.elastest.io/jenkins/).

Regarding the EBS (elastest-bigdata-service) there are two pipelines:

	# The first pipeline is named "ebs" and is responsible for the building and publishing of the ebs docker imnages. 
	  The ebs pipeline is consisted from the following stages:
		- Container Prep
		- Run EDM docker-compose
		- Build REST API image - Package
		- Build Spark Base image - Package
		- Run EBS docker-compose
		- Unit tests
		- Cobertura
		- publish
	
	# The second pipeline is named "ebs-e2e-test" and is responsible to run the end to end tests which check the component integration with the ElasTest platform.
	  The ebs-e2e-test is consisted from the following stages:
		- launch elastest
		- Container Prep
		- docker conf
		- E2E tests
		- release elastest

	
