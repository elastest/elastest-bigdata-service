# User documentation of the ElasTest Big data Service (EBS)

The ElasTest Big data Service is responsible for installing, uninstalling, starting, stopping and managing the different big data services available for the whole ElasTest platform.
The big data services under the responsibility of EBS are the following:

- Spark

## Features
The version 0.1 of the ElasTest Big data Service, provides the following features:

- Spark API to launch tasks (using lang clients / shell)
- Integration with Alluxio in EDM for importing/exporting data to/from HDFS


## How to run

### Prerequisites
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
       
### Start this component using docker-compose
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


## Basic usage

### Accessing the web interfaces
Each component provide its own web UI. Open you browser at one of the URLs below, where `dockerhost` is the name / IP of the host running the docker daemon. If using Linux, this is the IP of your linux box. If using OSX or Windows (via Boot2docker), you can find out your docker host by typing `boot2docker ip`. 

| Component               | Port                                               |
| ----------------------- | -------------------------------------------------- |
| Spark Master           | [http://localhost:8080](http://localhost:8080) |

### Scaling the number of instances
If you want to increase the number of Spark worker nodes in your cluster

    docker-compose -p ebs scale spark-worker=<number of instances>


