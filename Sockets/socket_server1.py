import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            try:
                #self.request if the TCP socket connected to the client
                self.data = self.request.recv(1024).strip()
                print("{} wrote:".format(self.client_address[0]))
                print(self.data)
                #just send back the same data, but upper-cased
                self.request.send(self.data.upper())
            except ConnectionResetError as e:
                print("err",e)
                break
if __name__ == "__main__":
    HOST, PORT = "localhost", 9997
    # Create the server, binding to localhost on port 9999 
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
    
    #activate the server; this will keep running until you interrrupt the program with ctrl+C
    
    server.serve_forever()