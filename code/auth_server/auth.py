import base64
import cryptography
import json
import jwt
import secrets
import time
from werkzeug.security import generate_password_hash, check_password_hash 
from pymongo import MongoClient

from cryptography.fernet import Fernet

#KEY = Fernet.generate_key()
KEY = b'YHD1m3rq3K-x6RxT1MtuGzvyLz4EWIJAEkRtBRycDHA='

ISSUER = 'sample-auth-server'
CODE_LIFE_SPAN = 600
JWT_LIFE_SPAN = 1800

client = MongoClient('db_mongo:27017')
db = client.OAuth

authorization_codes = {}

f = Fernet(KEY)

with open('/OAuth_Vuln/auth_server/private.pem', 'rb') as file:
  private_key = file.read()

def authenticate_user_credentials(username, password):
  data = db.Register.find_one({"Email":username})
  print(data)
  if data:
    authenticated = check_password_hash(data.get('Password'), password)
    if not authenticated:
      # data = {"error":"Invaid creds!"}
      return False
    else:
      return True
    #   token = jwt.encode({"ID":data.get('ID', None).encode('utf-8'), "exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=30)}, key=app.config["SECRET_KEY"],algorithm='HS256')
    #   data = {"token":token.decode("utf-8")}
    #   return data
  else:
    # data = {"error":"No user found!"}
    return False
  # data = {"message":"Invalid Credentials"}
  return False

def authenticate_client(client_id, client_secret):
  # print("Client_ID ==>" , client_id , "Client Scret==>",client_secret)
  data = db.Oauth2_cred.find_one({"Client_ID":client_id})
  # print(data.get)
  if data.get('Client_Secret') == client_secret:
    return True
  else:
    return False
  # if data:


def verify_client_info(client_id, redirect_url):
  return True

def generate_access_token(data):
  payload = {
    "username":data,
    "iss": ISSUER,
    "exp": time.time() + JWT_LIFE_SPAN
  }

  access_token = jwt.encode(payload, private_key, algorithm = 'RS256')

  return access_token

def generate_authorization_code(client_id, username):
  #f = Fernet(KEY)
  authorization_code = f.encrypt(json.dumps({
    "username":username,
    "client_id": client_id,
  }).encode())

  authorization_code = base64.b64encode(authorization_code, b'-_').decode().replace('=', '')

  expiration_date = time.time() + CODE_LIFE_SPAN

  authorization_codes[authorization_code] = {
    "username":username,
    "client_id": client_id,
    "exp": expiration_date
  }

  return authorization_code

def verify_authorization_code(authorization_code, client_id):
  #f = Fernet(KEY)
  record = authorization_codes.get(authorization_code)
  if not record:
    data = "False"
    return data

  client_id_in_record = record.get('client_id')
  username_in_record = record.get('username')
  exp = record.get('exp')

  if client_id != client_id_in_record:
    data = "False"
    return data

  # if exp < time.time():
  #   data = "False"
  #   return data

  # del authorization_codes[authorization_code]

  # return True
  return username_in_record
