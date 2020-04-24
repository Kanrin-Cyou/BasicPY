#ftp server
# 1.读取文件名
# 2.检测文件是否存在，并打开
# 3.检测文件大小
# 4.发送文件大小和md5给客户端
# 5.等待客户端确认
# 6.开始边读边发数据

import socket , os ,time, hashlib
server = socket.socket() #声明socket类型，同时生成socket连接对象,实例化

server.bind(('localhost',9997)) #IP,绑定需要监听的端口

server.listen() #监听数量

while True:
    conn, addr = server.accept() #等电话打进来
    print("new coon:", addr) #conn就是客户端连过来，而在服务器端为其生成的一个连接实例
    while True:
        data = conn.recv(1024)
        if not data:
            print('client is disconnected')
            break
        
        filename = data.decode()
        
        if os.path.isfile(filename):
            
            f = open(filename,'rb')
            #m = hashlib.md5()
            file_size = os.stat(filename).st_size
            conn.send(str(file_size).encode()) #send file size

            conn.recv(1024) # wait for ack

            for line in f:
                #m.update(line)
                conn.send(line)
            #print('file md5', m.hexdigest())
            f.close()

            conn.recv(1024) 
            #conn.send(m.hexdigest().encode())
            print('Reply Done') 

        else:
            err_msg="error"
            conn.send(err_msg.encode())

server.close()