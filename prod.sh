#!/bin/bash

port=4000
name=api

docker container stop $name
docker rm $(docker ps -a -q)

docker run -p $port:8081 --name $name $name:latest