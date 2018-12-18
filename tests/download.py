import requests

API_URL = 'http://127.0.0.1:8000'


response = requests.get('{}/files'.format(API_URL))

print response.json()