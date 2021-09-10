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
        if self.color=='heart':
            print('''
 _____
|'''+self.value+'''_ _ |
|( v )|
| \ / |
|  .  |
|____'''+'♥'+'''|
''')
        elif self.color=='club':
            print("""
 _____
|"""+self.value+""" _  |
| ( ) |
|(_'_)|
|  |  |
|____"""+'♣'+"""|""")
        elif self.color=='diamond':
            print("""
 _____
|"""+self.value+""" ^  |
| / \ |
| \ / |
|  .  |
|____"""+'♦'+"""|
""")
        elif self.color=='spade':
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
        self.hearts = []
        self.diamonds = []
        self.clubs = []
        self.spades = []

    def __init__(self, name, cardss):
        self.name = name
        self.cards = cardss
        self.woncards = []
        self.score = 0
        self.hearts = []
        self.diamonds = []
        self.clubs = []
        self.spades = []

    def get_card_value(self, card):
        return self.cardvalue[card.value]

    def print_player_cards(self):
        self.order_cards()
        for number, card in enumerate(self.hearts):
            print(card)
        for number, card in enumerate(self.spades):
            print(card)
        for number, card in enumerate(self.diamonds):
            print(card)
        for number, card in enumerate(self.clubs):
            print(card)

    def order_cards(self):
        self.cards.sort(key=self.get_card_value)
        self.hearts = []
        self.diamonds = []
        self.clubs = []
        self.spades = []
        for card in self.cards:
            if card.color == 'heart':
                self.hearts.append(card)
            elif card.color == 'spade':
                self.spades.append(card)
            elif card.color == 'diamond':
                self.diamonds.append(card)
            else:
                self.clubs.append(card)
        self.hearts.sort(key=self.get_card_value)
        self.spades.sort(key=self.get_card_value)
        self.diamonds.sort(key=self.get_card_value)
        self.clubs.sort(key=self.get_card_value)

    def list_playable_cards(self, cards_on_table, trump, is_trump_enabled, round, bidwinner):
        #temp_playa = Player()
        temp_playa = deepcopy(self)
        temp_list = []
        #for cards in range(len(temp_playa.cards)):
        #    temp_list.append(temp_playa.play_card(cardsontable, koz, kozciktimi, round))
        for cards in self.cards:
            if self.is_play_legal(cards, cards_on_table, trump, is_trump_enabled, bidwinner) == True:
                temp_list.append(cards)
        return temp_list

    def is_play_legal(self, card, cards_on_table, trump, is_trump_enabled, bidwinner):
        player_trump_card_number = 0
        if trump == "heart":
            player_trump_card_number = len(self.hearts)
        elif trump == "spade":
            player_trump_card_number = len(self.spades)
        elif trump == "diamond":
            player_trump_card_number = len(self.diamonds)
        elif trump == "club":
            player_trump_card_number = len(self.clubs)

        player_main_color_count = 0
        if len(cards_on_table) > 0:
            main_color = cards_on_table[0].color
            if main_color == "heart":
                player_main_color_count = len(self.hearts)
            elif main_color == "spade":
                player_main_color_count = len(self.spades)
            elif main_color == "diamond":
                player_main_color_count = len(self.diamonds)
            elif main_color == "club":
                player_main_color_count = len(self.clubs)

        if len(cards_on_table) == 0:
            if is_trump_enabled == 1 or (is_trump_enabled == 0 and card.color != trump):
                return True
        elif cards_on_table[0].color == card.color and self.get_card_value(cards_on_table[len(cards_on_table) - 1]) < self.get_card_value(card):
            return True
        elif cards_on_table[0].color == card.color and self.get_card_value(cards_on_table[len(cards_on_table) - 1]) > self.get_card_value(card):
            if cards_on_table[0].color == "heart":
                for cardd in self.hearts:
                    if self.get_card_value(cardd)>self.get_card_value(cards_on_table[len(cards_on_table) - 1]):
                        return False
                return True
            elif cards_on_table[0].color == "spade":
                for cardd in self.spades:
                    if self.get_card_value(cardd) > self.get_card_value(cards_on_table[len(cards_on_table) - 1]):
                        return False
                return True
            elif cards_on_table[0].color == "diamond":
                for cardd in self.diamonds:
                    if self.get_card_value(cardd) > self.get_card_value(cards_on_table[len(cards_on_table) - 1]):
                        return False
                return True
            elif cards_on_table[0].color == "club":
                for cardd in self.clubs:
                    if self.get_card_value(cardd) > self.get_card_value(cards_on_table[len(cards_on_table) - 1]):
                        return False
                return True
        elif player_main_color_count == 0 and (card.color == trump or player_trump_card_number == 0):
            return True
        return False

    def play_card(self, cardsontable, trump, is_trump_enabled, round):
        self.order_cards()
        if round == 0:
            if len(cardsontable) == 0:  # first game first card
                card_to_play = random.choice(self.cards)  # this means we are first to play
                while card_to_play.color == trump:
                    card_to_play = random.choice(self.cards)
                self.cards.remove(card_to_play)
                return card_to_play
            else:
                if (cardsontable[0].color == 'heart' and len(self.hearts) == 0) or (cardsontable[0].color == 'spade' and len(self.spades) == 0) or (cardsontable[0].color == 'club' and len(self.clubs) == 0) or (cardsontable[0].color == 'diamond' and len(self.diamonds) == 0): # this means we dont have same suit therefore we should play trump
                    if trump == 'spade':
                        if len(self.spades) > 0: # check if we have any trump
                            options = self.spades
                            for playable_cards in self.spades:
                                 for played_card in cardsontable:
                                     if played_card.value > playable_cards.value and played_card.color == self.get_card_value(playable_cards):
                                         options.remove(playable_cards) # if any of the played cards are higher rank then we must play higher rank if possible
                            if len(options) == 0:
                                options.append(self.spades[0])
                            card_to_play = options[0]
                        else:
                            card_to_play = self.cards[0] # if we dont have koz it doesnt matter we will lose anyways so use smallest possible card
                    elif trump == 'heart':
                        if len(self.hearts) > 0: # check if we have any trump
                            card_to_play = random.choice(self.hearts) #todo: fix ramdom choice implement an algorithm
                        else:
                            card_to_play =self.cards[0] # if we dont have trump it doesnt matter we will lose anyways
                    elif trump == 'club':
                        if len(self.clubs) > 0: # check if we have any trump
                            card_to_play = random.choice(self.clubs)
                        else:
                            card_to_play = self.cards[0] # if we dont have trump it doesnt matter we will lose anyways
                    elif trump == 'diamond':
                        if len(self.diamonds) > 0: # check if we have any trump
                            card_to_play = random.choice(self.diamonds)
                        else:
                            card_to_play = self.cards[0] # if we dont have trump it doesnt matter we will lose anyways
                else:
                    if cardsontable[0].color == 'heart':

                        card_to_play = random.choice(self.hearts)
                    elif cardsontable[0].color == 'diamond':
                        card_to_play = random.choice(self.diamonds)
                    elif cardsontable[0].color == 'spade':
                        card_to_play = random.choice(self.spades)
                    elif cardsontable[0].color == 'club':
                        card_to_play = random.choice(self.clubs)
                self.cards.remove(card_to_play)
                return card_to_play
        else:
            if len(cardsontable) == 0:#nth game first card
                card_to_play = random.choice(self.cards)#this means we are first to play
                card_suits = 0
                if len(self.spades) > 0:
                    card_suits = card_suits+1
                if len(self.hearts) > 0:
                    card_suits = card_suits+1
                if len(self.diamonds) > 0:
                    card_suits = card_suits+1
                if len(self.clubs) > 0:
                    card_suits = card_suits+1
                while card_to_play.color == trump and is_trump_enabled == 0 and (card_suits > 1):
                    card_to_play = random.choice(self.cards)
                self.cards.remove(card_to_play)
                return card_to_play
            else:
                card_to_play = random.choice(self.cards)  # first game round, not first card
                if (cardsontable[0].color == 'heart' and len(self.hearts) == 0) or (cardsontable[0].color == 'spade' and len(self.spades) == 0) or (cardsontable[0].color == 'club' and len(self.clubs) == 0) or (cardsontable[0].color == 'diamond' and len(self.diamonds) == 0): # this means we dont have same suit therefore we should play trump
                    if trump == 'spade':
                        if len(self.spades) > 0: # check if we have any trump
                            card_to_play = random.choice(self.spades)
                        else:
                            card_to_play = random.choice(self.cards) # if we dont have trump it doesnt matter we will lose anyways
                    elif trump == 'heart':
                        if len(self.hearts) > 0: # check if we have any trump
                            card_to_play = random.choice(self.hearts)
                        else:
                            card_to_play = random.choice(self.cards) # if we dont have trump it doesnt matter we will lose anyways
                    elif trump == 'club':
                        if len(self.clubs) > 0: # check if we have any trump
                            card_to_play = random.choice(self.clubs)
                        else:
                            card_to_play = random.choice(self.cards) # if we dont have trump it doesnt matter we will lose anyways
                    elif trump == 'diamond':
                        if len(self.diamonds) > 0: # check if we have any trump
                            card_to_play = random.choice(self.diamonds)
                        else:
                            card_to_play = random.choice(self.cards) # if we dont have trump it doesnt matter we will lose anyways
                else:
                    if cardsontable[0].color == 'heart':
                        card_to_play = random.choice(self.hearts)
                    elif cardsontable[0].color == 'diamond':
                        card_to_play = random.choice(self.diamonds)
                    elif cardsontable[0].color == 'spade':
                        card_to_play = random.choice(self.spades)
                    elif cardsontable[0].color == 'club':
                        card_to_play = random.choice(self.clubs)
                self.cards.remove(card_to_play)
                return card_to_play

    def bid(self):
        cardscores = [0, 0, 0, 0]
        card_list_hearts = []
        card_list_clubs = []
        card_list_spades = []
        card_list_diamonds = []
        chosen_one = 'heart'
        for card in self.cards:
            #print('player cards: '+card.color+' '+card.value)
            if card.color == 'heart':
                card_list_hearts.append(card.value)
                cardscores[0] += card.cardvalue[card.value]
            elif card.color == 'club':
                card_list_clubs.append(card.value)
                cardscores[1] += card.cardvalue[card.value]
            elif card.color == 'diamond':
                card_list_diamonds.append(card.value)
                cardscores[2] += card.cardvalue[card.value]
            elif card.color == 'spade':
                card_list_spades.append(card.value)
                cardscores[3] += card.cardvalue[card.value]
        if cardscores[0]==max(cardscores):
            chosen_one = 'heart'
        if cardscores[1]==max(cardscores):
            chosen_one = 'club'
        if cardscores[2]==max(cardscores):
            chosen_one = 'diamond'
        if cardscores[3]==max(cardscores):
            chosen_one = 'spade'

        return [round(max(cardscores)/10), chosen_one]


