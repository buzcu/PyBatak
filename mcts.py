# === mcts.py ===
import copy
import random
import math
from card import Card

class MCTSNode:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.wins = 0

    # Expand node by generating all valid child states
    def expand(self):
        if self.children:
            return
        valid_moves = self.state.get_valid_moves()
        for move in valid_moves:
            next_state = self.state.simulate_move(move)
            self.children.append(MCTSNode(next_state, parent=self, move=move))

    # Select the best child using UCB1 formula
    def best_child(self, exploration=1.41):
        best_score = float('-inf')
        best = None
        for child in self.children:
            if child.visits == 0:
                return child  # Prefer unexplored nodes
            exploit = child.wins / child.visits
            explore = exploration * math.sqrt(math.log(self.visits) / child.visits)
            score = exploit + explore
            if score > best_score:
                best_score = score
                best = child
        return best

# Representation of a game state for MCTS
class GameState:
    def __init__(self, hand, table, lead_suit, trump_suit, known_cards=None, player_index=0, tricks_won=None):
        self.hand = hand  # Current player's hand
        self.table = table  # Cards played in current trick
        self.lead_suit = lead_suit
        self.trump_suit = trump_suit
        self.known_cards = known_cards if known_cards is not None else list(hand) + [card for card, _ in table]
        self.player_index = player_index
        self.tricks_won = tricks_won if tricks_won is not None else [0, 0, 0, 0]

    # Return list of valid cards that can be played
    def get_valid_moves(self):
        valid = [c for c in self.hand if c.suit == self.lead_suit]
        return valid if valid else self.hand

    # Return a new GameState after playing a given card
    def simulate_move(self, move):
        new_hand = [card for card in self.hand if card != move]
        new_table = self.table + [(move, self.player_index)]
        new_known = list(self.known_cards) + [move]
        next_player = (self.player_index + 1) % 4
        return GameState(new_hand, new_table, self.lead_suit or move.suit, self.trump_suit, new_known, next_player, list(self.tricks_won))

    # Simulate random playout from current state to the end of the game
    def simulate_random_playout(self):
        hands = {self.player_index: list(self.hand)}
        used_cards = set(self.hand)
        known_cards = list(self.known_cards)
        full_table = list(self.table)

        # Construct full deck and determine unknown cards
        all_cards = [Card(suit, rank) for suit in ['S', 'H', 'D', 'C'] for rank in range(2, 15)]
        unknown_cards = [c for c in all_cards if c not in used_cards and c not in known_cards and c not in [card for card, _ in self.table]]
        random.shuffle(unknown_cards)

        # Assign unknown cards to other players
        for i in range(4):
            if i != self.player_index:
                hands[i] = [unknown_cards.pop() for _ in range(len(self.hand))]

        tricks_won = list(self.tricks_won)
        table = list(full_table)
        starting_player = self.player_index

        # Simulate tricks until all cards are played
        while hands[self.player_index]:
            while len(table) < 4:
                player = (starting_player + len(table)) % 4
                if table:
                    lead_suit = table[0][0].suit
                else:
                    lead_suit = None
                valid_cards = [c for c in hands[player] if lead_suit and c.suit == lead_suit]
                valid_cards = [c for c in hands[player] if lead_suit and c.suit == lead_suit]
                if not valid_cards:
                    valid_cards = hands[player]

                if not valid_cards:
                    # This should not happen, but if it does, break out of the loop to avoid crash
                    print(f"No valid cards for player {player}. Ending trick.")
                    break

                card = random.choice(valid_cards)
                
                table.append((card, player))
                hands[player].remove(card)

            # Determine winner of trick
            trump_cards = [entry for entry in table if entry[0].suit == self.trump_suit]
            if trump_cards:
                winner = max(trump_cards, key=lambda x: x[0].rank)[1]
            else:
                lead_suit = table[0][0].suit if table else None
                if lead_suit is None:
                    print("No lead suit found!!.")
                    
                lead_suit_cards = [entry for entry in table if entry[0].suit == lead_suit]
                winner = max(lead_suit_cards, key=lambda x: x[0].rank)[1]

            tricks_won[winner] += 1
            starting_player = winner
            table = []

        # Return result based on player's trick count
        return 1 if tricks_won[self.player_index] > max(t for i, t in enumerate(tricks_won) if i != self.player_index) else 0

# Main MCTS class to run simulations
class MCTS:
    def __init__(self, root_state, iterations=100):
        self.root = MCTSNode(root_state)
        self.iterations = iterations

    # Run simulations and return best move found
    def search(self):
        for _ in range(self.iterations):
            node = self.root

            # Selection
            while node.children:
                next_node = node.best_child()
                if next_node is None:
                    break
                node = next_node

            # Expansion
            node.expand()

            # Simulation
            if not node.children:
                result = node.state.simulate_random_playout()
            else:
                result = node.children[0].state.simulate_random_playout()

            # Backpropagation
            self.backpropagate(node, result)

        best_move = max(self.root.children, key=lambda child: child.visits).move
        return best_move

    # Update stats for visited nodes
    def backpropagate(self, node, result):
        while node:
            node.visits += 1
            node.wins += result
            node = node.parent