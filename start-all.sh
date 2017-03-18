#!/bin/bash
UNTRUSTEDNET="untrustednet"
SECURENET="securenet"

RUNNING=$(docker network ls | grep -c $UNTRUSTEDNET)
if [ $RUNNING -gt 0 ]; then
    echo "$UNTRUSTEDNET already exists."
else
    docker network create --driver bridge $UNTRUSTEDNET 
    echo "No instance of $UNTRUSTEDNET found - created."
fi

RUNNING=$(docker network ls | grep -c $SECURENET)
if [ $RUNNING -gt 0 ]; then
    echo "$SECURENET already exists."
else
    docker network create --driver bridge $SECURENET 
    echo "No instance of $SECURENET found - created."
fi

SERVERCONTAINER="authserver"
RUNNING=$(docker ps -a | grep -c $SERVERCONTAINER)
if [ $RUNNING -gt 0 ]; then
    docker rm -f $SERVERCONTAINER
    echo "$SERVERCONTAINER already exists and was removed."
else
    echo "No instance of $SERVERCONTAINER found."
fi

docker run --name $SERVERCONTAINER --network=$UNTRUSTEDNET --restart=always -p 8010:80 \
-v $PWD/authserver/:/app -d jazzdd/alpine-flask

SERVERCONTAINER="exampleclient"
RUNNING=$(docker ps -a | grep -c $SERVERCONTAINER)
if [ $RUNNING -gt 0 ]; then
    docker rm -f $SERVERCONTAINER
    echo "$SERVERCONTAINER already exists and was removed."
else
    echo "No instance of $SERVERCONTAINER found."
fi

rm $PWD/exampleclient/otpcodedb.json

docker run --name $SERVERCONTAINER --network=$UNTRUSTEDNET --restart=always -p 8012:80 \
-v $PWD/exampleclient/:/app -d jazzdd/alpine-flask

SERVERCONTAINER="secureservice"
RUNNING=$(docker ps -a | grep -c $SERVERCONTAINER)
if [ $RUNNING -gt 0 ]; then
    docker rm -f $SERVERCONTAINER
    echo "$SERVERCONTAINER already exists and was removed."
else
    echo "No instance of $SERVERCONTAINER found."
fi

docker run --name $SERVERCONTAINER --network=$SECURENET --restart=always -p 8011:80 \
-v $PWD/secureservice/:/app -d jazzdd/alpine-flask

SERVERCONTAINER="testngx"
RUNNING=$(docker ps -a | grep -c $SERVERCONTAINER)
if [ $RUNNING -gt 0 ]; then
    docker rm -f $SERVERCONTAINER
    echo "$SERVERCONTAINER already exists and was removed."
else
    echo "No instance of $SERVERCONTAINER found."
fi

#http://stackoverflow.com/questions/34110416/docker-start-container-with-multiple-network-interfaces

docker create --name $SERVERCONTAINER --network=$UNTRUSTEDNET \
-v /$PWD/ngxhtml:/data/upl:ro \
-v $PWD/ngxconf/nginx.conf:/etc/nginx/nginx.conf:ro -p 8081:80 nginx

docker network connect $SECURENET $SERVERCONTAINER

docker start $SERVERCONTAINER

docker ps
