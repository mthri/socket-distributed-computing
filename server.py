from queue import Queue
import socket
import threading
import time

job = Queue()
result = Queue()

def SocketThread(conn,addr,j,result):
    tmp = ''
    while True:
        data = conn.recv(1024)
        if not data: 
            conn.close()
            print(addr[0], ':', addr[1], 'was closed.') 
            break
        rec = str(data.decode('ascii'))
        if rec != 'ok':
            result.put(rec)

        # stay in loop until have any job
        while j.empty():
            print(':/')
        
        if not j.empty():
            tmp = j.get()
            conn.send(tmp.encode('ascii'))

        

def CreateWork(q,r):
    _max=100000
    step=100
    # generate number range with 100 step by default
    # For example first step: '0,100'
    # and put it on queue
    for i in range(step,_max,step):
        tmp = str(i-step) + ',' + str(i)
        q.put(tmp)

    # if any thread get response, write it on PrimeNumber file
    while True:
        time.sleep(.5)
        if not r.empty():
            f = open('PrimeNumber.txt','a')
            f.write(r.get())
            f.close()

            

def AcceptSocket():
    port = 12347
    # 127.0.0.1
    host = ''
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen(5)
    threading.Thread(target=CreateWork,args=(job,result)).start()
    try:
        while True:
            c, addr = s.accept()
            print('Connected to :', addr[0], ':', addr[1]) 
            threading.Thread(target=SocketThread,args=(c,addr,job,result)).start()
    except Exception as ex:
        print(ex)



if __name__ == "__main__":
    AcceptSocket()
