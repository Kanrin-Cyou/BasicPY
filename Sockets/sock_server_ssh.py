import socket , os ,time
server = socket.socket() #声明socket类型，同时生成socket连接对象,实例化

server.bind(('localhost',9998)) #IP,绑定需要监听的端口

server.listen() #监听数量

while True:
    conn, addr = server.accept() #等电话打进来
    print("new coon:", addr) #conn就是客户端连过来，而在服务器端为其生成的一个连接实例
    while True:
        data = conn.recv(1024)
        if not data:
            print('client is disconnected')
            break
        print("execute command:",data)
        cmd_res = os.popen(data.decode()).read()
        print('before send',len(cmd_res))
        if len(cmd_res) == 0:
            cmd_res = "cmd has no output"

        conn.send(str(len(cmd_res.encode())).encode('utf-8')) #先发大小给客户端
        #time.sleep(0.5) #防止粘包
        client_ack = conn.recv(1024) #wait client to confirm
        conn.send(cmd_res.encode('utf-8')) #两次紧挨着的操作，会当成一次
        print('Reply Done')

server.close()