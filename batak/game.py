from batak.card import Card
from batak.player import Player

class Game:
    def __init__(self,players):
        self.players = players
        self.trump = None
        self.is_trump_enabled = False
        self.cards_on_table = []
        self.current_player_index = 0
        self.bids = []
        self.trumps = []
        self.roundwinner = None
        self.roundwinnerindexoffset = 0

    def is_play_legal(self, card):
        player = self.players[self.current_player_index]

        if len(self.cards_on_table) == 0:
            if card.suit != self.trump:
                return True
            elif card.suit == self.trump:
                if not self.is_trump_enabled:
                    if len(player.hand) == player.number_of_cards_in_suit(self.trump):
                        return True # only left cards are trump cards
                    return False # trump is not out yet
                else:
                    return True 
        
        else:
            leading_suit = self.cards_on_table[0].suit
            if card.suit == leading_suit:
                if self.is_trump_enabled:
                    return True # player can play a card of the same suit without rank restriction if somebodyelse has played a trump card
                if card.get_value() > ( max(filter(lambda card: card.suit==leading_suit, self.cards_on_table))).get_value():
                    return True #player can play a card of the same suit with higher rank than the highest card played so far
                else:
                    if((max(filter(lambda card: card.suit==leading_suit, player.hand))).get_value() < (max(filter(lambda card: card.suit==leading_suit, self.cards_on_table))).get_value()):
                        return True # player can play a card of the same suit with lower rank than the highest card played so far, if he has no higher card in his hand
                    else:
                        return False

            else:
                if player.number_of_cards_in_suit(leading_suit) == 0:
                    if card.suit == self.trump:
                        return True # player can play trump card
                    elif player.number_of_cards_in_suit(self.trump) == 0:
                        return True # player can play any card
                    else:
                        return False # player must play trump card
                else:
                    return False # player must play the same suit as the first card played

    def register_bids(self, bid_and_trump):
        self.bids.append(bid_and_trump[0])
        self.trumps.append(bid_and_trump[1])
        
    def bidding_results(self):
        #bids = [player.bid() for player in self.players]
        max_bid_index = self.bids.index(max(self.bids))
        self.trump = self.trumps[max_bid_index]
        print('Trump: ' + self.trump + ' by player: ' + self.players[max_bid_index].name)
        self.current_player_index = max_bid_index #bid winner starts first
    
    def determine_winning_card(self):
        trump_cards = [card for card in self.cards_on_table if card.suit == self.trump]
        if trump_cards:
            winningcard = max(trump_cards)
        else:
            same_suit_cards = [card for card in self.cards_on_table if card.suit == self.cards_on_table[0].suit]
            winningcard = max(same_suit_cards)
        self.roundwinner = (self.cards_on_table.index(winningcard)+self.roundwinnerindexoffset)%4

    def get_legal_cards(self):
        player = self.players[self.current_player_index]
        legal_cards = [card for card in player.hand if self.is_play_legal(card)]
        return legal_cards

    def start_round(self):
        self.cards_on_table.clear()
        self.roundwinner = None
        self.roundwinnerindexoffset = self.current_player_index
        return self.current_player_index

    def register_played_card(self, card):
        if card == None:
            print(" !!! ERROR: No card played !!!")
            return
        print("" + self.players[self.current_player_index].name + " played: " + str(card))
        self.cards_on_table.append(card)
        self.current_player_index = (self.current_player_index + 1) % 4
        if card.suit == self.trump:
                self.is_trump_enabled = True
        
    def finalize_round(self):
        self.determine_winning_card()
        print("Round winner: " + self.players[self.roundwinner].name)
        self.players[self.roundwinner].score += 1
        self.current_player_index = self.roundwinner

    def get_trump(self):
        return self.trump
    
    def get_cards_on_table(self):
        return self.cards_on_table
 
        