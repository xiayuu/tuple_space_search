#!/usr/bin/env python
# encoding: utf-8
import random
import time

F = []
N = 100000
#length is 8bit, less length  means there is a wild card
#5-dimensional filter
def init_database():
    for i in range(0, N):
        fiter = {"A": random.randint(0, 255),
                 "B": random.randint(0, 255),
                 "C": random.randint(0, 255),
                 "D": random.randint(0, 255),
                 "E": random.randint(0, 255)}
        F.append(fiter)


#A tuple T is vector of K length. Thus, for example,[8, 16, 8, 0, 16]
#is a 5-dimensional tuple, whose ip source field is a 8bit prefix, ip
#destination field is a 16-bit prefix, and so on. We say that a filter
#F belongs or maps to tuple T if the ith field of F is specified to
#exactly T[i] bits. For example, considering 2-dimensional filters,
#both F1=(01*,111*) and F2=(11*,010*) map to the tuple[2,3].
def make_tuple():
    tmp = []
    for i in range(0, N):
        a = len(bin(F[i]['A'])[2:])
        b = len(bin(F[i]['B'])[2:])
        c = len(bin(F[i]['C'])[2:])
        d = len(bin(F[i]['D'])[2:])
        e = len(bin(F[i]['E'])[2:])
        tmp.append((a, b, c, d, e))
    return set(tmp)

def get_tuple(t, r):
    a = len(bin(r['A'])[2:])
    b = len(bin(r['B'])[2:])
    c = len(bin(r['C'])[2:])
    d = len(bin(r['D'])[2:])
    e = len(bin(r['E'])[2:])

    mask = (a, b, c, d, e)
    index = 0
    for i in t:
        if i == mask:
            return index
        index = index + 1
    return 0

def get_hash(r):
    h = hash(str(r))
    return h % 256

def make_tss_database(f):
    t = make_tuple()
    table = []
    for i in t:
        a = []
        for i in range(0, 256):
            a.append([])
        table.append(a)

    for i in f:
        index = get_tuple(t, i)
        table[index][get_hash(i)].append(i)

    return table, t

def tss_search(table, tup, r):
    index = get_tuple(tup, r)
    for i in table[index][get_hash(r)]:
        if i == r:
            return i

def liner_search(table, r):
    for i in table:
        if i == r:
            return i

def test():
    r = {"A": 0b10001111,
         "B": 0b10100000,
         "C": 0b10100101,
         "D": 0b01010011,
         "E": 0b00010110}

    init_database()
    table, tup = make_tss_database(F)


    start = time.time()
    print(tss_search(table, tup, r))
    end = time.time()
    print("tuple space search: %f" % (end - start))

    start = time.time()
    print(liner_search(F, r)
    end = time.time()
    print("liner search: %f" % (end - start))

test()
