from tkinter import *
from tkinter import ttk
import time
import controller.client_controller as controller
from queue import LifoQueue
queue = LifoQueue()

class QuizWindow:
    root = None
    frame = None
    display_data = []
    your_info = None
    opp_info = None
        
    def set_root(self):
        # Create the window itself
        self.root = Tk()
        
        # Create title for the window
        self.root.title('Quiz Wars')

        # Set window size
        self.root.geometry('350x200')
        
    def welcome_window(self):
        # Create frame inside window (root) to hold all widgets
        self.frame = ttk.Frame(self.root, padding="10 10 10 10")

        # Create grid layout inside the frame
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Create label
        label_1_txt = StringVar()
        label_1 = ttk.Label(self.frame, text='Enter your name')
        label_1.grid(column=1, row=1)

        # Entry widget
        entry_1_txt = StringVar()
        entry_1 = ttk.Entry(self.frame, width=24, textvariable=entry_1_txt)
        entry_1.grid(column=1, row=2, sticky=(W, E))

        # button
        button_1 = ttk.Button(self.frame, text='Start', command= lambda: controller.player_ready(entry_1_txt.get(), self, QuizWindow.quiz_window, queue))
        button_1.grid(column=1, row=3, sticky=(W, E))

    def quiz_window(self, player_name):
        # Fetch data
        data = controller.fetch_data(queue)
        self.your_info = controller.render_your_info(player_name, data)
        self.opp_info = controller.render_opponent_info(player_name, data)

        # Destroy previous frame
        self.frame.destroy()
        # Create frame inside window (root) to hold all widgets
        self.frame = ttk.Frame(self.root, padding="10 10 10 10")

        # Create grid layout inside the frame
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Descriptor label
        left_label = ttk.Label(self.frame, text='You:')
        left_label.grid(column=1, row=1)
        
        # Descriptor label
        right_label = ttk.Label(self.frame, text='Opponent:')
        right_label.grid(column=3, row=1)

        # Name label
        player_name_1 = ttk.Label(self.frame, text=self.your_info[0])
        player_name_1.grid(column=1, row=2)
        
        # Name label
        player_name_2 = ttk.Label(self.frame, text=self.opp_info[0])
        player_name_2.grid(column=3, row=2)
        
        # Hitpoints label
        player_hp_1 = ttk.Label(self.frame, text=self.your_info[1])
        player_hp_1.grid(column=1, row=3)
        
        # Hitpoints label
        player_hp_2 = ttk.Label(self.frame, text=self.opp_info[1])
        player_hp_2.grid(column=3, row=3)
        
        # Question label
        label_2 = ttk.Label(self.frame, text=data['data']['question'])
        label_2.grid(column=2, row=1)

        # Answer button 1
        button_2 = ttk.Button(self.frame, text=data['data']['answers'][0], command= lambda: controller.answer_question(0, queue))
        button_2.grid(column=2, row=2, sticky=(W, E))
        
        # Answer button 2
        button_3 = ttk.Button(self.frame, text=data['data']['answers'][1], command= lambda: controller.answer_question(1, queue))
        button_3.grid(column=2, row=3, sticky=(W, E))
        
        # Answer button 3
        button_4 = ttk.Button(self.frame, text=data['data']['answers'][2], command= lambda: controller.answer_question(2, queue))
        button_4.grid(column=2, row=4, sticky=(W, E))
        
        # Answer button 4
        button_5 = ttk.Button(self.frame, text=data['data']['answers'][3], command= lambda: controller.answer_question(3, queue))
        button_5.grid(column=2, row=6, sticky=(W, E))
        
        # Check for winner
        controller.check_for_winner(self, QuizWindow.winner_window, queue)
        
    def winner_window(self):
        # Destroy previous frame
        self.frame.destroy()
        # Create frame inside window (root) to hold all widgets
        self.frame = ttk.Frame(self.root, padding="10 10 10 10")

        # Create grid layout inside the frame
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Descriptor label
        left_label = ttk.Label(self.frame, text='Match Concluded')
        left_label.grid(column=1, row=1)
        
        # Name label
        player_name_1 = ttk.Label(self.frame, text=self.your_info[0])
        player_name_1.grid(column=1, row=2)
        
        # Name label
        player_name_2 = ttk.Label(self.frame, text=self.opp_info[0])
        player_name_2.grid(column=3, row=2)
        
        # Hitpoints label
        player_hp_1 = ttk.Label(self.frame, text=self.your_info[1])
        player_hp_1.grid(column=1, row=3)
        
        # Hitpoints label
        player_hp_2 = ttk.Label(self.frame, text=self.opp_info[1])
        player_hp_2.grid(column=3, row=3)
        
def main():
    quiz_window1 = QuizWindow()
    quiz_window1.set_root()
    quiz_window1.welcome_window()
    quiz_window1.root.mainloop()
        
main()