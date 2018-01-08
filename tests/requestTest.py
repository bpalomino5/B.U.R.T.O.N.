import requests
import json

r = requests.get('http://127.0.0.1:5000/',
	params={"access_token": 'mytoken'})

if r.status_code != requests.codes.ok:
	print(r.text)
else:
	print(r.json())