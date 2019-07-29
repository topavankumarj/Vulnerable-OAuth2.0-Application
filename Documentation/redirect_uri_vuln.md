
# Stealing Users OAUTH Tokens via redirect_uri
> Open redirection on oauth redirect_uri which can lead to users 
oauth tokens being leaked to any malicious user.

#### Step 1: 
> Tamper the redirect_uri ad chnage it to attacker malicious website

```
Visit localhost:5000
```
#### Step 2: 
> Now use the Burp to intercept the request

```
Click on Signin with authorization and intercept the request. 

Tamper and change the redirect_uri value to malicious attaker website. 
```
#### Step 3: 
> Now Signin with registered credentials 
> Once the signin completed it will be redirected to malicious webiste with access token
