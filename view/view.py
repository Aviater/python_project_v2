from tkinter import *
from tkinter import ttk
# from controller.player import Player
from controller.client_controller import spawn_connection_thread as app_start
from controller.client_controller import answer_question

class QuizWindow:
    root = None
    frame = None
    # def __init__(self):
        
    def set_frame_and_grid(self):
        # Create the window itself
        self.root = Tk()
        
        # Create title for the window
        self.root.title('Quiz Wars')

        # Create frame inside window (root) to hold all widgets
        self.frame = ttk.Frame(self.root, padding="10 10 10 10")

        # Create grid layout inside the frame
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
    def welcome_window(self):
        # Create label
        label_1_txt = StringVar()
        label_1 = ttk.Label(self.frame, text='Enter your name')
        label_1.grid(column=1, row=1)

        # Entry widget
        entry_1_txt = StringVar()
        entry_1 = ttk.Entry(self.frame, width=24, textvariable=entry_1_txt)
        entry_1.grid(column=1, row=2, sticky=(W, E))

        # button
        button_1 = ttk.Button(self.frame, text='Start', command= lambda: app_start(entry_1_txt.get()))
        button_1.grid(column=1, row=3, sticky=(W, E))
        
    def quiz_window(self):
        # Declare vars
        # question, answer1, answer2, answer3, answer4, correct = client_controller.fetch_data()
        # Create label
        label_1_txt = StringVar()
        label_1 = ttk.Label(self.frame, text='question')
        label_1.grid(column=1, row=1)

        # button 1
        button_1 = ttk.Button(self.frame, text='answer1', command= lambda: answer_question(1))
        button_1.grid(column=1, row=3, sticky=(W, E))
        
        # button 2
        button_1 = ttk.Button(self.frame, text='answer2', command= lambda: answer_question(2))
        button_1.grid(column=1, row=4, sticky=(W, E))
        
        # button 3
        button_1 = ttk.Button(self.frame, text='answer3', command= lambda: answer_question(3))
        button_1.grid(column=1, row=5, sticky=(W, E))
        
        # button 4
        button_1 = ttk.Button(self.frame, text='answer4', command= lambda: answer_question(4))
        button_1.grid(column=1, row=6, sticky=(W, E))
        
def main():
    quiz_window1 = QuizWindow()
    quiz_window1.set_frame_and_grid()
    quiz_window1.welcome_window()
    quiz_window1.root.mainloop()
main()