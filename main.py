import random
from collections import deque

class Card:
    cardvalue = {'A': 20, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 12, 'J': 14, 'Q': 16, 'K': 18}

    def __init__(self, value, color):
        self.value = value
        self.color = color
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

    def __init__(self):
        self.name = ''
        self.cards = []
        self.woncards = []
        self.score = 0

    def __init__(self, name, cardss):
        self.name = name
        self.cards = cardss
        self.woncards = []
        self.score = 0

    def play_card(self, cardsontable, koz, round):
        if round == 0:
            if len(cardsontable) == 0:#ilk el ilk oyun
                card_to_play = random.choice(self.cards)#this means we are first to play
                self.cards.remove(card_to_play)
                return card_to_play
        else:
            card_to_play = random.choice(self.cards)  # this means we are first to play
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
        #print('Kupa :')
        #print(cardlistkupa)
        #print('Sinek :')
        #print(cardlistsinek)
        #print('Karo :')
        #print(cardlistkaro)
        #print('Maça :')
        #print(cardlistmaca)
        #print('score for kupa:' + str(cardscores[0]))
        #print('score for sinek:' + str(cardscores[1]))
        #print('score for karo:' + str(cardscores[2]))
        #print('score for maça:' + str(cardscores[3]))

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

    def __init__(self):
        self.players = []
        self.currentpick = ''
        self.bidwinner = -1
        self.gamecount = 0
        self.kozciktimi = 0
        self.round = 0
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
        print(bids)
        print('Koz: ' + str(bids[max_bid][1]))
        self.currentpick = str(bids[max_bid][1])
        self.bidwinner = max_bid
        self.turn.rotate(-1*max_bid)
        print(self.turn[0])
        print(max_bid)
        print('Kozu alan oyuncu : ' + self.players[max_bid].name)

    def gameround(self):
        cards_on_table = []
        for x in range(4):
            played_card = self.players[self.turn[0]].play_card(cards_on_table, self.kozciktimi, self.round)
            print(type(played_card))
            if played_card.color == self.currentpick and self.kozciktimi == 0:
                self.kozciktimi = 1
            cards_on_table.append(played_card)
            print(self.players[self.turn[0]].name + " played: " + str(played_card.color) + str(played_card.value) )
            self.turn.rotate(-1)
        print("\n---\nCards played: ")
        for card in cards_on_table:
            print(card.value, card.color)



if __name__ == '__main__':

    mygame = Game()
    for player in mygame.players:
        print(player.name)
        print(len(player.cards))
        print(len(player.woncards))
        player.bid()
        print('\n--------------\n')

    mygame.bidding()
    mygame.gameround()
    print(len(mygame.players[0].cards))
    #for cart in gamblers[0].cards:
    #    cart.print()

