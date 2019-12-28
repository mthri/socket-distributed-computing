import socket
import json

data = []


def Prime(num):
    if num > 1: 
        chk = True
        for i in range(2, num//2): 
            if (num % i) == 0: 
                chk = False
                break
        if chk:   
            data.append(num)
            chk = False


def start(num):
    seq_num=num.split(',')
    for q in range(int(seq_num[0]),int(seq_num[1])):
        Prime(q) 


def Finish():
    tmp = ''
    for i in data:
        tmp = tmp + str(i) + ','
    return tmp

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1',12347))     
msg="ok"
client.send(str.encode(msg))

while True:
    res = client.recv(1024)
    x = str(res.decode('ascii'))
    start(x)
    data1 = Finish()
    client.send(data1.encode())
    print(res,' Sent!')