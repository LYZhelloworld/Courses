#!/usr/bin/env python
# Skeleton code to communicate with challenge server

import requests
import json
import string
from collections import Counter

def plaintext():
    print("Calling the API now...")
    url="http://scy-phy.net:8080/"
    headers={'Content-Type':'application/json'}
    r = requests.get(url+'challenges/plain')
    data=r.json()
    print("Obtained challenge (in hex): %s"%data['challenge'])
    m = data['challenge'].replace("0x","").decode("hex")
    print("Decoded challenge: %s"%m)

    payload={'cookie':data['cookie'],'solution':m}
    r = requests.post(url+'solutions/plain', headers=headers,data=json.dumps(payload))
    print("Obtained response: %s"%r.text)

def caesar():
    print("Calling the API now...")
    url="http://scy-phy.net:8080/"
    headers={'Content-Type':'application/json'}
    r = requests.get(url+'challenges/caesar')
    data=r.json()
    #print("Obtained challenge (in hex): %s"%data['challenge'])
    c = data['challenge'].replace("0x","").decode("hex")
    #print("Decoded challenge: %s"%m)

    for key in range(255):
        m = ''.join([(chr(ord(x) - key + 256) if (ord(x) - key) < 0 else chr(ord(x) - key)) for x in c]) # Decipher
        if not all(x in string.printable for x in m):
            continue # Non-printable string, skip this round

        payload={'cookie':data['cookie'],'solution':m}
        #print json.dumps(payload)
        r = requests.post(url+'solutions/caesar', headers=headers,data=json.dumps(payload))
        print('key = %d'%key)
        print("Obtained response: %s"%r.text)

        if r.text == 'Your answer is correct... of course!\n':
            print 'Correct key: %d'%key
            break

