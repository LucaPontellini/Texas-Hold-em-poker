import os
import sys
from flask import Flask, render_template, request, jsonify

sys.path.append(os.path.join(os.path.dirname(__file__), 'python_files'))

from python_files.game import Game, Bot

app = Flask(__name__, static_url_path="/static")
game = None

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
    global game
    print(f"Handling action: {action}, bet amount: {bet_amount}")
    if action in ['check', 'call', 'bet', 'raise', 'fold']:
        current_player = game.turn_manager.get_current_player()
        print(f"Current player: {current_player.name} ({type(current_player).__name__})")
        message = game.execute_turn(current_player, action, bet_amount)
        print(f"Result of action: {message}")

        while isinstance(current_player, Bot):
            game.execute_phase()
            current_player = game.turn_manager.get_current_player()
    else:
        message = 'Invalid action'

    response = game.generate_game_state_response()
    response['message'] = message
    print(f"Response data: {response}")
    return response  # Return as a JSON-serializable dictionary

@app.route("/new-game", methods=["POST"])
def new_game():
    global game
    game = Game()
    game.setup_players()
    response = game.generate_game_state_response()
    print("Generated game state response:", response)
    return jsonify(response)

@app.route("/start-game", methods=["POST"])
def start_game():
    global game
    try:
        game = Game()
        game.setup_players()
        response = game.generate_game_state_response()
        response['current_turn'] = game.assign_turns()
        response['blinds_info'] = game.assign_blinds()
        return jsonify(response)
    except Exception as e:
        print(f"Errore durante l'avvio del gioco: {e}")
        return jsonify({'error': str(e)}), 500
    
@app.route("/advance-turn", methods=["POST"])
def advance_turn():
    global game
    print("Advance turn endpoint called")
    game.turn_manager.next_turn()
    current_player = game.turn_manager.get_current_player()
    if isinstance(current_player, Bot) or isinstance(current_player, dict):
        game.execute_phase()
    response = game.generate_game_state_response()
    return jsonify(response)

@app.route("/execute-bot-turn", methods=["POST"])
def execute_bot_turn():
    global game
    print("Executing bot turn endpoint called")
    game.execute_phase()
    response = game.generate_game_state_response()
    return jsonify(response)

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