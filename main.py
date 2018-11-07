import sys


def shift(a, n):
    size = 2**16
    n = n % size
    return (a << n | a >> (size-n)) % 2**size


def to_bytes(a):
    res = bytearray()
    size = 2**8
    while a > size:
        res.append(a % size)
        a = a // size
    return res


def mpl(a, b):
    return (a+b) % (2**8)


def mml(a, b):
    return (a*b) % (2**8+1)


def ainv(a):
    return (2**8)-a


def minv(a):
    return pow(a, ((2**8+1)-2), (2**8+1))


def split(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    pice = arr[:size]
    arrs.append(pice)
    return arrs


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
    keys = []
    data = file.read()
    data = data[:16]
    print(data)
    temp = int.from_bytes(data, "little")
    print(temp)
    print(to_bytes(temp))
    print(int.from_bytes(to_bytes(temp),'little'))
    for i in range(7):
        keys.append([int.from_bytes(a, "little") for a in split(data, 2)])
        temp = shift(temp, 25)
        #data = temp.to_bytes(16, "little")
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
keys = get_keys_from_file("res/image.jpg")
