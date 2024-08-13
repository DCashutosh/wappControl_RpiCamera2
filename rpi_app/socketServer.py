import socket

class SocketServer:

    def __init__(self):
        self.s = None
        self.conn = None
        self.addr = None

    def setup_server(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((host, port))
        self.s.listen(1)
        print(f'Server listening on {host}:{port}')
        self.conn, self.addr = self.s.accept()
    
    def send_response(self, response):
        # response = input("Enter response: ")
        self.conn.sendall(b'MASG')
        self.conn.sendall(response.encode('utf-8'))
    
    def handle_messages(self):
        print(f'Connected by {self.conn.getpeername()}')
        data = self.conn.recv(1024)
        if not data:
            return None
        message = data.decode('utf-8')
        print(f'Received: {message}')
        return message
               
    def send_multimedia(self, path):
        
        print(f'Connected by {self.conn.getpeername()}')
        self.conn.sendall(b'FILE')

        with open(path, 'rb') as f:
            data = f.read(1024)
            while data:
                self.conn.sendall(data)
                data = f.read(1024)        
        self.conn.sendall(b'<EOF>')
        print("File sent successfully.")
    
    def close_server(self):
        self.conn.close()
        self.s.close()

    
   
