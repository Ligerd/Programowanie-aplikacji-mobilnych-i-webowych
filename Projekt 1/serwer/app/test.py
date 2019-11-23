import requests
w= {}
res = requests.get("http://localhost:3000/files")
w["files"]=res.json()
print(w['files']["my_files"])