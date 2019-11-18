from flask import Flask
from flask import render_template,redirect, request

app = Flask(__name__)

@app.route('/',methods=["GET"])
def index():
    return render_template('rejestracja.html')

@app.route('/upload-file',methods=['GET'])
def upload():
    return render_template('uploadfile.html')

@app.route('/login',methods=['GET'])
def rejestracja():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)