import requests

protocol = 'https://'

r = requests.post(protocol + 'localhost:5000/message/admin', auth=('guest', 'password'), data='{"message":"Hello World"}', verify=False)
print r.json()

r = requests.get(protocol + 'localhost:5000/messages', auth=('guest', 'password'), verify=False)
print r.json()