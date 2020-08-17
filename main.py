import random
from collections import deque
from mcts import mcts
from copy import copy, deepcopy


class Tree(object):
    # Generic tree node.
    def __init__(self, name='root', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)

    def __repr__(self):
        return self.name

    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)

class State:
    def getPossibleActions(self):
        # Returns an iterable of all actions which can be taken from this state
        print("")

    def takeAction(self, action):
        # Returns the state which results from taking action action
        print(action)

    def isTerminal(self):
        # Returns whether this state is a terminal state
        if len(self.getPossibleActions()) == 0:
            return True
        else:
            return False

    def getReward(self):
        # Returns the reward for this state. Only needed for terminal states.
        print("")


class Card:
    cardvalue = {'A': 20, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 12, 'J': 14, 'Q': 16, 'K': 18, '0': 0}

    def __init__(self, value, color):
        self.value = value
        self.color = color

    def __str__(self):
        return self.color + ' ' + self.value

    def __repr__(self):
        return self.color + ' ' + self.value

    def print(self):
        print(self.color, self.value)
        if self.color=='kupa':
            print('''
 _____
|'''+self.value+'''_ _ |
|( v )|
| \ / |
|  .  |
|____'''+'♥'+'''|
''')
        elif self.color=='sinek':
            print("""
 _____
|"""+self.value+""" _  |
| ( ) |
|(_'_)|
|  |  |
|____"""+'♣'+"""|""")
        elif self.color=='karo':
            print("""
 _____
|"""+self.value+""" ^  |
| / \ |
| \ / |
|  .  |
|____"""+'♦'+"""|
""")
        elif self.color=='maça':
            print("""
 _____
|"""+self.value+""" .  |
| /.\ |
|(_._)|
|  |  |
|____"""+'♠'+"""|
""")


