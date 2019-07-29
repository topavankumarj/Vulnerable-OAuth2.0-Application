import cryptography
import jwt

ISSUER = 'sample-auth-server'

with open('/OAuth_Vuln/API_server/public.pem', 'rb') as f:
  public_key = f.read()

def verify_access_token(access_token):
  try:
    decoded_token = jwt.decode(access_token, public_key,
                               issuer = ISSUER,
                               algorithm = 'RS256',**{"verify_exp":False})
  # except (jwt.exceptions.InvalidTokenError,
  #         jwt.exceptions.InvalidSignatureError,
  #         jwt.exceptions.InvalidIssuerError,
  #         jwt.exceptions.ExpiredSignatureError)
  except Exception as e:
    print("Error",e)
    return True

  return True
