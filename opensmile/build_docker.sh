#!/bin/bash
if [ $# -eq 1 ];
then
    docker_name=$1
else
    docker_name="acoustic-feat-debian-python39"
fi
docker build -t $docker_name .
