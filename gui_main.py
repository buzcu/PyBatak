"""This module is the attempt at making a gui."""
import tkinter as tk
from tkinter import messagebox, simpledialog, StringVar
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
        self.bottom_label = StringVar()
        self.build_ui()
        # self.draw_card(Card(suit="Hearts", rank=14), 50, 50)
        self.tkroot.after(200, self.start_game)
        #self.start_game()
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
        self.label = tk.Label(
            self.controls,
            textvariable=self.bottom_label,
            fg="white",
            bg="#1b5e20",
            font=("Arial", 12, "bold")
        )
        self.label.pack(pady=10)

    def set_bottom_label(self, text):
        """Sets the text of the bottom label."""
        self.bottom_label.set(text)

    def draw_card(self, card, x, y):
        """Draws a visual marker where a card might go."""
        card_image = self.card_library.get_image(card)
        img_id = self.table.create_image(
            x,
            y,
            image=card_image,
            anchor='nw'
        )
        self.drawn_cards.append(card_image)
        # We use lambda to pass the specific 'card' object and 'img_id' to the function
        self.table.tag_bind(img_id, "<Button-1>", lambda event, c=card, i=img_id: self.human_plays_card(c, i))

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

    def draw_played_card(self, card, position):
        """Draws a card in the center of the table based on who played it."""
        # Coordinates for the center area
        coords = {
            "North": (450, 180),
            "South": (450, 320),
            "East":  (550, 250),
            "West":  (350, 250)
        }
        x, y = coords.get(position, (450, 250))
        
        img = self.card_library.get_image(card)
        self.table.create_image(x, y, image=img, anchor='nw', tags="played_card")
        self.drawn_cards.append(img)

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
        self.write_names(north_name = [player for player in self.game.players if player.position=="North"][0].name,
                         east_name = [player for player in self.game.players if player.position=="East"][0].name,
                         west_name = [player for player in self.game.players if player.position=="West"][0].name,
                         south_name = [player for player in self.game.players if player.position=="South"][0].name)
        self.set_bottom_label("Welcome to the Batak Table, " + PLAYER_NAME + "!")
        self.player.player_bid = self.get_player_bid()
        self.player.chosen_trump = self.get_player_trump()
        bidding_result = self.game.bidding()
        print(bidding_result)
        self.set_bottom_label(bidding_result)
        #self.draw_played_card(self.player.hand[0], self.player.position)
        #self.draw_played_card(self.player.hand[0], "North")
        #self.draw_played_card(self.player.hand[0], "East")
        #self.draw_played_card(self.player.hand[0], "West")
    def play_round_until_player(self):
        """Play a round of the game."""
        self.game.cards_on_table.clear()
        self.game.roundwinner = None
        self.game.roundwinnerindexoffset = self.game.current_player_index
        current_player = self.game.players[self.game.current_player_index]
        for _ in range(4):
            if current_player is self.player:
                return
            legal_cards = [card for card in current_player.hand if self.game.is_play_legal(card)]
            played_card = current_player.play_card(self.game.cards_on_table, self.game.trump, legal_cards)
            if played_card.suit == self.game.trump:
                self.game.is_trump_enabled = True

            self.game.cards_on_table.append(played_card)
            self.game.current_player_index = (self.game.current_player_index + 1) % 4
            current_player = self.game.players[self.game.current_player_index]
    def human_plays_card(self, card, img_id):
        """Handle the human player playing a card."""
        legal_cards = [c for c in self.player.hand if self.game.is_play_legal(c)]
        if card not in legal_cards:
            messagebox.showwarning("Illegal Move", f"You cannot play {str(card)} right now.")
            return
        self.player.hand.remove(card)
        self.table.delete(img_id)
        self.game.cards_on_table.append(card)
        if card.suit == self.game.trump:
            self.game.is_trump_enabled = True
        self.draw_played_card(card, self.player.position)
        self.game.current_player_index = (self.game.current_player_index + 1) % 4
        self.play_round_after_player()
        if len(self.game.cards_on_table) == 4:
            self.evaluate_round_winner()
            self.set_bottom_label(f"Round won by {self.game.players[self.game.roundwinner].name}!")
            #self.tkroot.after(5000, self.start_game)  # Start next round after 2 seconds
    def evaluate_round_winner(self):
        """Evaluate and display the round winner."""
        self.game.determine_winning_card()
        print("Round winner: " + self.game.players[self.game.roundwinner].name)
        self.game.players[self.game.roundwinner].score += 1
        self.game.current_player_index = self.game.roundwinner

    def write_names(self, north_name, east_name, west_name, south_name):
        """Write the names of the players on the table."""
        self.table.create_text(450, 115, text=north_name, anchor='nw', font='Arial', fill='black')
        self.table.create_text(875, 400, text=east_name, anchor='nw', font='Arial', fill='black')
        self.table.create_text(25, 400, text=west_name, anchor='nw', font='Arial', fill='black')
        self.table.create_text(450, 430, text=south_name, anchor='nw', font='Arial', fill='black')

    def get_player_bid(self):
        user_bid = simpledialog.askinteger("Bid", "Enter your bid:")
        if user_bid is None or user_bid < 5 or user_bid > 13:
            messagebox.showwarning("Missing Bid", "Please enter your bid between 5 and 13")
            return self.get_player_bid()
        return user_bid
    
    def get_player_trump(self):
        user_trump = simpledialog.askstring("Trump Suit", "Enter your trump suit (Hearts, Diamonds, Clubs, Spades):")
        if user_trump is None or user_trump not in ["Hearts", "Diamonds", "Clubs", "Spades"]:
            messagebox.showwarning("Missing Trump Suit", "Please enter a valid trump suit")
            return self.get_player_trump()
        return user_trump

    def draw_cards(self):
        """
        Docstring for draw_cards
        
        :param self: Description
        """
        for card in self.player.hand:
            self.draw_card(card, 10 + self.player.hand.index(card)*75, 450)
        for bot in self.game.players:
            if bot is not self.player:
                if bot.position == "North":
                    self.draw_north_bot(bot)
                elif bot.position == "East":
                    self.draw_east_bot(bot)
                    pass
                elif bot.position == "West":
                    self.draw_west_bot(bot)
                    pass

    def draw_north_bot(self, bot):
        """
        Docstring for draw_north_bot
        
        :param self: Description
        :param bot: Description
        """
        for card in bot.hand:
            self.draw_back_card_vertical(200 + bot.hand.index(card)*47, 10)

    def draw_east_bot(self, bot):
        """
        Docstring for draw_east_bot

        :param self: Description
        :param bot: Description
        """
        for card in bot.hand:
            self.draw_back_card_horizontal(875, 25 + bot.hand.index(card)*25)

    def draw_west_bot(self, bot):
        """
        Docstring for draw_east_bot

        :param self: Description
        :param bot: Description
        """
        for card in bot.hand:
            self.draw_back_card_horizontal(25, 25 + bot.hand.index(card)*25)
# -----------------------------------------
# Launch welcome screen
# -----------------------------------------
PLAYER_NAME = "Unknown Player" # Default name
if __name__ == "__main__":
    root = tk.Tk()
    WelcomeUI(root)
    root = tk.Tk()
    BatakTableUI(root)
