=== LAB: GIAU TIN BANG DCT (Discrete Cosine Transform) ===

Ly thuyet: Giao trinh chuong 2, phan 2.3.1

QUY TRINH THUC HANH:
--------------------
Buoc 1: Tao anh goc
  python3 gen_cover.py

Buoc 2: Giau tin vao anh (embed)
  python3 embed.py
  -> Kiem tra output/stego.png duoc tao ra
  -> Xem gia tri PSNR (>= 40dB la tot)

Buoc 3: Tach tin tu anh (extract)
  python3 extract.py
  -> Kiem tra secret.txt co chua thong diep dung khong

CAU HOI SUY NGHI:
-----------------
1. PSNR la gi? Tai sao PSNR >= 40dB thi anh khong bi phat hien?
2. Tai sao giau vao he so tan so trung binh (mid-frequency)?
3. Dieu gi xay ra neu giau vao he so DC (F(0,0))?
4. Tai sao phai dung zigzag scan?

KHI HOAN THANH: chay stoplab de nop bai.
