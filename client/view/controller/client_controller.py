from .model.client import Connection
import threading
from queue import Queue

def player_ready(entered_name, view_instance, quiz_window, queue):
    player_name = entered_name
    print('player:', player_name)
    spawn_connection_thread(player_name, view_instance, quiz_window, queue)
    

def spawn_connection_thread(player_name, view_instance, quiz_window, queue):
    thread = threading.Thread(target= lambda: connection_thread(player_name, view_instance, quiz_window, queue))
    thread.daemon = True
    thread.start()
    print('Thread spawned:', thread)
    print('Thread name:', thread.name)
    
def connection_thread(player_name, view_instance, quiz_window, queue):
    HOST = Connection.HOST
    global con1
    con1 = Connection(64, 9999, HOST, 'utf-8')
    
    con1.connect_to_server()
    con1.send_message('str', player_name)
    setup = True
    while setup:
        con1.handle_response(queue)
        if not queue.empty():
            print('Queue not empty:', queue.queue)
            start_quiz(player_name, view_instance, quiz_window, queue)
        
def start_quiz(player_name, view_instance, quiz_window, queue):
    quiz_window(view_instance, player_name)
    return

def check_for_winner(view_instance, winner_window, queue):
    queue_data = queue.get()
    queue.put(queue_data)
    for player in queue_data['players']:
        if player[1] == 0:
            winner_window(view_instance)

def fetch_data(queue):
    queue_data = queue.get()
    queue.put(queue_data)
    print('Fetch question:', queue_data)
    return queue_data

def render_your_info(player_name, data):
    for player in data['players']:
        if player[0] == player_name:
            return player
        
def render_opponent_info(player_name, data):
    for player in data['players']:
        if player[0] != player_name:
            return player

def answer_question(num, queue):
    queue_data = queue.get()
    # queue.put(queue_data)
    print('Queue length:', queue.queue)
    print('Queue contents:', queue_data)
    if queue_data['header']['type'] == 'quiz_data':
        if num == queue_data['data']['correct']:
            con1.send_message('answer', True)
        else:
            con1.send_message('answer', False)
    elif queue_data['header']['type'] == 'state_update':
        answer_question(num, queue)
        
        