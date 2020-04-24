# 作业：开发一个支持多用户在线的FTP程序
# 要求：
# 1. 用户加密认证

# 2. 允许同时多用户登录

# 3. 每个用户有自己的家目录 ，且只能访问自己的家目录

# 4. 对用户进行磁盘配额，每个用户的可用空间不同

# 5. 允许用户在ftp server上随意切换目录

# 6. 允许用户查看当前目录下文件

# 7. 允许上传和下载文件，保证文件一致性  put/get
# 8. 文件传输过程中显示进度条 #progress

# 9. 附加功能：支持文件的断点续传

import socket
import sys,os
import getpass

class Client(object):
    
    func_dic = {
        'help': 'help',
        'get' : 'get_file',
        'put' : 'put_file',
        'exit': 'exit',
        'ls'  : 'list_file',
        'cd'  :  'switch_dir',
        'del' :  'delete'
    }

    def __init__(self,host,port):
        self.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None)
        
        # Socket Families(地址簇)
        #     socket.AF_UNIX unix本机进程间通信 
        #     socket.AF_INET　IPV4　
        #     socket.AF_INET6  IPV6
        
        # Socket Types
        #     socket.SOCK_STREAM  #for tcp
        #     socket.SOCK_DGRAM   #for udp 
        #     socket.SOCK_RAW  #原始套接字，普通的套接字无法处理ICMP、IGMP等网络报文，而SOCK_RAW可以；
        #              SOCK_RAW也可以处理特殊的IPv4报文；此外，利用原始套接字，可以通过IP_HDRINCL套接字选项由用户构造IP头。
        #     socket.SOCK_RDM  #是一种可靠的UDP形式，即保证交付数据报但不保证顺序。
        #              SOCK_RAM用来提供对原始协议的低级访问，在需要执行某些特殊操作时使用，如发送ICMP报文。
        #              SOCK_RAM通常仅限于高级用户或管理员运行的程序使用。
        self.sock.connect((host,port))

    def put_file(self,msg):
        pass

    def get_file(self,msg):
        pass

    def show_progress(self):
        pass

    def list_file(self):
        
        while True:

            msg = input('>>:').strip()
            self.sock.send(msg.encode('utf-8'))
            file_total_size = int(self.sock.recv(1024))
            self.sock.send(b'ready')

            received_size = 0

            while received_size < file_total_size:            
                if file_total_size - received_size > 1024: #要收不止一次
                    size = 1024
                else: #最后一次了，剩多少收多少
                    size = file_total_size - received_size
                data = self.sock.recv(size)
                received_size += size
                print(data.decode())

    def switch_dir(self):
        pass
    def delete(self):
        pass
    def exit(self):
        pass
    def help(self,msg):

        print('''
        help    help
        get     get remote_filename
        put     put local_filename
        exit    exit the system
        ls      list all the files in current directory
        cd      cd some_dir
        del     del remote_filename
        ''')

if __name__ == "__main__":
    #Host,Port = 'localhost', 9000
    s = Client('localhost', 9997)
    s.list_file()