import numpy as np
import binascii

# bpmファイルを生成するスクリプト
# === 以下のパラメタをセット ===
# width * height は 32bit使える(8k余裕)
width = 1920
height = 1080
num = 8
# ===

separate = width // num

a = np.empty([3, width, height], dtype='uint8')

# カラーバーはここで設定
for i in range(num): # B G R 各256まで
    a[0, (separate*i):(separate*i+separate), :] = 100;
    a[1, (separate*i):(separate*i+separate), :] = 100 - 10*i;
    a[2, (separate*i):(separate*i+separate), :] = 100;

with open('colorbar.bmp', 'wb') as fin:
    fmt = 'BM'.encode()
    fin.write(fmt)

    # 4byte でリトルエンディアン書き込み
    filesize            = 54 + (width * height * 3)
    filesize_bin        = filesize.to_bytes(4, 'little')
    fin.write(filesize_bin)

    # 予約領域を4byteで指定
    val = 0
    zero_4bytes = val.to_bytes(4, 'big')
    fin.write(zero_4bytes)

    # ファイルの先頭から画像データまでのバイト数を4バイトで指定。
    val = 54
    fin.write(val.to_bytes(4, 'little'))

    # 情報ヘッダサイズ
    val = 40
    fin.write(val.to_bytes(4, 'little'))
    
    # 横幅, 縦幅を4バイトで指定
    fin.write(width.to_bytes(4, 'little'))  # 横幅
    fin.write(height.to_bytes(4, 'little')) # 縦幅

    # プレーン数を2バイトで指定
    val = 1 # 常に1
    fin.write(val.to_bytes(2, 'little'))

    # 1画素に対するbit数を指定
    val = 24
    fin.write(val.to_bytes(2, 'little'))

    # 圧縮形式
    val = 0
    fin.write(val.to_bytes(4, 'little'))

    # 圧縮サイズ
    fin.write(val.to_bytes(4, 'little'))

    # 水平、垂直解像度
    val = width
    fin.write(width.to_bytes(4, 'little'))
    fin.write(height.to_bytes(4, 'little'))

    # 色数、重要色素
    val = 0
    fin.write(val.to_bytes(4, 'little'))
    fin.write(val.to_bytes(4, 'little'))


    # データ部
    for y in range(height):
        for x in range(width):
            for z in range(3):
                val = int(a[z,x,y])
                fin.write(val.to_bytes(1, 'little'))