def substitution():
    #print("Calling the API now...")
    url="http://scy-phy.net:8080/"
    headers={'Content-Type':'application/json'}
    #r = requests.get(url+'challenges/substitution')
    #data=r.json()
    challenge = '0xdcbf42a80368dcb6c4bf46b6c401bf7adc2dbfdcbf88a8dccd68b607cdbebf01dc032da8c461bfdcc42dbfb6c4bf687aa8bf01dc032da8c4bfb16889892dbfdcbf6803a8a8bfb37ab6427abf888903a8bf0189be2da8c4bfdc4848bea8b1a2bf687aa8b1a8bfdc4848bea8b1bfb3a803a8bfdcbeb3dc5eb1bf4289cdc468a82d61bfdcc42dbfdc8889cd68bf687aa8bf68b69ea8bfb37aa8c4bf687aa85ebf88a801dcc4bf6889bf010389b3bf03b648a8bfb668bfb3dcb1bf0789cdc42dbf687adc68bfa8a3a8035ebfc4b6017a68bf89c4a8bf8907bf687aa89ebfb3dcb1bf0189c4a8a2bf687aa8bf46b6c401bf88a842dc9ea8bfa3a8035ebfdcc401035ebfdc68bf687ab6b161bfdcc42dbf89032da803a82dbf687aa8bf01dc032da8c4a803bf6889bf46a8a848bfb3dc68427abfdcbebebfc4b6017a68bfcdc42da803bf687aa8bf6803a8a8a2bf687aa8bf01dc032da8c4a803bfb1a868bf7ab6b1bfa8be2da8b168bfb189c4bf6889bfb3dc68427a94bf88cd68bfdc8889cd68bf68b3a8bea3a8bf89bd42be894246bf7aa8bf07a8bebebfdcb1bea8a84861bfdcc42dbfb6c4bf687aa8bf9e8903c4b6c401bfdcc489687aa803bf8907bf687aa8bfdc4848bea8b1bfb3dcb1bf9eb6b1b1b6c401a2bf687aa8c4bf687aa8bfb1a84289c42dbfb189c4bfb3dcb1bf89032da803a82dbf6889bfb3dc68427a94bfdcc42dbfdc68bf9eb62dc4b6017a68bf7aa8bf688989bf07a8bebebfdcb1bea8a84861bfdcc42dbfb6c4bf687aa8bf9e8903c4b6c401bfdcc489687aa803bfdc4848bea8bfb3dcb1bf0189c4a8a2bf687aa8c4bf687aa8bf687ab6032dbfb189c4bf890707a803a82dbf6889bf46a8a848bfb3dc68427a94bf88cd68bf687aa8bf01dc032da8c4a803bfdc68bf07b603b168bfb389cdbe2dbfc48968bfbea868bf7ab69e61bf078903bf07a8dc03bfb1899ea8bf7adc039ebfb17a89cdbe2dbf42899ea8bf6889bf7ab69e4cbf7a89b3a8a3a80361bfdc68bfbedcb168bf7aa8bf4289c4b1a8c468a82d61bfdcc42dbf687aa8bf5e89cdc401bf9edcc4bfbedcb62dbf7ab69eb1a8be07bfcdc42da803bf687aa8bf6803a8a8bf6889bfb3dc68427aa2bfdcb1bf687aa8bf42be894246bfb16803cd4246bf68b3a8bea3a8bf7aa8bf7aa8dc032dbfdcbf03cdb168beb6c401bfc489b6b1a8bfb6c4bf687aa8bfdcb60361bfdcc42dbfdcbf88b6032dbf42dc9ea8bf07be5eb6c401bf687adc68bfb3dcb1bf8907bf48cd03a8bf0189be2d94bfdcc42dbfdcb1bfb668bfb3dcb1bfb1c4dc4848b6c401bfdc68bf89c4a8bf8907bf687aa8bfdc4848bea8b1bfb3b6687abfb668b1bf88a8dc4661bf687aa8bf01dc032da8c4a803bdb1bfb189c4bfb8cd9e48a82dbfcd48'
    print("Obtained challenge (in hex): %s"%challenge)
    c = challenge.replace("0x","").decode("hex")

    cookie = '0x0c383fe6b4d8f162d0add80426ff3065'
    count = Counter(c)
    freq = count.most_common()
    print freq
    rep = {}

    def replace_multiple(str, rep = {}):
        result = ''
        for i in str:
            if rep.has_key(i):
                result += rep[i]
            else:
                result += i
        return result

    def build_rep(pattern):
        for i in range(len(pattern)):
            rep[freq[i][0]] = pattern[i]

    build_rep(' etanhorsdilgwpcumfb,ky.v;\'j:')
    m = replace_multiple(c, rep)

    print("Decoded challenge: %s"%m)

    payload={'cookie':cookie,'solution':m}
    #print json.dumps(payload)
    r = requests.post(url+'solutions/substitution', headers=headers,data=json.dumps(payload))
    print("Obtained response: %s"%r.text)

def otp():
    print("Calling the API now...")
    url="http://scy-phy.net:8080/"
    headers={'Content-Type':'application/json'}
    r = requests.get(url+'challenges/otp')
    data=r.json()
    print("Obtained challenge (in hex): %s"%data['challenge'])
    c = data['challenge'].replace("0x","").decode("hex")
    #print("Decoded challenge: %s"%m)

    def str_bitwise(str1, str2):
        if len(str1) != len(str2):
            print 'Lengths are not equal'
            return
        result = ''
        for i in range(len(str1)):
            result += chr(ord(str1[i]) ^ ord(str2[i]))
        return result

    s1 = '           1000000      0       '
    s2 = '           1000426      4       '
    print str_bitwise(s1, s2).encode('hex')
    m = str_bitwise(str_bitwise(s1, s2), c)
    #m=c

    payload={'cookie':data['cookie'],'solution':'0x' + m.encode('hex')}
    print payload
    r = requests.post(url+'solutions/otp', headers=headers,data=json.dumps(payload))
    print("Obtained response: %s"%r.text)


if __name__ == '__main__':
    #print 'Plaintext'
    #plaintext()

    #print 'Caesar'
    #caesar()

    #print 'Substitution'
    #substitution()

    print 'OTP'
    otp()