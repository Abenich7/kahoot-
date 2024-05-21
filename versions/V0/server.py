# Imports
import socket
import threading

# Define constants
import time

HOST = '127.0.0.1'  # Standard loopback IP address (localhost)
PORT = 5000  # Port to listen on (non-privileged ports are > 1023)
FORMAT = 'utf-8'  # Define the encoding format of messages from client-server
ADDR = (HOST, PORT)  # Creating a tuple of IP+PORT


# Function that handles a single client connection
# handle client to operate like a continuous discussion server. 
#initial contact with our client. 


def handle_client1(conn, addr):
    print('[CLIENT CONNECTED] on address: ' , addr)  # Printing connection address
    #send and receive. thats your way to handle the client. 
    #sometimes you want to sned him multiple bits of information. 
    #send it as separate information packets according to the different components of the program
    #open threads where necessary to take care of client connections 
    #when you have two different processes, take care of presenting them in a way that makes sense in terms of parallel
    #pieces of information 
    total_messages = conn.recv(4096).decode(FORMAT)  # Receiving from client # of messages to expect
    received = 0

    # try:
    #     for i in range(int(total_messages)):
    #         data = conn.recv(1024).decode(FORMAT)
    #         print(f"Recieved message #{received} from client: \"" + data + "\"")
    #         conn.send(data.encode(FORMAT))
            
    #         received += 1
    #     print("\n[CLIENT DISCONNECTED] on address: ", addr)
    #     print()
    # except:
    #     print("[CLIENT CONNECTION INTERRUPTED] on address: ", addr)

      #send an image over the server connection 
    try:
        # Open the JPEG file
        with open('late_registration_2.jpg', 'rb') as file:
        # Read the file in chunks and send it to the client
            data = file.read(4096)
            while data:
                conn.send(data)
                data = file.read(4096)
            
    except Exception as e:
        print("Error:", e)
  #  finally:
        # Close the client connection
   #     conn.close()



# Function that handles the second parallel client
# Only when 2 clients are connected simultaneously, this function will handle the second client
def handle_client2(conn, addr):
    print('[CLIENT CONNECTED] on address: ', addr)  # Printing connection address

    try:
        conn.send("Welcome! This is your server:)\nPlease enter your name:".encode(FORMAT))
        name = conn.recv(1024).decode(FORMAT)
        print("Received name from client: \"" + name + "\"")

        conn.send(f"Hello {name}!\nWhat is your age?".encode(FORMAT))
        age = conn.recv(1024).decode(FORMAT)
        print("Received age from client: \"" + age + "\"")

        conn.send("What is your profession?".encode(FORMAT))
        profession = conn.recv(1024).decode(FORMAT)
        print("Received profession from client: \"" + profession + "\"")

        time.sleep(0.01)
        conn.send("Nice to meet you:)\nGoodbye for now...".encode(FORMAT))
        print("[CLIENT DISCONNECTED] on address: ", addr)
        print()
    except:
        print("[CLIENT CONNECTION INTERRUPTED] on address: ", addr)

  

# Function that starts the server
def start_server():
    server_socket.bind(ADDR)  # binding socket with specified IP+PORT tuple

    print(f"[LISTENING] server is listening on {HOST}")
    server_socket.listen()  # Server is open for connections

    while True:
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}\n")  # printing the amount of threads working

        connection, address = server_socket.accept()  # Waiting for client to connect to server (blocking call)

        if threading.activeCount() == 1:
            thread = threading.Thread(target=handle_client1, args=(connection, address))  # Creating new Thread object.
            # Passing the handle func and full address to thread constructor
            thread.start()  # Starting the new thread (<=> handling new client)
        else:
            thread = threading.Thread(target=handle_client2, args=(connection, address))
            thread.start()

        # print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}\n")  # printing the amount of threads working
        # on this process (opening another thread for next client to come!)


# Main
if __name__ == '__main__':
    IP = socket.gethostbyname(socket.gethostname())  # finding your current IP address

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Opening Server socket

    print("[STARTING] server is starting...")
    start_server()



    print("THE END!")

