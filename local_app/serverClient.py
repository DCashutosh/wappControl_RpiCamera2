import socket

class ServerClient:

    def __init__(self):
        self.s = None

    def connect_to_server(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        print(f'Connected to server at {host}:{port}')
        #return self.s
    
    def send_message(self, message):
        try:
            self.s.sendall(message.encode('utf-8'))
            print(f'Sent: {message}')
        except socket.error as e:
            print(f'Error sending message: {e}')
    
    def receive_response(self):
        try:
            data = self.s.recv(1024)
            response = data.decode('utf-8')
            print(f'Received: {response}')
            #return response
        except socket.error as e:
            print(f'Error receiving response: {e}')
    
    def receive_multimedia(self, save_path):
        try:
            with open(save_path, 'wb') as f:
                while True:
                    data = self.s.recv(1024)
                    if data.endswith(b"<EOF>"):  # Check for EOF marker
                        f.write(data[:-5])  # Write data excluding the EOF marker
                        break
                    f.write(data)
            print("File received successfully.")
        except socket.error as e:
            print(f'Error receiving multimedia: {e}')
        
    
    def receive_data(self,file_path):
        header = self.s.recv(4).decode('utf-8')

        if header == "MASG":
            self.receive_response()

        elif header == "FILE":
            # file_name = input("Please provide a file name : ")
            # file_path = "E:/tcp_ip_test"+f'/{file_name}'
            self.receive_multimedia(file_path)
        
        else:
            print("Unknown header received, stopping.")

