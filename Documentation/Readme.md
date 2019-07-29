# OAuth Vulnerable Application Lab Setup

#### OAuth 2 is an authorization framework that enables applications to obtain limited access to user accounts on an HTTP service, such as Facebook, GitHub, and DigitalOcean. It works by delegating user authentication to the service that hosts the user account, and authorizing third-party applications to access the user account. OAuth 2 provides authorization flows for web and desktop applications, and mobile devices.

#### I have created own Client application, Authorization server and Resource Server. 

#### The Client applicaiton runs on 5000 port,  Authorization server on 5001 and Resource server on 5002.
#### 

## Prerequisites for the lab setup
* Python 3
* MongoDB

### Step 1: 
> Run the MongoDB service from system or docker hub

`Issue the following command to start MongoDB from system(For Ubuntu systems)`


```
sudo service mongod start 
```

`Issue the following command to start the mongo server instance`

```
docker run --name db_mongo -p 27017:27017 mongo
````
### Step 2:
>Create a database with name ‘OAuth’ 

```
use OAuth
```

### Step 3: Download the Vulnerable app 
> Download the vulnerable code app from git repo URL

```
github url
```

### Step 4: Installing and Setting up python 3 virtual environment

>Install Virtual environment and python3-venv package
```
sudo pip3 install virtualenv
apt-get install python3-venv
```
>create the virtual environment

```
python3 -m venv envpy3 
```

>Activate the created virtual environment

```
source envpy3/bin/activate 
```
> install required packages
```
pip install -r requirements.txt
```
### Step 5: Run the Vulnerable app
>Run an API server on the activated virtual environment
```
python ~/OAuth_vuln_app/AC/API_server/API_server.py
```
>Run an authorization server in an another terminal
```
source envpy3/bin/activate
python ~/OAuth_vuln_app/AC/API_server/AC_auth_server.py
```

>Run client application in another terminal
```
source envpy3/bin/activate
python ~/OAuth_vuln_app/AC/API_server/AC_client.py
```
### Step 6: Register the user in Authorization Server 
> Register and login in the API server for Client ID and Client Secret 

```
http://localhost:5002/register
```
>Now login with credentials
```
http://localhost:5002/
```
>Now copy the Client Secret and replace the CLIENT_SECRET in AC_Client.py

> Lab setup process is completed. 

#### Vulnerability Demo 

* Stealing Users OAUTH Tokens via redirect_uri
* Authorization code not invalidated
