function createCardElement(card, isFaceDown=false) {
    const cardElement = document.createElement('div');
    cardElement.classList.add('card');
    const valueMap = {
        'A': '01',
        '2': '02',
        '3': '03',
        '4': '04',
        '5': '05',
        '6': '06',
        '7': '07',
        '8': '08',
        '9': '09',
        '10': '10',
        'J': '11',
        'Q': '12',
        'K': '13',
        'back': 'card_back'
    };
    const value = isFaceDown ? 'back' : valueMap[card.value];
    const suit = card.suit.toLowerCase();
    const img = document.createElement('img');
    img.src = `/static/card_images/${isFaceDown ? 'card_back.jpg' : `${suit}/${value}_${suit}.png`}`;
    img.alt = isFaceDown ? 'Card Back' : `${card.value} of ${card.suit}`;
    cardElement.appendChild(img);
    return cardElement;
}

function displayHand(hand, elementId, isFaceDown=false) {
    const handElement = document.getElementById(elementId);
    handElement.innerHTML = ''; // Pulisce le carte precedenti
    hand.forEach(card => {
        handElement.appendChild(createCardElement(card, isFaceDown));
    });
}

window.onload = function() {
    fetch('/')
    .then(response => response.json())
    .then(data => {
        displayHand(data.player_hand, 'player-hand');
        displayHand(data.dealer_hand, 'dealer-hand', true); // Il dealer vede le sue carte coperte
        displayHand(data.community_cards, 'community-cards');
        displayDeck(data.deck_card, 'deck');
    })
    .catch(error => {
        console.error('Errore:', error);
        alert('Si è verificato un errore durante il caricamento delle carte. Riprova.');
    });
};

function startGame() {
    fetch('/start-game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
    })
    .then(response => response.json())
    .then(data => {
        // Aggiorna l'interfaccia utente con i dati ricevuti
        displayHand(data.player_hand, 'player-hand');
        displayHand(data.dealer_hand, 'dealer-hand', true); // Il dealer vede le sue carte coperte
        displayHand(data.community_cards, 'community-cards');
        displayDeck(data.deck_card, 'deck');
        document.getElementById('winner').textContent = data.winner || '';
    })
    .catch(error => {
        console.error('Errore:', error);
        alert('Si è verificato un errore durante l'inizio del gioco. Riprova.');
    });
}

function executeAction(action) {
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'action': action,
        })
    })
    .then(response => response.json())
    .then(data => {
        // Aggiorna l'interfaccia utente con i dati ricevuti
        displayHand(data.player_hand, 'player-hand');
        displayHand(data.dealer_hand, 'dealer-hand', true); // Il dealer vede le sue carte coperte
        displayHand(data.community_cards, 'community-cards');
        displayDeck(data.deck_card, 'deck');
        document.getElementById('winner').textContent = data.winner || '';
    })
    .catch(error => {
        console.error('Errore:', error);
        alert('Si è verificato un errore durante l'esecuzione dell'azione. Riprova.');
    });
}

function displayDeck(deckCard, elementId) {
    const deckElement = document.getElementById(elementId);
    deckElement.innerHTML = ''; // Pulisce il mazzo precedente
    deckElement.appendChild(createCardElement(deckCard, true)); // Le carte del mazzo sono coperte
}

function placeBet() {
    // Aggiungi la logica per piazzare una scommessa
    console.log("Piazza una scommessa");
}

function newGame() {
    // Aggiungi la logica per iniziare una nuova partita
    console.log("Inizia una nuova partita");
}

function exitGame() {
    // Aggiungi la logica per uscire dal gioco
    console.log("Esce dal gioco");
    window.close(); // Chiude la finestra del browser
}