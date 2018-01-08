import requests
import json

r = requests.post('https://afternoon-cove-17562.herokuapp.com/',
	params={"access_token": 'mytoken'},
	data=json.dumps({
	  "message": {"text": 'hi'}
	}),
	headers={'Content-type': 'application/json'})

if r.status_code != requests.codes.ok:
	print(r.text)
else:
	print(r.json())