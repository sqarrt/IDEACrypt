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
        res.append(list(reversed(arr[i*size:(i+1)*size])))
    return res


def divarr(arr, parts):
    return [arr[i::parts] for i in range(parts)]


def merge_int(arr):
    numkeys = 0
    for i, a in enumerate(arr):
        numkeys = numkeys + a * ((2 ** 16) ** (len(arr) - i - 1))
    return numkeys


def split_int(val):
    arr = []
    lval = val
    for i in range(8):
        arr.append(lval%(2**16))
        lval = lval >> 16
    arr.reverse()
    return arr

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
    file = open(filepath, "rb")
    #keys = split_int(int.from_bytes(file.read()[:16], byteorder = 'big'))
    keys = [0x0001,
            0x0002,
            0x0003,
            0x0004,
            0x0005,
            0x0006,
            0x0007,
            0x0008]
    keys_num = lshift(merge_int(keys), 25, bsize=128)
    for i in range(6):
        keys.extend(split_int(keys_num))
        keys_num = lshift(keys_num, 25, bsize=128)
    res = [list(reversed(a)) for a in split(keys[:52], 6)]
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

#blocks = get_blocks_from_file("res/image.jpg")
#print(2**16)
keys = get_keys_from_file('res/image.jpg')
encoded = [43225,
           30640,
           6969,
           3326]
decoded = crypt(encoded, keys[1])
print('decoded block: ', list([hex(a) for a in decoded]))
