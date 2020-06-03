# from .player import Player
from .model.client import main as client_main
import threading
from queue import Queue

def player_ready(player_name, view_instance, view_method, queue):
    spawn_connection_thread(player_name, queue)
    start_quiz(view_instance, view_method, queue)

def spawn_connection_thread(player_name, queue):
    connection_thread = threading.Thread(target= lambda: client_main(player_name, queue))
    connection_thread.daemon = True
    connection_thread.start()
    print('Thread spawned:', connection_thread)
    print('Thread name:', connection_thread.name)

def start_quiz(view_instance, view_method, queue):
    queue_data = queue.get()
    queue.put(queue_data)
    if queue_data['ready'] == True:
        print('[Queue]:', queue_data)
        view_method(view_instance)
    
def fetch_question(queue):
    queue_data = queue.get()
    # queue.put(queue_data)
    return queue_data

def answer_question(num):
    print('Clicked', num)