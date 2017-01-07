#!/bin/bash

SERVERCONTAINER="secureservice"
RUNNING=$(docker ps -a | grep -c $SERVERCONTAINER)
if [ $RUNNING -gt 0 ]; then
    docker rm -f $SERVERCONTAINER
    echo "$SERVERCONTAINER already exists and was removed."
else
    echo "No instance of $SERVERCONTAINER found."
fi

docker run --name $SERVERCONTAINER --network=securenet --restart=always -p 8011:80 \
-v /Users/bendalby/GitHub/tokenrotatorproxy/secureservice/:/app -d jazzdd/alpine-flask

