import tkinter as tk
from tkinter import messagebox
from batak import Player, Deck


# -----------------------------------------
# Welcome screen
# -----------------------------------------2
class WelcomeUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Batak Game - Welcome")
        self.root.geometry("600x500")
        self.root.configure(bg="#2e2e2e")

        self.name_var = tk.StringVar()

        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(
            self.root,
            text="Welcome to Batak",
            font=("Arial", 24, "bold"),
            fg="white", bg="#2e2e2e"
        ).pack(pady=30)

        frame = tk.Frame(self.root, bg="#2e2e2e")
        frame.pack(pady=20)

        tk.Label(frame, text="Enter your name:", font=("Arial", 14), fg="white", bg="#2e2e2e")\
            .grid(row=0, column=0, padx=5)
        tk.Entry(frame, textvariable=self.name_var, font=("Arial", 14), width=20)\
            .grid(row=0, column=1, padx=5)

        btn_frame = tk.Frame(self.root, bg="#2e2e2e")
        btn_frame.pack(pady=40)
        tk.Button(btn_frame, text="Start Game", font=("Arial", 14), width=12, command=self.start_game)\
            .grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Quit", font=("Arial", 14), width=12, command=self.root.quit)\
            .grid(row=0, column=1, padx=10)

    def start_game(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Missing Name", "Please enter your name")
            return

        self.root.destroy()

        # Create players: 3 bots + human
        deck = Deck()
        deck.shuffle()
        players = [
            Player("North Bot", is_bot=True, hand=deck.deal(13)),
            Player("East Bot", is_bot=True, hand=deck.deal(13)),
            Player(name, is_bot=False, hand=deck.deal(13)),  # human player
            Player("West Bot", is_bot=True, hand=deck.deal(13)),
        ]

      #todo game screen


# -----------------------------------------
# Launch welcome screen
# -----------------------------------------
if __name__ == "__main__":
    WelcomeUI()
