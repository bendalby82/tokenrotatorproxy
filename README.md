# Token Rotator Proxy
Authenticating proxy that *pushes* tokens to an end point.  

# Basic Test Calls  
(From within Alpine Curl)  
    
    #Valid request
    curl -X GET -H "Otpcode: abc456" -H "Cache-Control: no-cache" "http://testngx/"
    
    #Expired token
    curl -X GET -H "Otpcode: abc123" -H "Cache-Control: no-cache" "http://testngx/" 
    
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


