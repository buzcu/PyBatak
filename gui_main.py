"""This module is the attempt at making a gui."""
import tkinter as tk
from tkinter import messagebox
from batak import Deck, Batak, HumanPlayer
from batak import BotPlayer, RandomPlayStrategies
from batak import RuleBasedPlayStrategies, HighCardPlayStrategies
from image_storage import CardFaces

# -----------------------------------------
# Welcome screen
# -----------------------------------------2
class WelcomeUI:
    """welcome screen for the Batak game."""
    def __init__(self, welcome_root):
        self.root = welcome_root
        self.root.title("Batak Game - Welcome")
        self.root.geometry("600x500")
        self.root.configure(bg="#2e2e2e")

        self.name_var = tk.StringVar()

        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        """
        Docstring for build_ui
        
        :param self: Description
        """
        tk.Label(
            self.root,
            text="Welcome to Batak",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#2e2e2e",
        ).pack(pady=30)

        frame = tk.Frame(self.root, bg="#2e2e2e")
        frame.pack(pady=20)

        tk.Label(
            frame, text="Enter your name:", font=("Arial", 14), fg="white", bg="#2e2e2e"
        ).grid(row=0, column=0, padx=5)
        tk.Entry(frame, textvariable=self.name_var, font=("Arial", 14), width=20).grid(
            row=0, column=1, padx=5
        )

        btn_frame = tk.Frame(self.root, bg="#2e2e2e")
        btn_frame.pack(pady=40)
        tk.Button(
            btn_frame,
            text="Start Game",
            font=("Arial", 14),
            width=12,
            command=self.start_game,
        ).grid(row=0, column=0, padx=10)
        tk.Button(
            btn_frame, text="Quit", font=("Arial", 14), width=12, command=self.root.quit
        ).grid(row=0, column=1, padx=10)

    def start_game(self)-> str:
        """
        Docstring for start_game
        
        :param self: Description
        """
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Missing Name", "Please enter your name")
            return
        global PLAYER_NAME
        PLAYER_NAME = name
        self.root.destroy()

class BatakTableUI():
    """Main game table UI for Batak."""
    def __init__(self, root):
        self.tkroot = root
        self.tkroot.title("Batak Game")
        self.tkroot.minsize(1000,600)
        self.tkroot.configure(bg="#1e1e1e")
        # 2. Configure grid weights so the canvas expands with the window
        self.tkroot.columnconfigure(0, weight=1)
        self.tkroot.rowconfigure(0, weight=1)
        self.card_library = CardFaces()
        self.card_library.load_images()
        self.drawn_cards = []
        self.build_ui()
        # self.draw_card(Card(suit="Hearts", rank=14), 50, 50)
        self.start_game()
        self.tkroot.mainloop()

    def build_ui(self):
        """
        Docstring for build_ui
        
        :param self: Description
        """
        # UI components would be built here
        # 3. Create the "Game Table" using a Canvas
        # We use a dark green color to mimic a classic card table
        self.table = tk.Canvas(
            self.tkroot,
            bg="#2e7d32",
            highlightthickness=0
        )
        self.table.grid(row=0, column=0, sticky="nsew")

        # 4. Add a status bar or control panel at the bottom
        self.controls = tk.Frame(self.tkroot, bg="#1b5e20", height=50)
        self.controls.grid(row=1, column=0, sticky="ew")
        global PLAYER_NAME
        self.label = tk.Label(
            self.controls,
            text="Welcome to the Batak Table, " + PLAYER_NAME + "!",
            fg="white",
            bg="#1b5e20",
            font=("Arial", 12, "bold")
        )
        self.label.pack(pady=10)

    def draw_card(self, card, x, y):
        """Draws a visual marker where a card might go."""
        card_image = self.card_library.get_image(card)
        self.table.create_image(
            x,
            y,
            image=card_image,
            anchor='nw'
        )
        self.drawn_cards.append(card_image)

    def draw_back_card_vertical(self, x, y):
        """Draws a visual marker where a card back might go."""
        back_image = self.card_library.get_back_image_vertical()
        self.table.create_image(
            x, y,
            image=back_image,
            anchor='nw'
        )
        self.drawn_cards.append(back_image)

    def draw_back_card_horizontal(self, x, y):
        """Draws a visual marker where a card back might go."""
        back_image = self.card_library.get_back_image_horizontal()
        self.table.create_image(
            x, y,
            image=back_image,
            anchor='nw'
        )
        self.drawn_cards.append(back_image)

    def start_game(self):
        """
        Docstring for start_game
        
        :param self: Description
        """
        deck = Deck()
        deck.shuffle()
        self.player = HumanPlayer(name=PLAYER_NAME, hand=deck.deal(13))
        self.game = Batak(
            players=[
                self.player,
                BotPlayer(name="John Malkovich",
                          hand=deck.deal(13),
                          position="North",
                          strategy=RandomPlayStrategies()),
                BotPlayer(name="Yoko Ono",
                          hand=deck.deal(13),
                          position="East",
                          strategy=RuleBasedPlayStrategies()),
                BotPlayer(name="Kanye West",
                          hand=deck.deal(13),
                          position="West",
                          strategy=HighCardPlayStrategies()),
            ]
        )
        self.draw_cards()

    def draw_cards(self):
        """
        Docstring for draw_cards
        
        :param self: Description
        """
        for card in self.player.hand:
            self.draw_card(card, 10 + self.player.hand.index(card)*75, 400)
        for bot in self.game.players:
            if bot is not self.player:
                if bot.position == "North":
                    self.draw_north_bot(bot)
                elif bot.position == "East":
                    # Draw east bot cards
                    pass
                elif bot.position == "West":
                    # Draw west bot cards
                    pass
                 # Draw bot cards
                 # dont forget to add sitting positions to
                 # bot players then create draw functions which
                 # draw card backs on those positions

    def draw_north_bot(self, bot):
        """
        Docstring for draw_north_bot
        
        :param self: Description
        :param bot: Description
        """
        for card in bot.hand:
            self.draw_back_card_vertical(10 + bot.hand.index(card)*77, 10)
# -----------------------------------------
# Launch welcome screen
# -----------------------------------------
PLAYER_NAME = "Unknown Player" # Default name
if __name__ == "__main__":
    root = tk.Tk()
    WelcomeUI(root)
    root = tk.Tk()
    BatakTableUI(root)
