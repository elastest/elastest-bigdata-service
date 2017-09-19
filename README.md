[![License badge](https://img.shields.io/badge/license-Apache2-green.svg)](http://www.apache.org/licenses/LICENSE-2.0)
[![Documentation badge](https://img.shields.io/badge/docs-latest-brightgreen.svg)](http://elastest.io/docs/)
[![Build Status](https://ci.elastest.io/jenkins/buildStatus/icon?job=elastest-bigdata-service/ebs-jenkinsfile/master)](https://ci.elastest.io/jenkins/job/elastest-bigdata-service/ebs-jenkinsfile/master)
[![codecov](https://codecov.io/gh/elastest/elastest-bigdata-service/branch/master/graph/badge.svg)](https://codecov.io/gh/elastest/elastest-bigdata-service)

[![][ElasTest Logo]][ElasTest]

Copyright © 2017-2019 [<member>]. Licensed under
[Apache 2.0 License].

elastest-bigdata-service
=================
The EBS is responsible for installing, uninstalling, starting, stopping and managing the different big data services available for the whole ElasTest platform.
The big data services under the responsibility of EBS are the following:

- Spark

## Prerequisites
- Install Docker Compose: https://docs.docker.com/compose/install/
- Install Git: https://www.atlassian.com/git/tutorials/install-git

### Clone the project
    # Clone the project to your system
    # Alternatively, you can download the zip file from Github and unzip it
    git clone https://github.com/elastest/elastest-bigdata-service.git

    # Change working directory to main project folder
    cd elastest-bigdata-service

### Prepare your environment

    # From main project folder
    
    # Make scripts executable
    chmod +x bin/* 
       
## Start this component using docker-compose
**Important**: This component depends on elastest-data-manager services. Please make sure elastest-data-manager component has been started before you start this component services. For instructions on how to start the elastest-data-manager component please refer to https://github.com/elastest/elastest-data-manager.

**Note**: your terminal need to be in the main project folder where the docker-compose.yml is located.

You can start this image using docker-compose. It will start the following:

- One Spark master
- One Spark worker

You have the possibility to scale the number of Spark worker nodes.

    # From main project folder
    
    # Start component
    bin/startup-linux.sh
    
    # View service status
    docker-compose -p ebs ps
    
    # View logs
    docker-compose -p ebs logs

Please note that it will take some time (in the order of several seconds - depending on your system) for all the services to be fully available. 

### Accessing the web interfaces
Each component provide its own web UI. Open you browser at one of the URLs below, where `dockerhost` is the name / IP of the host running the docker daemon. If using Linux, this is the IP of your linux box. If using OSX or Windows (via Boot2docker), you can find out your docker host by typing `boot2docker ip`. 

| Component               | Port                                               |
| ----------------------- | -------------------------------------------------- |
| Spark Master           | [http://localhost:8082](http://localhost:8082) |

### Scaling the number of instances
If you want to increase the number of Spark worker nodes in your cluster

    docker-compose -p ebs scale spark-worker=<number of instances>

### Accessing the spark-shell
Note: The Alluxio REST API is available at http://localhost:39999

You can try the following examples:

	# From main project folder
	
	# Get a shell inside Spark Master container
	docker exec -it spark-master /bin/bash

	# Change directory to spark project folder
	cd $SPARK_HOME

	# Upload file to Alluxio Local Filesystem
	alluxio fs copyFromLocal README.md /

	# Upload file to Alluxio HDFS
	alluxio fs copyFromLocal README.md /hdfs

	# List Alluxio HDFS root
	alluxio fs ls /hdfs
	# (You should be able to see the README.md file in the list)

	# Start spark-shell
	spark-shell
	
	# The following commands must be typed inside spark-shell at the "scala>" command prompt
	
	# Read text file from Alluxio Local Filesystem into Spark
	val s = sc.textFile("alluxio://alluxio-master:19998/README.md")
	
	# Count the lines
	s.count()
	
	# Double each line
	val double = s.map(line => line + '\n' + line)
	
	# Save a new file from Spark to Alluxio Local Filesystem
	double.saveAsTextFile("alluxio://alluxio-master:19998/README.double")
	
	# Read back the file we just saved (from Alluxio Local Filesystem into Spark)
	val d = sc.textFile("alluxio://alluxio-master:19998/README.double")
	
	# Count the lines - Result should be double than that of s.count()
	d.count()
	
	# Exit the shell
	:quit
	
	# You can repeat the above example with HDFS. 
	# HDFS is mounted on the /hdfs Alluxio path
	# The only difference for the user is to prepend above paths with /hdfs

	# For example:
	
	# Read text file from Alluxio HDFS into Spark
	val s = sc.textFile("alluxio://alluxio-master:19998/hdfs/README.md")
	
	# Save a new file from Spark to Alluxio HDFS
	double.saveAsTextFile("alluxio://alluxio-master:19998/hdfs/README.double")
	
	# Finally, exit the Spark Master container
	exit


### Submit a batch job using spark-submit
You can try the following examples:

	# From main project folder
	
	# Get a shell inside Spark Master container
	docker exec -it spark-master /bin/bash

	# Change directory to spark project folder
	cd $SPARK_HOME

	# Example 1: Submit a Java/Scala job locally
	spark-submit --class org.apache.spark.examples.SparkPi --master spark://spark-master:7077 examples/jars/spark-examples_2.11-2.1.1.jar 100
	
	# After some processing messages, you will be able to see the output:
	Pi is roughly 3.1422263142226314
	
	# Example 2: Submit a Python job locally
	spark-submit --master spark://spark-master:7077 examples/src/main/python/pi.py 10
	
	# After some processing messages, you will be able to see the output:
	Pi is roughly 3.143703

	# Example 3: Submit a Java/Scala job to cluster reading a file stored in Alluxio	
	
	# First use alluxio client to copy the executable to hdfs
	alluxio fs copyFromLocal $SPARK_HOME/examples/jars/spark-examples_2.11-2.1.1.jar /hdfs/spark-examples.jar

	# Now call spark-submit providing the following:
	# 	deploy-mode cluster - The job will run in the cluster. Output can be seen from cluster GUI
	# 	The hdfs path to the executable jar
	# 	The alluxio path to the input file
	spark-submit  --deploy-mode cluster --master spark://spark-master:7077 --class org.apache.spark.examples.HdfsTest hdfs://hdfs-namenode:9000/spark-examples.jar alluxio://alluxio-master:19998/README.md

	# After you finish, exit the Spark Master container:
	exit

## Stop this component using docker-compose

    # From main project folder
    
    # Teardown component
    bin/teardown-linux.sh

What is ElasTest
-----------------

This repository is part of [ElasTest], which is a flexible open source testing
platform aimed to simplify the end-to-end testing processes for different types
of applications, including web and mobile, among others.

The objective of ElasTest is to provide advance testing capabilities aimed to
increase the scalability, robustness, security and quality of experience of
large distributed systems. All in all, ElasTest will make any software
development team capable of delivering software faster and with fewer defects.

Documentation
-------------

The ElasTest project provides detailed [documentation][ElasTest Doc] including
tutorials, installation and development guide.

Source
------

Source code for other ElasTest projects can be found in the [GitHub ElasTest
Group].

News
----

Check the [ElasTest Blog] and follow us on Twitter [@elastestio][ElasTest Twitter].

Issue tracker
-------------

Issues and bug reports should be posted to the [GitHub ElasTest Bugtracker].

Licensing and distribution
--------------------------

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Contribution policy
-------------------

You can contribute to the ElasTest community through bug-reports, bug-fixes,
new code or new documentation. For contributing to the ElasTest community,
you can use GitHub, providing full information about your contribution and its
value. In your contributions, you must comply with the following guidelines

* You must specify the specific contents of your contribution either through a
  detailed bug description, through a pull-request or through a patch.
* You must specify the licensing restrictions of the code you contribute.
* For newly created code to be incorporated in the ElasTest code-base, you
  must accept ElasTest to own the code copyright, so that its open source
  nature is guaranteed.
* You must justify appropriately the need and value of your contribution. The
  ElasTest project has no obligations in relation to accepting contributions
  from third parties.
* The ElasTest project leaders have the right of asking for further
  explanations, tests or validations of any code contributed to the community
  before it being incorporated into the ElasTest code-base. You must be ready
  to addressing all these kind of concerns before having your code approved.

Support
-------

The ElasTest project provides community support through the [ElasTest Public
Mailing List] and through [StackOverflow] using the tag *elastest*.


<p align="center">
  <img src="http://elastest.io/images/logos_elastest/ue_logo-small.png"><br>
  Funded by the European Union
</p>

[Apache 2.0 License]: http://www.apache.org/licenses/LICENSE-2.0
[ElasTest]: http://elastest.io/
[ElasTest Blog]: http://elastest.io/blog/
[ElasTest Doc]: http://elastest.io/docs/
[ElasTest Logo]: http://elastest.io/images/logos_elastest/elastest-logo-gray-small.png
[ElasTest Public Mailing List]: https://groups.google.com/forum/#!forum/elastest-users
[ElasTest Twitter]: https://twitter.com/elastestio
[GitHub ElasTest Group]: https://github.com/elastest
[GitHub ElasTest Bugtracker]: https://github.com/elastest/bugtracker
[StackOverflow]: http://stackoverflow.com/questions/tagged/elastest
[<member>]: <member_url>
