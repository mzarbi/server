
import requests


API_URL = 'http://127.0.0.1:8000'

files={'files': open('/home/boussada/PycharmProjects/fileServer/tests/user.svg','rb')}

response = requests.post(
    '{}/files/upload_user_files'.format(API_URL), data={"user_name": "oussama_hmani","file_type" : "image", "file_name": "user2.svg", "format" : "reg", "content" : ""},files=files)

print response.__dict__
