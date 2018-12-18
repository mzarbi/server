
import requests


API_URL = 'http://127.0.0.1:8000'



response = requests.post(
    '{}/manifest'.format(API_URL), data={"user_name": "oussama_hmani"})

print response.__dict__
