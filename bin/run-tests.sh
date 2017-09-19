#!/bin/bash

echo "Running tests !!!"

docker-compose -p ebs exec rest-api tox
