#!/bin/bash

docker build -t sgioldasis/elastest-spark-base:2.1.0 spark/base
docker build -t sgioldasis/elastest-spark-master:2.1.0 spark/master
docker build -t sgioldasis/elastest-spark-worker:2.1.0 spark/worker