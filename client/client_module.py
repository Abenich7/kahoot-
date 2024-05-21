# client_module.py
import socket
import json
import threading
import sys
import logging

HOST = '127.0.0.1'
PORT = 5000
FORMAT = 'utf-8'
ADDR = (HOST, PORT)  # Creating a tuple of IP+PORT

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Client:
    def __init__(self):
        self.server = ADDR
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.fail = False
        self.username = None
        self.connect_to_server()
        self.check_connection()

    def connect_to_server(self):
        try:
            self.client_socket.connect(self.server)
            logging.info(f"Connected to server at {self.server}")
        except Exception as e:
            logging.error(f"Failed to connect to server: {e}")
            self.fail = True
            self.client_socket.close()

    def check_connection(self):
        try:
            request = "check_connection"
            self.send_request(request)
        except Exception as e:
            logging.error("Server disconnected")
            self.client_socket.close()
            sys.exit()

    def send_request(self, request):
        try:
            self.client_socket.sendall(request.encode(FORMAT))
            response = self.client_socket.recv(1024).decode(FORMAT)
            logging.debug(f"Response from server: {response}")
            return response
        except Exception as e:
            logging.error(f"Error processing request '{request}': {e}")
            self.fail = True
            self.client_socket.close()
            return None
