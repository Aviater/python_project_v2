from tkinter import *
from tkinter import ttk
import time
import controller.client_controller as controller
from queue import Queue
queue = Queue()

queue_data = {}

class QuizWindow:
    root = None
    frame = None
        
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

    def quiz_window(self):
        self.frame.destroy()
        # Create frame inside window (root) to hold all widgets
        self.frame = ttk.Frame(self.root, padding="10 10 10 10")

        # Create grid layout inside the frame
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        time.sleep(2)
        # controller.fetch_question()
        print('FETCHED: ', queue.get())

        # Declare vars
        # question, answer1, answer2, answer3, answer4, correct = client_controller.fetch_data()
        # Create label
        label_1_txt = StringVar()
        label_2 = ttk.Label(self.frame, text='question')
        label_2.grid(column=1, row=1)

        # button 1
        button_2 = ttk.Button(self.frame, text='answer1', command= lambda: controller.answer_question(1))
        button_2.grid(column=1, row=2, sticky=(W, E))
        
        # button 2
        button_3 = ttk.Button(self.frame, text='answer2', command= lambda: controller.answer_question(2))
        button_3.grid(column=1, row=3, sticky=(W, E))
        
        # button 3
        button_4 = ttk.Button(self.frame, text='answer3', command= lambda: controller.answer_question(3))
        button_4.grid(column=1, row=4, sticky=(W, E))
        
        # button 4
        button_5 = ttk.Button(self.frame, text='answer4', command= lambda: controller.answer_question(4))
        button_5.grid(column=1, row=6, sticky=(W, E))
        
def main():
    quiz_window1 = QuizWindow()
    quiz_window1.set_root()
    quiz_window1.welcome_window()
    quiz_window1.root.mainloop()
        
main()