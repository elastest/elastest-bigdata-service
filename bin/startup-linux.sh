#!/bin/bash

docker container prune -f
docker container rm -f 8b0d144567729cc3dd3d06b626bd2e68da6681b53f9c97b7e34ba96f5579ca0b
docker network create -d bridge elastest || echo "network already exists"


echo "Starting up using docker-compose"

docker-compose --project-name ebs up -d  --force-recreate

# docker-compose scale esnode=3
#docker volume create --driver local --opt o=size=20G,uid=1000 esdata1
#docker volume create --driver local --opt o=size=20G,uid=1000 esdata2
