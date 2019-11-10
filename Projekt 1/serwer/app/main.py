from flask import Flask, Blueprint, request, Response, jsonify,redirect
from flask import render_template
import os
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template("uploadfile.html")

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


@app.route('/singin',methods=['POST'])
def singin():
    bazadanych={
        "Jan" : 12345,
        "Jacek" : 11111,
        "Bartek" : 22222
    }
    login=request.form['name']
    print(type(login))
    password=request.form['password']
    if str(login) in bazadanych:
        if bazadanych[login]==int(password):
            return redirect('http://localhost:3001/upload-file')
        else:
            return jsonify({'error': ' Worng password'})
    else:
        return jsonify({'error': ' Użytkownika z takim loginem nie ma w bazie'})


app.config["IMAGE_UPLOADS"]="static/img"
app.config["ALLOWED_FORMAT"]=["PDF"]

def check_file(filename):
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
        if request.files:
            image=request.files["pdf"]
            if not check_file(image.filename):
                return redirect(request.url)
            image.save(os.path.join(app.config["IMAGE_UPLOADS"],image.filename))
            return redirect(request.url)
    return redirect('http://localhost:3001/upload-file')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
