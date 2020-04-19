import socket

client = socket.socket() #声明socket类型，同时生成socket连接对象

client.connect(('localhost',9998))

while True:
    cmd = input('>>:').strip()
    if len(cmd) == 0: continue
    client.send(cmd.encode())
    cmd_res_size = client.recv(1024) #接受命令结果的长度
    print('package size:',cmd_res_size)
    client.send('confirmed'.encode("utf-8"))
    
    received_size = 0
    received_data = b'' 
    
    while received_size < int(cmd_res_size.decode()):
        data = client.recv(1024)
        received_size += len(data) #每次收到的有可能小于1024，所以必须用len判断
        received_data += data
        print('received size:',received_size)
    else:
        print('cmd receive done:',received_size)
        print(received_data.decode())

client.close()