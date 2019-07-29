import json
from pymongo import MongoClient
import uuid
#import ssl
import requests
from auth import verify_access_token
from flask import Flask, request, jsonify, redirect, render_template, Response,request, make_response, url_for
from functools import wraps
from werkzeug.security import gen_salt, generate_password_hash, check_password_hash 
import jwt
import datetime
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pavankumar'

client = MongoClient('db_mongo:27017')
db = client.OAuth


cred_PATH = 'http://localhost:5002/credentials'

ISSUER = 'sample-auth-server'

with open('/OAuth_Vuln/API_server/public.pem', 'rb') as f:
  public_key = f.read()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
      auth_header = request.headers.get('Authorization','')
      if auth_header:
        label, token = auth_header.split('Bearer ')
        verified = verify_access_token(token)
        if not verified:
          return jsonify({'error':'Invalid token!'})
      else: 
        return redirect('/login')
      return f(*args, **kwargs)
    return decorated

@app.route('/users', methods = ['GET'])
@token_required
def get_user():
  print(request.headers)
  cursor = db.Register.find()
  users = []
  for document in cursor:
    user_data = {}
    Name = document.get('Name')
    Email = document.get('Email')
    user_data = { 'Name': Name, 'email': Email}
    users.append(user_data)
  print(users)
  
  return json.dumps({
    'results': users
  })

# =================================== Client Login functions ==============================================

def token_required1(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = request.cookies.get('access_token')
    print('printing access token in token function ====> ',token)
    if not token:
      return jsonify({"messege":"Token missing in header"}), 401
    token_data = jwt.decode(token.encode(), key=app.config['SECRET_KEY'],algorithms='HS256')
    print('token data ========> ', token_data)
    try:
      current_user = db.Register.find_one({"ID":token_data.get('ID')})
      print("current user details", current_user) 
    except:
      return jsonify({"msg":"Invalid Token"})    
    return f(current_user, *args, **kwargs)
  return decorated

@app.route('/', methods = ['GET'])
def home():
  return render_template('Client_login.html')

@app.route('/client')
@token_required1
def main(user_id):
  print('==================== Client ===========================')
  print('after token function')
  access_token = request.cookies.get('access_token')
  print('access token ===> ', access_token)

  r = requests.get(cred_PATH, cookies = {
    'access_token': access_token
  })
  print('==================== after credentails fuction===========================')
  if r.status_code != 200:
    return json.dumps({
      'error': 'The resource server returns an error: \n{}'.format(
        r.text)
    }), 500
  print("data from credentials",r.text)
  print('*'*100)
  cli_data = json.loads(r.text).get('results')
  print('Credentails ============> ',cli_data)
  for cli in cli_data:
    print(cli)

  return render_template('Credentails.html', cli_data = cli_data)

@app.route("/client/login", methods = ['POST'])
def client_login():
  form = request.form
  username = form.get('username')
  password = form.get('password')
  if not username or not password:
    return jsonify({"messege":"sorry"})
  data = db.Register.find_one({"Email":username})
  if data:
    authenticated = check_password_hash(data.get('Password'), password)
    if not authenticated:
      return jsonify({"error":"Invaid creds!"})
    else:
      token = jwt.encode({"ID":data.get('ID'), "exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=30)}, key=app.config["SECRET_KEY"],algorithm='HS256')
      print("login successfull==========> ", token)
      response = make_response(redirect(url_for('main')))
      response.set_cookie('access_token', token)
      return response
  else:
    return jsonify({"messege":"No user found!"})

@app.route("/credentials", methods = ['GET'])
@token_required1
def cred(user_id):
  cred_data = []
  print('====================Client credentials function===========================')
  client.user_id = user_id.get('ID' ) 
  print("user ID===> ",user_id)
  if not db.Oauth2_cred.find_one({"ID":user_id.get('ID')}):
      print("User details ===> ",client.user_id)
      client.client_id = "testing.com"
      print("Client ID ===> ",client.client_id)
      if client.token_endpoint_auth_method == 'none':
          client.client_secret = ''
      else:
        client.client_secret = base64.b64encode(gen_salt(12).encode() + client.user_id.encode()).decode()
        db.Oauth2_cred.insert_one({
          "ID" : client.user_id,
          "Client_ID" : client.client_id,
          "Client_Secret" : client.client_secret
        })
        cli_data = {'Client_ID':client.client_id,'Client_Secret':client.client_secret}
        cred_data.append(cli_data)
        return json.dumps({'results': cred_data})
  else:
      client_data = db.Oauth2_cred.find_one({"ID":user_id.get('ID')})
      cli_data = {'Client_ID':client_data.get('Client_ID'),'Client_Secret':client_data.get('Client_Secret')}
      cred_data.append(cli_data)
      return json.dumps({'results': cred_data})


@app.route('/register', methods = ['GET'])
def home_register():
  return render_template('register.html')

@app.route("/client/register", methods = ['POST'])
def register():
  form = request.form
  name = form.get('name')
  email = form.get('email')
  password = form.get('password')
  print('registration details ===>',request.form)
  hashed_pwd = generate_password_hash(password, method='sha256')
  print(hashed_pwd)
  db.Register.insert_one({
    "ID" : str(uuid.uuid4()),
    "Name" : name,
    "Email" : email,
    "Password" : hashed_pwd
  })
  response = make_response(redirect(url_for('home')))
  return response

@app.route("/user_details", methods = ['GET'])
@token_required
def src_user():
  users_data = []
  auth_header = request.headers.get('Authorization','')
  label,token = auth_header.split('Bearer ')
  print('Token data ==========> ',token)
  token_data = jwt.decode(token, public_key, issuer = ISSUER,
  algorithm = 'RS256')  
  user_id = token_data.get("username")
  print("user_ID from token data=========> ",user_id)
  collection = db['Register']
  cursor = collection.find({})
  for document in cursor:
    print('Document data ===========> ',document)
    us_id = document.get('Email' )
    print('Email details from docu',us_id)
    if document.get('Email' ) == user_id:
      user_data = {'Name':document.get('Name' ),'Email':document.get('Email' ),'UUID':document.get('ID')}
      users_data.append(user_data)
      return json.dumps({'results': users_data})
  return jsonify({'message': 'User not found'})  
  
if __name__ == '__main__':
  #context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
  #context.load_cert_chain('domain.crt', 'domain.key')
  #app.run(port = 5000, debug = True, ssl_context = context)
  app.run(port = 5002, host='0.0.0.0', debug = True)
