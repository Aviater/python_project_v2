import socket
import pickle
import threading, queue

class Connection:
    clientsocket = None
    address = None
    client = None
    def __init__(self, header_length, port, host, char_format):
        self.header_length = header_length
        self.port = port
        self.host = host
        self.char_format = char_format
    
    # Connect to socket
    def connect_to_server(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        
    # Handle the server response
    def handle_response(self):
        connected = True
        while connected:
            # Read header
            msg_length = self.client.recv(self.header_length).decode(self.char_format)
            if msg_length:
                msg_length = int(msg_length)
                
                # Read body
                msg_encoded = self.client.recv(msg_length)
                msg = pickle.loads(bytes(msg_encoded))
                print('[HEADER]:', msg_length)
                print('[ BODY ]:', msg['body']['content'])
                
                print('[PLAYER]:', msg['body']['players'])
            
            connected = False
            
    def send_message(self, payload):
        message = pickle.dumps({
            'header': {
                'type': 'str'
            },
            'body': payload
        })
        
        # Set header
        msg_length = len(message)
        header = str(msg_length).encode(self.char_format)
        header += b' ' * (self.header_length - len(header))
        self.client.send(header)
        self.client.send(bytes(message))
        
def main(player_name):
    HOST = socket.gethostbyname(socket.gethostname())
    
    con1 = Connection(64, 9999, HOST, 'utf-8')
    
    con1.connect_to_server()
    con1.send_message(player_name)
    con1.handle_response()
    con1.handle_response()
    con1.handle_response()
    con1.handle_response()
    con1.handle_response()