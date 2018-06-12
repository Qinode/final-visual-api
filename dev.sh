#!/bin/bash

docker rm $(docker ps -a -q)

docker rmi api:latest

docker build -t api .

docker run --env API_ENV=dev api py.test -s -v
