from deck import Card

# Regole del Texas Hold'em Poker:

# 1. Setup del Gioco:
#    - Ogni giocatore riceve due carte coperte (hole cards).
#    - Cinque carte comuni vengono distribuite sul tavolo in tre fasi: il flop (tre carte), il turn (una carta) e il river (una carta).

# 2. Turni di Puntata:
#    - Pre-Flop: I giocatori ricevono le loro due carte coperte e iniziano il primo turno di puntata.
#    - Flop: Vengono distribuite tre carte comuni sul tavolo, seguite da un secondo turno di puntata.
#    - Turn: Viene distribuita una quarta carta comune, seguita da un terzo turno di puntata.
#    - River: Viene distribuita una quinta carta comune, seguita dall'ultimo turno di puntata.

# 3. Azioni di Puntata:
#    - Check: Passare il turno senza scommettere.
#    - Bet: Scommettere una certa quantità di chip.
#    - Call: Pareggiare la scommessa di un altro giocatore.
#    - Raise: Aumentare la scommessa.
#    - Fold: Abbandonare la mano.

# 4. Valutazione delle Mani:
#    - Coppia: Due carte dello stesso valore.
#    - Doppia Coppia: Due coppie di carte.
#    - Tris: Tre carte dello stesso valore.
#    - Scala: Cinque carte consecutive (ad esempio, 2-3-4-5-6).
#    - Colore: Cinque carte dello stesso seme.
#    - Full: Una coppia più un tris.
#    - Poker: Quattro carte dello stesso valore.
#    - Scala Colore: Scala dello stesso seme.
#    - Scala Reale: Scala dall'asso al dieci dello stesso seme.

# 5. Showdown:
#    - Dopo l'ultimo turno di puntata, i giocatori rimanenti mostrano le loro carte.
#    - Il giocatore con la migliore mano di cinque carte vince il piatto.


class PokerRules:
    def __init__(self):
        self.hand_rankings = self.define_hand_rankings()

    def define_hand_rankings(self):
        return {
            'royal_flush': 10,
            'straight_flush': 9,
            'four_of_a_kind': 8,
            'full_house': 7,
            'flush': 6,
            'straight': 5,
            'three_of_a_kind': 4,
            'two_pairs': 3,
            'pair': 2,
            'high_card': 1
        }

# Punti delle Mani nel Texas Hold'em Poker:
#    - Scala Colore (Straight Flush): 9 punti
#    - Poker (Four of a Kind): 8 punti
#    - Full (Full House): 7 punti
#    - Colore (Flush): 6 punti
#    - Scala (Straight): 5 punti
#    - Tris (Three of a Kind): 4 punti
#    - Doppia Coppia (Two Pairs): 3 punti
#    - Coppia (Pair): 2 punti


    def distribute_cards(self, deck):
        player_cards = deck[:2]
        opponent_cards = deck[2:4]
        return player_cards, opponent_cards

    def extract_values(self, hand):
        return [card.value for card in hand]

    def extract_suits(self, hand):
        return [card.suit for card in hand]

    def extract_indices(self, hand):
        card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        indices = [card_values.index(card.value) for card in hand]
        return sorted(indices)

    # Royal Flush
    def royal_flush(self, hand):
        card_values = ['10', 'J', 'Q', 'K', 'A']
        return self.straight_flush(hand) and all(card.value in card_values for card in hand)

    # Straight Flush
    def straight_flush(self, hand):
        return self.straight(hand) and self.flush(hand)

    # Four of a Kind
    def four_of_a_kind(self, hand):
        values = self.extract_values(hand)
        return any(values.count(value) == 4 for value in values)

    # Full House
    def full_house(self, hand):
        values = self.extract_values(hand)
        return self.three_of_a_kind(hand) and any(values.count(value) == 2 for value in values)

    # Flush
    def flush(self, hand):
        suits = self.extract_suits(hand)
        return len(set(suits)) == 1

    # Straight
    def straight(self, hand):
        indices = self.extract_indices(hand)
        return indices == list(range(indices[0], indices[0] + 5)) or indices == [0, 1, 2, 3, 12]

    # Three of a Kind
    def three_of_a_kind(self, hand):
        values = self.extract_values(hand)
        return any(values.count(value) == 3 for value in values)

    # Two Pairs
    def two_pairs(self, hand):
        values = self.extract_values(hand)
        pairs = [value for value in set(values) if values.count(value) == 2]
        return len(pairs) == 2

    # Pair
    def pair(self, hand):
        values = self.extract_values(hand)
        return any(values.count(value) == 2 for value in values)

    # Determine the winner
    def determine_winner(self, player_hand, opponent_hand):
        player_ranking = self.calculate_hand_ranking(player_hand)
        opponent_ranking = self.calculate_hand_ranking(opponent_hand)
        return self.compare_hand_rankings(player_ranking, opponent_ranking)

    def calculate_hand_ranking(self, hand):
        for ranking, points in self.hand_rankings.items():
            if getattr(self, ranking)(hand):
                return points
        return self.hand_rankings['high_card']

    def compare_hand_rankings(self, player_ranking, opponent_ranking):
        if player_ranking > opponent_ranking:
            return "Player wins!"
        elif opponent_ranking > player_ranking:
            return "Dealer wins!"
        else:
            return "It's a tie!"