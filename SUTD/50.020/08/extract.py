# ECB plaintext extraction skeleton file for 50.020 Security
# Oka, SUTD, 2014
import argparse
from present import *

nokeybits=80
blocksize=64

def getInfo(headerfile):
    with open(headerfile, 'rb') as hf:
        return hf.read()

def extract(infile,outfile,headerfile):
    header_info = getInfo(headerfile)
    with open(infile, 'rb') as fin:
        with open(outfile, 'wb') as fout:
            fout.write(header_info)
            fin.read(len(header_info))
            fout.write('\n')
            fin.read(1)
            while True:
                c = fin.read(1)
                if c == '':
                    break
                fout.write(str(ord(c)) + ' ')
    return True

if __name__=="__main__":
    parser=argparse.ArgumentParser(description='Extract PBM pattern.')
    parser.add_argument('-i', dest='infile',help='input file, PBM encrypted format')
    parser.add_argument('-o', dest='outfile',help='output PBM file')
    parser.add_argument('-hh', dest='headerfile',help='known header file')

    args=parser.parse_args()
    infile=args.infile
    outfile=args.outfile
    headerfile=args.headerfile

    print 'Reading from: ',infile
    print 'Reading header file from: ',headerfile
    print 'Writing to: ',outfile

    success=extract(infile,outfile,headerfile)

            
