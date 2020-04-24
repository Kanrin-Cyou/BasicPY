import socket, os ,time, hashlib

client = socket.socket() #声明socket类型，同时生成socket连接对象

client.connect(('localhost',9998))

while True:
    cmd = input('>>:').strip()
    if len(cmd) == 0: continue
    if cmd.startswith('get'):

        client.send(cmd.encode())
        server_respond = client.recv(1024)
        print('server response:',server_respond)

    
        file_total_size = int(server_respond.decode())
        received_size = 0
        filename = cmd.split()[1]
        f = open(filename + '.new','wb')
        m = hashlib.md5()

        client.send(b'ready to recv file')

        while received_size < file_total_size:
            
            if file_total_size - received_size > 1024： #要收不止一次
                size = 1024
            else: #最后一次了，剩多少收多少
                size = file_total_size - received_size
            data = client.recv(size)

            received_size += len(data)
            m.update(data)
            f.write(data)
            print(file_total_size,received_size) 
        else:
            new_file_md5 = m.hexdigest()
            print('file recv done',file_total_size,received_size)
            client.send(b'done')
            f.close()
    
        server_file_md5 = client.recv(1024)
        print('server file md5',server_file_md5.decode())
        print('client file md5',new_file_md5)

client.close()
