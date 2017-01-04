#!/bin/bash

SERVERCONTAINER="testngx"
RUNNING=$(docker ps | grep -c $SERVERCONTAINER)
if [ $RUNNING -gt 0 ]; then
    docker rm -f $SERVERCONTAINER
    echo "$SERVERCONTAINER already exists and was removed."
else
    echo "No instance of $SERVERCONTAINER found."
fi

docker run --name $SERVERCONTAINER --network=proxynet -v /Users/bendalby/GitHub/EXPcontainers/ngxhtml:/data/upl:ro \
-v /Users/bendalby/GitHub/EXPcontainers/ngxconf/nginx.conf:/etc/nginx/nginx.conf:ro -d -p 8081:80 nginx
