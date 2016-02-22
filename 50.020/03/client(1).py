#!/usr/bin/env python
# Skeleton code to communicate with challenge server

import binascii
import requests
import json
import hashlib
import os
import random
# XOR two strings with each other, return string
def xorString(s1,s2):
    rval = [ord(a) ^ ord(b) for a,b in zip(s1,s2)]
    return ''.join([chr(r) for r in rval])

def crcToString(crc):
    value = crc
    result = ''
    result += chr(value >> 24)
    value -= (value >> 24 << 24)
    result += chr(value >> 16)
    value -= (value >> 16 << 16)
    result += chr(value >> 8)
    value -= (value >> 8 << 8)
    result += chr(value)
    return result


url="http://scy-phy.net:8080/"
#url="http://localhost:5000/"
headers={'Content-Type':'application/json'}

# Lab 3 skeleton part
r = requests.get(url+'challenges/otpcrc')
data=r.json()
print("Obtained challenge ciphertext: %s with len %d"%(data['challenge'],len(data['challenge'])))

# translate from hex to ascii range
s = data['challenge'].replace('0x',"")
s = binascii.unhexlify(s)

# we know that the last 32 bit are the CRC checksum
# in ascii, that are 4 characters
encrypted_m=s[:-4]
encrypted_crc=s[-4:]

# apply the masks (these do nothing actually)
#mask = "\x00"*(len(encrypted_m))
mask = "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x02\x06\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00"
#crcmask = "\x00"*(len(encrypted_crc))
# to check a failed crc manipulation:
#crcmask = "\x01"*(len(encrypted_crc))
magic = 0xFFFFFFFF
crcmask = crcToString((binascii.crc32(mask, magic) & magic) ^ magic)

manipulated_encrypted_m = xorString(encrypted_m,mask)
manipulated_encrypted_crc = xorString(encrypted_crc,crcmask)
solution = manipulated_encrypted_m + manipulated_encrypted_crc

# ascii hex encode them
solutionHex = '0x'+''.join(['%02x'%ord(i) for i in solution])

payload = {'cookie':data['cookie'],'solution':solutionHex}
r = requests.post(url+'solutions/otpcrc', headers=headers,data=json.dumps(payload))
print("Obtained response: %s"%r.text)

# Demo of the hash part

req_list = []
for i in range(15):
    r = requests.get(url+'challenges/pwdhash')
    data=r.json()
    print("Received hash challenge %s"%data['challenge'])
    req_list.append((r, data['challenge'].replace('0x',"")))

#solution = 'test'
#m = hashlib.md5()
#m.update(solution)
#mhash="0x"+m.hexdigest()

#payload = {'hash':mhash,'solution':solution}
#r = requests.post(url+'solutions/pwdhash', headers=headers,data=json.dumps(payload))
#print("Obtained response: %s"%r.text)

with open('words4.json') as data_file:
    json_data = json.load(data_file)

dict_data = {}
for word in json_data:
    if len(word) == 4:
        try:
            dict_data[hashlib.md5(word.lower()).hexdigest()] = word.lower()
        except UnicodeEncodeError:
            pass

for req in req_list:
    if dict_data.has_key(req[1]):
        print 'Found ' + req[1] + ' : ' + dict_data[req[1]]

with open('hash_list', 'w') as hash_file:
    for req in req_list:
        hash_file.write(req[1] + '\n')
os.system('cd ./rainbowcrack-1.6-linux64/ && ./rcrack md5_loweralpha#4-4_0_3800x475254_0.rt -l ../hash_list && cd ..')

pwds = ['aasn', 'abcq', 'aamg', 'aacg', 'aasw', 'aalx', 'qwer', 'aadq', 'aaaq', 'aafz', 'aafx', 'aawv', 'aaee', 'aawa', 'aazj']
new_pwds = []
for pwd in pwds:
    new_pwds.append(random.choice('abcdefghijklmnopqrstuvwxyz') + pwd)
with open('hash_list2', 'w') as hash_file2:
    for pwd in new_pwds:
        hash_file2.write(hashlib.md5(pwd).hexdigest() + '\n')
os.system('cd ./rainbowcrack-1.6-linux64/ && ./rcrack md5_loweralpha#5-5_0_3800x475254_0.rt -l ../hash_list2 && cd ..')