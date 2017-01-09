# Token Rotator Proxy
Proof of concept for a HTTP proxy that *pushes* rotating authentication tokens to an end point that is known to be under the control of legitimate requestors.  
## Motivation
A common requirement for container-based platforms is to be able to secure access to external resources by an inherence factor such as IP address as well as a knowledge factor such as a password (which might be shared with or stolen by an unauthorized entity).  

Although it is *possible* to map applications in the container world back to IP addresses in the infrastructure world (e.g. [Calico](https://www.projectcalico.org/)), it is not straightforward, and also it limits the velocity of the container platform to the speed of change in the world of firewalls and networks.  

This proof of concept is based on the idea that although we can't rely on anything in the network packets we *receive* from an application to identify it, we know that the application is identified by the URL on which it *receives* information.  

By configuring our authentication service to push transient tokens to an application's URL, we can therefore make the sharing of these tokens arbitrarily difficult, depending on the rate at which requests are made, and our strategy for token expiry.

## Overview
This proof-of-concept will create two subnets connected by an Nginx proxy server. The Nginx proxy offloads authentication decisions to an auth server that pushes fresh tokens to applications on their published URLs. An example client on the untrusted subnet attempts to connect to a secure service on the secure network, and the demo walkthrough shows how the example client is primed with a stale token, and can then connect with the fresh token sent by the auth server.

![Overview image](https://github.com/bendalby82/tokenrotatorproxy/blob/master/images/overview.png)

## Proof-of-Concept Walkthrough
### Requirements
Docker (tested on v1.12.5 on OSX 10.12.2)
### Setup
1. Clone this repository to your local machine  
2. Open a terminal inside the root `tokenrotatorproxy` folder
3. Run `./start-all.sh`
4. Run `./start-alpine-curl-untrustednet.sh` (keep this terminal somewhere handy)
5. Open a new terminal and run `docker logs -f authserver` to watch activity on the `authserver` as requests are made.
6. Open a new terminal and run `docker logs -f exampleclient` to watch activity on the `exampleclient` as requests are made.

### Verifying Setup
1. Open a web browser on [http://localhost:8012](http://localhost:8012) to verify the `exampleclient` is running.  
![exampleclient image](https://github.com/bendalby82/tokenrotatorproxy/blob/master/images/01-1-exampleclient-up.png)
2. Open a web browser on [http://localhost:8010](http://localhost:8010) to verify the `authserver` is running.  
![authserver image](https://github.com/bendalby82/tokenrotatorproxy/blob/master/images/01-2-authserver-up.png)
3. Open a web browser on [http://localhost:8081](http://localhost:8081) to verify the `testngx` proxy is running.  
![testngx image](https://github.com/bendalby82/tokenrotatorproxy/blob/master/images/01-3-proxy-up.png)
4. Open a web browser on [http://localhost:8011](http://localhost:8011) to verify the `secureservice` is running.  
![secureservice image](https://github.com/bendalby82/tokenrotatorproxy/blob/master/images/01-4-secureservice-up.png)


# Basic Test Calls  
(From within Alpine Curl)  

    #Valid request
    curl -X GET -H "Otpcode: abc456" -H "Cache-Control: no-cache" "http://testngx/"

    #Expired token
    curl -X GET -H "Otpcode: abc123" -H "Cache-Control: no-cache" "http://testngx/"

    #Prime client with an expired code
    curl -X POST -F "Otpcode=abc123" "http://exampleclient/tokencatcher"

# Notes  
Nginx - Beginner’s Guide  
http://nginx.org/en/docs/beginners_guide.html  

Docker Nginx Image  
https://hub.docker.com/_/nginx/  

Nginx Proxy Pass Directive  
http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_pass  

Nginx http auth request module  
https://nginx.org/en/docs/http/ngx_http_auth_request_module.html  

The Three R’s of Enterprise Security: Rotate, Repave, and Repair  
https://medium.com/built-to-adapt/the-three-r-s-of-enterprise-security-rotate-repave-and-repair-f64f6d6ba29d#.bxjtdmav4  
