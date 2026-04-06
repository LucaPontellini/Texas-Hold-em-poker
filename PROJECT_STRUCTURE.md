## Panoramica del progetto

Questo progetto implementa la logica completa del Texas Hold’em Poker — dalla distribuzione delle carte alla valutazione delle mani — e rappresenta un’evoluzione significativa rispetto alle prime iterazioni, grazie a una struttura più modulare e ordinata. Tuttavia, l’assenza dell’interfaccia grafica impedisce di collegare la logica del gioco all’esperienza dell’utente finale: la partita si svolge correttamente nel terminale, ma non è ancora visibile nell’interfaccia web. Il progetto è pensato per essere integrato in futuro nel sistema più ampio di Ponte’s Casino.


## Struttura del progetto:

La seguente struttura rappresenta l’organizzazione attuale del progetto Texas-Hold-em-poker.


```text
Texas-Hold-em-poker/
│   
├── python_files/                               # Contiene i file Python che implementano la logica del poker, organizzati in moduli specifici per ogni aspetto del gioco.
│   ├── __init__.py                             # File di inizializzazione del pacchetto, necessario per rendere la cartella un modulo Python.
│   ├── deck.py                                 # Definisce la classe Card, carica il mazzo da deck.json (o ne crea uno standard), genera le istanze delle carte, mescola, pesca 
│   │                                             e stampa il contenuto del mazzo per debug.
│   ├── game.py                                 # Modulo principale che gestisce la logica completa della partita: crea giocatori e bot, distribuisce le carte, controlla turni 
│   │                                             e fasi (pre-flop → flop → turn → river → showdown), gestisce puntate, blinds, pot, azioni dei bot, valutazione delle mani e 
│   │                                             comunicazione con il server Flask. Include anche il TurnManager per la rotazione dei turni e la sincronizzazione con 
│   │                                             l’interfaccia web (funziona solamente nel terminale, ma non lato web).
│   ├── players.py                              # Modulo che definisce tutte le entità del tavolo da poker: il giocatore umano, il dealer e i bot. Gestisce carte personali, 
│   │                                             fiches, aggressività, puntate, stato del turno e valutazione della mano tramite le regole del poker. Include anche le 
│   │                                             enumerazioni BotType e BettingRound, oltre alla logica decisionale avanzata dei bot (pre-flop e post-flop), analisi del 
│   │                                             comportamento degli avversari, calcolo delle pot odds e valutazione della posizione al tavolo.
│   └── poker_rules.py                          # Modulo dedicato alla valutazione delle mani nel Texas Hold’em: definisce il ranking ufficiale delle combinazioni, fornisce 
│                                                 funzioni per riconoscere ogni tipo di mano (dalla carta alta alla scala reale), calcola il punteggio, confronta due mani, 
│                                                 determina il vincitore e genera spiegazioni testuali delle combinazioni. Include anche la logica per estrarre valori/semi, │                                                 gestire scale speciali e trovare la migliore mano possibile tramite combinazioni da 5 carte.  
│   
├── static/                                     # Contiene tutte le risorse statiche come immagini, stili CSS e musica.
│   ├── card_images/                            # Contiene le immagini di tutte le carte da gioco riutilizzabili per ogni gioco di carte del casinò.
│   │   ├── hearts/                             # Contiene le immagini delle carte di cuori, numerate da 1 a 13 (Asso, 2-10, Jack, Regina, Re).
│   │   │   ├── 01_hearts.png                   # Immagine dell'Asso di cuori.
│   │   │   ├── 02_hearts.png                   # Immagine del 2 di cuori.
│   │   │   ├── 03_hearts.png                   # Immagine del 3 di cuori.
│   │   │   ├── 04_hearts.png                   # Immagine del 4 di cuori.
│   │   │   ├── 05_hearts.png                   # Immagine del 5 di cuori.
│   │   │   ├── 06_hearts.png                   # Immagine del 6 di cuori.
│   │   │   ├── 07_hearts.png                   # Immagine del 7 di cuori.
│   │   │   ├── 08_hearts.png                   # Immagine del 8 di cuori.
│   │   │   ├── 09_hearts.png                   # Immagine del 9 di cuori.
│   │   │   ├── 10_hearts.png                   # Immagine del 10 di cuori.
│   │   │   ├── 11_hearts.png                   # Immagine del Jack di cuori.
│   │   │   ├── 12_hearts.png                   # Immagine della Regina di cuori.
│   │   │   └── 13_hearts.png                   # Immagine del Re di cuori.
│   │   │                   
│   │   ├── diamonds/                           # Contiene le immagini delle carte di quadri, numerate da 1 a 13 (Asso, 2-10, Jack, Regina, Re). 
│   │   │   ├── 01_diamonds.png                 # Immagine dell'Asso di quadri. 
│   │   │   ├── 02_diamonds.png                 # Immagine del 2 di quadri. 
│   │   │   ├── 03_diamonds.png                 # Immagine del 3 di quadri. 
│   │   │   ├── 04_diamonds.png                 # Immagine del 4 di quadri. 
│   │   │   ├── 05_diamonds.png                 # Immagine del 5 di quadri. 
│   │   │   ├── 06_diamonds.png                 # Immagine del 6 di quadri. 
│   │   │   ├── 07_diamonds.png                 # Immagine del 7 di quadri. 
│   │   │   ├── 08_diamonds.png                 # Immagine del 8 di quadri. 
│   │   │   ├── 09_diamonds.png                 # Immagine del 9 di quadri. 
│   │   │   ├── 10_diamonds.png                 # Immagine del 10 di quadri. 
│   │   │   ├── 11_diamonds.png                 # Immagine del Jack di quadri. 
│   │   │   ├── 12_diamonds.png                 # Immagine della Regina di quadri. 
│   │   │   └── 13_diamonds.png                 # Immagine del Re di quadri. 
│   │   │ 
│   │   ├── clubs/                              # Contiene le immagini delle carte di fiori, numerate da 1 a 13 (Asso, 2-10, Jack, Regina, Re).
│   │   │   ├── 01_clubs.png                    # Immagine dell'Asso di fiori.
│   │   │   ├── 02_clubs.png                    # Immagine del 2 di fiori.
│   │   │   ├── 03_clubs.png                    # Immagine del 3 di fiori.
│   │   │   ├── 04_clubs.png                    # Immagine del 4 di fiori.
│   │   │   ├── 05_clubs.png                    # Immagine del 5 di fiori.
│   │   │   ├── 06_clubs.png                    # Immagine del 6 di fiori.
│   │   │   ├── 07_clubs.png                    # Immagine del 7 di fiori.
│   │   │   ├── 08_clubs.png                    # Immagine del 8 di fiori.
│   │   │   ├── 09_clubs.png                    # Immagine del 9 di fiori.
│   │   │   ├── 10_clubs.png                    # Immagine del 10 di fiori.
│   │   │   ├── 11_clubs.png                    # Immagine del Jack di fiori.
│   │   │   ├── 12_clubs.png                    # Immagine della Regina di fiori.
│   │   │   └── 13_clubs.png                    # Immagine del Re di fiori.
│   │   │
│   │   ├── spades/                             # Contiene le immagini delle carte di picche, numerate da 1 a 13 (Asso, 2-10, Jack, Regina, Re).
│   │   │   ├── 01_spades.png                   # Immagine dell'Asso di picche.
│   │   │   ├── 02_spades.png                   # Immagine del 2 di picche.
│   │   │   ├── 03_spades.png                   # Immagine del 3 di picche.
│   │   │   ├── 04_spades.png                   # Immagine del 4 di picche.
│   │   │   ├── 05_spades.png                   # Immagine del 5 di picche.
│   │   │   ├── 06_spades.png                   # Immagine del 6 di picche.
│   │   │   ├── 07_spades.png                   # Immagine del 7 di picche.
│   │   │   ├── 08_spades.png                   # Immagine del 8 di picche.
│   │   │   ├── 09_spades.png                   # Immagine del 9 di picche.
│   │   │   ├── 10_spades.png                   # Immagine del 10 di picche.
│   │   │   ├── 11_spades.png                   # Immagine del Jack di picche.
│   │   │   ├── 12_spades.png                   # Immagine della Regina di picche.
│   │   │   └── 13_spades.png                   # Immagine del Re di picche.
│   │   │
│   │   └── card_back.png                       # Immagine del retro delle carte, che viene usata sia come mazzo che come retro delle carte dei giocatori e del dealer.
│   │
│   ├── css/                                    # Contiene i file CSS usati per lo stile delle pagine del poker, ognuna con il proprio.
│   │   ├── game.css                            # Gestisce il layout delle carte, i pannelli informativi, le animazioni e l'interfaccia del tavolo.            
│   │   ├── home_poker.css                      # Gestisce lo sfondo, l'header, i pulsanti e i messaggi di errore.
│   │   └── poker_rules.css                     # Gestisce le tabelle, le immagini delle carte, i pulsanti e la formattazione dei contenuti informativi.
│   │
│   ├── javascript/                             # Contiene i file JavaScript usati per gestire l'interattività delle pagine del poker, con funzioni specifiche per ogni pagina.
│   │   ├── game.js                             # Gestisce la visualizzazione delle carte, le puntate, i turni, le azioni del giocatore e del bot, l'aggiornamento 
│   │   │                                         dell’interfaccia e la musica di sottofondo.
│   │   └── home_poker.js                       # Gestisce i messaggi di errore nella pagina introduttiva del poker, mostrando notifiche temporanee e reindirizzando 
│   │                                             automaticamente l’utente.                                            
│   │
│   ├── music/                                  # Contiene i file audio utilizzati come sottofondo musicale per la pagina del poker (l'obiettivo era riprodurle in loop).
│   │   ├── best_jazz_club_NO.mp3               # Sottofondo musicale per la pagina di gioco del poker, con un ritmo rilassante e sofisticato che richiama l'atmosfera di un 
│   │   │                                         elegante jazz club a New Orleans, perfetto per accompagnare le partite di poker con stile e classe.
│   │   ├── casino.mp3                          # Sottofondo musicale per la pagina di gioco del poker, con un ritmo energico e coinvolgente che richiama l'atmosfera vivace e 
│   │   │                                         frenetica di un casinò, creando un ambiente stimolante per i giocatori.
│   │   ├── jazz_casino_bar.mp3                 # Sottofondo musicale per la pagina di gioco del poker, con un ritmo rilassante e sofisticato che richiama l'atmosfera di un 
│   │   │                                         elegante jazz bar in un casinò, perfetto per accompagnare le partite di poker con stile e classe.
│   │   ├── jazz_whiskey_casino.mp3             # Sottofondo musicale per la pagina di gioco del poker, con un ritmo rilassante e sofisticato che richiama l'atmosfera di un 
│   │   │                                         elegante bar di un casinò, perfetto per accompagnare le partite di poker con stile e classe.
│   │   ├── two_cigarettes_please.mp3           # Sottofondo musicale per la pagina di gioco del poker, con un ritmo più vivace e dinamico che accompagna l'azione del gioco.
│   │   └── welcome_to_new_orleans.mp3          # Sottofondo musicale per la pagina di gioco del poker, con un ritmo allegro e festoso che richiama l'atmosfera di New 
│   │                                             Orleans, famosa per il suo legame con il poker e i casinò.
│   ├── poker_chips/                            # Contiene le immagini delle fiches usate nel gioco del poker, con diversi colori che rappresentano valori in denaro differenti.
│   │   │                                         Sono presenti solo alcuni colori, ma l'intenzione era di avere una gamma completa di fiches per rappresentare tutti i valori │   │   │                                         necessari per il gioco.
│   │   ├── black_chips.jpg                     # Immagine delle fiches nere.
│   │   ├── blue_chips.jpg                      # Immagine delle fiches blu.
│   │   ├── dark_green_chips.jpg                # Immagine delle fiches verdi scure.
│   │   ├── light_blue_chips.jpg                # Immagine delle fiches azzurre.
│   │   ├── light_green_chips.jpg               # Immagine delle fiches verdi chiare.
│   │   ├── orange_chips.jpg                    # Immagine delle fiches arancioni.
│   │   ├── purple_chips.jpg                    # Immagine delle fiches viola.
│   │   ├── red_chips.jpg                       # Immagine delle fiches rosse.
│   │   ├── white_chips.jpg                     # Immagine delle fiches bianche.
│   │   └── yellow_chips.jpg                    # Immagine delle fiches gialle.
│   │
│   ├── poker_table.jpg                         # Immagine di presentazione del Poker pre-pagina del gioco.
│   └── texas_hold_em_table.jpg                 # Immagine del tavolo da poker, che funge da sfondo per la pagina di gioco del poker, creando un'atmosfera più immersiva e      
│                                                realistica per i giocatori.
│
├── templates/                                  # Contiene tutti i file HTML utilizzati per il rendering della pagina del poker.
│   ├── fiches_poker_test.html                  # Mostra le immagini delle fiches, consente di modificarne le quantità e include funzioni base di incremento, decremento e reset 
│   │                                             (è un prototipo per le future implementazioni per puntare dinamicamente durante le partite, ma non è stato implementato nella 
│   │                                             versione finale del progetto). 
│   ├── game.html                               # Mostra tavolo, carte, pannelli di gioco, pulsanti delle azioni e include la logica interattiva tramite game.js e gli stili 
│   │                                             dedicati (è la pagina del progetto che presenta il problema di non funzionare correttamente come lato utente finale).
│   ├── home_poker.html                         # Mostra il titolo, i pulsanti di navigazione verso gioco e le regole, gestisce gli eventuali messaggi di errore e include gli 
│   │                                             stili e lo script dedicati.
│   └── poker_rules.html                        # Presenta i valori delle carte, il ranking delle mani, le fasi di gioco, le azioni di puntata e la tabella dei valori delle 
│                                                 fiches, con immagini integrate per ogni seme.
│
├── tests/                                      # Contiene tutti i file di test per verificare la correttezza della logica del progetto, con test specifici per ogni modulo.
│   ├── test_deck.py                            # Verifica la creazione del mazzo standard, il mescolamento, l’estrazione delle carte e il caricamento da file JSON tramite mock.
│   ├── test_game_functions.py                  # Verifica mazzo, giocatori, bot, regole, gestione dei turni e avanzamento delle fasi tramite unittest.
│   ├── test_game.py                            # Gestisce turni, fasi di gioco, azioni dei giocatori e bot, mostrando carte, piatto e stato della partita tramite interfaccia 
│   │                                             testuale colorata.
│   ├── test_players.py                         # Verifica gestione delle carte, fiches, distribuzione, determinazione del vincitore e logiche decisionali del bot tramite pytest
│   └── test_poker_rules.py                     # Verifica estrazione di valori e semi, riconoscimento delle combinazioni, calcolo del punteggio, determinazione del vincitore e 
│                                                 identificazione della mano migliore tramite pytest.
│
├── test_music.py                               # Carica una playlist locale, verifica l’esistenza dei file, li riproduce in sequenza tramite pygame.mixer e segnala eventuali 
│                                                 problemi, includendo un avviso specifico per ambienti SSH.
│
├── texas_hold_em_poker.py                      # Server Flask dell’applicazione: gestisce routing, avvio e reset delle partite, avanzamento dei turni, azioni dei giocatori e 
│                                                 dei bot, generazione dello stato di gioco e rendering delle pagine HTML.
│
├── Texas_Hold_em_poker.md                      # Documento tecnico che contiene il diagramma UML dell’intero progetto: rappresenta classi, metodi principali e relazioni tra i 
│                                                 moduli (mazzo, giocatori, bot, regole, gestione turni, logica di gioco e server Flask). Include anche note operative sull’uso 
│                                                 del server Flask come punto di accesso alle funzionalità web. Il diagramma ha varie incoerenze: relazioni non allineate al 
│                                                 codice, una FlaskApp che non rappresenta davvero texas_hold_em_poker.py, moduli e dipendenze parziali o mancanti. In generale, 
│                                                 la struttura va rivista per riflettere l’implementazione attuale.
│
├── poker_rules.md                              # Documento che raccoglie tutte le regole del Texas Hold’em: setup del gioco, posizioni, turni di puntata, azioni consentite, 
│                                                 valori delle fiches, ranking delle mani, showdown, strategia, etichetta, psicologia, varianti e concetti avanzati. Funziona 
│                                                 come guida completa per principianti e giocatori intermedi.
│
├── deck.json                                   # File JSON contenente l’intero mazzo standard da 52 carte: valori da 2 ad A e quattro semi (Hearts, Diamonds, Clubs, Spades). 
│                                                 Utilizzato dal modulo Deck per caricare e generare il mazzo di gioco.
│
├── requirements.txt                            # Gestione Dipendenze
│                                               # - Flask: Framework web leggero usato per gestire routing, server HTTP e rendering delle pagine dell’applicazione.
│                                               # - Requests: Libreria per effettuare richieste HTTP semplici e leggibili, utile per comunicazioni client–server o API esterne.
│                                               # - Pytest: Framework di testing rapido e modulare, utilizzato per eseguire test automatici su logica di gioco, bot e componenti 
│                                                           del progetto.
│                                               # - Termcolor: Libreria che permette di colorare il testo nel terminale, utile per migliorare la leggibilità dell’interfaccia 
│                                                              testuale.
│                                               # - Requests==2.32.3: Versione specifica e stabile della libreria Requests, usata per garantire compatibilità e comportamento 
│                                                                     prevedibile (la ripetizione di requests è stata fatta per garantire compatibilità nello sviluppo).
│                                               # - Werkzeug==2.3.7: Toolkit WSGI utilizzato internamente da Flask per gestire server, routing e componenti di basso livello.
│                                               
├── LICENSE                                     # Licenza MIT: Uso libero, obbligo di citazione
│                                               # - Garantisce il mio copyright.
│                                               # - Permette a chiunque di usare, copiare e modificare il codice.
│                                               # - Esclude la responsabilità (Disclaimer "AS IS").
│
├── .gitignore                                  # Esclude file e cartelle non necessari dal controllo di versione, come __pycache__, file temporanei, dati sensibili, ecc.
│
├── README.md                                   # Contiene una panoramica del progetto, istruzioni per l'installazione e l'uso, e informazioni sullo sviluppo 
│                                                 futuro.                                  
│                                  
└── PROJECT_STRUCTURE.md                        # File più recente del progetto, che funge da panoramica dettagliata della struttura del progetto, con le caratteristiche di 
                                                  ogni elemento del progetto, e una riflessione sulle aree di disorganizzazione e miglioramento.
```

## 📝 Nota generale sui file del progetto

Alcuni file contengono appunti, codice provvisorio e funzioni di test utilizzati esclusivamente per il debugging e la verifica del comportamento del sistema. Questi elementi non fanno parte della versione finale e non verranno inclusi nella build di produzione: servono solo a monitorare lo stato del gioco, tracciare errori e facilitare lo sviluppo.