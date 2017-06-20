#!/bin/bash

echo "Tearing down using docker-compose"
docker-compose kill
docker-compose rm -f
