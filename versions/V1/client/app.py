import tkinter as tk
import json
from client_module import Client  # Import the Client class or module


class LoginPage(tk.Frame):
    def __init__(self, root, client):
        super().__init__(root)
        self.root = root
        self.client = client
      #  self.generate_login_success_event()
       # self.bind_event_handler()  # Bind event handler when initializing the LoginPage


        self.root.title("Login")

        self.label_username = tk.Label(root, text="Username:")
        self.entry_username = tk.Entry(root)
        self.label_password = tk.Label(root, text="Password:")
        self.entry_password = tk.Entry(root, show="*")
        self.button_login = tk.Button(root, text="Login", command=lambda: self.send_login_data(action="login"))
        self.button_signup = tk.Button(root, text="First time? Sign up", command=lambda: self.send_login_data(action="signup"))
        self.label_username.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)
        self.label_password.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)
        self.button_login.grid(row=2, column=1, padx=5, pady=5)
        self.button_signup.grid(row=4, column=1, padx=5, pady=5)
    
    #def generate_login_success_event(self):
        # Simulate a successful login
     #   self.event_generate("<<LoginSuccess>>", when="tail")

   # def generate_login_success_event(self):
        # Simulate a successful login
    #    self.event_generate("<<LoginSuccess>>", when="tail")

    def transition_to_choose_quiz(root, client):
            root.destroy()  # Close login window
            ChooseQuizPage(tk.Toplevel(root), client)  # Create ChooseQuizPage instance

   # def bind_event_handler(self):
    #    self.bind("<<LoginSuccess>>", lambda event: self.transition_to_choose_quiz(self.root, self.client))

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
            print("Before root window destruction")
            self.transition_to_choose_quiz(self.root,self.client)
            
            print("After root window destruction")

             # Calls constructor for ChooseQuizPage class



class ChooseQuizPage(tk.Frame):
    def __init__(self, root, client):
        super().__init__(root)
        self.root = root
        self.client = client

        self.root.title("Choose Quiz")

        self.container = tk.Frame(self.root)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.label_title = tk.Label(self.container, text="Select a Quiz:")
        self.label_title.pack(padx=5, pady=5)

        self.quiz_listbox = tk.Listbox(self.container)
        self.quiz_listbox.pack(padx=5, pady=5)

        self.button_select_quiz = tk.Button(self.container, text="Select Quiz", command=self.select_quiz)
        self.button_select_quiz.pack(padx=5, pady=5)

        self.load_quizzes()

    def load_quizzes(self):
        response = self.client.send_request("get_quizzes")
        quizzes = json.loads(response)
        for quiz in quizzes:
            self.quiz_listbox.insert(tk.END, quiz)

    def select_quiz(self):
        selected_index = self.quiz_listbox.curselection()
        if selected_index:
            quiz_name = self.quiz_listbox.get(selected_index)
            # Transition to the next page (e.g., the game room page)

            game_room_page = GameRoomPage(self.root, self.client, quiz_name)
            self.root.withdraw()    # Close choose quiz window




class GameRoomPage(tk.Frame):
    def __init__(self, root, client, quiz_name):
        super().__init__(root)
        self.root = root
        self.client = client
        self.quiz_name = quiz_name
        self.root.title("Game Room")

        # Create a frame to contain all widgets
        self.container = tk.Frame(self.root)
        self.container.pack(fill=tk.BOTH, expand=True)

        # Initialize attributes for question and answers
        self.question_label = None
        self.answer_buttons = []

        # Fetch quiz data from the server
        self.fetch_quiz()

    def fetch_quiz(self):
        # Fetch quiz data from the server
        response = self.client.send_request(f"quiz {self.quiz_name}")
        quiz_data = json.loads(response)

        # Extract questions and answers
        questions = quiz_data.get("questions", {})
        answers = quiz_data.get("answers", {})

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
        else:
            for i, (question_key, answer_text) in enumerate(answers.items()):
                self.answer_buttons[i].config(text=answer_text)

    def choose_answer(self, question_key):
        # Handle when an answer button is clicked
        chosen_answer = self.answer_buttons[question_key]['text']
        # Do something with the chosen answer, e.g., send it to the server
        print("Chosen answer:", chosen_answer)

#def start_app(client):
 #   root = tk.Tk()
  #  LoginPage(root, client)  # Note: no need to assign to a variable
    #LoginPage.bind("<<LoginSuccess>>", lambda event: transition_to_choose_quiz(root, client))
   # ChooseQuizPage(root,client)
    
   # root.mainloop()


#if __name__ == "__main__":
 #   client=0
  #  client = Client()  # Create an instance of the Client class
   # if client:
    #    print("Connection established with:",client.server_ip,":",client.server_port)
    #start_app(client)
