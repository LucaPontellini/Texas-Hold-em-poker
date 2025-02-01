import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'python_files'))

from flask import Flask, render_template, request, jsonify
from python_files.game import Game

app = Flask(__name__, static_url_path="/static")
game = Game()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("game.html")
    elif request.method == "POST":
        action = request.form.get("action")
        bet_amount = int(request.form.get("betAmount", 0))
        response = handle_post_request(action, bet_amount)
        return jsonify(response)

def handle_post_request(action, bet_amount):
    print(f"Handling action: {action}, bet amount: {bet_amount}")  # Log dell'azione e dell'importo della scommessa
    if action in ['check', 'call', 'bet', 'raise']:
        result = game.execute_turn(game.players[0], action, bet_amount)  # Utilizza `execute_turn` invece di `execute_player_turn`
        print(f"Result of action: {result}")  # Log del risultato dell'azione
        if result == 'opponent wins':
            return {'winner': 'opponent', 'phase': game.phase}

    response = generate_game_state_response()
    print(f"Response data: {response}")  # Log dei dati della risposta
    return response

def generate_game_state_response():
    player_hand = format_hand(game.players[1].cards)
    dealer_hand = format_hand(game.players[2].cards) if game.phase == Game.SHOWDOWN else [{'value': 'back', 'suit': 'card_back'}] * 2
    community_cards = format_hand(game.community_cards)
    deck_card = {'value': 'back', 'suit': 'card_back'}
    winner = game.get_winner() if game.phase == Game.SHOWDOWN else None

    return {
        'player_hand': player_hand,
        'dealer_hand': dealer_hand,
        'community_cards': community_cards,
        'deck_card': deck_card,
        'winner': winner,
        'phase': game.phase
    }

def format_hand(cards):
    return [{'value': card.value, 'suit': card.suit} for card in cards]

@app.route("/start-game", methods=["POST"])
def start_game():
    global game
    game = Game()  # Inizializza una nuova partita
    game.setup_players()  # Inizializza le carte dei giocatori e del mazzo
    return jsonify(generate_game_state_response())

@app.route("/new-game", methods=["POST"])
def new_game():
    global game
    game = Game()  # Crea una nuova istanza del gioco per riavviare la partita
    game.setup_players()  # Inizializza le carte dei giocatori e del mazzo
    response = jsonify(generate_game_state_response())
    print(response.get_data(as_text=True))  # Log dei dati della risposta
    return response

@app.route("/home_poker", methods=["GET"])
def home_poker():
    return render_template("home_poker.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)


#TODO:
#gestire i casi in cui il giocatore vince o perde per aggiornare le fiches
#gestire il caso in cui il giocatore non ha più soldi o fiches
#gestire il caso in cui il giocatore si arrende
#aggiungere la possibilità di giocare con più giocatori
#se si realizza la possibilità di giocare con più giocatori, aggiungere la possibilità di scegliere il numero di giocatori e di creare i turni di gioco
#creare una tabella per l'utente per vedere il quantitativo di fiches durante la partita per aggiornarla dinamicamente
#sistemare la parte del pulsante bet perchè non si può scommettere
#controllare se ci sono duplicati
#integrare i file home_poker e poker_rules (tocchera trovare un moddo per collegarle tra loro senza impicci)
#il link dek repository del mio progetto: https://github.com/LucaPontellini/Texas-Hold-em-poker.git
#mostrare in output un pulsante che faccia mostrare a video la spiegazione del perchè il giocatore o il dealer ha vinto per far capire meglio la vincita, in caso mostrare solo i punteggi
#sistemare la scritta deck sopra alla carta coperta che funge da deck (card_back.jpg)
#togliere il bordo delle carte in campo dal file CSS perchè è più realistico
#posizionare i pulsanti in questo modo:
#Exit
#Poker Rules
#lasciare uno spazio per dare più slancio alla grafica (è più leggibile)
#Check
#Bet
#Call
#Raise
#Fold
#cambiare i colori ai pulsanti per una maggiore leggibilità essendo pulsanti di gioco
#opzioni di grafica (regole del poker):
#- spostare il mazzo a sinistra del dealer per non coprire le regole del poker


#per attivare il venv:
#- andare sopra alla cartella del progetto
#- aprire un nuovo reminale
#- digitare il comando --> F:\Texas-Hold-em-poker\venv\Scripts\Activate.ps1
#- se si vuole avviare il progetto --> python texas_hold_em_poker.py 