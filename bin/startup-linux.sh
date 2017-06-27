#!/bin/bash

echo "Starting up using docker-compose"

docker-compose up -d

# docker-compose scale esnode=3
#docker volume create --driver local --opt o=size=20G,uid=1000 esdata1
#docker volume create --driver local --opt o=size=20G,uid=1000 esdata2