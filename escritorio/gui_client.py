import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog
from datetime import datetime

HOST = '127.0.0.1'
PORT = 65432

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

class ChatApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Python Chat Client")

        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled', width=50, height=20)
        self.chat_area.pack(padx=10, pady=10)

        self.entry = tk.Entry(self.root, width=40)
        self.entry.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=10, pady=(0, 10))

        self.username = simpledialog.askstring("Username", "Enter your name:", parent=self.root)
        if not self.username:
            self.root.destroy()
            return

        self.running = True
        threading.Thread(target=self.receive_messages, daemon=True).start()

        self.chat_area.tag_config("self", foreground="blue")
        self.chat_area.tag_config("other", foreground="green")

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def receive_messages(self):
        while self.running:
            try:
                message = client.recv(1024).decode()
                sender = message.split(":")[0]
                if sender == self.username:
                    self.display_message(message, tag="self")
                else:
                    self.display_message(message, tag="other")
            except:
                self.display_message("Error receiving message. Connection closed.", tag="other")
                break

    def send_message(self, event=None):
        msg = self.entry.get()
        if msg:
            full_msg = f"{self.username}: {msg}"
            self.display_message(full_msg, tag="self")  # Show own message
            client.send(full_msg.encode())
            self.entry.delete(0, tk.END)

    def display_message(self, msg, tag="other"):
        timestamp = datetime.now().strftime("[%H:%M:%S] ")
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, timestamp + msg + "\n", tag)
        self.chat_area.configure(state='disabled')
        self.chat_area.see(tk.END)

    def on_closing(self):
        self.running = False
        client.close()
        self.root.destroy()

if __name__ == "__main__":
    ChatApp()