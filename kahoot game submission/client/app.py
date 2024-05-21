import tkinter as tk
import json
from client_module import Client  # Import the Client class or module
import time

#quiz_name=""
game_id=0


class PageController:
    def __init__(self, root,client):
        self.root = root
        self.client=client
        self.current_page = None

    def show_page(self, page_class):
        if self.current_page:
            self.current_page.destroy()
        self.current_page = page_class(self.root,self.client, self.show_next_page)
        self.current_page.pack()

    def show_next_page(self, next_page_class):
        self.show_page(next_page_class)

class LoginPage(tk.Frame):
    def __init__(self, master,client, callback):
        super().__init__(master)
        self.master = master
        self.client = client
        self.callback=callback
      #  self.generate_login_success_event()
       # self.bind_event_handler()  # Bind event handler when initializing the LoginPage


        self.master.title("Login")

        self.label_username = tk.Label(master, text="Username:")
        self.entry_username = tk.Entry(master)
        self.label_password = tk.Label(master, text="Password:")
        self.entry_password = tk.Entry(master, show="*")
        self.button_login = tk.Button(master, text="Login", command=lambda: self.send_login_data(action="login"))
        self.button_signup = tk.Button(master, text="First time? Sign up", command=lambda: self.send_login_data(action="signup"))
        self.label_username.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)
        self.label_password.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)
        self.button_login.grid(row=2, column=1, padx=5, pady=5)
        self.button_signup.grid(row=4, column=1, padx=5, pady=5)
    

    def finish_login(self):
        self.callback(ChooseQuizPage)


    def send_login_data(self, action):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if action == "login":
            login_data = f"login {username} {password}"
        elif action == "signup":
            login_data = f"signup {username} {password}"  # Change this to match your server's expected format
        response = self.client.send_request(login_data)

        parts = response.split()

        if parts[0] == "Login" and parts[1]=="successful":
            
            # Transition to the next page
            self.client.username=username
            print("Username:",self.client.username)
            self.client.password=password
            self.finish_login()
            

             # Calls constructor for ChooseQuizPage class



class ChooseQuizPage(tk.Frame):
    def __init__(self, master, client, callback):
        super().__init__(master)
        self.master = master
        self.client = client
        self.callback = callback

        self.master.title("Choose Quiz")

        self.container = tk.Frame(self.master)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.label_title = tk.Label(self.container, text="Select a Quiz:")
        self.label_title.pack(padx=5, pady=5)

        self.quiz_listbox = tk.Listbox(self.container)
        self.quiz_listbox.pack(padx=5, pady=5)

        self.button_select_quiz = tk.Button(self.container, text="Select Quiz", command=self.select_quiz)
        self.button_select_quiz.pack(padx=5, pady=5)

        # Option to enter using Game ID
        self.label_game_id = tk.Label(self.container, text="Enter Game ID:")
        self.label_game_id.pack(padx=5, pady=5)

        self.entry_game_id = tk.Entry(self.container)
        self.entry_game_id.pack(padx=5, pady=5)

        self.button_enter_game_id = tk.Button(self.container, text="Enter Game ID", command=self.enter_game_id)
        self.button_enter_game_id.pack(padx=5, pady=5)


        self.flag=0
        self.load_quizzes()

    def load_quizzes(self):
        response = self.client.send_request("get_quizzes")
        quizzes = json.loads(response)
        for quiz in quizzes:
            self.quiz_listbox.insert(tk.END, quiz)

    def finish_choose_quiz(self):
        if self.flag==1:
            self.callback(ChooseQuizPage)
        else:
            self.callback(WaitingRoomPage)


    def select_quiz(self):
        selected_index = self.quiz_listbox.curselection()
        if selected_index:
            self.quiz_name = self.quiz_listbox.get(selected_index)
            # Send a message indicating that the user is the admin
            message = f"admin {self.client.username} {self.quiz_name}"
            response = self.client.send_request(message)
        # Extract the game ID from the response
            game_id = int(response.decode())
            self.game_id.append(game_id) 
            self.finish_choose_quiz()

    def enter_game_id(self):
        game_id = self.entry_game_id.get()
        if game_id:
            # Send the game ID to the server
            response = self.client.send_request(f"join_game {game_id}")
            if response == "success":
                self.finish_choose_quiz()
            elif response == "No":
                self.flag=1
                self.finish_choose_quiz()



class WaitingRoomPage(tk.Frame):
    def __init__(self, master, client, callback):
        super().__init__(master)
        self.master = master
        self.client = client
        self.callback = callback
        self.game_id=game_id
        self.master.title("Waiting Room")

        self.label_waiting = tk.Label(self, text="Waiting for admin to start game...")
        self.label_waiting.pack(pady=10)

        self.label_other_players = tk.Label(self, text="")
        self.label_other_players.pack(pady=10)

        self.button_start_game = tk.Button(self, text="Start Game", command=self.start_game)
        self.button_start_game.pack(pady=10)
        self.button_start_game.grid_forget()  # Hide the button initially

        self.update_waiting_room()

    def update_waiting_room(self):
    # Query the server to check if other players have connected to the game
        response = self.client.send_request("check_players_connected")
        if response:
        # Display usernames of other players
                other_players = json.loads(response)
                player_names = ", ".join(other_players)
                self.label_other_players.config(text=f"Other players connected: {player_names}")

        # Check if the current user is the admin
        is_admin = self.client.send_request("check_admin")
        if is_admin:
            self.button_start_game.grid()  # Show the button if the user is admin
        else:
            # Continuously check if the game has started
            while True:
                game_started = self.client.send_request("check_game_started")
                if game_started:
                    # Proceed to the next page or action when the game has started
                    self.close_waiting_room()  # Exit the loop
                else:
                    time.sleep(0.5)  # Wait for 0.5 second before checking again

    def close_waiting_room(self):
        # Close the waiting room interface
        self.callback(GameRoomPage)

    def start_game(self):
        # Send a request to the server to start the game
        response = self.client.send_request("start_game")
        if response == "success":
            self.close_waiting_room()



