
# Generating 'N' number of access tokens usng 

### OAuth2 API makes it possible for users to grant access to their accounts with autorization server. When some user denies access for the application, all access_tokens are being revoked and become invalid. But not only access_tokens should be revoked, authorization codes (it is intermediate token used in OAuth2 Authorization Flow) must be revoked too. In this vulnerable application implementation does not revoke authorization code during access revocation. It may be exploited to restore access to user's account by malicious application after access revocation.

### Use the Burp to intercept the request 
  
#### Step 1: 
>  Visit Client applicaiton

```
Visit locahost:5000 and click on Signin with authorization.
```
#### Step 2: 
>  Signin with registerd credentails. 

```
Enter the credetials and click on signin.

Before you click on signin, intercept the request. 
```
#### Step 3: 
> Copy the Authorization_code and the URL
```
Intercept the callback request and copy the authorization code and the URL
Example: http://localhost:5000/callback?authorization_code=Z0FBQUFBQmN3RkFWMjJzNUxCdmVHZzZBaEI4Um82TUdNemJnWDhyRW1WeHRHSmZncS1jNmV1bEtlWmFGSU9aM053MWpaOGZ0TXBER3BESHhXQlNiV3lVVS1VNEo0ZTFuNzVkT0dlb1lKRUFsb0NoeUlEVXJNMl9pTS1UQ1U1cFJndmxMbldjZ0lIekhDRzYydy1EWUlNRXpmVEl0Sl94MURyN2RETHhmRS04dnVYQVk0LVZJYWF3Yms1UWg5VDUwdm1BcWtkempTWWRxQW5FNXJvSHJRZ3RuMU9yajFVRDJNdz09"
```
#### Step 4: 
>  By using Authorization_Exploit script we can generate 'N' number of access token .

```
Change the authorization code and URL in the script.
```
