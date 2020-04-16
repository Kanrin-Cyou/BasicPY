import socket

server = socket.socket()

server.bind(('localhost',6969)) #IP,绑定需要监听的端口
server.listen(2) #监听数量

print('waiting...')
conn,addr = server.accept() #等电话打进来
print(conn,addr)
print('coming...')
while True:
    #conn就是客户端连过来，而在服务器端为其生成的一个连接实例
    data = conn.recv(1024)
    print('recv:',data)
    if not data:
        print('client has lost...')
        break
    conn.send(data.upper())

server.close()



