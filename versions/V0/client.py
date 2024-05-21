import socket
import time
import json

HOST = '127.0.0.1'
PORT = 5000
FORMAT = 'utf-8'
ADDR = (HOST, PORT)  # Creating a tuple of IP+PORT
IP_set=0

def start_client():
    #if client was called from app.py, 
    #IP not set yet so IP_set==0 and client_socket==NULL
    if IP_set==0:
        IP = socket.gethostbyname(socket.gethostname())
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    return client_socket

def send_login_data(login_data):
    client_socket.send(login_data.encode(FORMAT))
    print("[SENT LOGIN DATA]")

if __name__ == "__main__":
    IP = socket.gethostbyname(socket.gethostname())
    IP_set=1
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("[CLIENT] Started running")
    start_client()
    print("\nGoodbye client:)")
