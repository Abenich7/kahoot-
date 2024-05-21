import tkinter as tk
import json

class AppGUI:
    def __init__(self, root, client):
        self.root = root
        self.client = client

        self.root.title("Login")

        self.label_username = tk.Label(root, text="Username:")
        self.entry_username = tk.Entry(root)
        self.label_password = tk.Label(root, text="Password:")
        self.entry_password = tk.Entry(root, show="*")
        self.button_login = tk.Button(root, text="Login", command=self.send_login_data)

        self.label_username.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)
        self.label_password.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)
        self.button_login.grid(row=2, column=1, padx=5, pady=5)

    def send_login_data(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        login_data = {'username': username, 'password': password}
        self.client.send_login_data(json.dumps(login_data))

def start_app(client):
    root = tk.Tk()
    app_gui = AppGUI(root, client)
    root.mainloop()

if __name__ == "__main__":
    import client
    client_socket = client.start_client()
    start_app(client_socket)
