import socket
import json

HOST = '127.0.0.1'
PORT = 5000
FORMAT = 'utf-8'
ADDR = (HOST, PORT)  # Creating a tuple of IP+PORT

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    return client_socket

def send_login_data(login_data, client_socket):
    client_socket.send(login_data.encode(FORMAT))
    print("[SENT LOGIN DATA]")

if __name__ == "__main__":
    client_socket = start_client()
    print("[CLIENT] Started running")
    
    # Example usage: sending login data
    login_data = json.dumps({"username": "example", "password": "example123"})
    send_login_data(login_data, client_socket)
    
    print("\nGoodbye client:)")
