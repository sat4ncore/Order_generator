#!/usr/bin/env bash

docker-compose up
docker build -t generator .
docker run -i --network generator_default --name=generator generator