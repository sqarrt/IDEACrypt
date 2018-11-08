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
    res = []
    parts = len(arr)//size+1
    for i in range(parts):
        res.append(arr[i*size:(i+1)*size])
    return res


def divarr(arr, parts):
    return [arr[i::parts] for i in range(parts)]


def merge_int(arr, bsize = 16):
    numkeys = 0
    for i, a in enumerate(arr):
        numkeys = numkeys + a * ((2 ** bsize) ** (len(arr) - i - 1))
    return numkeys


def split_int(val, bsize = 8):
    arr = []
    lval = val
    for i in range(bsize):
        arr.append(lval % (2**16))
        lval = lval >> 16
    arr.reverse()
    return arr


def split_int_(val, bsize):
    numr = (len(bin(val))-2)
    least = numr % bsize
    parts = numr//bsize if least == 0 else numr//bsize+1
    arr = []
    lval = val
    for i in range(parts):
        arr.append(lval % (2**bsize))
        lval = lval >> bsize
    arr.reverse()
    return arr


def get_blocks_from_file(filepath):
    file = open(filepath, "rb")
    data = file.read()
    print(data.hex())
    blocks = split(data, 8)
    blocks = [split_int(merge_int(a, bsize = 8), bsize = 4) for a in blocks]
    file.close()
    return blocks


def write_file_from_blocks(blocks, filepath):
    file = open(filepath, "wb")
    ba = bytearray()
    for a in blocks:
        bytess = split_int_(merge_int(a, 16), 8)
        if(a != blocks[-1]):
            while len(bytess) < 8:
                bytess.reverse()
                bytess.append(0)
                bytess.reverse()
        for b in bytess:
            ba.append(b)
    print(ba.hex())
    file.write(ba)
    file.close()


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


def crypt_blocks(blocks, keys):
    cblocks = []
    for a in blocks:
        cblock = crypt(a, keys)
        cblocks.append(cblock)
    return cblocks


def get_keys_from_file(filepath):
    file = open(filepath, "rb")
    keys = split_int(int.from_bytes(file.read()[:16], byteorder = 'big'), bsize = 8)
    file.close()
    keys_num = lshift(merge_int(keys), 25, bsize=128)
    for i in range(6):
        keys.extend(split_int(keys_num, bsize = 8))
        keys_num = lshift(keys_num, 25, bsize=128)
    res = [a for a in split(keys[:52], 6)]
    dkeys = []
    for i, a in enumerate(res):
        if i == 8:
            rdkey = [minv(a[0]),
                     ainv(a[1]),
                     ainv(a[2]),
                     minv(a[3]),
                     res[i-1][4],
                     res[i-1][5]]
            dkeys.append(rdkey)
        elif i == 0:
            rdkey = [minv(a[0]),
                     ainv(a[1]),
                     ainv(a[2]),
                     minv(a[3])]
            dkeys.append(rdkey)
        else:
            rdkey = [minv(a[0]),
                     ainv(a[2]),
                     ainv(a[1]),
                     minv(a[3]),
                     res[i-1][4],
                     res[i-1][5]]
            dkeys.append(rdkey)
    dkeys.reverse()
    return res, dkeys


keys = get_keys_from_file('res/key.gif')
blocks = get_blocks_from_file('res/source.jpg')
cblocks = crypt_blocks(blocks, keys[0])
enblocks = crypt_blocks(cblocks, keys[1])
write_file_from_blocks(enblocks, 'res/res_gif.jpg')


