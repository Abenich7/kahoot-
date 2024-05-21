import socket
import json
from threading import Thread
import threading
import time 
from quiz import Quiz
import os

#app=KahootGame()

HOST = '127.0.0.1'  # Standard loopback IP address (localhost)
PORT = 5000  # Port to listen on (non-privileged ports are > 1023)
FORMAT = 'utf-8'  # Define the encoding format of messages from client-server
ADDR = (HOST, PORT)  # Creating a tuple of IP+PORT

####### GAME DATA  ##########

users= {
        "ariel": "123",
        "ben": "456"
    }

# Define the dummy quizzes data here
dummy_quizzes = {
    "quizA": {
        "Q1": {
            "question": "What's my name?",
            "answers": ["ariel", "arik", "arti", "abeni"],
            "correct_answer": "ariel"
        },
        "Q2": {
            "question": "Where am I from?",
            "answers": ["paris", "salem", "arrakis", "chi town"],
            "correct_answer": "paris"
        }
    },
    "quizB": {
        "Q1": {
            "question": "How old am I?",
            "answers": ["3", "25", "120", "1000000"],
            "correct_answer": "3"
        },
        "Q2": {
            "question": "Who is Kanye West?",
            "answers": ["rapper", "musician", "designer", "all of the above"],
            "correct_answer": "all of the above"
        }
    }
}


quizzes_names=["quizA","quizB"]

#counter to initialize new game id
game_id_counter = 0

#following three dictionaries make up the game server data
game_admins = {
    # "GameID":"admin"
}

game_events = {
    # "GameID":"event"
}

game_users={
    "12":["ariel","aaron","keren"],
    "13":["vanessa"],
    "14":["moshe"],
    "11":["yitz"]

    # "GameID":["player1","player2",...]
}



####### END OF GAME DATA  ########




####### OPERATIONS ON DATA ###########





# Function to increment game ID counter and return the new game ID
def increment_game_id():
    global game_id_counter
    game_id_counter += 1
    # Update JSON file with new game ID
    with open("game_id.json", "w") as file:
        json.dump(game_id_counter, file)
    return game_id_counter


def start_game(game_id):
    # Create an event object for the game ID if it doesn't exist
    if game_id not in game_events:
        game_events[game_id] = threading.Event()
    # Set the event associated with the game ID
    game_events[game_id].set()

def get_game_id(username):
    for game_id, admin_username in game_admins.items():
        if admin_username == username:
            return game_id
    return None  # Return None if username is not found






####### END OF OPERATIONS ON DATA ########











#class KahootGame:
    def __init__(self):
        self.users = Users()
        self.rooms = Rooms()
     #   self.quizzes = Quizzes()
      

    #upon request of the first user to enter the game. create a room and put him in it. and update relevant fields in relevant classes
    def create_room(self, room_id, quiz_index):
        quiz = self.quizzes.quizzes_list[quiz_index]
        self.rooms.create_room(room_id, quiz)

#class Users:
    def __init__(self):
        self.num_users = 0
        self.user_limit = 0
        self.users_list = []

    def add_user(self, user_data):
        self.users_list.append(user_data)
        self.num_users += 1

    def update_num_users(self, num_users):
        self.num_users = num_users

    def update_user_limit(self, user_limit):
        self.user_limit = user_limit

    def compare_num_users_user_limit(self):
        return self.num_users <= self.user_limit

#class Rooms:
    def __init__(self):
        self.room_ids = []
        self.full_rooms = {}
        self.rooms_underway = {}
        self.room_limit = 0
        self.leaderboard = {}

    def update_full_rooms(self, room_id, is_full):
        self.full_rooms[room_id] = is_full

    def update_room_ids(self, room_id, add=True):
        if add:
            self.room_ids.append(room_id)
        else:
            self.room_ids.remove(room_id)

    def update_rooms_underway(self, room_id, is_underway):
        self.rooms_underway[room_id] = is_underway

    def update_leaderboard(self, username, points):
        self.leaderboard[username] = points

    def __init__(self):
        self.rooms_map = {}

    def create_room(self, room_id, quiz):
        self.rooms_map[room_id] = Room(quiz)

#class Room:
    def __init__(self, quiz):
        self.quiz = quiz


