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
    b = split(data, 8)
    b = [split_int(merge_int(a, bsize = 8), bsize = 4) for a in b]
    file.close()
    return b


def write_file_from_blocks(b, filepath):
    file = open(filepath, "wb")
    ba = bytearray()
    for a in b:
        bytess = split_int_(merge_int(a, 16), 8)
        if a != b[-1]:
            while len(bytess) < 8:
                bytess.reverse()
                bytess.append(0)
                bytess.reverse()
        for c in bytess:
            ba.append(c)
    file.write(ba)
    file.close()


def crypt(block, k):
    d = block
    k = k
    for i in range(0, 8):
        ka = mml(d[0], k[i][0])
        kb = mpl(d[1], k[i][1])
        kc = mpl(d[2], k[i][2])
        kd = mml(d[3], k[i][3])
        ke = ka ^ kc
        kf = kb ^ kd
        d[0] = ka ^ mml(mpl(kf, mml(ke, k[i][4])), k[i][5])
        d[1] = kc ^ mml(mpl(kf, mml(ke, k[i][4])), k[i][5])
        d[2] = kb ^ mpl(mml(ke, k[i][4]), mml(mpl(mml(ke, k[i][4]), kf), k[i][5]))
        d[3] = kd ^ mpl(mml(ke, k[i][4]), mml(mpl(mml(ke, k[i][4]), kf), k[i][5]))
    d1 = mml(d[0], k[8][0])
    d2 = mpl(d[2], k[8][1])
    d3 = mpl(d[1], k[8][2])
    d4 = mml(d[3], k[8][3])
    out = list()
    out.append(d1)
    out.append(d2)
    out.append(d3)
    out.append(d4)
    return out


def crypt_blocks(b, k):
    cb = []
    for a in b:
        cblock = crypt(a, k)
        cb.append(cblock)
    return cb


def get_keys_from_file(filepath):
    file = open(filepath, "rb")
    k = split_int(int.from_bytes(file.read()[:16], byteorder = 'big'), bsize = 8)
    file.close()
    keys_num = lshift(merge_int(k), 25, bsize=128)
    for i in range(6):
        k.extend(split_int(keys_num, bsize = 8))
        keys_num = lshift(keys_num, 25, bsize=128)
    res = [a for a in split(k[:52], 6)]
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


#check for target of execution
if __name__ == "__main__":
    keys = get_keys_from_file('res/key.gif')
    blocks = get_blocks_from_file('res/source.jpg')
    cblocks = crypt_blocks(blocks, keys[0])
    enblocks = crypt_blocks(cblocks, keys[1])
    write_file_from_blocks(enblocks, 'res/res_gif.jpg')
