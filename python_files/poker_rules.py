from itertools import combinations
from deck import Card

#Regole del Texas Hold'em Poker:

## 1. Setup del Gioco:
#- Ogni giocatore riceve due carte coperte (hole cards).
#- Cinque carte comuni vengono distribuite sul tavolo in tre fasi: il flop (tre carte), il turn (una carta) e il river (una carta).

## 2. Turni di Puntata:
#- **Pre-Flop**: I giocatori ricevono le loro due carte coperte e iniziano il primo turno di puntata.
#- **Flop**: Vengono distribuite tre carte comuni sul tavolo, seguite da un secondo turno di puntata.
#- **Turn**: Viene distribuita una quarta carta comune, seguita da un terzo turno di puntata.
#- **River**: Viene distribuita una quinta carta comune, seguita dall'ultimo turno di puntata.

## 3. Azioni di Puntata:
#- **Check**: Passare il turno senza scommettere.
#- **Bet**: Scommettere una certa quantità di chip.
#- **Call**: Pareggiare la scommessa di un altro giocatore.
#- **Raise**: Aumentare la scommessa.
#- **Fold**: Abbandonare la mano.

## 4. Valutazione delle Mani:
#- **Coppia**: Due carte dello stesso valore.
#- **Doppia Coppia**: Due coppie di carte.
#- **Tris**: Tre carte dello stesso valore.
#- **Scala**: Cinque carte consecutive (ad esempio, 2-3-4-5-6).
#- **Colore**: Cinque carte dello stesso seme.
#- **Full**: Una coppia più un tris.
#- **Poker**: Quattro carte dello stesso valore.
#- **Scala Colore**: Scala dello stesso seme.
#- **Scala Reale**: Scala dall'asso al dieci dello stesso seme.

## 5. Showdown:
#- Dopo l'ultimo turno di puntata, i giocatori rimanenti mostrano le loro carte.
#- Il giocatore con la migliore mano di cinque carte vince il piatto.