class Player:
    cardvalue = {'A': 20, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 12, 'J': 14, 'Q': 16,
                 'K': 18, '0': 0}

    def __init__(self):
        self.name = ''
        self.cards = []
        self.woncards = []
        self.score = 0
        self.kupas = []
        self.karos = []
        self.sineks = []
        self.macas = []

    def __init__(self, name, cardss):
        self.name = name
        self.cards = cardss
        self.woncards = []
        self.score = 0
        self.kupas = []
        self.karos = []
        self.sineks = []
        self.macas = []

    def get_card_value(self, card):
        return self.cardvalue[card.value]

    def print_player_cards(self):
        self.order_cards()
        for number, card in enumerate(self.kupas):
            print(card)
        for number, card in enumerate(self.macas):
            print(card)
        for number, card in enumerate(self.karos):
            print(card)
        for number, card in enumerate(self.sineks):
            print(card)

    def order_cards(self):
        self.cards.sort(key=self.get_card_value)
        self.kupas = []
        self.karos = []
        self.sineks = []
        self.macas = []
        for card in self.cards:
            if card.color == 'kupa':
                self.kupas.append(card)
            elif card.color == 'maça':
                self.macas.append(card)
            elif card.color == 'karo':
                self.karos.append(card)
            else:
                self.sineks.append(card)
        self.kupas.sort(key=self.get_card_value)
        self.macas.sort(key=self.get_card_value)
        self.karos.sort(key=self.get_card_value)
        self.sineks.sort(key=self.get_card_value)

    def list_playable_cards(self, cardsontable, koz, kozciktimi, round, bidwinner):
        #temp_playa = Player()
        temp_playa = deepcopy(self)
        temp_list = []
        #for cards in range(len(temp_playa.cards)):
        #    temp_list.append(temp_playa.play_card(cardsontable, koz, kozciktimi, round))
        for cards in self.cards:
            if self.is_play_legal(cards, cardsontable, koz, kozciktimi, bidwinner) == True:
                temp_list.append(cards)
        return temp_list

    def is_play_legal(self, card, cardsontable, koz, kozciktimi, bidwinner):
        player_koz_number = 0
        if koz == "kupa":
            player_koz_number = len(self.kupas)
        elif koz == "maça":
            player_koz_number = len(self.macas)
        elif koz == "karo":
            player_koz_number = len(self.karos)
        elif koz == "sinek":
            player_koz_number = len(self.sineks)

        player_main_color_count = 0
        if len(cardsontable) > 0:
            main_color = cardsontable[0].color
            if main_color == "kupa":
                player_main_color_count = len(self.kupas)
            elif main_color == "maça":
                player_main_color_count = len(self.macas)
            elif main_color == "karo":
                player_main_color_count = len(self.karos)
            elif main_color == "sinek":
                player_main_color_count = len(self.sineks)

        if len(cardsontable) == 0:
            if kozciktimi == 1 or (kozciktimi == 0 and card.color != koz):
                return True
        elif cardsontable[0].color == card.color and self.get_card_value(cardsontable[len(cardsontable)-1]) < self.get_card_value(card):
            return True
        elif cardsontable[0].color == card.color and self.get_card_value(cardsontable[len(cardsontable)-1]) > self.get_card_value(card):
            if cardsontable[0].color == "kupa":
                for cardd in self.kupas:
                    if self.get_card_value(cardd)>self.get_card_value(cardsontable[len(cardsontable)-1]):
                        return False
                return True
            elif cardsontable[0].color == "maça":
                for cardd in self.macas:
                    if self.get_card_value(cardd) > self.get_card_value(cardsontable[len(cardsontable) - 1]):
                        return False
                return True
            elif cardsontable[0].color == "karo":
                for cardd in self.karos:
                    if self.get_card_value(cardd) > self.get_card_value(cardsontable[len(cardsontable) - 1]):
                        return False
                return True
            elif cardsontable[0].color == "sinek":
                for cardd in self.sineks:
                    if self.get_card_value(cardd) > self.get_card_value(cardsontable[len(cardsontable) - 1]):
                        return False
                return True
        elif player_main_color_count == 0 and (card.color == koz or player_koz_number == 0):
            return True
        return False

    def play_card(self, cardsontable, koz, kozciktimi, round):
        self.order_cards()
        if round == 0:
            if len(cardsontable) == 0:  # first game first card
                card_to_play = random.choice(self.cards)  # this means we are first to play
                while card_to_play.color == koz:
                    card_to_play = random.choice(self.cards)
                self.cards.remove(card_to_play)
                return card_to_play
            else:
                if (cardsontable[0].color == 'kupa' and len(self.kupas) == 0) or (cardsontable[0].color == 'maça' and len(self.macas) == 0) or (cardsontable[0].color == 'sinek' and len(self.sineks) == 0) or (cardsontable[0].color == 'karo' and len(self.karos) == 0): # this means we dont have same club therefore we should play koz
                    if koz == 'maça':
                        if len(self.macas) > 0: # check if we have any koz
                            card_to_play = random.choice(self.macas)
                        else:
                            card_to_play = self.cards[0] # if we dont have koz it doesnt matter we will lose anyways so use smallest possible card
                    elif koz == 'kupa':
                        if len(self.kupas) > 0: # check if we have any koz
                            card_to_play = random.choice(self.kupas)
                        else:
                            card_to_play =self.cards[0] # if we dont have koz it doesnt matter we will lose anyways
                    elif koz == 'sinek':
                        if len(self.sineks) > 0: # check if we have any koz
                            card_to_play = random.choice(self.sineks)
                        else:
                            card_to_play = self.cards[0] # if we dont have koz it doesnt matter we will lose anyways
                    elif koz == 'karo':
                        if len(self.karos) > 0: # check if we have any koz
                            card_to_play = random.choice(self.karos)
                        else:
                            card_to_play = self.cards[0] # if we dont have koz it doesnt matter we will lose anyways
                else:
                    if cardsontable[0].color == 'kupa':
                        card_to_play = random.choice(self.kupas)
                    elif cardsontable[0].color == 'karo':
                        card_to_play = random.choice(self.karos)
                    elif cardsontable[0].color == 'maça':
                        card_to_play = random.choice(self.macas)
                    elif cardsontable[0].color == 'sinek':
                        card_to_play = random.choice(self.sineks)
                self.cards.remove(card_to_play)
                return card_to_play
        else:
            if len(cardsontable) == 0:#nth game first card
                card_to_play = random.choice(self.cards)#this means we are first to play
                card_species = 0
                if len(self.macas) > 0:
                    card_species = card_species+1
                if len(self.kupas) > 0:
                    card_species = card_species+1
                if len(self.karos) > 0:
                    card_species = card_species+1
                if len(self.sineks) > 0:
                    card_species = card_species+1
                while card_to_play.color == koz and kozciktimi == 0 and (card_species > 1):
                    card_to_play = random.choice(self.cards)
                self.cards.remove(card_to_play)
                return card_to_play
            else:
                card_to_play = random.choice(self.cards)  # ilk game other cards
                if (cardsontable[0].color == 'kupa' and len(self.kupas) == 0) or (cardsontable[0].color == 'maça' and len(self.macas) == 0) or (cardsontable[0].color == 'sinek' and len(self.sineks) == 0) or (cardsontable[0].color == 'karo' and len(self.karos) == 0): # this means we dont have same club therefore we should play koz
                    if koz == 'maça':
                        if len(self.macas) > 0: # check if we have any koz
                            card_to_play = random.choice(self.macas)
                        else:
                            card_to_play = random.choice(self.cards) # if we dont have koz it doesnt matter we will lose anyways
                    elif koz == 'kupa':
                        if len(self.kupas) > 0: # check if we have any koz
                            card_to_play = random.choice(self.kupas)
                        else:
                            card_to_play = random.choice(self.cards) # if we dont have koz it doesnt matter we will lose anyways
                    elif koz == 'sinek':
                        if len(self.sineks) > 0: # check if we have any koz
                            card_to_play = random.choice(self.sineks)
                        else:
                            card_to_play = random.choice(self.cards) # if we dont have koz it doesnt matter we will lose anyways
                    elif koz == 'karo':
                        if len(self.karos) > 0: # check if we have any koz
                            card_to_play = random.choice(self.karos)
                        else:
                            card_to_play = random.choice(self.cards) # if we dont have koz it doesnt matter we will lose anyways
                else:
                    if cardsontable[0].color == 'kupa':
                        card_to_play = random.choice(self.kupas)
                    elif cardsontable[0].color == 'karo':
                        card_to_play = random.choice(self.karos)
                    elif cardsontable[0].color == 'maça':
                        card_to_play = random.choice(self.macas)
                    elif cardsontable[0].color == 'sinek':
                        card_to_play = random.choice(self.sineks)
                self.cards.remove(card_to_play)
                return card_to_play

    def bid(self):
        cardscores = [0, 0, 0, 0]
        cardlistkupa = []
        cardlistsinek = []
        cardlistmaca = []
        cardlistkaro = []
        chosenone = 'kupa'
        for card in self.cards:
            #print('player cards: '+card.color+' '+card.value)
            if card.color == 'kupa':
                cardlistkupa.append(card.value)
                cardscores[0] += card.cardvalue[card.value]
            elif card.color == 'sinek':
                cardlistsinek.append(card.value)
                cardscores[1] += card.cardvalue[card.value]
            elif card.color == 'karo':
                cardlistkaro.append(card.value)
                cardscores[2] += card.cardvalue[card.value]
            elif card.color == 'maça':
                cardlistmaca.append(card.value)
                cardscores[3] += card.cardvalue[card.value]
        if cardscores[0]==max(cardscores):
            chosenone = 'kupa'
        if cardscores[1]==max(cardscores):
            chosenone = 'sinek'
        if cardscores[2]==max(cardscores):
            chosenone = 'karo'
        if cardscores[3]==max(cardscores):
            chosenone = 'maça'

        return [round(max(cardscores)/10), chosenone]



