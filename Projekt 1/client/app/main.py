from flask import Flask
from flask import render_template

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

@app.route('/error',methods=['GET'])
def wrong():
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)