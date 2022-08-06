#_*_ coding:utf-8 _*_
import socket
import os
import platform



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


#Beep
import ctypes
#ctypes.WinDLL('user32.dll').SetCursorPos(0,0)
ret=ctypes.WinDLL('Kernel32.dll').Beep(2000,1000)
print(ret)
print(os.popen('cmd').read())




