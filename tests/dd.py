import requests
API_URL = 'http://127.0.0.1:8000'

response = requests.get(
    '{}/files/users/med_zied_arbi/user.svg'.format(API_URL)
)

print response.text