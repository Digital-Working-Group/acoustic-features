#!/bin/bash

if [ $# -eq 1 ];
then
    container_name=$1
else
    container_name="acoustic-feat-debian-python39-ctr"
fi

if [ $# -eq 2 ];
then
    docker_name=$1
else
    docker_name="acoustic-feat-debian-python39"
fi

docker run -v $(pwd):/scripts -it --rm --name $container_name $docker_name bash