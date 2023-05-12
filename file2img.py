#!/bin/python3
import argparse
import os
import numpy as np
from sys import stderr
from PIL import Image


def set_color(byte, bit):
    # 转为奇数
    byte = byte | 1
    if bit == 1:
        return byte
    else:
        return byte - 1


def get_bit(byte):
    if byte & 1 != 0:
        return 1
    else:
        return 0


def int_to_bits(val, length):
    bits = np.zeros((length,), dtype="uint8")
    length -= 1

    while length >= 0:
        bits[length] = val & 1
        val = val >> 1
        length -= 1

    return bits


def bits_to_int(bits):
    val = 0
    bits = np.flip(bits)
    for i in range(bits.size):
        if bits[i] == 1:
            val += pow(2, i)

    return val


def read(image, dest):
    img = Image.open(image)
    colors = np.array(img).flatten()

    fname_size_bits = np.zeros(16, dtype="uint8")
    fsize_bits = np.zeros(32, dtype="uint8")

    for i in range(colors.size):
        if i < 16:
            fname_size_bits[i] = get_bit(colors[i])
        elif i < 16 + 32:
            fsize_bits[i - 16] = get_bit(colors[i])
        else:
            break
        i += 1

    fname_size = bits_to_int(fname_size_bits)
    fsize = bits_to_int(fsize_bits)

    fname_bits = np.zeros(fname_size, dtype="uint8")
    fbits = np.zeros(fsize, dtype="uint8")

    for i in range(colors.size):
        if i < 16 + 32:
            continue
        if i < 16 + 32 + fname_size:
            fname_bits[i - 16 - 32] = get_bit(colors[i])
        elif i < 16 + 32 + fname_size + fsize:
            fbits[i - 16 - 32 - fname_size] = get_bit(colors[i])
        else:
            break
        i += 1

    save_path = dest + str(bytes(np.packbits(fname_bits)), encoding="utf-8")
    with open(save_path, "wb") as f:
        file_bytes = bytes(np.packbits(fbits))
        f.write(file_bytes)


def write(file, image, dest_file):
    fsize = os.path.getsize(file)
    fname = os.path.basename(file)
    img = Image.open(image)

    width = img.size[0]
    height = img.size[1]
    img_size = width * height * 3

    print("%-9s: %s" % ("File Name", fname))
    print("%-9s: %d bits" % ("File Size", fsize * 8))
    print("%-9s: %d bits" % ("Max Size", img_size - 48))

    if img_size < fsize * 8 + 16 + 32:
        stderr.write("File too large!")
        exit(1)

    # 文件名的 bit 数组
    fname_bits = np.unpackbits(np.frombuffer(bytes(fname, "utf-8"), dtype="uint8"))
    # 文件名长度的 bit 数组
    fname_size_bits = int_to_bits(fname_bits.size, 16)
    # 文件内容的 bit 数组
    fbits = np.unpackbits(np.fromfile(file, dtype="uint8"))
    # 文件长度的 bit 数组
    fsize_bits = int_to_bits(fbits.size, 32)

    total_bits = np.concatenate((fname_size_bits, fsize_bits, fname_bits, fbits))

    i = 0
    pix = np.array(img)
    length = total_bits.size
    print("Saving...")
    for x in range(height):
        for y in range(width):
            if i >= length:
                break
            r, g, b = pix[x, y]

            if i < length:
                r = set_color(r, total_bits[i])
            i += 1
            if i < length:
                g = set_color(g, total_bits[i])
            i += 1
            if i < length:
                b = set_color(b, total_bits[i])
            i += 1

            pix[x, y] = (r, g, b)

    Image.fromarray(pix).save(dest_file, "bmp")
    print("Complete")


if __name__ == "__main__":
    args = argparse.ArgumentParser(description="Save file to RGBs of image.")
    args.add_argument("-r", "--read", action="store_true", dest="read", help=u"读取")
    args.add_argument("-w", "--write", action="store_true", dest="write", help=u"写入")
    args.add_argument("-f", "--file", type=str, dest="file", help=u"文件路径")
    args.add_argument("-i", "--img", type=str, dest="img", help=u"图片路径")
    args.add_argument("-d", "--dest", type=str, dest="dest", help=u"保存路径(读取时为目录)")

    args = args.parse_args()
    if args.read:
        read(args.img, args.dest)
    elif args.write:
        write(args.file, args.img, args.dest)
