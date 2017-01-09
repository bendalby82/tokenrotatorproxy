#!/bin/bash
UNTRUSEDNET="untrustednet"
SECURENET="securenet"

RUNNING=$(docker network ls | grep -c $UNTRUSEDNET)
if [ $RUNNING -gt 0 ]; then
    echo "$UNTRUSEDNET already exists."
else
    docker network create --driver bridge $UNTRUSEDNET 
    echo "No instance of $UNTRUSEDNET found - created."
fi

RUNNING=$(docker network ls | grep -c $SECURENET)
if [ $RUNNING -gt 0 ]; then
    echo "$SECURENET already exists."
else
    docker network create --driver bridge $SECURENET 
    echo "No instance of $SECURENET found - created."
fi

