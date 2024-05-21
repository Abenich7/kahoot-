import tkinter as tk
import json
from client_module import Client  # Import the Client class or module
from app import LoginPage, ChooseQuizPage, GameRoomPage
import sys


def start_app(client):
    root = tk.Tk()
    #login=LoginPage(root, client) 
    test=ChooseQuizPage(root,client)
    
    
    
     # Note: no need to assign to a variable
    #LoginPage.bind("<<LoginSuccess>>", lambda event: transition_to_choose_quiz(root, client))
   # ChooseQuizPage(root,client)
   # while()
    #    self.root.destroy
     #   ChooseQuizPage

    #print('test')

    
    root.mainloop()


if __name__ == "__main__":
    
    client = Client()  # Create an instance of the Client class
    if client.fail:
        print("Aw snap :/ Something went wrong")
        sys.exit()

    start_app(client)
