#_*_ coding:utf-8 _*_
import pyautogui
import base64
from PIL import Image
import io
import os


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
