from flask import  Flask, request, jsonify,redirect, make_response ,send_file

import sys, os
import redis

from jwt import decode, InvalidTokenError
from uuid import uuid4
from flask import Flask
from flask import request

JWT_SECRET="HELLO"
SESSION_ID = "session-id"

app = Flask(__name__)

db = redis.Redis(host='serwer_redis', port=6380, decode_responses=True)
db.flushdb()


DIR_PATH = "files/"
FILE_COUNTER = "file_counter"
ORG_FILENAME = "org_filename"
NEW_FILENAME = "new_filename"
PATH_TO_FILE = "path_to_file"
FILENAMES = "filenames"
FILENAMESDATABASE="filenamesDATABASE"

PORT = int(os.environ.get("PORT", 5000))
print(PORT)

@app.route('/')
def index():
    return "OK!"

@app.route('/files')
def show_articles():
    files = db.hvals(FILENAMES)
    response=jsonify(my_files=files)
    return response


@app.route('/download/<fid>')
def download(fid):
    token = request.headers.get('token') or request.args.get('token')
    if len(fid) == 0:
        return '<h1>CDN</h1> Missing fid', 404
    if token is None:
        return '<h1>CDN</h1> No token', 401
    if not valid(token):
        return '<h1>CDN</h1> Invalid token', 401
    payload = decode(token, JWT_SECRET)
    if payload.get('fid', fid) != fid:
        return '<h1>CDN</h1> Incorrect token payload', 401

  #content_type = request.headers.get('Accept') or request.args.get('content_type')
  #with open('/tmp/' + fid, 'rb') as f:
  #  d = f.read()
  #  response = make_response(d, 200)
  #  response.headers['Content-Type'] = content_type
  #  return response
    article_hash = db.hget(fid,FILENAMESDATABASE)
    full_name = db.hget(article_hash, PATH_TO_FILE)
    org_filename = db.hget(article_hash, ORG_FILENAME)
    if (full_name != None):
        try:
            return send_file(full_name, attachment_filename=org_filename)
        except Exception as e:
            print(e, file=sys.stderr)

    return org_filename, 200
'''
def download_article(name):
    article_hash=db.hget(name,FILENAMESDATABASE)
    full_name = db.hget(article_hash, PATH_TO_FILE)
    org_filename = db.hget(article_hash, ORG_FILENAME)
    if(full_name != None):
        try:
            return send_file(full_name, attachment_filename = org_filename)
        except Exception as e:
            print(e, file = sys.stderr)

    return org_filename, 200
'''
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response



app.config["ALLOWED_FORMAT"]=["PDF"]

def allowed_image(filename):
    if not "." in filename:
        return False
    ext=filename.rsplit(".",1)[1]
    if ext.upper() in app.config["ALLOWED_FORMAT"]:
        return True
    else:
        return False

@app.route("/upload",methods=["POST"])
def upload_image():
    f = request.files.get('file')
    t = request.form.get('token')
    c = request.form.get('callback')
    print(c," ", t)
    if f is None:
        return redirect(f"{c}?error=No+file+provided") if c \
            else ('<h1>CDN</h1> No file provided', 400)
    if t is None:
        return redirect(f"{c}?error=No+token+provided") if c \
            else ('<h1>CDN</h1> No token provided', 401)
    if not valid(t):
        return redirect(f"{c}?error=Invalid+token") if c \
            else ('<h1>CDN</h1> Invalid token', 401)
    if not allowed_image(f.filename):
        return redirect(f"{c}?error=Invalid format file")
    fid, content_type = str(uuid4()), f.content_type
    save_file(f,fid)
    return redirect(f"{c}?fid={fid}&content_type={content_type}&namefile={f.filename}") if c \
        else (f'<h1>CDN</h1> Uploaded {fid}', 200)



def save_file(file_to_save,fid):
    if(len(file_to_save.filename) > 0):
        filename_prefix = str(db.incr(FILE_COUNTER))
        new_filename = filename_prefix + file_to_save.filename
        path_to_file = DIR_PATH + new_filename
        file_to_save.save(path_to_file)
        print("new_filename: ",new_filename)
        #print("path_to_file", path_to_file)
        db.hset(new_filename, ORG_FILENAME, file_to_save.filename)
        db.hset(new_filename, PATH_TO_FILE, path_to_file)
        db.hset(FILENAMES, new_filename, file_to_save.filename)
        db.hset(fid,FILENAMESDATABASE, new_filename)
        print("FILENAMES:",db.hvals(FILENAMES))
        print(db.hvals(new_filename))
    else:
        print("\n\t\t[WARN] Empty content of file\n", file = sys.stderr)

def valid(token):
  try:
    decode(token, JWT_SECRET)
  except InvalidTokenError as e:
    app.logger.error(str(e))
    return False
  return True