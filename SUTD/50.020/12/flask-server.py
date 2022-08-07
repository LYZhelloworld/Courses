from flask import Flask
from flask import json
from flask import jsonify
from flask import request
from functools import wraps
app = Flask(__name__)
msg = {}

def check_auth(username, password):
    return username == 'guest' and password == 'password'

def authenticate():
    message = {'message': "Authenticate."}
    resp = jsonify(message)

    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'

    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth: 
            return authenticate()

        elif not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


@app.route('/message/<username>', methods = ['POST'])
@requires_auth
def api_message(username):
    resp = jsonify({})
    resp.status_code = 200
    try:
        msg[username] = json.loads(request.data)['message']
    except:
        print 'An error occurred when parsing JSON data.'
        print 'JSON:'
        print request.data
        resp.status_code = 400
    return resp

@app.route('/messages', methods = ['GET'])
@requires_auth
def api_messages():
    resp = jsonify(msg)
    resp.status_code = 200
    return resp

if __name__ == '__main__':
    app.run(debug = False, ssl_context=(r'/home/student/Downloads/server.crt', r'/home/student/Downloads/server.key'))