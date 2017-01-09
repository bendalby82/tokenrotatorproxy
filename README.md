# Token Rotator Proxy
Proof of concept for a HTTP proxy that *pushes* rotating authentication tokens to an end point that is known to be under the control of legitimate requestors.  
## Contents


## 1. Overview
This proof-of-concept will create two subnets connected by an Nginx proxy server. The Nginx proxy offloads authentication decisions to an auth server that pushes fresh tokens to applications on their published URLs. An example client on the untrusted subnet attempts to connect to a secure service on the secure network, and the demo walkthrough shows how the example client is primed with a stale token, and can then connect with the fresh token sent by the auth server.

![Overview image](https://github.com/bendalby82/tokenrotatorproxy/blob/master/images/overview.png)

## 2. Proof-of-Concept Walkthrough
### 2.1 Requirements
Docker (tested on v1.12.5 on OSX 10.12.2)
### 2.2 Setup
1. Clone this repository to your local machine  
2. Open a terminal inside the root `tokenrotatorproxy` folder
3. Run `./start-all.sh`
4. Run `./start-alpine-curl-untrustednet.sh` (keep this Alpine terminal somewhere handy)
5. Open a new terminal and run `docker logs -f authserver` to watch activity on the `authserver` as requests are made.
6. Open a new terminal and run `docker logs -f exampleclient` to watch activity on the `exampleclient` as requests are made.

### 2.3 Verifying Setup
1. Open a web browser on [http://localhost:8012](http://localhost:8012) to verify the `exampleclient` is running.  
![exampleclient image](https://github.com/bendalby82/tokenrotatorproxy/blob/master/images/01-1-exampleclient-up.png)
2. Open a web browser on [http://localhost:8010](http://localhost:8010) to verify the `authserver` is running.  
![authserver image](https://github.com/bendalby82/tokenrotatorproxy/blob/master/images/01-2-authserver-up.png)
3. Open a web browser on [http://localhost:8081](http://localhost:8081) to verify the `testngx` proxy is running.  
![testngx image](https://github.com/bendalby82/tokenrotatorproxy/blob/master/images/01-3-proxy-up.png)
4. Open a web browser on [http://localhost:8011](http://localhost:8011) to verify the `secureservice` is running.  
![secureservice image](https://github.com/bendalby82/tokenrotatorproxy/blob/master/images/01-4-secureservice-up.png)

NOTE: Even though `secureservice` is accessible to the Docker host (your machine), it is not accessible to machines on the `untrustednet` subnet. You can verify this by attempting to curl to the `secureservice` from the Alpine terminal.
### 2.4 Running the Walkthrough
#### 2.4.1 First Call
1. We first make a call from `exampleclient` to `secureservice` via `testngx` proxy, without any tokens being present. We can do this by calling [http://localhost:8012/secure](http://localhost:8012/secure)  
2. We note that the call quickly fails:  
![exampleclient fails](https://github.com/bendalby82/tokenrotatorproxy/blob/master/images/02-example-client-first-time.png)  

#### 2.4.2 Second Call
1. We now 'prime the pump,' by sending a stale token from our Alpine terminal to the `exampleclient` container:  
  `curl -X POST -F "Otpcode=abc123" "http://exampleclient/tokencatcher"`
2. We should see a result like the following in our terminal:  
![alpine result](https://github.com/bendalby82/tokenrotatorproxy/blob/master/images/03-1-post-expired-token.png)  
3. If we are monitoring the logs for `exampleclient`, we will also see a message there:  
![exampleclient receives](https://github.com/bendalby82/tokenrotatorproxy/blob/master/images/03-2-exampleclient-receives.png)  
4. We now make another call from `exampleclient` to `secureservice` ([http://localhost:8012/secure](http://localhost:8012/secure)) - the call fails again, but we a get a different message:  
![exampleclient round two](https://github.com/bendalby82/tokenrotatorproxy/blob/master/images/03-3-exampleclient-secondtime.png)  
5. Behind the scenes, our `authserver` has posted a new token to the URL it holds for the `exampleclient` application. Note that it does this via DNS. We can again see this in the logs for the `exampleclient` container:  
![exampleclient more logs](https://github.com/bendalby82/tokenrotatorproxy/blob/master/images/03-4-exampleclient-receives.png)  

#### 2.4.3 Third Call
1. We make a final call from `exampleclient` ([http://localhost:8012/secure](http://localhost:8012/secure)) - this time the call succeeds:  
![exampleclient success](https://github.com/bendalby82/tokenrotatorproxy/blob/master/images/04-1-exampleclient-thirdtime.png)  
2. And we can see that the token has been accepted in the logs for `authserver` also:  
![authserver yes](https://github.com/bendalby82/tokenrotatorproxy/blob/master/images/04-2-authserver.png)  

## 3. Directions for Further Research
1. The proxy in the PoC uses an external auth server for making authentication decisions. It may be much more performant to run the auth function on the same machine, perhaps using something like the [Lua scripting capabilities](http://www.arpalert.org/haproxy-lua.html) of HA Proxy.  
2. How do we decide to expire a token? Strategies could include by time, and by usage. We could use a fixed count, or even a random count.  
3. The client in the PoC uses TinyDB as a trivial external data store, to allow for multiple instances to feed off the same pile of tokens. For a high volume system, we would need to think about things such as keeping the token pile at a certain depth, and perhaps giving grace periods on expiring tokens, so an application has enough time to receive new ones.  
4. The auth server in the PoC helpfully sends a new token when it thinks an application might need one. This could equally be a client request, so long as delivery is to a URL defined by the administrator, not provided by the client.
5. The auth server would need a management in real life.  
6. Can we create something like this PoC using an existing security framework such as OAuth 2.0?
7. The PoC requires any external client to implement a REST endpoint (`/tokencatcher`) to receive new tokens on. Is there a way of hiding this from applications by using some kind of container plugin strategy?

## 4. Motivation
A common requirement for container-based platforms is to be able to secure access to external resources by an inherence factor such as IP address as well as a knowledge factor such as a password (which might be shared with or stolen by an unauthorized entity).  

Although it is *possible* to map applications in the container world back to IP addresses in the infrastructure world (e.g. [Calico](https://www.projectcalico.org/)), it is not straightforward, and also it limits the velocity of the container platform to the speed of change in the world of firewalls and networks.  

This proof of concept is based on the idea that although we can't rely on anything in the network packets we *receive* from an application to identify it, we know that the application is identified by the URL on which it *receives* information.  

By configuring our authentication service to push transient tokens to an application's URL, we can therefore make the sharing of these tokens arbitrarily difficult, depending on the rate at which requests are made, and our strategy for token expiry.
## 5. References  
Docker Nginx Image  
https://hub.docker.com/_/nginx/  

Nginx Proxy Pass Directive  
http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_pass  

Nginx http auth request module  
https://nginx.org/en/docs/http/ngx_http_auth_request_module.html  

The Three R’s of Enterprise Security: Rotate, Repave, and Repair  
https://medium.com/built-to-adapt/the-three-r-s-of-enterprise-security-rotate-repave-and-repair-f64f6d6ba29d#.bxjtdmav4  
