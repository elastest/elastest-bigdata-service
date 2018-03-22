#!/bin/bash


docker network create -d bridge elastest || echo "network already exists"


echo "Starting up using docker-compose"

docker-compose --project-name ebs up -d  --force-recreate

# docker-compose scale esnode=3
#docker volume create --driver local --opt o=size=20G,uid=1000 esdata1
#docker volume create --driver local --opt o=size=20G,uid=1000 esdata2
