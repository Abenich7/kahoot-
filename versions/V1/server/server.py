import socket
import json
from threading import Thread
import time 
import game_data 
from quiz import Quiz

#app=KahootGame()

HOST = '127.0.0.1'  # Standard loopback IP address (localhost)
PORT = 5000  # Port to listen on (non-privileged ports are > 1023)
FORMAT = 'utf-8'  # Define the encoding format of messages from client-server
ADDR = (HOST, PORT)  # Creating a tuple of IP+PORT


class KahootGame:
    def __init__(self):
        self.users = Users()
        self.rooms = Rooms()
     #   self.quizzes = Quizzes()
      

    #upon request of the first user to enter the game. create a room and put him in it. and update relevant fields in relevant classes
    def create_room(self, room_id, quiz_index):
        quiz = self.quizzes.quizzes_list[quiz_index]
        self.rooms.create_room(room_id, quiz)

class Users:
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

class Rooms:
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

class Room:
    def __init__(self, quiz):
        self.quiz = quiz

dummy_data = {
        "ariel": "123",
        "ben": "456"
    }


class RequestHandler(Thread):
    def __init__(self, client_socket, game):
        super().__init__()
        
        self.client_socket = client_socket
        self.game = game
        self.dummy_data = {
            "ariel": "123",
            "ben": "456"
        }
      #  self.quiz = Quiz(dummy_quizzes)  # Instantiate Quiz object with dummy_quizzes data

    def run(self):
        try:
            while True:
                data = self.client_socket.recv(1024).decode()
                if not data:
                    break
                response = self.process_request(data)
                self.client_socket.sendall(response.encode())
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

            if username_sent in self.dummy_data:
                if self.dummy_data[username_sent] == password_sent:
                    return "Login successful"
                else:
                    return "Incorrect password"
            else:
                return "Username not found"
        
        elif parts[0]== "signup" and len(parts) == 3:
            username = parts[1]
            password = parts[2]
            # Add user to dummy_data
            self.dummy_data[username] = password
            return "Signup successful"
        
        elif parts[0] == "create_room" and len(parts) == 3:
            room_id = parts[1]
            quiz_index = int(parts[2])
            self.game.create_room(room_id, quiz_index)
            return "Room created successfully"
        
        elif parts[0] == "get_quizzes":
            # Fetch quizzes data using Quiz object and return as response
            quizzes_names = json.dumps(["quizA","quizB"])
            return quizzes_names
        
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

     # Dummy dictionary storing usernames and passwords
    
        #if user clicked on login without inputting parts 
        

       # if parts[0] == "signup" and len(parts) == 3:
        #    username=parts[1]
         #   password=parts[2]

       # elif parts[0] == "create_room" and len(parts) == 3:
        #    room_id = parts[1]
         #   quiz_index = int(parts[2])
          #  self.game.create_room(room_id, quiz_index)
           # return "Room created successfully"
       # elif parts[0] == "get_quizzes":
        #    return self.get_quizzes()
        
        #else:
         #   return "Invalid request"
        

def load_database(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def save_database(database, filename):
    with open(filename, 'w') as file:
        json.dump(database, file, indent=4)

def start_server(host, port, game):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print("Server started on {}:{}".format(host, port))
   
    try:
        while True:
            #server stays on the following line waiting for new clients to connect
            client_socket, client_address = server_socket.accept()
            print("Connection from:", client_address)
            handler = RequestHandler(client_socket, game)
           # start the handler like a thread
            handler.start()
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
 
    import os

    # Check if the game data file exists
  #  if not os.path.exists("game_data.json"):
        # Create initial game data
      
        # Save initial game data to game_data.json
        #save_database(initial_game_data, "game_data.json")
    
    game = KahootGame()
    # Start the server
    start_server(HOST, PORT, game)


    

    # Create KahootGame instance with loaded game data
    


    
