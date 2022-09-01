#_*_ coding:utf-8 _*_
import pyautogui
import base64
from PIL import Image
import io
import os

import time

for i in range(1, 101):
    print("\r", end="")
    print("Download progress: {}%: ".format(i), "▋" * (i // 2), end="")
    #sys.stdout.flush()
    time.sleep(0.05)

scale=100
print("执行开始".center(scale+28,'-'))
start = time.perf_counter()
for i in range(scale+1):
    a = '*' * i
    b = '.' * (scale - i)
    c = (i/scale)*100
    t = time.perf_counter() - start
    print("\r任务进度:{:>3.0f}% [{}->{}]消耗时间:{:.2f}s".format(c,a,b,t),end="")
    time.sleep(0.03)
print("\n"+"执行结束".center(scale+28,'-'))


img = pyautogui.screenshot()
print(img)
#img.show()
print(img.size)
print(img.format)

img_byte=io.BytesIO()
img.save(img_byte,format="JPEG")
binary_str=img_byte.getvalue()

print(len(binary_str))
fileName='screenTest.jpg'
with open(fileName,'wb')as file:
        file.write(binary_str)
        file.close()
