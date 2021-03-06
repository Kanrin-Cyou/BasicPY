import socketserver
import account
import os,sys,time

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    func_dic = {
            'auth': 'authentication',
            'get' : 'get_file',
            'put' : 'put_file',
            'exit': 'exit',
            'ls'  : 'list_file',
            'cd'  :  'switch_dir',
            'del' :  'delete',
        }

    exit_flag = False
    status = False

    def handle(self):
        # self.request is the TCP socket connected to the client

        while not self.exit_flag:
            
            while not self.status:
                msg = self.request.recv(1024).decode()
                print(msg)
                cmd_parse = msg.split()
                self.authentication(cmd_parse)

            else:
                msg = self.request.recv(1024).decode()
                print(msg)
                cmd_parse = msg.split()
                msg_type = cmd_parse[0]

                #print 'msg_type::',msg_type
                if msg_type in self.func_dic:
                    func = getattr(self,self.func_dic[msg_type])
                    func(cmd_parse)
                else:
                    msg = "Invalid instruction,type [help] to see available cmd list"
                    self.std_send(msg)

    def authentication(self,msg):
        if msg[0] in account.accounts:
            if msg[1] == account.accounts[msg[0]]['passwd']:
                self.login_user = msg[0]
                self.folder = account.accounts[msg[0]]['home']
                self.status = True
                msg = "Welcome"
                self.std_send(msg)
            else:
                msg = "Wrong Password"
                self.std_send(msg)    

        else:
            msg = "The Account doesn't exist, Please consult with your manager"
            self.std_send(msg)    

    def std_send(self,msg,isfile=False):

        if isfile == True:
            f = open(msg,'rb')
            size = os.stat(msg).st_size

        else:
            f = msg.encode()
            size = len(msg)

        self.request.send(str(size).encode()) #send filesize to client
        self.request.recv(1024) #wait client to confirm
        
        if isfile == True: 
            size_left = size
            #print "--size left:",size_left
            while size_left > 0:
                if size_left < 1024:
                    self.request.send(f.read(size_left))
                    size_left = 0
                else:
                    self.request.send(f.read(1024))
                    size_left -= 1024
        else:
            self.request.send(f)
        self.request.recv(1024) #client ack

        if isfile == True:
            f.close()
        print('Sent')

    def std_recv(self,msg,isfile=False):
        #need to send cmd before this function
        size = self.request.recv(1024)
        filename = msg
        file_total_size = int(size)
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
        
        print(filename)

        f = open(filename,'wb')

        self.request.send(b'ready to recv file')

        while received_size < file_total_size:
            if file_total_size - received_size > 1024: 
                size = 1024
            else: 
                size = file_total_size - received_size
            data = self.request.recv(size)
            received_size += len(data)
            f.write(data)

        self.request.send(b'Received')
        f.close()
        print('Received')

    def get_file(self,msg):
        filename = msg[1]
        if os.path.isfile(filename):
            self.std_send(filename,True)
        else:
            self.request.send(b'error')

    def put_file(self,msg):
        filename = msg[1]
        self.std_recv(filename,True)

    def list_file(self,msg):
        cmd = 'ls'
        cmd_res = os.popen(cmd).read()
        self.std_send(cmd_res)

    def switch_dir(self,msg):

        cmd = 'cd'
        os.popen(cmd)
        time.sleep(0.1)
        cmd_res = os.popen('ls').read()
        self.std_send(cmd_res)

    def delete(self,msg):
        filename = msg[1]
        print(filename)
        if os.path.isfile(filename):
            cmd = 'rm ' + msg[1]
            print(cmd)
            os.popen(cmd)
            time.sleep(0.1)
            cmd_res = os.popen('ls').read()
            self.std_send(cmd_res)
        else:
            self.std_send("The file doesn't exist in current disk.")

if __name__ == "__main__":
    
    # Create the server, binding to localhost on port 9999
    server = socketserver.ThreadingTCPServer(("localhost", 9002), MyTCPHandler)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()