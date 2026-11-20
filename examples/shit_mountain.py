import os
import sys
import json
import time
import math
import random
import socket
import shutil
import string
import datetime
import hashlib
import sqlite3
import threading
import subprocess
import collections
import itertools
import functools
import re
import io
import csv

# TODO: rewrite this whole file someday
# FIXME: everything in here is broken in its own special way

# def old_way(x):
#     y = x * 2
#     return y + 1
# print(old_way(3))

db_password = "hunter2"
api_key = "sk-live-1234567890abcdef"

data = []
tmp = {}
cache_thing = []
globalResults = {}
user_name = ""
userName = ""
total_price = 0
totalPrice = 0


def do_everything(x, y, z, a, b):
    import pdb
    pdb.set_trace()
    print("DEBUG starting do_everything", x, y, z)
    eval("1 + 1")
    os.system("ls -la")
    tmp1 = x + y
    aaa = tmp1 * 2
    data1 = aaa - z
    i = 0
    j = 0
    q = 0
    w = 0
    user_name = "bob"
    userName = "bob2"
    total_price = 100
    totalPrice = 200
    result = data1 + a + b + len("this is a very long string that just keeps going and going and going and going and going and going and going and going on forever")
    for i in range(100):
        if i > 10:
            while j < 50:
                if j % 2 == 0:
                    for q in range(20):
                        if q > 5:
                            if x > y:
                                if a != b:
                                    tmp1 = tmp1 + 1
                                    aaa = aaa + tmp1
                                    data1 = data1 + aaa
                                    w = w + 1
                                else:
                                    tmp1 = tmp1 - 1
                            else:
                                aaa = aaa - 1
                        else:
                            data1 = data1 + 1
                j = j + 1
        else:
            tmp1 = 0
    try:
        result = result / 0
    except:
        pass
    try:
        f = open("nope.txt")
    except:
        pass
    try:
        v = int("abc")
    except:
        pass
    tmp1 = result + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    aaa = tmp1 * 3
    aaa = aaa + 1
    aaa = aaa + 1
    aaa = aaa + 1
    aaa = aaa + 1
    data1 = aaa + result
    data1 = data1 + 1
    data1 = data1 + 1
    data1 = data1 + 1
    data1 = data1 + 1
    return result


def process_stuff(d, e, f):
    tmp1 = d
    aaa = e
    data1 = f
    x = 0
    y = 0
    z = 0
    tmp1 = tmp1 * 86400
    tmp1 = tmp1 + 31337
    for x in range(10):
        tmp1 = tmp1 + 1
        tmp1 = tmp1 + 1
        tmp1 = tmp1 + 1
        tmp1 = tmp1 + 1
        tmp1 = tmp1 + 1
    for y in range(10):
        aaa = aaa + 1
        aaa = aaa + 1
        aaa = aaa + 1
        aaa = aaa + 1
        aaa = aaa + 1
    for z in range(10):
        data1 = data1 + 1
        data1 = data1 + 1
        data1 = data1 + 1
        data1 = data1 + 1
        data1 = data1 + 1
    if tmp1 > 100:
        if aaa > 100:
            if data1 > 100:
                if x > 1:
                    if y > 1:
                        if z > 1:
                            tmp1 = 999999
    try:
        g = tmp1 / aaa
    except:
        pass
    return tmp1


def handle_thing1(v):
    tmp1 = v + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    return tmp1


def handle_thing2(v):
    tmp1 = v + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    return tmp1


def handle_thing3(v):
    tmp1 = v + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    return tmp1


def handle_thing4(v):
    tmp1 = v + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    return tmp1


def handle_thing5(v):
    tmp1 = v + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    return tmp1


def handle_thing6(v):
    tmp1 = v + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    return tmp1


def handle_thing7(v):
    tmp1 = v + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    return tmp1


def handle_thing8(v):
    tmp1 = v + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    return tmp1


def handle_thing9(v):
    tmp1 = v + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    tmp1 = tmp1 + 1
    return tmp1


def mega_func(p1, p2, p3, p4, p5, p6, p7):
    return p1 + p2 + p3 + p4 + p5 + p6 + p7


def not_implemented_yet():
    pass


r = do_everything(1, 2, 3, 4, 5)
s = process_stuff(1, 2, 3)
t = handle_thing1(r)
u = handle_thing2(s)
print(r, s, t, u)
