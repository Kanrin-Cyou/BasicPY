import socketserver
import account
import os,sys

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    func_dic = {
            'get' : 'get_file',
            'put' : 'put_file',
            'exit': 'exit',
            'ls'  : 'list_file',
            'cd'  :  'switch_dir',
            'del' :  'delete'
        }

    exit_flag = False

    def handle(self):
        # self.request is the TCP socket connected to the client

        while not self.exit_flag:
            
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

    def std_recv(self):
        #need to send cmd before this function
        self.request.recv(1024)
        self.request.send(b'ready')
        print(self.request.recv(1024).decode())

    def get_file(self,msg):
        filename = msg[1]
        print(filename)
        if os.path.isfile(filename):
            self.std_send(filename,True)
        else:
            self.request.send(b'error')

    def put_file(self,msg):
        pass
    def list_file(self,msg):
        pass
    def switch_dir(self,msg):
        pass
    def delete(self,msg):
        pass

if __name__ == "__main__":
    
    # Create the server, binding to localhost on port 9999
    server = socketserver.ThreadingTCPServer(("localhost", 9002), MyTCPHandler)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()