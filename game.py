from card import Card
from player import Player

class Game:
    def __init__(self,players, trump, bidwinner):
        self.players = players
        self.deck = []
        self.trump = trump
        self.is_trump_enabled = false
        self.bidwinner = bidwinner
        self.cards_on_table = []
        self.current_player_index = 0

    def is_play_legal(self, card):

        if len(self.cards_on_table) == 0:
            if card.suit != self.trump:
                return true
            elif card.suit == self.trump:
                if self.is_trump_enabled == false:
                    if len(self.players[self.current_player_index].hand) == self.players[self.current_player_index].number_of_cards_in_suit(self.trump)):
                        return true # only left cards are trump cards
                    return false # trump is not out yet
                else:
                    return true 
        
        else:
            if card.suit == self.cards_on_table[0].suit:
                if self.get_card_value(card) > self.get_card_value(self.cards_on_table[len(self.cards_on_table) - 1]):
                    return true #it must be in increasing value order if able to play
                else:
                    for cardd in self.players[self.current_player_index].hand:
                        if cardd.suit == self.cards_on_table[0].suit and self.get_card_value(cardd) > self.get_card_value(self.cards_on_table[len(self.cards_on_table) - 1]):
                            return false # this card is not legal because player has a higher ranked card of the same suit
                    return true # there is no higher ranked card from the same suit in hand

            else:
                if self.players[self.current_player_index].number_of_cards_in_suit(self.cards_on_table[0].suit) == 0:
                    if card.suit == self.trump:
                        return true # player can play trump card
                    elif self.players[self.current_player_index].number_of_cards_in_suit(self.trump) == 0:
                        return true # player can play any card
                    else:
                        return false # player must play trump card
                else:
                    return false # player must play the same suit as the first card played

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
        self.current_player_index = max_bid
      
       