class PokerRules:
    def __init__(self):
        self.hand_rankings = self.define_hand_rankings()

    # Punti delle Mani nel Texas Hold'em Poker:
    def define_hand_rankings(self):
        return {
            'royal_flush': 10,  # Scala reale (Royal Flush)
            'straight_flush': 9,  # Scala colore (Straight Flush)
            'four_of_a_kind': 8,  # Poker (Four of a Kind)
            'full_house': 7,  # Full (Full House)
            'flush': 6,  # Colore (Flush)
            'straight': 5,  # Scala (Straight)
            'three_of_a_kind': 4,  # Tris (Three of a Kind)
            'two_pairs': 3,  # Doppia coppia (Two Pairs)
            'pair': 2,  # Coppia (Pair)
            'high_card': 1  # Carta alta (High Card)
        }

    def distribute_cards(self, deck, num_players=2):
        hands = []
        for i in range(num_players):
            start_index = i * 2
            end_index = (i + 1) * 2
            hand = deck[start_index:end_index]
            hands.append(hand)
        return hands

    def extract_values(self, hand):
        values = []
        for card in hand:
            values.append(card.value)
        return values

    def extract_suits(self, hand):
        suits = []
        for card in hand:
            suits.append(card.suit)
        return suits

    def extract_indices(self, hand):
        card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        indices = []
        for card in hand:
            index = card_values.index(card.value)
            indices.append(index)
        return sorted(indices)

    def royal_flush(self, hand):
        # Scala reale (Royal Flush): Scala colore con 10, J, Q, K, A
        card_values = ['10', 'J', 'Q', 'K', 'A']
        return self.straight_flush(hand) and all(card.value in card_values for card in hand)

    def straight_flush(self, hand):
        # Scala colore (Straight Flush): Scala con tutte le carte dello stesso seme
        return self.straight(hand) and self.flush(hand)

    def four_of_a_kind(self, hand):
        # Poker (Four of a Kind): Quattro carte dello stesso valore
        values = self.extract_values(hand)
        for value in values:
            if values.count(value) == 4:
                return True
        return False

    def full_house(self, hand):
        # Full (Full House): Tris e Coppia
        values = self.extract_values(hand)
        three_of_a_kind = self.three_of_a_kind(hand)
        two_of_a_kind = any(values.count(value) == 2 for value in values)
        return three_of_a_kind and two_of_a_kind

    def flush(self, hand):
        # Colore (Flush): Cinque carte dello stesso seme
        suits = self.extract_suits(hand)
        return len(set(suits)) == 1

    def straight(self, hand):
        # Scala (Straight): Cinque carte in sequenza
        indices = self.extract_indices(hand)
        return indices == list(range(indices[0], indices[0] + 5)) or indices == [0, 1, 2, 3, 12]

    def three_of_a_kind(self, hand):
        # Tris (Three of a Kind): Tre carte dello stesso valore
        values = self.extract_values(hand)
        for value in values:
            if values.count(value) == 3:
                return True
        return False

    def two_pairs(self, hand):
        # Doppia coppia (Two Pairs): Due coppie di carte dello stesso valore
        values = self.extract_values(hand)
        pairs = []
        for value in set(values):
            if values.count(value) == 2:
                pairs.append(value)
        return len(pairs) == 2

    def pair(self, hand):
        # Coppia (Pair): Due carte dello stesso valore
        values = self.extract_values(hand)
        for value in values:
            if values.count(value) == 2:
                return True
        return False

    def determine_winner(self, player_hand, opponent_hand, community_cards, player_name="Giocatore", opponent_name="Bot1"):
        player_best_hand = self.get_best_hand(player_hand + community_cards)
        opponent_best_hand = self.get_best_hand(opponent_hand + community_cards)
        player_ranking = self.calculate_hand_ranking(player_best_hand)
        opponent_ranking = self.calculate_hand_ranking(opponent_best_hand)
        
        result = self.compare_hand_rankings(player_ranking, opponent_ranking)
        player_hand_name = self.hand_name(player_best_hand)
        opponent_hand_name = self.hand_name(opponent_best_hand)
        
        if result == "win":
            return f"{player_name} wins with {player_hand_name} worth {player_ranking} points against {opponent_name}'s {opponent_hand_name} worth {opponent_ranking} points!"
        elif result == "lose":
            return f"{opponent_name} wins with {opponent_hand_name} worth {opponent_ranking} points against {player_name}'s {player_hand_name} worth {player_ranking} points!"
        else:
            return f"It's a tie! Both {player_name} and {opponent_name} have {player_hand_name} worth {player_ranking} points."

    def get_best_hand(self, cards):
        best_hand = None
        highest_ranking = 0

        all_combinations = list(combinations(cards, 5))

        for hand in all_combinations:
            hand_ranking = self.calculate_hand_ranking(hand)
            if hand_ranking > highest_ranking:
                highest_ranking = hand_ranking
                best_hand = hand

        return best_hand

    def calculate_hand_ranking(self, hand):
        for ranking, points in self.hand_rankings.items():
            if getattr(self, ranking)(hand):
                return points
        return self.hand_rankings['high_card']

    def compare_hand_rankings(self, player_ranking, opponent_ranking):
        if player_ranking > opponent_ranking:
            return "win"
        elif opponent_ranking > player_ranking:
            return "lose"
        else:
            return "tie"

    def hand_name(self, hand):
        for ranking in self.hand_rankings.keys():
            if getattr(self, ranking)(hand):
                return ranking.replace('_', ' ').title()
        return "High Card"
    
    def get_hand_explanation(self, hand):
        if self.royal_flush(hand):
            return ("Hand: Royal Flush\n"
                    "The highest straight flush, consisting of the ace, king, queen, jack and ten all of the same suit.\n"
                    "Worth 10 points.")
        elif self.straight_flush(hand):
            return ("Hand: Straight Flush\n"
                    "Five consecutive cards of the same suit.\n"
                    "Worth 9 points.")
        elif self.four_of_a_kind(hand):
            return ("Hand: Four of a Kind\n"
                    "Four cards of the same rank.\n"
                    "Worth 8 points.")
        elif self.full_house(hand):
            return ("Hand: Full House\n"
                    "Three of a kind combined with a pair.\n"
                    "Worth 7 points.")
        elif self.flush(hand):
            return ("Hand: Flush\n"
                    "Five cards of the same suit, not in sequence.\n"
                    "Worth 6 points.")
        elif self.straight(hand):
            return ("Hand: Straight\n"
                    "Five consecutive cards of different suits.\n"
                    "Worth 5 points.")
        elif self.three_of_a_kind(hand):
            return ("Hand: Three of a Kind\n"
                    "Three cards of the same rank.\n"
                    "Worth 4 points.")
        elif self.two_pairs(hand):
            return ("Hand: Two Pairs\n"
                    "Two different pairs.\n"
                    "Worth 3 points.")
        elif self.pair(hand):
            return ("Hand: Pair\n"
                    "Two cards of the same rank.\n"
                    "Worth 2 points.")
        else:
            return ("Hand: High Card\n"
                    "None of the above combinations.\n"
                    "Worth 1 point.")