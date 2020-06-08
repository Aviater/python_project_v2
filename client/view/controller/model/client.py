import socket
import pickle
import threading
from queue import Queue

# UI reads state_update response and tries to parse in
# non-existent data.

# Hint: Player properties must be rendered in their own UI method for parsing
# state_update data only.

class Connection:
    clientsocket = None
    address = None
    client = None
    HOST = socket.gethostbyname(socket.gethostname())
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
    def handle_response(self, queue):
        connected = True
        while connected:
            # Read header
            msg_length = self.client.recv(self.header_length).decode(self.char_format)
            if msg_length:
                msg_length = int(msg_length)
                
                # Read body
                msg_encoded = self.client.recv(msg_length)
                msg = pickle.loads(bytes(msg_encoded))
                
                if msg['header']['clients'] == 2:
                    payload = {
                        'ready': True,
                        'players': msg['body']['players'],
                        'header': msg['header'],
                        'data': msg['body']['content']
                    }
                    queue.put(payload)
                    
                # Output
                print('---- RESPONSE ----')
                print('[LENGTH]:', msg_length)
                print('[HEADER]:', msg['header'])
                print('[PLAYER]:', msg['body']['players'])
                print('[ BODY ]:', msg['body']['content'])
                print('------------------')
            
            connected = False
            
    def send_message(self, header, payload):
        message = pickle.dumps({
            'header': {
                'type': header
            },
            'body': payload
        })
        
        # Set header
        msg_length = len(message)
        header = str(msg_length).encode(self.char_format)
        header += b' ' * (self.header_length - len(header))
        self.client.send(header)
        self.client.send(bytes(message))
        
        print('---- REQUEST ----')
        print('[LENGTH]:', msg_length)
        print('[BODY]:', pickle.loads(bytes(message)))
    