class RequestHandler(Thread):
    def __init__(self, client_socket):
        super().__init__()
        
        self.client_socket = client_socket
      #  self.game = game
   
    def run(self):
        try:
            while True:
                data = self.client_socket.recv(1024).decode()
                if not data:
                    break
                response = self.process_request(data)
               # response_to_send=json.dumps(response)
                self.client_socket.sendall(response.encode(FORMAT))
        except ConnectionResetError:
            print("Client forcibly closed the connection. Server still live.")
        except Exception as e:
            print("Error:", e)
        finally:
            self.client_socket.close()

    def process_request(self, data):
        parts = data.split()

        if parts[0] == "login":
            if len(parts) < 3:
                return "No username or password entered"

            username_sent = parts[1]
            password_sent = parts[2]

            if not username_sent or not password_sent:
                return "No username or password entered"

            
            if username_sent in users:
                if users[username_sent] == password_sent:
                    return "successful login"
                else:
                    return "Incorrect password"
            else:
                return "Username not found"
        
        elif parts[0]== "signup" and len(parts) == 3:
            username = parts[1]
            password = parts[2]
            # Add user to dummy_data
            users[username] = password
            with open("users.json", "w") as file:
                json.dump(users, file)
            
            return "successful signup"
          
        elif parts[0] == "get_quizzes":
            quizzes_names_send=json.dumps(quizzes_names)
            return quizzes_names_send
        
        elif parts[0] == "admin": 
            username = parts[1]
            quiz_name = parts[2]
        # Store the username as the admin for the game ID (e.g., using the game name)
            game_id = increment_game_id()
            game_admins[game_id] = username

            game_events[game_id] = threading.Event()
 
            return(str(game_id))
        
        elif parts[0] == "join_game":
            game_id = parts[1]
            # Handle join game request
            if game_id in game_events:
                if game_events[game_id].is_set():
                    return "Game already underway"
                else:
                    return "success"
            else:
                return "Invalid Game ID"
            
        elif parts[0] == "check_players_connected":
            game_id=parts[1]
            if game_id in game_users:
                game_users_send=json.dumps(game_users[game_id])
                return game_users_send


        elif parts[0] == "create_room" and len(parts) == 3:
            room_id = parts[1]
            quiz_index = int(parts[2])
            self.game.create_room(room_id, quiz_index)
            return "Room created successfully"
    

        elif parts[0]== "start_game":
              
            game_id=get_game_id(username)

            if game_id not in game_events:
                game_events[game_id] = threading.Event()
    # Set the event associated with the game ID
            game_events[game_id].set()

           # start_game(game_id)
        
        elif parts[0] == "quiz":
            quiz_name = parts[1]
    # Create a Quiz object and retrieve specific quiz data
            quiz = Quiz(dummy_quizzes, quiz_name)
            quiz_data = {
                 quiz_name: {
                    "questions": quiz.questions.get(quiz_name),
                    "answers": quiz.answers.get(quiz_name),
                    "correct_answers": quiz.correct_answers.get(quiz_name)
              }
              }
    # Return the quiz data as a JSON response
            response_data = json.dumps(quiz_data)
            return response_data


        else:
            return "Invalid request"
        

#GameServer is activated for admin and particular game id
class GameServer:
    def __init__(self,game_ids,game_admins,game_events):
        self.game_ids=game_ids
        self.game_admins=game_admins
        self.game_events=game_events

    def players(self):
        pass
        #for game_id

   # def start_game(self):
        # Check if the user is an admin
    #    if admin_username in self.admins.get(game_id, []):
            # Create an Event object for the game ID if it doesn't exist
     #       if game_id not in self.game_events:
      #          self.game_events[game_id] = threading.Event()
            # Set the Event to signal game start
       #     self.game_events[game_id].set()
       # else:
        #    return "You are not authorized to start the game."

#    def add_admin(self, game_id, admin_username):
 #       if game_id not in self.admins:
  #          self.admins[game_id] = [admin_username]
   #     else:
    #        self.admins[game_id].append(admin_username)

    def remove_admin(self, game_id, admin_username):
        if game_id in self.admins and admin_username in self.admins[game_id]:
            self.admins[game_id].remove(admin_username)

    def is_admin(self, game_id, username):
        return username in self.admins.get(game_id, [])

    def is_game_started(self, game_id):
        return game_id in self.game_events and self.game_events[game_id].is_set()




def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print("Server started on {}:{}".format(host, port))
   
    try:
        while True:
            #server stays on the following line waiting for new clients to connect
            client_socket, client_address = server_socket.accept()
            print("Connection from:", client_address)
            handler = RequestHandler(client_socket)
           # start the handler like a thread
            handler.start()
    except KeyboardInterrupt:
            print("Server shutting down...")
    finally:
            server_socket.close()



if __name__ == "__main__":
 
    
    # Load game ID from JSON file

    try:
        with open("game_id.json", "r") as file:
            game_id_counter = json.load(file)
    except FileNotFoundError:
    # If file doesn't exist, create one with initial value
    #    game_id_counter = 0  # Initialize game_id_counter
        with open("game_id.json", "w") as file:
            json.dump(game_id_counter, file)

# Load users
    try:
        with open("users.json", "r") as file:
            users = json.load(file)
    except FileNotFoundError:
    # If file doesn't exist, create one with initial value
    #    users = {}  # Initialize users dictionary
        with open("users.json", "w") as file:
            json.dump(users, file)
    #load game events 
    

    game_server = GameServer(game_users,game_admins,game_events)
    # Start the server
    start_server(HOST, PORT)









    

######## ADDITIONAL FUNCTIONS ##########
# Function to add a user and game identifier to the database
#def add_user(username, game_identifier):
 #   game_database[username] = game_identifier

# Function to retrieve the game identifier for a given username
#def get_game_identifier(username):
 #   return game_database.get(username)

# Function to remove a user from the database (e.g., when the game session ends)
#def remove_user(username):
 #   if username in game_database:
  #      del game_database[username]

def load_database(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def save_database(database, filename):
    with open(filename, 'w') as file:
        json.dump(database, file, indent=4)


