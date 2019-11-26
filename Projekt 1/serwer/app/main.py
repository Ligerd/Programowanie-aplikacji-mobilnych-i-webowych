from flask import  Flask, request, jsonify,redirect, make_response ,send_file

import sys
import redis
import hashlib

POST = "POST"
GET = "GET"
SESSION_ID = "session-id"
INVALIDATE = -1

app = Flask(__name__)

db = redis.Redis(host='redis', port=6379, decode_responses=True)
db.flushdb()

bazadanych = {'admin': "admin"}

DIR_PATH = "files/"
FILE_COUNTER = "file_counter"
ORG_FILENAME = "org_filename"
NEW_FILENAME = "new_filename"
PATH_TO_FILE = "path_to_file"
FILENAMES = "filenames"
FILENAMESDATABASE="filenamesDATABASE"

@app.route('/files')
def show_articles():
    files = db.hvals(FILENAMES)
    response=jsonify(my_files=files)
    return response

@app.route("/download/<string:name>", methods=["GET"])
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

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

@app.route('/rejestracja',methods=['POST','GET'])
def logint():
    login=request.form['login'].rstrip()
    password=request.form['password'].rstrip()
    bazadanych[login]=password
    print(bazadanych)
    return redirect("http://localhost:3001/")


@app.route('/singin',methods=['POST','GET'])
def singin():
    if request.method == "POST":
        print("FSAFASFASFAS")
        lg=request.form["login"].rstrip()
        password = request.form["password"].rstrip()
        if lg in bazadanych.keys():
            print("login zgadza się")
            if bazadanych[lg] == password:
                print("hsało")
                name_hash = hashlib.sha512(lg.encode("utf-8")).hexdigest()
                db.set(SESSION_ID, name_hash)
                response = make_response('', 303)
                response.set_cookie(SESSION_ID, name_hash, max_age=180)
                response.headers["Location"] = "http://localhost:3001/upload-file"
                return response
            else:
                return redirect("http://localhost:3001/")
        else:
            return redirect("http://localhost:3001/")



app.config["ALLOWED_FORMAT"]=["PDF"]

def allowed_image(filename):
    if not "." in filename:
        return False
    ext=filename.rsplit(".",1)[1]
    if ext.upper() in app.config["ALLOWED_FORMAT"]:
        return True
    else:
        return False

@app.route("/upload-image",methods=["GET","POST"])
def upload_image():
    if request.method=="POST":
        name_hash=request.cookies.get(SESSION_ID)
        #print("ZE STRONY UPLOADU",name_hash)
        dbname_hash=db.get(SESSION_ID)
        #print("database hash",dbname_hash)
        if (request.cookies.get(SESSION_ID)==None):
            response = redirect("http://localhost:3001/error")
            response.set_cookie("session_id", "INVALIDATE", max_age=INVALIDATE)
            db.delete(SESSION_ID)
            return response
        if(name_hash==dbname_hash):
            f = request.files["pdf"]
            if allowed_image(f):
                save_file(f)
                return redirect("http://localhost:3001/upload-file")
            else:
                return redirect("http://localhost:3001/format_error")
        else:
            response = redirect("http://localhost:3001/error")
            response.set_cookie(SESSION_ID, "INVALIDATE", max_age=INVALIDATE)
            db.delete(SESSION_ID)
            return response


@app.route('/logout')
def logout():
  response = redirect("http://localhost:3001/")
  response.set_cookie(SESSION_ID, "INVALIDATE", max_age=INVALIDATE)
  db.delete(SESSION_ID)
  return response

def save_file(file_to_save):
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
        db.hset(file_to_save.filename, FILENAMESDATABASE, new_filename)
        print("FILENAMES:",db.hvals(FILENAMES))
        print(db.hvals(new_filename))
    else:
        print("\n\t\t[WARN] Empty content of file\n", file = sys.stderr)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
