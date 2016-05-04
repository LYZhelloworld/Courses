# ECB wrapper skeleton file for 50.020 Security
# Oka, SUTD, 2014
from present import *
import argparse

nokeybits=80
blocksize=64


def ecb(infile,outfile,keyfile,mode):
    key = 0x0
    with open(keyfile, 'rb') as fkey:
        for i in range(nokeybits / 8):
            key |= ord(fkey.read(1)) << i * 8
    with open(infile, 'rb') as fin:
        with open(outfile, 'wb') as fout:
            while True:
                buf = fin.read(blocksize / 8)
                chunk = 0x0
                if buf == '':
                    break
                if len(buf) != blocksize / 8:
                    buf += '\0' * (blocksize / 8 - len(buf))
                for i in range(blocksize / 8):
                    chunk |= ord(buf[i]) << i * 8
                if mode == 'c':
                    result = present(chunk, key)
                else:
                    result = present_inv(chunk, key)
                for i in range(blocksize / 8):
                    fout.write(chr((result >> i * 8) & 0xff))

if __name__=="__main__":
    parser=argparse.ArgumentParser(description='Block cipher using ECB mode.')
    parser.add_argument('-i', dest='infile',help='input file')
    parser.add_argument('-o', dest='outfile',help='output file')
    parser.add_argument('-k', dest='keyfile',help='key file')
    parser.add_argument('-m', dest='mode',help='mode')

    args=parser.parse_args()
    infile=args.infile
    outfile=args.outfile
    keyfile=args.keyfile
    mode=args.mode

    ecb(infile, outfile, keyfile, mode)