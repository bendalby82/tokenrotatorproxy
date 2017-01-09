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
