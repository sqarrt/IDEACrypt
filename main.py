import sys

BLOCK_SIZE = 16


def lshift(a, n, bsize = BLOCK_SIZE):
    size = 2**bsize
    n = n % bsize
    return (a << n | a >> (bsize-n)) % size


def rshift(a, n, bsize = BLOCK_SIZE):
    return lshift(-a, n, bsize = bsize)


def mpl(a, b, bsize = BLOCK_SIZE):
    return (a+b) % (2**bsize)


def mml(a, b, bsize = BLOCK_SIZE):
    return (a*b) % (2**bsize+1)


def ainv(a, bsize = BLOCK_SIZE):
    return (2**bsize)-a


def minv(a, bsize = BLOCK_SIZE):
    return pow(a, ((2**bsize+1)-2), (2**bsize+1))


def split(arr, size):
    return divarr(arr, len(arr)//size)


def divarr(arr, parts):
    return [arr[i::parts] for i in range(parts)]


def get_blocks_from_file(filepath):
    file = open(filepath, "rb")
    data = file.read()
    blocks = split(data, 8)
    for i in range(len(blocks)):
        blocks[i] = bytearray(blocks[i])
    if len(blocks[-1]) != 8:
        filler = len(blocks[-1])
        blocks[-1].extend(bytes([filler]*(8-filler)))
    return blocks


def crypt(block, keys):
    D = block
    K = keys
    for i in range(0, 8):
        KA = mml(D[0], K[i][0])
        KB = mpl(D[1], K[i][1])
        KC = mpl(D[2], K[i][2])
        KD = mml(D[3], K[i][3])
        KE = KA ^ KC
        KF = KB ^ KD
        D[0] = KA ^ mml(mpl(KF, mml(KE, K[i][4])), K[i][5])
        D[1] = KC ^ mml(mpl(KF, mml(KE, K[i][4])), K[i][5])
        D[2] = KB ^ mpl(mml(KE, K[i][4]), mml(mpl(mml(KE, K[i][4]), KF), K[i][5]))
        D[3] = KD ^ mpl(mml(KE, K[i][4]), mml(mpl(mml(KE, K[i][4]), KF), K[i][5]))
    D1 = mml(D[0], K[8][0])
    D2 = mpl(D[2], K[8][1])
    D3 = mpl(D[1], K[8][2])
    D4 = mml(D[3], K[8][3])
    out = []
    out.append(D1)
    out.append(D2)
    out.append(D3)
    out.append(D4)
    return out


def get_keys_from_file(filepath):
    """file = open(filepath, "rb")
    keys = []
    data = file.read()
    data = data[:16].hex()
    print(data)
    #keys = divarr(data, 8)
    #print(keys)"""
    keys = [0b0000000000000001,
            0b0000000000000010,
            0b0000000000000011,
            0b0000000000000100,
            0b0000000000000101,
            0b0000000000000110,
            0b0000000000000111,
            0b0000000000001000]
    numkeys = 0;
    for a, i in enumerate(keys):
        numkeys = numkeys + a*(2**16)**(len(keys)-i+1)
        print(hex(a))
    print(bin(numkeys))
    print(
        '0b10000000000000010000000000000001100000000000001000000000000000101000000000000011000000000000001110000000000001000')
    print(0b10000000000000000, 2**16)
    print(bin(0b0000000000000111*0b10000000000000000+0b0000000000001000))
    print('0b110000000000000010000000000000001100000000000001000000000000000101000000000000011000000000000001110000000000001000')
    """for i in range(len(keys)):
        if i == 0:
            dkeys.append([minv(keys[8 - i][0]),
                          ainv(keys[8 - i][1]),
                          ainv(keys[8 - i][2]),
                          minv(keys[8 - i][3]),
                          keys[8 - i - 1][4],
                          keys[8 - i - 1][5]])
        elif i < 8:
            dkeys.append([minv(keys[8 - i][0]),
                          ainv(keys[8 - i][2]),
                          ainv(keys[8 - i][1]),
                          minv(keys[8 - i][3]),
                          keys[8 - i - 1][4],
                          keys[8 - i - 1][5]])
        elif i == 8:
            dkeys.append([minv(keys[8 - i][0]),
                          ainv(keys[8 - i][1]),
                          ainv(keys[8 - i][2]),
                          minv(keys[8 - i][3])])"""
    return keys #, dkeys

#blocks = get_blocks_from_file("res/image.jpg")
#print(2**16)
keys = get_keys_from_file('res/image.jpg')
#print(keys)
