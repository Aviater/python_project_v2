import socket
import json
import pickle
import threading
import player
from queue import Queue

class Connection:
    clientsocket = None
    address = None
    server = None
    clients = []
    player_info = []
    queue = Queue()
    def __init__(self, header_length, port, host, char_format):
        self.header_length = header_length
        self.port = port
        self.host = host
        self.char_format = char_format

    # Bind server to socket
    def bind_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))

    # Load the JSON file containing questions
    def load_json(self):
        with open('./data/questions.json', 'r') as json_file:
            data = json.load(json_file)
            # print(data[0])
            return data

    # Start the server
    def start_server(self, max_connections):
        print(f'Server running listening on {self.host}...')
        self.server.listen(max_connections)
        # Connection loop
        while True:
            try:
                self.clientsocket, self.address = self.server.accept()
                self.clients.append({
                    'connection': self.clientsocket,
                    'address': self.address
                })
                self.spawn_new_thread()
            except ConnectionError:
                print('Server was unable to establish a connection')

    # Spawn a new client handler thread.
    def spawn_new_thread(self):
        thread = threading.Thread(target=self.client_handler)
        thread.daemon = True
        thread.start()
        print(f'Thread spawned: {thread}')
        print(f'Active connections: {threading.activeCount() - 1}')

    # Handle client connection
    def client_handler(self):
        connected = True
        print(f"Connection from {self.address} has been established!")
        while connected:
            request = self.handle_request()
            print(f'[{self.address}]: {request["body"]} has joined the game.')
            self.generate_player(request['body'])
            self.send_response(self.clientsocket, 'Connected successfully!')
            self.broadcast()
            
            # questions = self.load_json()
            # self.send_response_to_all

        self.clientsocket.close()
        
    # Generate player
    def generate_player(self, name):
        for client in self.clients:
            if client['connection'] == self.clientsocket:
                client['player'] = player.Player(name, 10)
                
                print('clients:', self.clients)

    def handle_request(self):
        # Read header
        msg_length = self.clientsocket.recv(self.header_length).decode(self.char_format)
        if msg_length:
            print(msg_length)
            msg_length = int(msg_length)

            # Read body
            msg_encoded = self.clientsocket.recv(msg_length)
            msg = pickle.loads(bytes(msg_encoded))

            # Output
            print('[HEADER]:', msg_length)
            print('[ BODY ]:', msg)

        return msg
    
    def get_all_players(self):
        player_info = []
        for client in self.clients:
            print('PLAYER INFO:', client['player'].get_props())
            player_info.append(client['player'].get_props())
        
        return player_info

    # Send response to client
    def send_response(self, clientsocket, payload):
        message = pickle.dumps({
            'header': {
                'type': 'str'
            }, 
            'body': {
                'players': self.get_all_players(),
                'content': payload
            }
        })

        # Set header
        msg_length = len(message)
        header = str(msg_length).encode(self.char_format)
        header += b' ' * (self.header_length - len(header))
        clientsocket.send(header)
        clientsocket.send(bytes(message))

    # Send message to all clients
    def broadcast(self):
        if (threading.activeCount() - 1) == 2:
            print('==== Players Ready ==== \n')
            for i,client in enumerate(self.clients):
                self.send_response(self.clients[i]['connection'], 'All players ready!')
                print(f'[{i}]:', client)
                

def main():
    HOST = socket.gethostbyname(socket.gethostname())

    con1 = Connection(64, 9999, HOST, 'utf-8')

    con1.bind_server()
    con1.load_json()
    con1.start_server(5)
main()