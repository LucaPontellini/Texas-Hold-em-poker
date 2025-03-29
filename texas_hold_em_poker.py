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
from python_files.game import Game, BettingRound, Bot

# Definizione di Flask
app = Flask(__name__, static_url_path="/static")
game = None

@app.route("/", methods=["GET"])
def index():
    return render_template("game.html")

@app.route("/new-game", methods=["POST"])
def new_game():
    global game
    game = Game()
    game.setup_players()
    response = game.generate_game_state_response()
    logger.info("Nuovo gioco creato con successo!")
    return jsonify(response)

@app.route("/start-game", methods=["POST"])
def start_game():
    global game
    try:
        logger.info("Avvio di una nuova partita...")
        game = Game()
        game.setup_players()
        response = game.generate_game_state_response()
        logger.info("Partita avviata con successo.")
        return jsonify(response), 200  # Assicurati di restituire un codice 200
    except Exception as e:
        logger.error(f"Errore durante l'avvio della partita: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/advance-turn", methods=["POST"])
def advance_turn():
    global game
    logger.info("Chiamata dell'endpoint advance-turn")
    try:
        current_player = game.turn_manager.get_current_player()
        logger.info(f"Turno attuale: {current_player.name}")
        game.turn_manager.next_turn()
        
        if game.check_phase_end():
            game.next_phase()
        
        response = game.generate_game_state_response()
        logger.info("Turno avanzato correttamente")
        return jsonify(response)
    except Exception as e:
        logger.error(f"Errore durante l'avanzamento del turno: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/update-state", methods=["POST"])
def update_state():
    global game
    try:
        data = request.get_json()
        logger.info(f"Aggiornamento dello stato ricevuto: {data}")
        return jsonify({'message': 'Stato aggiornato con successo', 'data': data})
    except Exception as e:
        logger.error(f"Errore nell'aggiornamento dello stato: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/action", methods=["POST"])
def handle_action():
    global game
    try:
        action = request.json.get("action")
        bet_amount = int(request.json.get("betAmount", 0))
        logger.info(f"Gestione dell'azione: {action}, Importo: {bet_amount}")

        current_player = game.turn_manager.get_current_player()
        message = game.execute_turn(current_player, action, bet_amount)
        response = game.generate_game_state_response()
        response['message'] = message

        logger.info(f"Azione gestita con successo: {response}")
        return jsonify(response)
    except Exception as e:
        logger.error(f"Errore durante la gestione dell'azione: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/execute-bot-turn", methods=["POST"])
def execute_bot_turn():
    global game
    try:
        logger.info("Esecuzione del turno del bot.")
        bot_id = request.json.get('bot_id')
        
        bot = next((player for player in game.players if player.id == bot_id), None)
        if not bot:
            raise ValueError(f"Bot con ID {bot_id} non trovato.")
        
        logger.info(f"Bot trovato: {bot.name}")
        game_state = game.generate_game_state_response()
        decision, bet_amount = bot.make_decision(game_state, BettingRound.PRE_FLOP)

        response = {
            'decision': decision,
            'bet_amount': bet_amount
        }
        logger.info(f"Risultato del turno bot: {response}")
        return jsonify(response), 200
    except Exception as e:
        logger.error(f"Errore durante il turno del bot: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/home_poker", methods=["GET"])
def home_poker():
    return render_template("home_poker.html")

@app.route("/poker_rules", methods=["GET"])
def poker_rules():
    return render_template("poker_rules.html")

def clean_up():
    logger.info("Pulizia prima della chiusura dell'applicazione.")
    # Operazioni di chiusura eventuali

# Registra la funzione clean_up per l'arresto dell'applicazione
atexit.register(clean_up)

if __name__ == "__main__":
    logger.info("Avvio del server Flask...")
    app.run(debug=True, port=5001)

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