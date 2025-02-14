import os
import sys
import logging
from flask import Flask, render_template, request, jsonify
import atexit

# Configurazione del logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importazione dei moduli di gioco
sys.path.append(os.path.join(os.path.dirname(__file__), 'python_files'))
from python_files.game import Game, Bot

# Definizione di Flask
app = Flask(__name__, static_url_path="/static")
game = None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("game.html")
    elif request.method == "POST":
        try:
            action = request.form.get("action")
            bet_amount = int(request.form.get("betAmount", 0))
            response = handle_post_request(action, bet_amount)
            return jsonify(response)
        except Exception as e:
            logger.error(f"Error handling post request: {e}")
            return jsonify({'error': str(e)}), 500

def handle_post_request(action, bet_amount):
    global game
    logger.info(f"Handling action: {action}, bet amount: {bet_amount}")
    if action in ['check', 'call', 'bet', 'raise', 'fold']:
        current_player = game.turn_manager.get_current_player()
        logger.info(f"Current player: {current_player.name} ({type(current_player).__name__})")
        message = game.execute_turn(current_player, action, bet_amount)
        logger.info(f"Result of action: {message}")

        # Esegui le azioni dei bot solo se non c'è un ciclo infinito
        max_bot_actions = 10  # Numero massimo di azioni consecutive dei bot
        bot_actions = 0

        while isinstance(current_player, Bot) and bot_actions < max_bot_actions:
            game.execute_phase()
            current_player = game.turn_manager.get_current_player()
            bot_actions += 1
    else:
        message = 'Invalid action'

    response = game.generate_game_state_response()
    response['message'] = message
    logger.info(f"Response data: {response}")
    return response

@app.route("/new-game", methods=["POST"])
def new_game():
    global game
    game = Game()
    game.setup_players()
    response = game.generate_game_state_response()
    return jsonify(response)

@app.route("/start-game", methods=["POST"])
def start_game():
    global game
    try:
        game = Game()
        game.setup_players()
        response = game.generate_game_state_response()
        print("Game setup completed successfully:", response)  # Aggiungi un log per il debug
        return jsonify(response)
    except Exception as e:
        logger.error(f"Errore durante l'avvio del gioco: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/advance-turn", methods=["POST"])
def advance_turn():
    global game
    logger.info("Chiamata dell'endpoint advance-turn")
    try:
        game.turn_manager.next_turn()
        if game.check_phase_end():
            game.next_phase()
        response = game.generate_game_state_response()
        logger.info(f"Advance turn response: {response}")
        return jsonify(response)
    except Exception as e:
        logger.error(f"Errore durante l'avanzamento del turno: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/execute-bot-turn", methods=["POST"])
def execute_bot_turn():
    global game
    logger.info("Chiamata dell'endpoint execute-bot-turn")
    try:
        game.execute_phase()
        response = game.generate_game_state_response()
        logger.info(f"Execute bot turn response: {response}")
        return jsonify(response)
    except Exception as e:
        logger.error(f"Errore durante l'esecuzione del turno del bot: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/home_poker", methods=["GET"])
def home_poker():
    return render_template("home_poker.html")

def clean_up():
    logger.info("Cleaning up before shutdown...")
    # Esegui eventuali operazioni di chiusura necessarie

# Registra la funzione clean_up per essere chiamata alla chiusura dell'app
atexit.register(clean_up)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

#TODO:

#capire il motivo per cui il file flask faccia mandare in tilt il programma e crea un ciclo infinito
#premendo il pulsante exit quando è attivo il server flask
#trovare un modo per collegare il file html a quello javascript
#trovare il modo di simulare correttamente il gioco collegando il file javascript e se serve
#approtare modifiche al game.py per fare sì che si possa giocare da terminale tramite il file
#_test_game.py e tramite il file texas_hold_em_poker.py
#trovare un modo per mostrare a video le zioni dei bot con un messaggio che dura un tot di tempo (parte web)
#idem per capire di chi è il turno
#trovare un modo per avere file json già creato (per adesso) per avere un tot di fiches iniziali
#è una base espandibile perchè bisogna trovare una compatibilità con i progetti passati
#gestire tutto dinamicamente
#cambiare il file html per le regole del poker (poker_rules.md)
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
#- spostare le altre cose per avere più pulizia per le regole del poker


#per attivare il venv:
#- andare sopra alla cartella del progetto
#- aprire un nuovo reminale
#- digitare il comando --> F:\Texas-Hold-em-poker\venv\Scripts\Activate.ps1
#- se si vuole avviare il progetto --> python texas_hold_em_poker.py