class Game:
    colors = ['kupa', 'karo', 'sinek', 'maça']
    lastnames = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor',
                 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin', 'Thompson', 'Garcia', 'Martinez',
                 'Robinson', 'Clark', 'Rodriguez', 'Lewis', 'Lee', 'Walker', 'Collins', 'Edwards', 'Evans', 'PArker',
                 'Campbell', 'Philips', 'Turner', 'Roberts', 'Perez', 'Mitchell', 'Carter', 'Nelson', 'Gonzales',
                 'Richardson', 'Cox', 'Howard', 'Ward', 'Torres', 'Peterson', 'Gray', 'Ramirez', 'James', 'Watson',
                 'Brooks', 'Kelly', 'Sanders', 'Hughes', 'Flores', 'Washington', 'Butler', 'Simmons']
    firstnames = ['Emma', 'Olivia', 'Ava', 'Isabella', 'Sophia', 'Charlotte', 'Mia', 'Amelia', 'Harper', 'Evelyn',
                  'Abigail', 'Emily', 'Elizabeth', 'Sofia', 'Camila', 'Scarlett', 'Victoria', 'Liam', 'Noah', 'William',
                  'James', 'Oliver', 'Benjamin', 'Elijah', 'Lucas', 'Mason', 'Logan', 'Alexander', 'Ethan', 'Jacob',
                  'Michael', 'Trevor', 'CJ', 'Sebastian', 'Matthew', 'Samuel']
    values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    cardvalue = {'A': 20, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 12, 'J': 14, 'Q': 16,
                 'K': 18, '0': 0}

    def __init__(self):
        self.players = []
        self.currentpick = ''
        self.bidwinner = -1
        self.gamecount = 0
        self.kozciktimi = 0
        self.round = 0
        self.winner = -1
        self.roundwinner = -1
        self.turn = deque([0, 1, 2, 3])
        self.deck = [Card(value, color) for value in self.values for color in self.colors]
        random.shuffle(self.deck)
        self.playerss = self.partition(self.deck, 4)
        for self.parts in self.playerss:
            self.players.append(Player("".join(random.choice(self.firstnames)+" "+random.choice(self.lastnames)), self.parts))

    def partition(self, lst, n):
        division = len(lst) / n
        return [lst[round(division * i):round(division * (i + 1))] for i in range(n)]

    def bidding(self):
        bids = []
        bids.append(self.players[0].bid())
        max_bid = 0
        bids.append(self.players[1].bid())
        if bids[1][0]>bids[0][0]:
            max_bid=1
        bids.append(self.players[2].bid())
        if bids[2][0]>bids[max_bid][0]:
            max_bid=2
        bids.append(self.players[3].bid())
        if bids[3][0]>bids[max_bid][0]:
            max_bid=3
        self.currentpick=bids[max_bid][1]
        #print(bids)
        for num, bidd in enumerate(bids):
            print(str(bidd)+' '+self.players[num].name)
            self.players[num].print_player_cards()
        print('Koz: ' + str(bids[max_bid][1]))
        self.currentpick = str(bids[max_bid][1])
        self.bidwinner = max_bid
        self.turn.rotate(-1*max_bid)
        #print(self.turn[0])
        #print(max_bid)
        print('Kozu alan oyuncu : ' + self.players[max_bid].name)

    def gameround(self):
        cards_on_table = []
        self.round = self.round +1
        print("\nRound: " + str(self.round))
        self.roundwinner = -1
        self.winningcard = Card('0', '')
        for x in range(4):
            print("players card options are as follows: \n")
            print(self.players[self.turn[0]].list_playable_cards(cards_on_table, self.currentpick, self.kozciktimi, self.round, self.players[self.bidwinner]))
            print("\n----------")
            played_card = self.players[self.turn[0]].play_card(cards_on_table, self.currentpick, self.kozciktimi, self.round)
            if self.roundwinner == -1:
                self.roundwinner = self.turn[0]
                self.winningcard = played_card
            if self.roundwinner > -1:
                if played_card.color == self.winningcard.color and self.winningcard.color != self.currentpick:
                    if self.cardvalue[played_card.value] > self.cardvalue[self.winningcard.value]:
                        self.winningcard = played_card
                        self.roundwinner=self.turn[0]
                elif played_card.color == self.currentpick:
                    if self.winningcard.color != self.currentpick:
                        self.winningcard = played_card
                        self.roundwinner = self.turn[0]
                    else:
                        if self.cardvalue[played_card.value] > self.cardvalue[self.winningcard.value]:
                            self.winningcard = played_card
                            self.roundwinner = self.turn[0]

            if played_card.color == self.currentpick and self.kozciktimi == 0:
                self.kozciktimi = 1
            cards_on_table.append(played_card)
            print(self.players[self.turn[0]].name + " played: " + str(played_card.color) + str(played_card.value) )
            self.turn.rotate(-1)
        print("\n---\nCards played: ")
        for card in cards_on_table:
            print(card.value, card.color)
        print("Round winner: " + self.players[self.roundwinner].name)
        self.players[self.roundwinner].score += 1
        while self.players[self.roundwinner] != self.players[self.turn[0]]:
            self.turn.rotate(-1)


if __name__ == '__main__':

    mcts = mcts(timeLimit=1000)
    mygame = Game()
    mygame.bidding()
    for i in range(13):
        mygame.gameround()
        print(len(mygame.players[0].cards))


    #for cart in gamblers[0].cards:
    #    cart.print()

