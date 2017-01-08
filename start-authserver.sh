#!/bin/bash

SERVERCONTAINER="authserver"
RUNNING=$(docker ps -a | grep -c $SERVERCONTAINER)
if [ $RUNNING -gt 0 ]; then
    docker rm -f $SERVERCONTAINER
    echo "$SERVERCONTAINER already exists and was removed."
else
    echo "No instance of $SERVERCONTAINER found."
fi

docker run --name $SERVERCONTAINER --network=untrustednet --restart=always -p 8010:80 \
-v $PWD/authserver/:/app -d jazzdd/alpine-flask

