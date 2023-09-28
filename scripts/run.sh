#!/bin/bash

docker build . -t scheduler
{ # try
    docker network create --driver=bridge main
} || { # catch
    echo "network ok"
}
docker run -d --name=scheduler --net=main -p 8001:8001 --hostname=scheduler scheduler
