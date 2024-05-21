import json

# Load database from JSON file
def load_database(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Save database to JSON file
def save_database(database, filename):
    with open(filename, 'w') as file:
        json.dump(database, file, indent=4)

# Kahoot game methods
def update_num_quizzes(database, num_quizzes):
    database['root']['num_quizzes'] = num_quizzes

def update_num_rooms(database, num_rooms):
    database['root']['num_rooms'] = num_rooms

def update_num_players(database, num_players):
    database['root']['num_players'] = num_players

# Users methods
def add_user(database, user_data):
    database['users']['users_list'].append(user_data)
    database['users']['num_users'] += 1

def update_num_users(database, num_users):
    database['users']['num_users'] = num_users

def update_user_limit(database, user_limit):
    database['users']['user_limit'] = user_limit

def compare_num_users_user_limit(database):
    return database['users']['num_users'] <= database['users']['user_limit']

# Rooms methods
def update_full_rooms(database, room_id, is_full):
    database['rooms']['full_rooms'][room_id] = is_full

def update_room_ids(database, room_id, add=True):
    if add:
        database['rooms']['room_ids'].append(room_id)
    else:
        database['rooms']['room_ids'].remove(room_id)

def update_rooms_underway(database, room_id, is_underway):
    database['rooms']['rooms_underway'][room_id] = is_underway

# Leaderboard methods
def update_leaderboard(database, username, points):
    database['rooms']['leaderboard'][username] = points

# Quizzes methods
def update_quiz(database, quiz_data):
    database['quizzes']['quizzes_list'].append(quiz_data)

def change_quiz_name(database, quiz_index, new_name):
    database['quizzes']['quiz_names'][quiz_index] = new_name

# Other helper functions
def create_user(ip_port, username, password, level, games_won):
    return {
        "ADDR": ip_port,
        "username": username,
        "password": password,
        "level": level,
        "gamesWon": games_won
    }

def create_quiz(questions, answers, correct_answers, num_questions, level):
    return {
        "questions": questions,
        "answers": answers,
        "correct_answers": correct_answers,
        "num_questions": num_questions,
        "level": level
    }
