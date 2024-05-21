# client_module.py
import socket
import json
from time import sleep

HOST = '127.0.0.1'
PORT = 5000
FORMAT = 'utf-8'
ADDR = (HOST, PORT)  # Creating a tuple of IP+PORT


class Client:
    def __init__(self):
        self.server_ip = HOST
        self.server_port = PORT
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.fail=0
        self.connect_to_server()
        
    

    def connect_to_server(self):
        try:
            self.client_socket.connect((self.server_ip,self.server_port))
        except Exception as e:
                self.fail=1
                self.client_socket.close()
        
           


    def send_request(self, request):
        self.client_socket.sendall(request.encode(FORMAT))
        response = self.client_socket.recv(1024).decode()
        print("Response from server:", response)
        return response
