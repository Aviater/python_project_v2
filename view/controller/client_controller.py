# from .player import Player
from .model.client import main as client_main
import threading
from queue import Queue

def spawn_connection_thread(player_name):
    connection_thread = threading.Thread(target= lambda: client_main(player_name))
    connection_thread.daemon = True
    connection_thread.start()
    print('Thread spawned:', connection_thread)

def answer_question(num):
    print('Clicked', num)