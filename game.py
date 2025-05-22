from card import Card
from player import Player

class Game:
    def __init__(self,players):
        self.players = players
        self.deck = []
        self.trump = None
        self.is_trump_enabled = False
        self.bidwinner = None
        self.cards_on_table = []
        self.current_player_index = 0

    def is_play_legal(self, card):

        if len(self.cards_on_table) == 0:
            if card.suit != self.trump:
                return True
            elif card.suit == self.trump:
                if self.is_trump_enabled == False:
                    if len(self.players[self.current_player_index].hand) == self.players[self.current_player_index].number_of_cards_in_suit(self.trump):
                        return True # only left cards are trump cards
                    return False # trump is not out yet
                else:
                    return True 
        
        else:
            if card.suit == self.cards_on_table[0].suit:
                if card.get_value() > (self.cards_on_table[len(self.cards_on_table) - 1]).get_value():
                    return True #it must be in increasing value order if able to play
                else:
                    for cardd in self.players[self.current_player_index].hand:
                        if cardd.suit == self.cards_on_table[0].suit and (cardd.get_value() > ((max([card for card in self.cards_on_table if card.suit == self.cards_on_table[0].suit],  key=lambda card: card.rank)).get_value())):
                            return False # this card is not legal because player has a higher ranked card of the same suit
                    return True # there is no higher ranked card from the same suit in hand

            else:
                if self.players[self.current_player_index].number_of_cards_in_suit(self.cards_on_table[0].suit) == 0:
                    if card.suit == self.trump:
                        return True # player can play trump card
                    elif self.players[self.current_player_index].number_of_cards_in_suit(self.trump) == 0:
                        return True # player can play any card
                    else:
                        return False # player must play trump card
                else:
                    return False # player must play the same suit as the first card played

    def bidding(self):
        bids = []
        bids.append(self.players[0].bid())
        max_bid = 0
        bids.append(self.players[1].bid())
        if bids[1] > bids[0]:
            max_bid = 1
        bids.append(self.players[2].bid())
        if bids[2] > bids[max_bid]:
            max_bid = 2
        bids.append(self.players[3].bid())
        if bids[3] > bids[max_bid]:
            max_bid = 3
    
        self.trump = self.players[max_bid].choose_trump()
        print('Trump: ' + self.trump + ' by player: ' + self.players[max_bid].name)
        self.current_player_index = max_bid #bid winner starts first
    
    def determine_winning_card(self):
        trump_cards = [card for card in self.cards_on_table if card.suit == self.trump]
        if trump_cards:
            winningcard = max(trump_cards, key=lambda card: card.rank)
        else:
            same_suit_cards = [card for card in self.cards_on_table if card.suit == self.cards_on_table[0].suit]
            winningcard = max(same_suit_cards, key=lambda card: card.rank)
        self.roundwinner = (self.cards_on_table.index(winningcard)+self.roundwinnerindexoffset)%4

    def gameround(self):
        self.cards_on_table.clear()
        self.roundwinner = None
        self.roundwinnerindexoffset = self.current_player_index
        self.winningcard = None
        for x in range(4):
            print("players card options are as follows: \n")
            legal_cards = [ card for card in self.players[(self.current_player_index)].hand if self.is_play_legal(card)]
            print("\n----------")
            if len(legal_cards) == 0:
                print(" !!! ERROR: No legal cards available !!!")
                print("Player cards are: " + str(self.players[(self.current_player_index)].hand))
                print("Cards on table are: " + str(self.cards_on_table))
                print("Trump is: " + str(self.trump))
                print("Current player is: " + str(self.players[(self.current_player_index)].name))
                return
            played_card = self.players[(self.current_player_index)].play_card(self.cards_on_table, self.trump, legal_cards)
            if played_card == None:
                print(" !!! ERROR: No card played !!!")
                return
            if played_card not in legal_cards:
                print(" !!! ERROR: Card not legal !!!")
                return
            self.cards_on_table.append(played_card)
            self.current_player_index = (self.current_player_index+1)%4
        
                
        self.determine_winning_card()
        
        print("Round winner: " + self.players[self.roundwinner].name)
        self.players[self.roundwinner].score += 1
        self.current_player_index = self.roundwinner
        