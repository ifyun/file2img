# FILE2IMG

将任意文件储存到图片的像素中，保存为 BMP 图片，储存文件后的图片肉眼看不出区别。

## 原理

用图片 RGB 数值的奇偶表示二进制，达到储存文件的目的，奇数表示 1，偶数表示 0

- RGB 第 0 ~ 15 位表示文件名的长度
- RGB 第 16 ~ 48 位表示文件长度
- RGB 第 48 位之后存储文件名 + 文件内容

文件最大长度限制：2<sup>32</sup> bits = 524288 KiB

一张图片可存储的文件长度：height * width * 3 - 48 bits

一张 1920 x 1080 的图片可存储长度为：

```
1920 * 1080 * 3 - 48 bits = 777594 Bytes ≈ 759 KiB
```

> 原图片不会被修改，不支持 PNG 图片

## 环境要求

- Python 3.11
- numpy
- PIL(pillow)

```bash
pip install numpy
pip install pillow
```

## 使用

### 将文件写入图片

```bash
python file2img.py -w --file D:\\archive.zip --img D:\\image.jpg --dest D:\\archive.bmp
```

`D:\archive.zip` 文件内容将会写入到 `D:\image.jpg`，带有数据的图片会保存到 `D:\archive.bmp`。

### 从图片中提取文件

```bash
python file2img.py -r --img D:\\archive.bmp --dest D:\\
```

`D:\archive.bmp` 中的文件将被读取并写入到 `D:` 目录，文件名从图片中读取。

### 完整选项

```
options:
  -h, --help            show this help message and exit
  -r, --read            读取
  -w, --write           写入
  -f FILE, --file FILE  文件路径
  -i IMG, --img IMG     图片路径
  -d DEST, --dest DEST  保存路径(读取时为目录)
```
