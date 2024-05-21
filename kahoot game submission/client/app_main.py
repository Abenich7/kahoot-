import tkinter as tk
import json
from client_module import Client  # Import the Client class or module
from app import PageController,LoginPage, ChooseQuizPage, GameRoomPage,WaitingRoomPage,ResultsPage
import sys


def start_app(client):
    root = tk.Tk()
    root.geometry("400x300")

    page_controller = PageController(root,client)
    page_controller.show_page(LoginPage)

    root.mainloop()
    

if __name__ == "__main__":
    
    client = Client()  # Create an instance of the Client class
    if client.fail:
        print("Aw snap :/ Something went wrong")
        sys.exit()

    start_app(client)
