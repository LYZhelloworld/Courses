#!/usr/bin/python
# Notepad

from flask import Flask, jsonify, request
from functools import wraps

# Set logging
import logging
file_handler = logging.FileHandler("app.log")

app = Flask(__name__)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

authlist = {} # User list
msglist = {} # Message list

@app.route("/")
def api_root():
	# Displaying "How to use"
	app.logger.info("root")
	resp = jsonify({"message":
"""Hello.
Here are some APIs available:

/register	Register a new username
/read		Read the message stored
/write		Store message"""})
	resp.status_code = 200
	return resp

@app.route("/register")
def api_register():
	# Register new user
	app.logger.info("register")
	app.logger.info(str(request.args))
	if "usn" in request.args and "pwd" in request.args:
		# Correct format
		if not request.args["usn"] in authlist:
			# New user
			authlist[request.args["usn"]] = request.args["pwd"]
			app.logger.info(str(authlist))
			resp = jsonify({"message": "New user has been created successfully."})
			resp.status_code = 201
			return resp
		else:
			# Username exists
			resp = jsonify({"message": "Username already exists."})
			resp.status_code = 200
			return resp
	else:
		# Incorrect format
		resp = jsonify({"message": "Username and password required."})
		resp.status_code = 400
		return resp

def check_auth(username, password):
	# Check if username and password is correct
	if username in authlist:
		if authlist[username] == password:
			# Correct
			app.logger.info("Authorized")
			return True
	# Incorrect
	app.logger.info("Unauthorized")
	return False

def authenticate():
	# 401 Error message
	resp = jsonify({"message": "Authentication required."})
	resp.status_code = 401
	resp.headers["WWW-Authenticate"] = 'Basic realm="Example"'
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

@app.route("/read/<title>")
@requires_auth
def api_read(title):
	# Read message with a specific title
	app.logger.info("read")
	if not title in msglist:
		# Message is created if it does not exist
		msglist[title] = ""
	app.logger.info(str(msglist))
	resp = jsonify({"message": msglist[title]})
	resp.status_code = 200
	return resp

@app.route("/write/<title>", methods = ["POST"])
@requires_auth
def api_write(title):
	# Write message with a specific title
	app.logger.info("write")
	if request.headers["Content-Type"] == "text/plain":
		app.logger.info(request.data)
		msglist[title] = request.data
		app.logger.info(str(msglist))
		resp = jsonify({"message": "OK."})
		resp.status_code = 200
		return resp
	else:
		# Accepts plain text only
		resp = jsonify({"message": "Unsupported Media Type.\nPlease use plain text."})
		resp.status_code = 415
		return resp

if __name__ == "__main__":
	app.run(debug=True)

