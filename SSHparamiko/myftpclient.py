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
        self.exit_flag = False
        # if self.auth():
        self.interactive()

    def auth(self):
        retry_count = 0
        while retry_count < 3:
            username = input("username:").strip()
            if len(username) == 0:continue
            passwd = getpass.getpass()
            auth_str = "ftp_authentication|%s|%s" %(username,passwd)

            self.sock.send(auth_str)
            auth_feedback = self.sock.recv(1024)

            if auth_feedback == "ftp_authentication::success":
                print("\033[32;1mAuthentication Passed!\033[0m")
                self.username  = username
                self.cur_path = username
                return True
            else:
                print("\033[31;1mWrong username or password\033[0m")
                retry_count +=1
        else:
            print("\033[31;1mToo many attempts,exit!\033[0m")

    def interactive(self):
        '''allowcate task to different function according to msg type'''
        try:
            while not self.exit_flag:
                cmd = input("[\033[;32;1m%s:\033[0m%s]>>:" %(self.username,self.cur_path)).strip()
                if len(cmd) == 0:continue
                cmd_parse = cmd.split()
                msg_type = cmd_parse[0]

                #print 'msg_type::',msg_type
                if msg_type in self.func_dic:
                    func = getattr(self,self.func_dic[msg_type])
                    func(cmd_parse)
                else:
                    print("Invalid instruction,type [help] to see available cmd list")
        except KeyboardInterrupt:
            self.exit('exit')
        except EOFError:
            self.exit('exit')

    def put_file(self,msg):
        filename = msg[1]
        
        if os.path.isfile(filename):

            f = open(filename,'rb')
            file_size = os.stat(filename).st_size

            self.sock.send(str(file_size).encode()) #send file size
            self.sock.recv(1024) # wait for ack
            
            sent_size = 0

            while not sent_size == file_size:
                        if file_size - sent_size <= 1024:
                            data = f.read(file_size - sent_size)
                            sent_size += file_size - sent_size
                        else:
                            data = f.read(1024)
                            sent_size += 1024
                        self.sock.send(data)
                        self.show_progress(file_size,sent_size)
            else:
                self.sock.recv(1024) 
                print('\n')
                print('Upload Finished') 

        else:
            print("file [%s] doesn't exist on local disc"%filename) 

    def get_file(self,msg):
        
        filename = msg[1]
        self.sock.send(filename.encode())
        server_respond = self.sock.recv(1024).decode()
        
        if server_respond == "error" :

            print("file [%s] doesn't exist on local disc"%filename)      
        
        else:
            
            file_total_size = int(server_respond)
            received_size = 0
            f = open(filename + '.new','wb')
            self.sock.send(b'ready to recv file')

            while received_size < file_total_size:
                if file_total_size - received_size > 1024: 
                    size = 1024
                else: 
                    size = file_total_size - received_size
                data = self.sock.recv(size)
                received_size += len(data)
                f.write(data)
                
                self.show_progress(file_total_size,received_size)

            else:
                print('\n')
                print('Download Finished')
                self.sock.send(b'done')
                f.close()

    def show_progress(self,total,finished):
        percent=str(int(float(total)/float(finished)*100))
        sys.stdout.write("[%s/%s] %s%s>%s%s\r" %(total,finished,percent,'%','100','%'))
        sys.stdout.flush()

    def list_file(self,cmd):
        
        msg = 'ls'
        self.sock.send(msg.encode('utf-8'))
        file_total_size = int(self.sock.recv(1024))
        self.sock.send(b'ready')

        received_size = 0

        while received_size < file_total_size:            
            if file_total_size - received_size > 1024: 
                size = 1024
            else: 
                size = file_total_size - received_size
            data = self.sock.recv(size)
            received_size += size
            print(data.decode())

    def switch_dir(self,msg):
        #print '--swtich dir:',msg
        self.sock.send("cd".encode())
        self.std_recv()
        #print '==>',feedback
        # if feedback.startswith("switch_dir::ok"):
        #     self.cur_path  = feedback.split("::")[-1]
        # else:
        #     print("\033[31;1m%s\033[0m" % feedback.split("::")[-1])

    def delete(self,msg):
        if len(msg) > 1:
            self.sock.send(('rm'+' '+msg[1]).encode())
            self.std_recv()
        else:
            print("\033[31;1mWrong command usage\033[0m")

    def exit(self,msg):
        self.sock.shutdown(socket.SHUT_WR)
        #sys.exit("Bye! %s" % self.username)

    def std_recv(self):
        self.sock.recv(1024)
        self.sock.send(b'ready')
        print(self.sock.recv(1024).decode())

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