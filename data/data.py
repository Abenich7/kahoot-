import json

class KahootGame:
    def __init__(self):
        self.users = Users()
        self.rooms = Rooms()
        self.quizzes = Quizzes()

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

class Quizzes:
    def __init__(self):
        self.quiz_names = []
        self.quizzes_list = []

    def update_quiz(self, quiz_data):
        self.quizzes_list.append(quiz_data)

    def change_quiz_name(self, quiz_index, new_name):
        self.quiz_names[quiz_index] = new_name

def load_database(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def save_database(database, filename):
    with open(filename, 'w') as file:
        json.dump(database, file, indent=4)

# Example usage:
# game = KahootGame()
# game.users.add_user(user_data)
# game.rooms.update_full_rooms(room_id, is_full)
# etc.
