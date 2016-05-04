# Present skeleton file for 50.020 Security
# Oka, SUTD, 2014

#constants
fullround=31

#S-Box Layer
sbox=[0xC,0x5,0x6,0xB,0x9,0x0,0xA,0xD,0x3,0xE,0xF,0x8,0x4,0x7,0x1,0x2]

#PLayer
pmt=[0,16,32,48,1,17,33,49,2,18,34,50,3,19,35,51,\
     4,20,36,52,5,21,37,53,6,22,38,54,7,23,39,55,\
     8,24,40,56,9,25,41,57,10,26,42,58,11,27,43,59,\
     12,28,44,60,13,29,45,61,14,30,46,62,15,31,47,63]

# Rotate left: 0b1001 --> 0b0011
rol = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))
 
# Rotate right: 0b1001 --> 0b1100
ror = lambda val, r_bits, max_bits: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))

def genRoundKeys(key):
    return key >> 16

def addRoundKey(state,Ki):
    return state ^ Ki

def sBoxLayer(state):
    result = 0x0
    for i in range(16):
        result |= sbox[state >> (4 * i) & 0xF] << (4 * i)
    return result

def sBoxLayer_inv(state):
    result = 0x0
    for i in range(16):
        result |= sbox.index(state >> (4 * i) & 0xF) << (4 * i)
    return result

def pLayer(state):
    result = 0x0
    for i in range(64):
        result |= (state >> i & 0x1) << pmt[i]
    return result

def pLayer_inv(state):
    result = 0x0
    for i in range(64):
        result |= (state >> i & 0x1) << pmt.index(i)
    return result

def present_rounds(plain, key, rounds):
    key_reg = key
    state = plain

    for i in range(1, rounds + 1):
        ki = genRoundKeys(key_reg)
        state = addRoundKey(state, ki)
        state = sBoxLayer(state)
        state = pLayer(state)

        key_reg = ror(key_reg, 19, 80)
        key_reg = sBoxLayer(key_reg >> 76) << 76 | (key_reg & 0x0FFFFFFFFFFFFFFFFFFF)
        key_reg ^= i << 15
    ki = genRoundKeys(key_reg)
    state = addRoundKey(state, ki)
    return state

def present_rounds_inv(cipher, key, rounds):
    key_reg = key
    ki = {}
    for i in range(1, rounds + 1):
        ki[i] = genRoundKeys(key_reg)
        key_reg = ror(key_reg, 19, 80)
        key_reg = sBoxLayer(key_reg >> 76) << 76 | (key_reg & 0x0FFFFFFFFFFFFFFFFFFF)
        key_reg ^= i << 15
    ki[rounds + 1] = genRoundKeys(key_reg)

    state = cipher
    state = addRoundKey(state, ki[rounds + 1])
    for i in range(rounds, 0, -1):
        state = pLayer_inv(state)
        state = sBoxLayer_inv(state)
        state = addRoundKey(state, ki[i])

    return state

def present(plain, key):
    return present_rounds(plain, key, fullround)

def present_inv(plain, key):
    return present_rounds_inv(plain, key, fullround)



if __name__=="__main__":
    plain1=0x0000000000000000
    key1=0x00000000000000000000
    cipher1= present(plain1,key1)
    plain11 = present_inv(cipher1,key1)
    print format(cipher1,'x')
    print format(plain11,'x')
    plain2=0x0000000000000000
    key2=0xFFFFFFFFFFFFFFFFFFFF
    cipher2= present(plain2,key2)
    plain22 = present_inv(cipher2,key2)
    print format(cipher2,'x')
    print format(plain22,'x')
    plain3=0xFFFFFFFFFFFFFFFF
    key3=0x00000000000000000000
    cipher3= present(plain3,key3)
    plain33 = present_inv(cipher3,key3)
    print format(cipher3,'x')
    print format(plain33,'x')
    plain4=0xFFFFFFFFFFFFFFFF
    key4=0xFFFFFFFFFFFFFFFFFFFF
    cipher4= present(plain4,key4)
    plain44 = present_inv(cipher4,key4)
    print format(cipher4,'x')
    print format(plain44,'x')


