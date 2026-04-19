#!/usr/bin/env python3
"""
Bai 1: Giau tin bang DCT
Giao trinh phan 2.3.1 - Chi dung python3, numpy, PIL
"""
import numpy as np
from PIL import Image
import math, json, os

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
    """DCT 2D theo cong thuc 2.7 trong giao trinh"""
    N = 8
    result = np.zeros((N, N), dtype=np.float64)
    for u in range(N):
        for v in range(N):
            cu = 1.0/math.sqrt(2) if u == 0 else 1.0
            cv = 1.0/math.sqrt(2) if v == 0 else 1.0
            s = 0.0
            for j in range(N):
                for k in range(N):
                    s += block[j,k] * \
                         math.cos((2*j+1)*u*math.pi/16) * \
                         math.cos((2*k+1)*v*math.pi/16)
            result[u,v] = 0.25 * cu * cv * s
    return result

def idct2d(block):
    """IDCT 2D theo cong thuc 2.10"""
    N = 8
    result = np.zeros((N, N), dtype=np.float64)
    for j in range(N):
        for k in range(N):
            s = 0.0
            for u in range(N):
                for v in range(N):
                    cu = 1.0/math.sqrt(2) if u == 0 else 1.0
                    cv = 1.0/math.sqrt(2) if v == 0 else 1.0
                    s += cu * cv * block[u,v] * \
                         math.cos((2*j+1)*u*math.pi/16) * \
                         math.cos((2*k+1)*v*math.pi/16)
            result[j,k] = 0.25 * s
    return result

def str_to_bits(s):
    bits = []
    for c in s:
        b = ord(c)
        for i in range(7,-1,-1):
            bits.append((b>>i)&1)
    return bits

def embed(img_path, message, out_path):
    img = Image.open(img_path).convert('L')
    arr = np.array(img, dtype=np.float64)
    H, W = arr.shape
    msg_bits = str_to_bits(message)
    length = len(msg_bits)
    header = [(length>>(31-i))&1 for i in range(32)]
    all_bits = header + msg_bits
    bit_idx = 0
    out = arr.copy()
    total_blocks = (H//8) * (W//8)
    done = 0
    print(f"[*] Dang xu ly {total_blocks} khoi 8x8...")
    for bi in range(H//8):
        for bj in range(W//8):
            if bit_idx >= len(all_bits):
                break
            r0, c0 = bi*8, bj*8
            block = arr[r0:r0+8, c0:c0+8] - 128.0
            dct_block = dct2d(block)
            q = np.round(dct_block / Q50).astype(np.int32)
            for (r,c) in ZIGZAG[MID]:
                if bit_idx >= len(all_bits):
                    break
                if q[r,c] == 0:
                    continue
                bit = all_bits[bit_idx]
                if q[r,c] > 0:
                    q[r,c] = (q[r,c]&~1)|bit
                else:
                    q[r,c] = -((-q[r,c]&~1)|bit)
                bit_idx += 1
            dq = (q * Q50).astype(np.float64)
            restored = idct2d(dq) + 128.0
            out[r0:r0+8, c0:c0+8] = np.clip(np.round(restored), 0, 255)
            done += 1
            if done % 50 == 0:
                print(f"  {done}/{total_blocks} khoi...", end='\r')
    Image.fromarray(out.astype(np.uint8), 'L').save(out_path)
    mse = np.mean((arr-out)**2)
    psnr = 10*np.log10(255**2/mse) if mse > 0 else float('inf')
    print(f"\n[OK] Da giau {len(msg_bits)} bits vao {out_path}")
    print(f"[OK] PSNR = {psnr:.2f} dB {'(Xuat sac!)' if psnr>=40 else '(Tot)'}")
    with open('embed_meta.json','w') as f:
        json.dump({'msg_len_bits': len(msg_bits)}, f)

if __name__ == '__main__':
    os.makedirs('output', exist_ok=True)
    if not os.path.exists('cover.png'):
        print("[LOI] Chua co cover.png. Chay gen_cover.py truoc!")
        exit(1)
    SECRET = "PTIT_AnToanThongTin"
    print(f"[*] Giau tin: '{SECRET}'")
    embed('cover.png', SECRET, 'output/stego.png')
    print("[XONG] Chay extract.py de kiem tra")
