#!/bin/bash

NETNAME="untrustednet"
RUNNING=$(docker network ls | grep -c $NETNAME)
if [ $RUNNING -gt 0 ]; then
    echo "$NETNAME already exists."
else
    docker network create --driver bridge $NETNAME 
    echo "No instance of $NETNAME found - created."
fi

NETNAME="securenet"
RUNNING=$(docker network ls | grep -c $NETNAME)
if [ $RUNNING -gt 0 ]; then
    echo "$NETNAME already exists."
else
    docker network create --driver bridge $NETNAME 
    echo "No instance of $NETNAME found - created."
fi

