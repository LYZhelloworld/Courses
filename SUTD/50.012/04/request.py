#!/usr/bin/python

import requests

print "Request /"
r = requests.get("http://localhost:5000/")
print r.json()["message"]
print

print "Register new user"
r = requests.get("http://localhost:5000/register", params={"usn": "user", "pwd": "123456"})
print "Status code:", r.status_code
print r.json()["message"]
print

print "Write something"
r = requests.post("http://localhost:5000/write/newarticle", data="test", auth=("user", "123456"), headers={"Content-Type": "text/plain"})
print "Status code:", r.status_code
print r.json()["message"]
print

print "Read it"
r = requests.get("http://localhost:5000/read/newarticle", auth=("user", "123456"))
print "Status code:", r.status_code
print r.json()["message"]
print