class Human(Player):
    cardvalue = {'A': 20, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 12, 'J': 14, 'Q': 16,
                 'K': 18, '0': 0}

    def __init__(self):
        super().__init__()
        self.name = input('Name: ')

    def __init__(self, name, cardss):
        super(Human, self).__init__(name, cardss)
        self.name = input('Name: ')

    def get_card_value(self, card):
        return self.cardvalue[card.value]

    def print_player_cards(self):
        self.order_cards()
        for number, card in enumerate(self.hearts):
            print(card)
        for number, card in enumerate(self.spades):
            print(card)
        for number, card in enumerate(self.diamonds):
            print(card)
        for number, card in enumerate(self.clubs):
            print(card)

    def order_cards(self):
        self.cards.sort(key=self.get_card_value)
        self.hearts = []
        self.diamonds = []
        self.clubs = []
        self.spades = []
        for card in self.cards:
            if card.color == 'heart':
                self.hearts.append(card)
            elif card.color == 'spade':
                self.spades.append(card)
            elif card.color == 'diamond':
                self.diamonds.append(card)
            else:
                self.clubs.append(card)
        self.hearts.sort(key=self.get_card_value)
        self.spades.sort(key=self.get_card_value)
        self.diamonds.sort(key=self.get_card_value)
        self.clubs.sort(key=self.get_card_value)

    def list_playable_cards(self, cards_on_table, trump, is_trump_enabled, round, bidwinner):
        # temp_playa = Player()
        temp_playa = deepcopy(self)
        temp_list = []
        # for cards in range(len(temp_playa.cards)):
        #    temp_list.append(temp_playa.play_card(cardsontable, koz, kozciktimi, round))
        for cards in self.cards:
            if self.is_play_legal(cards, cards_on_table, trump, is_trump_enabled, bidwinner) == True:
                temp_list.append(cards)
        return temp_list

    def is_play_legal(self, card, cards_on_table, trump, is_trump_enabled, bidwinner):
        player_trump_card_number = 0
        if trump == "heart":
            player_trump_card_number = len(self.hearts)
        elif trump == "spade":
            player_trump_card_number = len(self.spades)
        elif trump == "diamond":
            player_trump_card_number = len(self.diamonds)
        elif trump == "club":
            player_trump_card_number = len(self.clubs)

        player_main_color_count = 0
        if len(cards_on_table) > 0:
            main_color = cards_on_table[0].color
            if main_color == "heart":
                player_main_color_count = len(self.hearts)
            elif main_color == "spade":
                player_main_color_count = len(self.spades)
            elif main_color == "diamond":
                player_main_color_count = len(self.diamonds)
            elif main_color == "club":
                player_main_color_count = len(self.clubs)

        if len(cards_on_table) == 0:
            if is_trump_enabled == 1 or (is_trump_enabled == 0 and card.color != trump):
                return True
        elif cards_on_table[0].color == card.color and self.get_card_value(
                cards_on_table[len(cards_on_table) - 1]) < self.get_card_value(card):
            return True
        elif cards_on_table[0].color == card.color and self.get_card_value(
                cards_on_table[len(cards_on_table) - 1]) > self.get_card_value(card):
            if cards_on_table[0].color == "heart":
                for cardd in self.hearts:
                    if self.get_card_value(cardd) > self.get_card_value(cards_on_table[len(cards_on_table) - 1]):
                        return False
                return True
            elif cards_on_table[0].color == "spade":
                for cardd in self.spades:
                    if self.get_card_value(cardd) > self.get_card_value(cards_on_table[len(cards_on_table) - 1]):
                        return False
                return True
            elif cards_on_table[0].color == "diamond":
                for cardd in self.diamonds:
                    if self.get_card_value(cardd) > self.get_card_value(cards_on_table[len(cards_on_table) - 1]):
                        return False
                return True
            elif cards_on_table[0].color == "club":
                for cardd in self.clubs:
                    if self.get_card_value(cardd) > self.get_card_value(cards_on_table[len(cards_on_table) - 1]):
                        return False
                return True
        elif player_main_color_count == 0 and (card.color == trump or player_trump_card_number == 0):
            return True
        return False

    def play_card(self, cards_on_table, trump, is_trump_enabled, round):
        self.order_cards()
        print('Cards on table:')
        for card in cards_on_table:
            print(card)
        print('\nYour cards:')
        self.print_player_cards()
        serie = int(input('\nKupa -> 1\nSinek -> 2\nKaro -> 3\nMaca -> 4\nChosen card serie (1-4): '))
        print('\n')
        if serie == 1:
            chosen_one = 'heart'
            for i, cards in enumerate(self.hearts):
                print(str(i) +' -> ' + str(cards))
            chosen_card = int(input('\nChosen card: '))
            return self.hearts[chosen_card]
        elif serie == 2:
            chosen_one = 'club'
            for i, cards in enumerate(self.clubs):
                print(str(i) +' -> ' + str(cards))
            chosen_card = int(input('\nChosen card: '))
            return self.clubs[chosen_card]
        elif serie == 3:
            chosen_one = 'diamond'
            for i, cards in enumerate(self.diamonds):
                print(str(i) +' -> ' + str(cards))
            chosen_card = int(input('\nChosen card: '))
            return self.diamonds[chosen_card]
        elif serie == 4:
            chosen_one = 'spade'
            for i, cards in enumerate(self.spades):
                print(str(i) +' -> ' + str(cards))
            chosen_card = int(input('\nChosen card: '))
            return self.spades[chosen_card]
        return self.cards[0]

    def bid(self):
        cardscores = [0, 0, 0, 0]
        card_list_hearts = []
        card_list_clubs = []
        card_list_spades = []
        card_list_diamonds = []
        chosen_suit = 'heart'

        for card in self.cards:
            #print('player cards: '+card.color+' '+card.value)
            if card.color == 'heart':
                card_list_hearts.append(card.value)
                cardscores[0] += card.cardvalue[card.value]
            elif card.color == 'club':
                card_list_clubs.append(card.value)
                cardscores[1] += card.cardvalue[card.value]
            elif card.color == 'diamond':
                card_list_diamonds.append(card.value)
                cardscores[2] += card.cardvalue[card.value]
            elif card.color == 'spade':
                card_list_spades.append(card.value)
                cardscores[3] += card.cardvalue[card.value]
        self.print_player_cards()
        print('\nHearts point total: ' + str(cardscores[0]))
        print('\nClubs point total: ' + str(cardscores[1]))
        print('\nDiamonds point total: ' + str(cardscores[2]))
        print('\nSpades point total: ' + str(cardscores[3]))
        bid_value = int(input('Bid: '))
        bid_type = int(input('\nHeart -> 1\nClub -> 2\nDiamond -> 3\nSpade -> 4\nChosen card suit (1-4): '))
        if bid_type == 1:
            chosen_suit = 'heart'
        elif bid_type == 2:
            chosen_suit = 'club'
        elif bid_type == 3:
            chosen_suit = 'diamond'
        elif bid_type == 4:
            chosen_suit = 'spade'
        else:
            print('You have entered invalid answer. you will have heart as default chosen card suit.')

        return [bid_value, chosen_suit]


