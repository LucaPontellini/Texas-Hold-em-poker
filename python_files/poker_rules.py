from itertools import combinations
from deck import Card

class PokerRules:
    def __init__(self):
        self.hand_rankings = self.define_hand_rankings()

    # Hand rankings in Texas Hold'em Poker
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

    # Distribuisce le hole cards e le community cards
    def distribute_cards(self, deck, num_players=2):
        hands = [deck[i*2:(i+1)*2] for i in range(num_players)]
        community_cards = deck[num_players*2:num_players*2+5]
        return hands, community_cards

    def extract_values(self, hand):
        values = []
        for card in hand:
            if isinstance(card, dict):
                values.append(card['value'])
            else:
                values.append(card.value)
        return values

    def extract_indices(self, hand):
        card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        indices = []
        for card in hand:
            if isinstance(card, dict):
                index = card_values.index(card['value'])
            else:
                index = card_values.index(card.value)
            indices.append(index)
        return sorted(indices)

    def extract_suits(self, hand):
        suits = []
        for card in hand:
            if isinstance(card, dict):
                suits.append(card['suit'])
            else:
                suits.append(card.suit)
        return suits

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
        return any(values.count(value) == 4 for value in values)

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
        return any(values.count(value) == 3 for value in values)

    def two_pairs(self, hand):
        # Doppia coppia (Two Pairs): Due coppie di carte dello stesso valore
        values = self.extract_values(hand)
        pairs = [value for value in set(values) if values.count(value) == 2]
        return len(pairs) == 2

    def pair(self, hand):
        # Coppia (Pair): Due carte dello stesso valore
        values = self.extract_values(hand)
        return any(values.count(value) == 2 for value in values)
    
    def high_card(self, hand):
        # Carta alta (High Card): Nessuna delle combinazioni sopra
        return True

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