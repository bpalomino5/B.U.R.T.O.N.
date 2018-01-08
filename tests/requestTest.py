import requests
import json

r = requests.get('https://afternoon-cove-17562.herokuapp.com/',
	params={"access_token": 'mytoken'})

if r.status_code != requests.codes.ok:
	print(r.text)
else:
	print(r.json())