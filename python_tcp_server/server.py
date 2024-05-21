from socketserver import BaseRequestHandler, TCPServer


class MyTCPHandler(BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print(self.client_address[0])
        self.request.sendall(self.data.upper())


if __name__ == '__main__':
    HOST, PORT = "localhost", 9999
    with TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
