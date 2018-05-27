#!/bin/bash

docker rm $(docker ps -a -q)

docker rmi api:latest

docker build -t api .

docker run api py.test -s
