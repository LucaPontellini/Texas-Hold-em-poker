import pytest
from itertools import combinations

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

@pytest.fixture
def poker_rules():
    from python_files.poker_rules import PokerRules
    return PokerRules()

@pytest.fixture
def sample_hands():
    return {
        'royal_flush': [Card('10', 'hearts'), Card('J', 'hearts'), Card('Q', 'hearts'), Card('K', 'hearts'), Card('A', 'hearts')],
        'straight_flush': [Card('6', 'spades'), Card('7', 'spades'), Card('8', 'spades'), Card('9', 'spades'), Card('10', 'spades')],
        'four_of_a_kind': [Card('9', 'clubs'), Card('9', 'diamonds'), Card('9', 'hearts'), Card('9', 'spades'), Card('3', 'hearts')],
        'full_house': [Card('8', 'clubs'), Card('8', 'diamonds'), Card('8', 'spades'), Card('K', 'hearts'), Card('K', 'clubs')],
        'flush': [Card('2', 'hearts'), Card('5', 'hearts'), Card('7', 'hearts'), Card('9', 'hearts'), Card('Q', 'hearts')],
        'straight': [Card('5', 'clubs'), Card('6', 'diamonds'), Card('7', 'hearts'), Card('8', 'spades'), Card('9', 'clubs')],
        'three_of_a_kind': [Card('4', 'clubs'), Card('4', 'diamonds'), Card('4', 'spades'), Card('J', 'hearts'), Card('K', 'clubs')],
        'two_pairs': [Card('3', 'hearts'), Card('3', 'diamonds'), Card('J', 'hearts'), Card('J', 'spades'), Card('7', 'clubs')],
        'pair': [Card('5', 'hearts'), Card('5', 'diamonds'), Card('Q', 'clubs'), Card('K', 'spades'), Card('A', 'hearts')],
        'high_card': [Card('2', 'diamonds'), Card('4', 'spades'), Card('7', 'clubs'), Card('10', 'hearts'), Card('Q', 'spades')]
    }

def test_define_hand_rankings(poker_rules):
    hand_rankings = poker_rules.define_hand_rankings()
    assert hand_rankings['royal_flush'] == 10
    assert hand_rankings['straight_flush'] == 9
    assert hand_rankings['four_of_a_kind'] == 8

def test_extract_values(poker_rules, sample_hands):
    hand = sample_hands['royal_flush']
    values = poker_rules.extract_values(hand)
    assert values == ['10', 'J', 'Q', 'K', 'A']

def test_extract_suits(poker_rules, sample_hands):
    hand = sample_hands['royal_flush']
    suits = poker_rules.extract_suits(hand)
    assert suits == ['hearts', 'hearts', 'hearts', 'hearts', 'hearts']

def test_royal_flush(poker_rules, sample_hands):
    hand = sample_hands['royal_flush']
    assert poker_rules.royal_flush(hand) == True

def test_straight_flush(poker_rules, sample_hands):
    hand = sample_hands['straight_flush']
    assert poker_rules.straight_flush(hand) == True

def test_four_of_a_kind(poker_rules, sample_hands):
    hand = sample_hands['four_of_a_kind']
    assert poker_rules.four_of_a_kind(hand) == True

def test_full_house(poker_rules, sample_hands):
    hand = sample_hands['full_house']
    assert poker_rules.full_house(hand) == True

def test_flush(poker_rules, sample_hands):
    hand = sample_hands['flush']
    assert poker_rules.flush(hand) == True

def test_straight(poker_rules, sample_hands):
    hand = sample_hands['straight']
    assert poker_rules.straight(hand) == True

def test_three_of_a_kind(poker_rules, sample_hands):
    hand = sample_hands['three_of_a_kind']
    assert poker_rules.three_of_a_kind(hand) == True

def test_two_pairs(poker_rules, sample_hands):
    hand = sample_hands['two_pairs']
    assert poker_rules.two_pairs(hand) == True

def test_pair(poker_rules, sample_hands):
    hand = sample_hands['pair']
    assert poker_rules.pair(hand) == True

def test_high_card(poker_rules, sample_hands):
    hand = sample_hands['high_card']
    assert poker_rules.high_card(hand) == True

def test_calculate_hand_ranking(poker_rules, sample_hands):
    hand = sample_hands['royal_flush']
    assert poker_rules.calculate_hand_ranking(hand) == 10

def test_determine_winner(poker_rules, sample_hands):
    player_hand = sample_hands['royal_flush']
    opponent_hand = sample_hands['straight_flush']
    community_cards = []
    result = poker_rules.determine_winner(player_hand, opponent_hand, community_cards)
    assert "wins" in result

def test_get_best_hand(poker_rules, sample_hands):
    cards = sample_hands['royal_flush'] + sample_hands['high_card'][:2]
    best_hand = poker_rules.get_best_hand(cards)
    assert poker_rules.royal_flush(best_hand) == True

def test_hand_name(poker_rules, sample_hands):
    hand = sample_hands['royal_flush']
    assert poker_rules.hand_name(hand) == "Royal Flush"

def test_get_hand_explanation(poker_rules, sample_hands):
    hand = sample_hands['royal_flush']
    explanation = poker_rules.get_hand_explanation(hand)
    assert "Royal Flush" in explanation

if __name__ == "__main__":
    pytest.main(['-k', 'test_poker_rules'])