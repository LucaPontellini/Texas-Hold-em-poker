```mermaid

    classDiagram
    %% deck.py
    class Card {
        +__init__(self, seed: str, value: str): none
        +__repr__(self): str
        +__eq__(self, other: object): bool
    }

    class Deck {
        +__init__(self, deck_file_path): none
        +load_deck(self, deck_file_path): list[Card]
        +create_cards(self, deck): list[Card]
        +shuffle(self): none
        +draw_card(self): Card | None
        +print_deck(self): none
    }

    %% turn_manager.py
    class TurnManager {
        +__init__(self, players: list[Player]): none
        +find_big_blind(self): int
        +next_turn(self): none
        +get_current_player(self): Player
    }

    %% game.py
    class Game {
        +PRE_FLOP: str
        +FLOP: str
        +TURN: str
        +RIVER: str
        +SHOWDOWN: str
        +VALID_ACTIONS: list[str]
        +__init__(self, num_players=4): none
        +create_players(self, num_players: int): list[Player]
        +set_blinds(self): tuple[int, int]
        +setup_players(self): none
        +post_blinds(self): none
        +deal_hole_cards(self): none
        +move_to_flop(self): none
        +deal_flop(self): none
        +move_to_turn(self): none
        +deal_turn_card(self): none
        +move_to_river(self): none
        +deal_river_card(self): none
        +move_to_showdown(self): none
        +execute_phase(self): none
        +execute_turn(self, player: Player, action: str, bet_amount=0): str
        +next_phase(self): none
        +evaluate_hands(self): none
        +combine_hands(self, player_cards: list[Card]): list[Card]
        +start_game(self): none
        +get_winner(self): str
        +assign_turns(self): str
        +assign_blinds(self): dict
        +generate_game_state_response(self): dict
        +format_hand(self, cards: list[Card]): list[dict]
    }

    %% player.py
    class Player {
        +__init__(self, name: str): none
        +add_card(self, card: Card): none
        +remove_card(self, card: Card): none
        +has_card(self, card: Card): bool
        +increase_aggressiveness(self): none
        +bet_chips(self, amount: int): int
        +get_chips(self): int
        +add_chips(self, amount: int): none
    }

    class Dealer {
        +__init__(self, name: str = "Dealer"): none
    }

    class BettingRound {
        <<enumeration>>
        PRE_FLOP
        FLOP
        TURN
        RIVER
    }

    class Bot {
        +__init__(self, name: str): none
        +make_decision(self, game_state: dict, betting_round: BettingRound): str
        +pre_flop_decision(self, hand_strength: int, pot_odds: float, opponent_behavior: int): str
        +post_flop_decision(self, hand_strength: int, game_state: dict, pot_odds: float, opponent_behavior: int): str
        +evaluate_hand(self, community_cards: list[Card]): int
        +calculate_pot_odds(self, game_state: dict): float
        +count_aggressive_players(self, game_state: dict): int
        +analyze_opponent_behavior(self, game_state: dict): int
        +increase_aggressiveness(self): none
    }

    %% poker_rules.py
    class PokerRules {
        +__init__(self): none
        +define_hand_rankings(self): dict
        +distribute_cards(self, deck, num_players=2): list[list[Card]]
        +extract_values(self, hand: list[Card]): list[str]
        +extract_suits(self, hand: list[Card]): list[str]
        +extract_indices(self, hand: list[Card]): list[int]
        +royal_flush(self, hand: list[Card]): bool
        +straight_flush(self, hand: list[Card]): bool
        +four_of_a_kind(self, hand: list[Card]): bool
        +full_house(self, hand: list[Card]): bool
        +flush(self, hand: list[Card]): bool
        +straight(self, hand: list[Card]): bool
        +three_of_a_kind(self, hand: list[Card]): bool
        +two_pairs(self, hand: list[Card]): bool
        +pair(self, hand: list[Card]): bool
        +determine_winner(self, player_hand: list[Card], opponent_hand: list[Card], community_cards: list[Card], player_name="Giocatore", opponent_name="Bot1"): str
        +get_best_hand(self, cards: list[Card]): list[Card]
        +calculate_hand_ranking(self, hand: list[Card]): int
        +compare_hand_rankings(self, player_ranking: int, opponent_ranking: int): str
        +hand_name(self, hand: list[Card]): str
        +get_hand_explanation(self, hand: list[Card]): str
    }

    %% app.py
    class FlaskApp {
        +__init__(self): none
        +index(self): str
        +handle_post_request(self, action: str, bet_amount: int): dict
        +generate_game_state_response(self): dict
        +format_hand(self, cards: list[Card]): list[dict]
        +start_game(self): dict
        +new_game(self): dict
        +home_poker(self): str
        +advance_turn(self): dict
    }


%% Relationships
Game "1" --> "1" Deck : uses
Game "1" --> "2..*" Player : uses
Game "1" --> "1" PokerRules : uses
Game "1" --> "1" TurnManager : uses
Deck "1" --> "52" Card : contains
Player "0..*" --> "1" Card : has
PokerRules "1" --> "1" Deck : uses
PokerRules "1" --> "2..*" Player : uses
PokerRules "0..*" --> "1" Card : evaluates
FlaskApp "1" --> "1" Game : uses
```


Note:

To access the online functionalities of this poker game, use Flask as a server within the texas_hold_em_poker.py file.<br>
This file not only manages web-based interactions but also initiates the game, serving as the central hub for the system's dynamic operations.