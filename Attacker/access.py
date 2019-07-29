import requests

session = requests.Session()

paramsGet = {"authorization_code":"Z0FBQUFBQmROVnI2VUIycmtfZURvX1VkT1J4dkRKWjdKTlZ2R2NmRlJ5Vi1SN1ozbXkyZ1BBX2NjMktva0xVX3JjaWFVcXc1bTZ2ODdDWWZsaXhXeHI2Vm5McDdQMF8xd3NOUVNWTGlKYnNWUzBreDdVUDl4cmRjRE52TE5jZDVjRTBpYTNIMUdNS1dZUVdZTUgxUE90ZGF2ZGRyUTVEOUxRPT0"}

headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0","Referer":"http://51a6a3e1.ngrok.io//auth?response_type=code&client_id=testing.com&redirect_url=http://51a6a3e1.ngrok.io/callback","Connection":"close","Accept-Language":"en-US,en;q=0.5","Accept-Encoding":"gzip, deflate"}
response = session.get("http://localhost:5000/callback", params=paramsGet, headers=headers)

print("Status code:   %i" % response.status_code)
print("Response body: %s" % response.content)

