import socket

client = socket.socket() #声明socket类型，同时生成socket连接对象
client.connect(('localhost',6969))

print('start sending')
while True:
    msg= input('>>:').strip()
    client.send(msg.encode('utf-8'))
    data = client.recv(1024)
    print('recv:',data.decode())

client.close()
