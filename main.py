from game import Game
from player import Player
from deck import Deck

if __name__ == '__main__':
    mydeck = Deck()
    mydeck.shuffle()
    players = []
    players.append(Player('Player 1', True, mydeck.deal(13)))
    players.append(Player('Player 2', True, mydeck.deal(13)))
    players.append(Player('Player 3', True, mydeck.deal(13)))
    players.append(Player('Player 4', True, mydeck.deal(13)))
    mygame = Game(players)
    mygame.bidding()
    for i in range(13):
        mygame.gameround()
    for i in range(4):
        print(players[i].name +' '+ str(players[i].score))


