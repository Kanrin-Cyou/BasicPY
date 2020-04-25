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
        self.status = False
        self.sock.connect((host,port))
        self.exit_flag = False
        
        if self.auth():
            self.interactive()

    def auth(self):
        while not self.status:
            #cmd = input("[\033[;32;1m%s:\033[0m%s]>>:" %(self.username,self.cur_path)).strip()
            msg = input('>>name pwd:').strip()
            print(msg)
            self.sock.send(msg.encode())
            self.sock.recv(1024)
            self.sock.send(b'ready')
            msg = self.sock.recv(1024)
            self.sock.send(b'recevied')
            
            msg = msg.decode()
            if msg == 'Welcome':
                print(msg)
                self.status = True
            else:
                print(msg)
        return True
        

    def interactive(self):
        '''allowcate task to different function according to msg type'''
        try:
            while True:
                #cmd = input("[\033[;32;1m%s:\033[0m%s]>>:" %(self.username,self.cur_path)).strip()
                cmd = input('>>:').strip()
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
            
            send = msg[0]+' '+filename
            self.sock.send(send.encode())    

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
        send_msg = msg[0] + ' ' + msg[1]
        self.sock.send(send_msg.encode())
        server_respond = self.sock.recv(1024).decode()
        
        if server_respond == "error" :

            print("file [%s] doesn't exist on local disc"%filename)      
        
        else:
            
            file_total_size = int(server_respond)
            received_size = 0

            n=3
            if os.path.isfile(filename):
                name = filename.rsplit('.',1)
                filetype = '.' + name[1]
                filename = name[0] + '[2]' + filetype
                while os.path.isfile(filename):
                    name = filename.rsplit('[',1)
                    filename = name[0] + '[%i]'%n + filetype
                    n += 1
            
            f = open(filename,'wb')

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

        self.sock.send(b'received')

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
            self.sock.send(('del'+' '+msg[1]).encode())
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
        self.sock.send(b'done')
        
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
    s = Client('localhost', 9002)