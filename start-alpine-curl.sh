#!/bin/bash

docker run --rm -it --network=proxynet --name=curlbox appropriate/curl /bin/ash
