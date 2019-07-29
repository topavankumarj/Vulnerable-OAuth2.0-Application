import requests

session = requests.Session()

headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0","Referer":"http://localhost:5001/auth?response_type=code&client_id=testing.com&redirect_url=http://localhost:5000/callback","Connection":"close","Accept-Language":"en-US,en;q=0.5","Accept-Encoding":"gzip, deflate"}

cookies = {"access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VybmFtZSI6InBhdmFuLmt1bWFyQHdlNDUuaW4iLCJpc3MiOiJzYW1wbGUtYXV0aC1zZXJ2ZXIiLCJleHAiOjE1NjM3ODE3OTAuNTEyNDI0Mn0.CACy4iwbRkS47lYIkN9tz8wfiNVTafItonphO6B6yBnK8u8M5VI3nIXL9197DsJn4-5oTXsPkWZXmcZfwX7WG0-Escol1mGeJ9YUIHAgPyUYRPsofTUxSRYrB5F40txV4lGdas0887L8TckiK4bhcFy2H_1HsfG-CU2T8xAjrK2Dk2Ihh898GuZMrH7i9IY91VBie0YcOGdsCYqfx0UyM2cO8EJDLyEiJvN_DSfXZ4sD3vA4X81nO0Up9VombSL5jzKyhFeg7JjG8LYMyroiPmlJU6pBleXMC0vmRg4JGmiH1Xv1D1c1415cFbasI1WdBkvU8-yONSn_7reSbW0ZMw"}
response = session.get("http://localhost:5000/", headers=headers, cookies=cookies)

print("Status code:   %i" % response.status_code)
print("Response body: %s" % response.content)

