from flask import session, Flask, Blueprint, request, Response, jsonify,redirect, g , url_for, make_response
from flask import render_template
import os
import sys
import redis
import hashlib

POST = "POST"
GET = "GET"
SESSION_ID = "session-id"

app = Flask(__name__)
db = redis.Redis(host='redis', port=6379, decode_responses=True)
db.flushdb()

DIR_PATH = "files/"
FILE_COUNTER = "file_counter"
ORG_FILENAME = "org_filename"
NEW_FILENAME = "new_filename"
PATH_TO_FILE = "path_to_file"
FILENAMES = "filenames"

@app.route('/')
def show_articles():
    files = db.hvals(FILENAMES)
    #return redirect(url_for("http://localhost:3001/upload-file", my_files=files))
    return render_template("uploadfileSerwer.html", my_files = files)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

@app.route('/login',methods=['POST'])
def logint():
    login=request.form['login']
    baza="karolik"
    if login==baza:
        return jsonify({'error' : 'Ten login już został wybrany przez innego użytkownika. Proszę o wybranie innego loginu.'})
    return jsonify({'answer': 'Okej'})


@app.route('/singin',methods=['POST','GET'])
def singin():
    print("HELLO`1")
    bazadanych = {
        "Jan": 12345,
        "Jacek": 11111,
        "Bartek": 22222
    }
    lg=request.form["name"]
    password = request.form["password"]
    if lg in bazadanych:
        if bazadanych[lg] == int(password):
            name_hash = hashlib.sha512(lg.encode("utf-8")).hexdigest()
            print("HELLO")
            db.set(SESSION_ID, name_hash)
            response = make_response(render_template("uploadfileSerwer.html"))
            response.set_cookie(SESSION_ID, name_hash, max_age=30, secure=True, httponly=True)
            return response
        else:
            return redirect("http://localhost:3001/")
    else:
            return redirect("http://localhost:3001/")


app.config["IMAGE_UPLOADS"]="static/img"
app.config["ALLOWED_FORMAT"]=["PDF"]

@app.route("/upload-image",methods=["GET","POST"])
def upload_image():
    if request.method=="POST":
        name_hash=request.cookies.get(SESSION_ID)
        print("hash")
        print(name_hash)
        dbname_hash=db.get("session-id")
        print("hello")
        print(dbname_hash)
        if(name_hash==dbname_hash):
            f = request.files["pdf"]
            save_file(f)
            return redirect(url_for("show_articles"))

def save_file(file_to_save):
    if(len(file_to_save.filename) > 0):
        filename_prefix = str(db.incr(FILE_COUNTER))
        new_filename = filename_prefix + file_to_save.filename
        path_to_file = DIR_PATH + new_filename
        db.hset(new_filename, ORG_FILENAME, file_to_save.filename)
        db.hset(new_filename, PATH_TO_FILE, path_to_file)
        db.hset(FILENAMES, new_filename, file_to_save.filename)
    else:
        print("\n\t\t[WARN] Empty content of file\n", file = sys.stderr)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
