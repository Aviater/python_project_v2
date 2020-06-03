import socket
import pickle
import threading
from queue import Queue

# queue = Queue()

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
                    queue.put({
                        'ready': True,
                        'players': msg['body']['players'],
                        'data': msg['body']['content']
                    })
                    # print('[QUEUE]:', queue.get())
                    
                # Output
                print('[LENGTH]:', msg_length)
                print('[HEADER]:', msg['header'])
                print('[PLAYER]:', msg['body']['players'])
                print('[ BODY ]:', msg['body']['content'])
            
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
        
def main(player_name, queue):
    HOST = socket.gethostbyname(socket.gethostname())
    
    con1 = Connection(64, 9999, HOST, 'utf-8')
    
    con1.connect_to_server()
    con1.send_message(player_name)
    setup = True
    while setup:
        con1.handle_response(queue)
    # con1.handle_response(queue)
    # con1.handle_response(queue)
    # con1.handle_response(queue)
    # con1.handle_response(queue)