from flask import render_template

from jwt import encode
from uuid import uuid4
from flask import Flask
from flask import session
from flask import request
from flask import redirect
from flask import make_response
from functools import wraps
import json
from flask_swagger_ui import get_swaggerui_blueprint
from authlib.flask.client import OAuth
import redis
import datetime
import requests
from flask import url_for
from six.moves.urllib.parse import urlencode
app = Flask(__name__)

app.secret_key = 'super secret key'
db = redis.Redis(host='client_redis', port=6381, decode_responses=True)

JWT_SECREATE_DATABASE="SECRET"
CDN_HOST = "http://localhost:3000"
JWT_SECRET="HELLO"
JWT_SESSION_TIME=30
SESSION_TIME = 180
WEB_HOST = "http://localhost:3001"
INVALIDATE = -1
SESSION_ID = "session-id"
USER_COUNTER = "user_counter"
USERLOGIN="userlogin"
USERPASSWORD="userpassword"
USER='user'
FILENAMES="filenames"

db.set("users:"+"admin","admin")


SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)

app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='vtXO9jaGP5PgdJ84661EPPHBp0PnBMxO',
    client_secret='uckIqaGr-qlqtMQPTys03eP5ARxLr_HJJw6wIn3Al_jUUWBCg3pxp7W8dFBQyHzu',
    api_base_url='https://dev-yp6kyw55.auth0.com',
    access_token_url='https://dev-yp6kyw55.auth0.com/oauth/token',
    authorize_url='https://dev-yp6kyw55.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)



@app.route('/swagger')
def swagger():
    return "/static/swagger.json"

@app.route('/')
def index():
    return render_template('login.html',WEB_HOST=WEB_HOST)

@app.route('/auth', methods=['POST'])
def auth():
    response = make_response('', 303)
    login = request.form.get('login')
    password = request.form.get('password')
    if db.get("users:"+login)==password:
        session_id = str(uuid4())
        #db.hset(user,SESSION_ID,session_id)
        #db.hset(session_id,FILENAMES,"")
        db.hset("session:"+session_id, "username", login)
        print("SESSION ID",session_id)
        response.set_cookie(SESSION_ID, session_id, max_age=SESSION_TIME)
        response.headers["Location"] = "/file_manage"
    else:
        response.set_cookie(SESSION_ID, "INVALIDATE", max_age=INVALIDATE)
        response.headers["Location"] = "/"
    return response

@app.route('/format_error',methods=["GET"])
def format_error():
    return render_template('format_error.html',WEB_HOST=WEB_HOST)

@app.route('/file_manage',methods=['GET'])
def upload():
    session_id = request.cookies.get(SESSION_ID)
    if session_id:
        #if session_id in session:
        #    fid, content_type = session[session_id]
        #else:
        #    fid, content_type = '', 'text/plain'

        content_type="application/pdf"
        #fileNames=getFileNames()
        #print(fileNames)
        login = db.hget("session:" + session_id, "username")
        allfids= db.hvals("files:"+login)
        print(allfids)
        download_tokens=[]
        filenames=[]
        for fidx in allfids:
            download_tokens.append(create_download_token(fidx).decode())
            filenames.append(db.hget("filename:"+login,fidx))
        #download_token = create_download_token(fid).decode('ascii')
        upload_token = create_upload_token().decode('ascii')
        return render_template("file_manage.html",allfids=allfids,content_type=content_type,CDN_HOST=CDN_HOST,upload_token=upload_token,download_tokens=download_tokens,WEB_HOST=WEB_HOST,filenames=filenames)
    return my_redirect("/")

def getFileNames():
    filesName=requests.get(CDN_HOST+"/files")
    return filesName.json()

def create_download_token(fid):
    exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_SESSION_TIME)
    return encode({"iss":"CLIENT", "exp":exp}, JWT_SECRET, "HS256")

def create_upload_token():
    exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_SESSION_TIME)
    return encode({"iss":"CLIENT", "exp":exp}, JWT_SECRET, "HS256")

@app.route('/rejestracja')
def rejestracja():
    return render_template('rejestracja.html',WEB_HOST=WEB_HOST)


@app.route('/userRegistration',methods=['POST'])
def userRegistration():

    login=request.form['login'].rstrip()
    password=request.form['password'].rstrip()
    db.set("users:"+login,password)
    return my_redirect("/")

@app.route('/error',methods=['GET'])
def wrong():
    return render_template('error.html')

@app.route('/logout')
def logout():
    response = make_response('', 303)
    response.set_cookie(SESSION_ID, "INVALIDATE", max_age=INVALIDATE)
    response.headers["Location"] = "/"
    return response


@app.route('/callback')
def uploaded():
    session_id = request.cookies.get(SESSION_ID)
    print("SESSION ID", session_id)
    fid = request.args.get('fid')
    err = request.args.get('error')

    filename=request.args.get('namefile')
    print(filename)
    if not session_id:
        return my_redirect("/")
    if err:
        if err=="Invalid format file":
            return my_redirect("/format_error")
        return f"<h1>APP</h1> Upload failed: {err}", 400
    if not fid:
        return f"<h1>APP</h1> Upload successfull, but no fid returned", 500
    #content_type = request.args.get('content_type','text/plain')
    #session[session_id] = (fid, content_type)
    new_fied_prefix = str(db.incr(JWT_SECREATE_DATABASE))
    new_fied= new_fied_prefix + fid
    login = db.hget("session:"+session_id,"username")
    db.hset("files:"+login,new_fied, fid)
    db.hset("filename:"+login,fid,filename)
    #filenames=db.hget(session_id,FILENAMES)
    #filenames.append()
    #print("FILENAMES")
    #print(filenames)
    #db.hset(session_id,FILENAMES,filenames)
    return my_redirect("/file_manage")

@app.route('/auth0_callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return my_redirect('/dashboard')

@app.route('/auth0_login')
def login():
    return auth0.authorize_redirect(redirect_uri='http://localhost:3001/auth0_callback')


def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      # Redirect to Login page here
      return my_redirect('/')
    return f(*args, **kwargs)

  return decorated

@app.route('/dashboard')
@requires_auth
def dashboard():
    print(session['profile'])
    userinfo=session['jwt_payload']
    print(userinfo)
    print(type(userinfo))
    response = make_response('', 303)
    session_id = str(uuid4())
    login=userinfo['name']
    db.hset("session:" + session_id, "username", login)
    print("SESSION ID", session_id)
    response.set_cookie(SESSION_ID, session_id, max_age=SESSION_TIME)
    response.headers["Location"] = "/file_manage"
    return response

@app.route('/auth0_logout')
def auth0_logout():
    # Clear session stored data
    session.clear()
    return redirect(auth0.api_base_url + '/v2/logout?' + "http%3A%2F%2localhost:3001%2Flogout&client_id=vtXO9jaGP5PgdJ84661EPPHBp0PnBMxO")


def my_redirect(location):
    response = make_response('', 303)
    response.headers["Location"] = location
    return response