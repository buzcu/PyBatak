from .card import Card
from .player import Player

class Game:
    def __init__(self,players):
        self.players = players
        self.trump = None
        self.is_trump_enabled = False
        self.cards_on_table = []
        self.current_player_index = 0

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

    def bidding(self):
        bids = [player.bid() for player in self.players]
        max_bid_index = bids.index(max(bids))
    
        self.trump = self.players[max_bid_index].choose_trump()
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

    def gameround(self):
        self.cards_on_table.clear()
        self.roundwinner = None
        self.roundwinnerindexoffset = self.current_player_index
        player = self.players[self.current_player_index]
        for _ in range(4):
            print("\nCurrent player: " +player.name)
            print("Cards on table: " + str(self.cards_on_table))
            print("Player hand: " + str(player.hand))
            print("players card options are as follows:")
            legal_cards = [ card for card in player.hand if self.is_play_legal(card)]
            
            if len(legal_cards) == 0:
                print(" !!! ERROR: No legal cards available !!!")
                print("Player cards are: " + str(player.hand))
                print("Cards on table are: " + str(self.cards_on_table))
                print("Trump is: " + str(self.trump))
                print("Current player is: " + str(player.name))
                return
            print("Cards: " + str(legal_cards))    
            played_card = player.play_card(self.cards_on_table, self.trump, legal_cards)
            if played_card == None:
                print(" !!! ERROR: No card played !!!")
                return
            if played_card not in legal_cards:
                print(" !!! ERROR: Card not legal !!!")
                return
            if played_card.suit == self.trump:
                self.is_trump_enabled = True
                
            print("" + player.name + " played: " + str(played_card))
            self.cards_on_table.append(played_card)
            self.current_player_index = (self.current_player_index+1)%4
            player = self.players[self.current_player_index]
        
                
        self.determine_winning_card()
        
        print("Round winner: " + self.players[self.roundwinner].name)
        self.players[self.roundwinner].score += 1
        self.current_player_index = self.roundwinner
        