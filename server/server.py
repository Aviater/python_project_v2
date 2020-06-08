import socket
import json
import pickle
import threading
import player
from queue import Queue

queue = Queue()

# clients = []
class Connection:
    clientsocket = None
    address = None
    server = None
    clients = []
    player = None
    QUESTION_DAMAGE = 1
    def __init__(self, HEADER, HOST, PORT, FORMAT, quiz_data, clientsocket, address):
        self.header_length = HEADER
        self.host = HOST
        self.port = PORT
        self.char_format = FORMAT
        self.clientsocket = clientsocket
        self.address = address
        self.quiz_data = quiz_data
        
        self.spawn_new_thread()
        
    # Get all Player objects information
    @staticmethod
    def get_all_players():
        player_info = []
        for client in Connection.clients:
            player_info.append(client.player.get_props())
        return player_info

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
        # Connection step
        print(f"Connection from {self.address} has been established!")
        request = self.handle_request()
        print(f'[{self.address}]: {request["body"]} has joined the game.')
        self.player = player.Player(request['body'], 10)
        # self.send_response('Connected successfully!')
        
        # Quiz loop step
        i = 0
        broadcast('quiz_data', self.quiz_data[i])
        while connected:
            # broadcast(self.quiz_data[i])
            request = self.handle_request()
            i = i + 1
            
            if request['body'] == True:
                for client in Connection.clients:
                    if client.clientsocket != self.clientsocket:
                        client.player.reduce_health(self.QUESTION_DAMAGE)
                        self.send_response('quiz_data', self.quiz_data[i])
                        
                        for client in Connection.clients:
                            if self != client:
                                client.send_response('state_update', '')
            elif request['body'] == False:
                self.send_response('quiz_data', self.quiz_data[i])
            print('INDEX:', i)
            

            # Send new question
            # self.send_response(self.get_quiz_data(index))
            #     broadcast()
        self.clientsocket.close()

    def handle_request(self):
        # Read header
        msg_length = self.clientsocket.recv(self.header_length).decode(self.char_format)
        if msg_length:
            msg_length = int(msg_length)
            # Read body
            msg_encoded = self.clientsocket.recv(msg_length)
            message = pickle.loads(bytes(msg_encoded))
            
            # Output
            print('\n')
            print('[---- Request ----]')
            print('[ FROM ]:', self.clientsocket)
            print('[---------------]')
            print('[LENGTH]:', msg_length)
            print('[HEADER]:', message['header']['type'])
            print('[ BODY ]:', message['body'])
            print('[-----------------]')
            print('\n')

        return message

    # Send response to client
    def send_response(self, header, content):
        payload = {
            'header': {
                'type': header,
                'clients': len(Connection.clients)
            }, 
            'body': {
                'players': Connection.get_all_players(),
                'content': content
            }
        }
        message = pickle.dumps(payload)

        # Set header
        msg_length = len(message)
        header = str(msg_length).encode(self.char_format)
        header += b' ' * (self.header_length - len(header))
        self.clientsocket.send(header)
        self.clientsocket.send(bytes(message))
        
        # Output
        print('\n')
        print('[---- Response ----]')
        print('[  TO  ]:', self.clientsocket)
        print('[---------------]')
        print('[LENGTH]:', msg_length)
        print('[HEADER]:', payload['header']['type'])
        print('[PLAYER]:', payload['body']['players'])
        print('[ BODY ]:', payload['body']['content'])
        print('[------------------]')
        print('\n')
        
    def get_quiz_data(self):
        
        self.quiz_data

# Send message to all clients
def broadcast(header, content):
    print('\n')
    print('[---- Broadcast ----]')
    for client in Connection.clients:
        client.send_response(header, content)
    print('[-------------------]')
    print('\n')
            
def start_server(MAX_CONNECTIONS, HEADER, HOST, PORT, FORMAT):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    print(f'Server running listening on {HOST}...')
    server.listen(MAX_CONNECTIONS)
    
    # Load quiz questions
    quiz_data = load_json()
    
    # Connection loop
    while True:
        try:
            clientsocket, address = server.accept()
            Connection.clients.append(Connection(HEADER, HOST, PORT, FORMAT, quiz_data, clientsocket, address))
        except ConnectionError:
            print('Server was unable to establish a connection')

# Load JSON data
def load_json():
    with open('./data/questions.json', 'r') as json_file:
        data = json.load(json_file)
        return data

def main():
    MAX_CONNECTIONS = 2
    HEADER = 64
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 9999
    FORMAT = 'utf-8'

    start_server(MAX_CONNECTIONS, HEADER, HOST, PORT, FORMAT)

main()