import os
import base64
from io import BytesIO
from PIL import Image
from flask import Flask, request, abort, jsonify, send_from_directory
import datetime as dt
from tinydb import TinyDB, Query

UPLOAD_DIRECTORY = r'/home/medzied/Dev_Hedi_Works/server/FilePool'
USERS_MANIFEST = r'/home/medzied/Dev_Hedi_Works/server/FilePool/users/manifest.json'


if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

api = Flask(__name__)


@api.route('/manifest', methods=['POST', 'GET'])
def user_manifest():
    """Create user manifest"""
    if request.method == 'POST':
        USERS_DIR = os.path.join(UPLOAD_DIRECTORY, "users")
        if not os.path.exists(UPLOAD_DIRECTORY):
            os.makedirs(UPLOAD_DIRECTORY)

        user = request.form['user_name']
        db = TinyDB(USERS_MANIFEST)
        qu = Query()
        qur = db.search(qu.username == user)
        if not os.path.exists(os.path.join(os.path.join(USERS_DIR, user))):
            os.makedirs(os.path.join(os.path.join(USERS_DIR, user)))

        if len(qur) == 0:
            db.insert({'username': user, 'path': os.path.join(os.path.join(USERS_DIR, user))})


            db = TinyDB(os.path.join(os.path.join(USERS_DIR, user), "manifest.json"))
            db.insert({"name": user,
                    "logs": {
                        "log": {
                            "desc": "manifest created",
                            "date": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "details" : {}
                            }
                        }
                    })

        return "manifest created with success"
    return "manifest not created"

@api.route('/files/upload_user_files', methods=['POST'])
def upload_user_file():
    """Upload a file."""
    user_name =  request.form['user_name']
    file_type = request.form['file_type']
    format = request.form['format']

    db = TinyDB(USERS_MANIFEST)
    qu = Query()
    qur = db.search(qu.username == user_name)

    if len(qur) == 0:
        return abort(400, 'user manifest not found')

    path = qur[0]["path"]

    file_name = request.form['file_name']
    if '/' in file_name:
        # Return 400 BAD REQUEST
        abort(400, 'no subdirectories directories allowed')

    if format == "b64":
        content = request.form['content']
        dat = base64.b64decode(content)
    else:
        dat = request.files['files'].read()

    print dat
    #im = Image.open(BytesIO(base64.b64decode(dat)))
    sender = request.form['sender']


    if sender != None:
        if sender == "mobileApp":
            work = request.form['work_name']
            batch = request.form['batch_name']
            construction_site = request.form['construction_site_name']
            zone = request.form['zone_name']
            path = os.path.join(path, zone)
            path = os.path.join(path, construction_site)
            path = os.path.join(path, batch)
            path = os.path.join(path, work)


    with open(os.path.join(path, file_name), 'wb') as fp:
        fp.write(dat)

    db = TinyDB(os.path.join(path, "manifest.json"))
    db.insert({"name": user_name,
               "logs": {
                   "log": {
                       "desc": "file uploaded : " + file_name,
                       "date": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                       "details":{
                           "type": file_type,
                           "path": os.path.join(path, file_name)
                       }

                   }
               }
               })

    # Return 201 CREATED
    return '', 201


@api.route('/files')
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)


@api.route('/files/users')
def list_users_in_pool():
    """Endpoint to list files on the server."""
    files = []
    USERS_DIR = os.path.join(UPLOAD_DIRECTORY, "users")
    for filename in os.listdir(USERS_DIR):
        path = os.path.join(USERS_DIR, filename)
        if os.path.isdir(path):
            files.append(filename)
    return jsonify(files)

@api.route('/files/users/<user>/<path:path>')
def get_file2(user,path):
    """Download a file."""
    p1 = os.path.join(UPLOAD_DIRECTORY,"users")
    p1 = os.path.join(p1, user)
    return send_from_directory(p1, path, as_attachment=True)

@api.route('/files/<path:path>')
def get_file(path):
    """Download a file."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


@api.route('/files/post_file', methods=['POST'])
def post_file(filename):
    """Upload a file."""

    if '/' in filename:
        # Return 400 BAD REQUEST
        abort(400, 'no subdirectories directories allowed')

    with open(os.path.join(UPLOAD_DIRECTORY, filename), 'wb') as fp:
        fp.write(request.args.get('file'))

    # Return 201 CREATED
    return '', 201


if __name__ == '__main__':
    api.run(debug=True, port=5000)
