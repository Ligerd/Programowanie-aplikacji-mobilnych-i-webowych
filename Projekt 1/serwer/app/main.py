from flask import Flask, Blueprint, request, Response, jsonify

app = Flask(__name__)

# Index
#@app.route('/', methods=['GET'])
#def app_index():
#    return 'PAMIW >> Hello World'

@app.route('/', methods=['GET'])
def home():
    return 'PAMIW >> Hello World'

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
