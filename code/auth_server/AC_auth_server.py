import json
#import ssl
from urllib.parse import urlparse, parse_qsl, urlunparse, urlencode
from werkzeug.security import generate_password_hash, check_password_hash 

from auth import (authenticate_user_credentials, authenticate_client,
                  generate_access_token, generate_authorization_code, 
                  verify_authorization_code, verify_client_info,
                  JWT_LIFE_SPAN)
from flask import Flask, redirect, render_template, request,jsonify
from cryptography.fernet import Fernet

KEY = b'YHD1m3rq3K-x6RxT1MtuGzvyLz4EWIJAEkRtBRycDHA='

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'pavankumar'

# client = MongoClient('127.0.0.1:27017')
# # db = client.OAuth

f = Fernet(KEY)

@app.route('/auth')
def auth():
  # Describe the access request of the client and ask user for approval
  client_id = request.args.get('client_id')
  redirect_url = request.args.get('redirect_url')

  if None in [ client_id, redirect_url ]:
    return json.dumps({
      "error": "invalid_request"
    }), 400

  if not verify_client_info(client_id, redirect_url):
    return json.dumps({
      "error": "invalid_client"
    })

  return render_template('AC_grant_access.html',
                         client_id = client_id,
                         redirect_url = redirect_url)

def process_redirect_url(redirect_url, authorization_code):
  # Prepare the redirect URL
  url_parts = list(urlparse(redirect_url))
  queries = dict(parse_qsl(url_parts[4]))
  queries.update({ "authorization_code": authorization_code })
  url_parts[4] = urlencode(queries)
  url = urlunparse(url_parts)
  return url

@app.route('/signin', methods = ['POST'])
def signin():
  # Issues authorization code
  username = request.form.get('username')
  password = request.form.get('password')
  client_id = request.form.get('client_id')
  redirect_url = request.form.get('redirect_url')

  if None in [ username, password, client_id, redirect_url ]:
    return json.dumps({
      "error": "invalid_request"
    }), 400

  if not verify_client_info(client_id, redirect_url):
    return json.dumps({
      "error": "invalid_client"
    })

  if not authenticate_user_credentials(username, password):
    # return data
    return json.dumps({
      'error': 'access_denied'
    }), 401

  authorization_code = generate_authorization_code(client_id, username)

  url = process_redirect_url(redirect_url, authorization_code)

  return redirect(url, code = 303)

@app.route('/token', methods = ['POST'])
def exchange_for_token():
  # Issues access token
  authorization_code = request.form.get('authorization_code')
  client_id = request.form.get('client_id')
  client_secret = request.form.get('client_secret')
  redirect_url = request.form.get('redirect_url')
  
  if None in [ authorization_code, client_id, client_secret, redirect_url ]:
    return json.dumps({
      "error": "invalid_request"
    }), 400

  if not authenticate_client(client_id, client_secret):
    return json.dumps({
      "error": "invalid_client"
    }), 400
  
  data = verify_authorization_code(authorization_code, client_id)
  if data == "False":
    return json.dumps({
      "error": "access_denied"
    }), 400
  access_token = generate_access_token(data)
  
  return json.dumps({ 
    "access_token": access_token.decode(),
    "token_type": "JWT",
    "expires_in": JWT_LIFE_SPAN
  })


if __name__ == '__main__':
  #context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
  #context.load_cert_chain('domain.crt', 'domain.key')
  #app.run(port = 5000, debug = True, ssl_context = context)
  app.run(port = 5001, host='0.0.0.0', debug = True)
