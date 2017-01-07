#!/bin/bash

SERVERCONTAINER="exampleclient"
RUNNING=$(docker ps -a | grep -c $SERVERCONTAINER)
if [ $RUNNING -gt 0 ]; then
    docker rm -f $SERVERCONTAINER
    echo "$SERVERCONTAINER already exists and was removed."
else
    echo "No instance of $SERVERCONTAINER found."
fi

docker run --name $SERVERCONTAINER --network=untrustednet --restart=always -p 8012:80 \
-v /Users/bendalby/GitHub/tokenrotatorproxy/exampleclient/:/app -d jazzdd/alpine-flask