class GameRoomPage(tk.Frame):
    def __init__(self, master, client, game_id, callback):
        super().__init__(master)
        self.client = client
        self.game_id = game_id
        self.callback = callback
        self.master.title("Game Room")

        # Create a frame to contain all widgets
        self.container = tk.Frame(self.master)
        self.container.pack(fill=tk.BOTH, expand=True)

        # Initialize attributes for question and answers
        self.question_label = None
        self.answer_buttons = []

        # Fetch quiz data from the server
        self.fetch_quiz()

        # Start timer for 30 seconds
        self.timer_label = tk.Label(self.container, text="Timer: 30 seconds remaining")
        self.timer_label.pack()
        self.timer_seconds = 30
        self.update_timer()

    def fetch_quiz(self):
        # Fetch quiz data from the server
        response = self.client.send_request(f"quiz {self.game_id}")
        quiz_data = json.loads(response)
        questions = quiz_data.get("quizA", {}).get("questions", {})
        answers = quiz_data.get("quizA", {}).get("answers", {})
        # Update question and answers
        self.update_question(questions)
        self.update_answers(answers)

    def update_question(self, questions):
        # Create or update question label
        if self.question_label is None:
            self.question_label = tk.Label(self.container, text="Question")
            self.question_label.pack()
        else:
            # Assuming Q1 is the first question in the questions dictionary
            question_text = questions.get("Q1", "")
            self.question_label.config(text=question_text)

    def update_answers(self, answers):
        # Create or update answer buttons
        if len(self.answer_buttons) == 0:
            for question_key, answer_text in answers.items():
                button = tk.Button(self.container, text=answer_text, command=lambda: self.choose_answer(question_key))
                button.pack()
                self.answer_buttons.append(button)

    def choose_answer(self, question_key):
        # Handle when an answer button is clicked
        chosen_answer = self.answer_buttons[question_key]['text']
        # Do something with the chosen answer, e.g., send it to the server
        print("Chosen answer:", chosen_answer)

    def update_timer(self):
        # Update timer label
        self.timer_seconds -= 1
        self.timer_label.config(text=f"Timer: {self.timer_seconds} seconds remaining")
        if self.timer_seconds <= 0:
            # Timer expired, redirect to ResultsPage
            self.callback(ResultsPage, self.game_id)
        else:
            # Schedule next update after 1 second
            self.after(1000, self.update_timer)


    #display the scoreboard. Make each question worth 10 points, and in this page display the scoreboard. 
    #the server will have a scoreboard defined, with multiple dictionaries for every game id, and in it the players 
        #with their current score. every time a player sends a request from here, the server will send him the 
        #scoreboard data for the current game id. 
        #also, to move to next quesiton, implement a similar mechnaism where a "next" button can only be clicked by the admin
        #which triggers the next_question, in the meantime non-admin users must wait. 

class ResultsPage(tk.Frame):
    def __init__(self, master, client, game_id, callback):
        super().__init__(master)
        self.client = client
        self.game_id = game_id
        self.callback = callback
        self.master.title("Results Page")

        # Initialize scoreboard display
        self.scoreboard_label = tk.Label(self, text="Scoreboard")
        self.scoreboard_label.pack()

        # Display initial scoreboard
        self.display_scoreboard()

        # Initialize 'Next Question' button (visible only to admin)
        self.next_question_button = tk.Button(self, text="Next Question", command=self.next_question)
        self.next_question_button.pack()

    def display_scoreboard(self):
        # Request scoreboard data from the server
        response = self.client.send_request(f"get_scoreboard {self.game_id}")
        if response:
            scoreboard_data = json.loads(response)
            # Display scoreboard data
            for player, score in scoreboard_data.items():
                player_score_label = tk.Label(self, text=f"{player}: {score}")
                player_score_label.pack()

    def next_question(self):
        # Check if the current user is the admin
        is_admin = self.client.send_request("check_admin")
        if is_admin:
            # Send request to server to move to next question
            response = self.client.send_request("next_question")
            if response == "success":
                # Move to next question
                self.callback(GameRoomPage, self.game_id)
        else:
            print("Only admin can proceed to the next question.")

    def finish_results_page(self):
        # Implementation for finishing the ResultsPage, e.g., returning to LoginPage
        pass


def start_app(client):
    root = tk.Tk()
    root.geometry("400x300")

    page_controller = PageController(root,client)
    page_controller.show_page(LoginPage)

    root.mainloop()
    

if __name__ == "__main__":
    
    client = Client()  # Create an instance of the Client class
    if client.fail:
        print("Aw snap :/ Something went wrong")
        sys.exit()
    game_id
    start_app(client)
