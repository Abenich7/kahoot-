import tkinter as tk
from tkinter import messagebox
import socket
import time
from PIL import Image

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5000  # The port used by the server
FORMAT = 'utf-8'
ADDR = (HOST, PORT)  # Creating a tuple of IP+PORT

class ClientGUI:
    def __init__(self, root, client_socket):
        self.root = root
        self.client_socket = client_socket

        self.root.title("Client GUI")

        # Create labels, entry, and buttons
        self.label_message = tk.Label(root, text="Message:")
        self.entry_message = tk.Entry(root)
        self.button_send_message = tk.Button(root, text="Send Message", command=self.send_message)

        self.label_image_path = tk.Label(root, text="Image Path:")
        self.entry_image_path = tk.Entry(root)
        self.button_send_image = tk.Button(root, text="Send Image", command=self.send_image)

        # Grid layout
        self.label_message.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_message.grid(row=0, column=1, padx=5, pady=5)
        self.button_send_message.grid(row=0, column=2, padx=5, pady=5)

        self.label_image_path.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_image_path.grid(row=1, column=1, padx=5, pady=5)
        self.button_send_image.grid(row=1, column=2, padx=5, pady=5)

    def send_message(self):
        message = self.entry_message.get()
        self.client_socket.send(message.encode(FORMAT))  # Sending data to server
        print(f"[SENT DATA] {message}")  # Printing sent data
        messagebox.showinfo("Message Sent", "Message sent successfully!")  # Sending data to server                         
        
        time.sleep(0.5)

        #add a way to receive a message. ie make client wait to accept message from server 



def start_client():
    client_socket.connect((HOST, PORT))  # Connecting to server's socket

    total_messages = input("Please enter # of messages you would like to send to server: ")
    client_socket.send(total_messages.encode(FORMAT))
   # count = 0

    print(total_messages)
    #for i in range(int(total_messages)):
  #  print(f"count: {i}, total: {total_messages}")
    new_message = input("Please enter message for server: ")

    client_socket.send(new_message.encode(FORMAT))  # Sending data to server
    print(f"[SENT DATA] {new_message}")  # Printing recieved data from server

    time.sleep(0.5)
    
    with open('received_image.jpg', 'wb') as file:
        while True:
            data = client_socket.recv(4096)  # Receive data from server
            if not data:
                break  # No more data, exit loop
            file.write(data)
         
    

    client_socket.close()  # Closing client's connection with erver (<=> closing socket)

    image = Image.open('received_image.jpg')
    image.show()

    # Further processing or cleanup code here
    print("Image received successfully!")


if __name__ == "__main__":
    IP = socket.gethostbyname(socket.gethostname())
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("[CLIENT] Started running")
    start_client()
    print("\nGoodbye client:)")