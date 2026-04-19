#!/usr/bin/env python3
"""Tao anh cover.png de dung lam anh goc"""
import numpy as np
from PIL import Image
np.random.seed(42)
arr = np.zeros((256,256), dtype=np.uint8)
for i in range(256):
    for j in range(256):
        arr[i,j] = int(128 + 60*np.sin(2*np.pi*i/32) + 40*np.cos(2*np.pi*j/16)) % 256
Image.fromarray(arr, 'L').save('cover.png')
print("[OK] Da tao cover.png (256x256)")
