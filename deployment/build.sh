#!/usr/bin/env bash

docker build -t map:0.0.1 .
docker run --name map -d -p 8080:80 map:0.0.1 &