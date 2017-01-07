#!/bin/bash

SERVERCONTAINER="testngx"
RUNNING=$(docker ps -a | grep -c $SERVERCONTAINER)
if [ $RUNNING -gt 0 ]; then
    docker rm -f $SERVERCONTAINER
    echo "$SERVERCONTAINER already exists and was removed."
else
    echo "No instance of $SERVERCONTAINER found."
fi

#http://stackoverflow.com/questions/34110416/docker-start-container-with-multiple-network-interfaces

docker create --name $SERVERCONTAINER --network=untrustednet \
-v /Users/bendalby/GitHub/tokenrotatorproxy/ngxhtml:/data/upl:ro \
-v /Users/bendalby/GitHub/tokenrotatorproxy/ngxconf/nginx.conf:/etc/nginx/nginx.conf:ro -p 8081:80 nginx

docker network connect securenet $SERVERCONTAINER

docker start $SERVERCONTAINER