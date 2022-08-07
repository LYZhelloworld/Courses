#!/usr/bin/env python

import sys
import argparse

ascii_a = ord('a')
ascii_A = ord('A')
ascii_z = ord('z')
ascii_Z = ord('Z')

def encrypt(plaintext, key):
    output = ''
    for i in plaintext:
        if i >= 'a' and i <= 'z': # Lowercase
            temp = ord(i) + key
            while temp > ascii_z:
                temp -= 26
            output += chr(temp)
        elif i >= 'A' and i <= 'Z': # Uppercase
            temp = ord(i) + key
            while temp > ascii_Z:
                temp -= 26
            output += chr(temp)
        else:
            output += i

    return output

def decrypt(ciphertext, key):
    output = ''
    for i in ciphertext:
        if i >= 'a' and i <= 'z': # Lowercase
            temp = ord(i) - key
            while temp < ascii_a:
                temp += 26
            output += chr(temp)
        elif i >= 'A' and i <= 'Z': # Uppercase
            temp = ord(i) - key
            while temp < ascii_A:
                temp += 26
            output += chr(temp)
        else:
            output += i

    return output

if __name__ == '__main__':
    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='filein',help='input file')
    parser.add_argument('-o', dest='fileout', help='output file')
    parser.add_argument('-k', dest='key',help='key')
    parser.add_argument('-m', dest='mode', help='mode')

    # parse our arguments
    args = parser.parse_args()
    filein = args.filein
    fileout = args.fileout
    key = args.key
    mode = args.mode

    if not key.isdigit():
        print 'Invalid key value.'
        parser.print_help()
    elif mode != 'd' and mode != 'e':
        print 'Mode should be either \'d\' or \'e\'.'
        parser.print_help()
    else:
        fin = open(filein, 'r')
        fout = open(fileout, 'w')

        if mode == 'd':
            fout.write(decrypt(fin.read(), int(key)))
        else:
            fout.write(encrypt(fin.read(), int(key)))

        fout.close()
        fin.close()