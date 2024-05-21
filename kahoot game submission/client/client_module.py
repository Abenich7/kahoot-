# client_module.py
import socket
import json
from time import sleep
import threading

HOST = '127.0.0.1'
PORT = 5000
FORMAT = 'utf-8'
ADDR = (HOST, PORT)  # Creating a tuple of IP+PORT


class Client:
    def __init__(self):
        self.server = (HOST,PORT)
       
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.fail=0
        self.connect_to_server()

        self.username
        self.password
        
        #the following request has to be called by the clients in the Waiting Room page 
       # self.game_room_initialized = threading.Event()  # Event for synchronization

       # self.game_room_page = None

    def join_waiting_room(self):
        self.server.handle_client_join(self)

    def connect_to_server(self):
        try:
            self.client_socket.connect(self.server)
        except Exception as e:
                self.fail=1
                self.client_socket.close()
        
           
    def send_request(self, request):
        self.client_socket.sendall(request.encode(FORMAT))
        response = self.client_socket.recv(1024).decode()
        print("Response from server:", response)
        return response
