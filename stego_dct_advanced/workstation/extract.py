#!/usr/bin/env python3
"""Bai 2: Tach tin tu anh DCT"""
import numpy as np
from PIL import Image
import math, os

Q50 = np.array([
    [16,11,10,16,24,40,51,61],
    [12,12,14,19,26,58,60,55],
    [14,13,16,24,40,57,69,56],
    [14,17,22,29,51,87,80,62],
    [18,22,37,56,68,109,103,77],
    [24,35,55,64,81,104,113,92],
    [49,64,78,87,103,121,120,101],
    [72,92,95,98,112,100,103,99]
], dtype=np.float64)

ZIGZAG = [
    (0,0),(0,1),(1,0),(2,0),(1,1),(0,2),(0,3),(1,2),
    (2,1),(3,0),(4,0),(3,1),(2,2),(1,3),(0,4),(0,5),
    (1,4),(2,3),(3,2),(4,1),(5,0),(6,0),(5,1),(4,2),
    (3,3),(2,4),(1,5),(0,6),(0,7),(1,6),(2,5),(3,4),
    (4,3),(5,2),(6,1),(7,0),(7,1),(6,2),(5,3),(4,4),
    (3,5),(2,6),(1,7),(2,7),(3,6),(4,5),(5,4),(6,3),
    (7,2),(7,3),(6,4),(5,5),(4,6),(3,7),(4,7),(5,6),
    (6,5),(7,4),(7,5),(6,6),(5,7),(6,7),(7,6),(7,7)
]
MID = slice(5, 30)

def dct2d(block):
    N = 8
    result = np.zeros((N,N), dtype=np.float64)
    for u in range(N):
        for v in range(N):
            cu = 1.0/math.sqrt(2) if u==0 else 1.0
            cv = 1.0/math.sqrt(2) if v==0 else 1.0
            s = 0.0
            for j in range(N):
                for k in range(N):
                    s += block[j,k] * \
                         math.cos((2*j+1)*u*math.pi/16) * \
                         math.cos((2*k+1)*v*math.pi/16)
            result[u,v] = 0.25*cu*cv*s
    return result

def extract(stego_path):
    img = Image.open(stego_path).convert('L')
    arr = np.array(img, dtype=np.float64)
    H, W = arr.shape
    bits = []
    HEADER = 32
    total_need = HEADER
    header_done = False
    msg_len = 0
    for bi in range(H//8):
        for bj in range(W//8):
            if len(bits) >= total_need and header_done:
                break
            r0,c0 = bi*8, bj*8
            block = arr[r0:r0+8, c0:c0+8] - 128.0
            q = np.round(dct2d(block) / Q50).astype(np.int32)
            for (r,c) in ZIGZAG[MID]:
                if len(bits) >= total_need and header_done:
                    break
                if q[r,c] == 0:
                    continue
                coeff = int(q[r,c])
                bits.append(coeff&1 if coeff>0 else (-coeff)&1)
                if not header_done and len(bits)==HEADER:
                    val = 0
                    for b in bits[:32]: val=(val<<1)|b
                    msg_len = val
                    total_need = HEADER + msg_len
                    header_done = True
    msg_bits = bits[HEADER:HEADER+msg_len]
    chars = []
    for i in range(0, len(msg_bits)-7, 8):
        val = 0
        for j in range(8): val=(val<<1)|msg_bits[i+j]
        chars.append(chr(val))
    message = ''.join(chars)
    print(f"[OK] Thong diep: '{message}'")
    with open('secret.txt','w') as f:
        f.write(message)
    print(f"[OK] Da luu vao secret.txt")
    return message

if __name__ == '__main__':
    if not os.path.exists('output/stego.png'):
        print("[LOI] Chua co output/stego.png. Chay embed.py truoc!")
        exit(1)
    print("[*] Dang tach tin...")
    extract('output/stego.png')
