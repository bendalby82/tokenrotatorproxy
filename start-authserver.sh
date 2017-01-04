docker run --name authserver --network=proxynet --restart=always -p 8010:80 -v /Users/bendalby/GitHub/EXPcontainers/authserver/:/app -d jazzdd/alpine-flask

