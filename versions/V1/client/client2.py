import socket
import json

server_ip = '127.0.0.1'
server_port = 5000
FORMAT = 'utf-8'
ADDR = (server_ip, server_port)  # Creating a tuple of IP+PORT


#class User:
 #   def __init__(self, username, password):
  #      self.username = username
   #     self.password = password

def start_client():
   
    client_socket.connect(ADDR)
 
    return client_socket


def send_request(host, port, request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.sendall(request.encode())
        response = client_socket.recv(1024).decode()
        print("Response from server:", response)

if __name__ == "__main__":
    # Create a user instance
   # user = User("example_user", "password123")

    # Convert user data to JSON format
   # user_data = json.dumps({"username": user.username, "password": user.password})

    # Example: send a request to the server to add a user
   # request = "add_user " + user_data
   # send_request("localhost", 8888, request)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    start_client()


   

