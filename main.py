import random
from collections import deque
from copy import copy, deepcopy

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
    mygame = Game()
    mygame.bidding()
    for i in range(13):
        mygame.gameround()
        #print(len(mygame.players[0].cards))
    for i in range(4):
        print(mygame.players[i].name +' '+ str(mygame.players[i].score))