class Game:
    colors = ['heart', 'diamond', 'club', 'spade']
    lastnames = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor',
                 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin', 'Thompson', 'Garcia', 'Martinez',
                 'Robinson', 'Clark', 'Rodriguez', 'Lewis', 'Lee', 'Walker', 'Collins', 'Edwards', 'Evans', 'Parker',
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
        self.is_trump_enabled = 0
        self.round = 0
        self.winner = -1
        self.roundwinner = -1
        self.turn = deque([0, 1, 2, 3])
        self.deck = [Card(value, color) for value in self.values for color in self.colors]
        random.shuffle(self.deck)
        self.playerss = self.partition(self.deck, 4)
        for player_number, self.parts in enumerate(self.playerss):
            # 3 ai player classes and 1 human class
            if player_number < 3:
                self.players.append(Player("".join(random.choice(self.firstnames)+" "+random.choice(self.lastnames)), self.parts))
            else:
                self.players.append(
                    Human("".join(random.choice(self.firstnames) + " " + random.choice(self.lastnames)), self.parts))

    def partition(self, lst, n):
        division = len(lst) / n
        return [lst[round(division * i):round(division * (i + 1))] for i in range(n)]

    def bidding(self):
        bids = []
        bids.append(self.players[0].bid())
        max_bid = 0
        bids.append(self.players[1].bid())
        if bids[1][0] > bids[0][0]:
            max_bid = 1
        bids.append(self.players[2].bid())
        if bids[2][0] > bids[max_bid][0]:
            max_bid = 2
        bids.append(self.players[3].bid())
        if bids[3][0] > bids[max_bid][0]:
            max_bid = 3
        self.currentpick=bids[max_bid][1]
        # print(bids)
        for num, bidd in enumerate(bids):
            print(str(bidd)+' '+self.players[num].name)
            self.players[num].print_player_cards()
        print('Trump: ' + str(bids[max_bid][1]))
        self.currentpick = str(bids[max_bid][1])
        self.bidwinner = max_bid
        self.turn.rotate(-1*max_bid)
        #print(self.turn[0])
        #print(max_bid)
        print('Player who determined the trump: ' + self.players[max_bid].name)

    def gameround(self):
        cards_on_table = []
        self.round = self.round +1
        print("\nRound: " + str(self.round))
        self.roundwinner = -1
        self.winningcard = Card('0', '')
        for x in range(4):
            print("players card options are as follows: \n")
            self.players[self.turn[0]].print_player_cards()
            #print(self.players[self.turn[0]].list_playable_cards(cards_on_table, self.currentpick, self.is_trump_enabled, self.round, self.players[self.bidwinner]))
            print("\n----------")
            played_card = self.players[self.turn[0]].play_card(cards_on_table, self.currentpick, self.is_trump_enabled, self.round)
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

            if played_card.color == self.currentpick and self.is_trump_enabled == 0:
                self.is_trump_enabled = 1
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
        #print(len(mygame.players[0].cards))
    for i in range(4):
        print(mygame.players[i].name +' '+ str(mygame.players[i].score))


    #for cart in gamblers[0].cards:
    #    cart.print()

