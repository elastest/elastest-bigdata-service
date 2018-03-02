# Development documentation of the ElasTest Big data Service (EBS)

## Architecture

![](images/ebs_architecture_diagram.png) 

**Spark Master/Worker**: Spark uses a master/worker architecture. There is a driver that talks to a single coordinator called master that manages workers in which executors run.
	

**HDFS Client**: The native client for the HDFS filesystem.  The client is pre-configured with the details of the HDFS Cluster. It allows the communication of the Spark Master/Workers with the HDFS filesystem.

**Alluxio Client**: The native client for the Alluxio filesystem interface.  The client is pre-configured with the details of the Alluxio Cluster. It allows the communication of the Spark Master/Workers with the Alluxio filesystem interface which abstracts other filesystems (local/HDFS etc).

## Development documentation
This repository contains Dockerfiles to create the two used images, as well as the configuration files and source code for the whole cluster. Each Dockerfile along with any source code and conf files required to build it is contained in a separate folder: 

**rest-api**: Contains all the required source/configuration to build the EBS Healthcheck API image (Image name: elastest/ebs). 

**spark**: Contains all the required configuration templates to build the EBS spark node image (Image name: elastest/ebs-spark). The actual cluster topology is controlled by TORM, but a demonstration of how to create a cluster can be found in `docker-compose.yml`.

**e2e-test**: As per ElasTest specification, this is a python script that will use TORM API to generate a project containing a TJob that will pull a java spark project, build it, deploy it on the cluster and verify the results. 

### Development procedure

First build local tags of your images:

```bash
# Spark image:
cd spark
docker build -t elastest/ebs-spark:<your tag> .
# Api Image: 
cd ../rest-api
docker build -t elastest/ebs:<your tag> .
```

Then alter `docker-compose.yml` in the base project directory to reflect your local tag, and run `docker-compose up` to start a local version of the cluster (or follow the relevant documentation to start a whole ElasTest platform).
Once you verify your changes, revert docker-compose.yml and push your changes. CI (details below) will test the whole system, and generate/push the images to Docker Registry.


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
	
	# The second pipeline is named "ebs-e2e-test" and is responsible to run the end to end tests which check the component integration with the ElasTest platform. The ebs-e2e-test uses the ElasTest TORM API to create a project and TJob. The specific TJob will perform a full git pull/build/deploy pipeline of a demo project, as described in [user docs](https://github.com/elastest/elastest-bigdata-service/blob/master/docs/user-docs.md#using-ebs-from-a-tjob).

