import requests


API_URL = 'http://127.0.0.1:8000'

with open('/home/boussada/PycharmProjects/fileServer/FilePool/README.md') as fp:
    content = fp.read()

response = requests.post(
    '{}/files/newdata.csv'.format(API_URL), data=content
)
