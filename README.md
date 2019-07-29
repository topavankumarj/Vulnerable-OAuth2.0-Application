# Vulnerable-OAuth2.0-Application
>OAuth 2 is an authorization framework that enables applications to obtain limited access to user accounts on an HTTP service, such as Facebook, GitHub, and DigitalOcean. It works by delegating user authentication to the service that hosts the user account, and authorizing third-party applications to access the user account. OAuth 2 provides authorization flows for web and desktop applications, and mobile devices.

### Components

* Client application
    * It runs on 5000 port
* Authorization server
    * It runs on 5001 port
* Resource Server
    * It runs on 5002 port 

### Prerequisites

* Python 3
* MongoDB

[Getting Started](Documentation/Lab_Setup.md)
 
### List of Exploitations 

* [Stealing Users OAUTH Tokens via redirect_uri](Documentation/redirect_uri_vuln.md)
* [Authorization code not invalidated](Documentation/Authorization_code_not_invalidated.md)


## Start Labs 
* Pull vulnerable `oauth2.0` docker container

``` docker pull topavankumarj/oauth2.0_vuln_app```

* Run `mongoDB` database 

``` docker run -d --link db_mongo:db_mongo -p 5000:5000 -p 5001:5001 -p 5002:5002 topavankumarj/oauth2.0_vuln_app```

## For more information

### Slides: [ Security For OAuth : How To Handle Protected Data ](https://www.slideshare.net/PavanKumar1220/security-for-oauth-20-topavankumarj/PavanKumar1220/security-for-oauth-20-topavankumarj)