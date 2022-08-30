# Progetto_Esame_AI

Per replicare i risultati ottenuti nei test, è sufficiente aprire con il proprio IDE il progetto ed eseguire i moduli NQueensProblem.py, BlockedNQueensProblem.py, KillerSudokuPrroblem.py e KillerSudokuWithPulp.py

Questo elaborato, nell'ambito dell'esame di Intelligenza Artificiale, consiste nel testare l'algoritmo di ricerca con backtracking, usando sia forward checking che MAC
come strategie di propagazione dei vincoli, al fine di trovare la soluzione a 3 CSP scelti a piacere da CSPLib (https://www.csplib.org/).
All'interno sono contenuti i seguenti file python:

1. NQueensProblem.py: Questo modulo contiene il codice sviluppato per risolvere il problema delle n regine (https://www.csplib.org/Problems/prob054/). Il metodo checkForwardAttempt() si occupa di propagare i vincoli,
ogni qualvolta una regina viene posizionata sulla scacchiera, usando il meccanismo del forward checking, andando a segnare le caselle interessate dai vincoli con dei placeholder 'XY', X = riga e Y = colonna della regina "responsabile" del vincolo.
Il metodo checkAttemptWithMAC() tenta la mossa corrente usando lo stesso meccanismo di AC-3 usato da MAC: ogni volta che piazza una regina, controlla le celle "illegali"
nella successiva colonna di destra e, se nessuna regina può esservi piazzata in modo sicuro, torna indietro alla precedente regina e prova a spostarla nella successiva riga disponibile.

2. KillerSudokuProblem.py: Modulo contenente il codice per il problema del Killer Sudoku (per una spiegazione dettagliata, https://www.csplib.org/Problems/prob057/). 
Il metodo defineCagesFromJson() si occupa di leggere dal file CagesDataSource.json quali celle compongono i cages e a quanto ammonta la somma dei valori al loro interno,
per poi crearne delle tuple. Troviamo poi una serie di metodi per controllare che in ogni quadrato, riga o colonna non ci siano valori duplicati; inferenceOnPossibleAssignmentsWithFC()
propaga i vincoli usando il forward checking, e allo stesso tempo controlla che la somma dei valori all'interno di un cage non superi quella prestabilita dai vincoli del
problema.

3. KillerSudokuWithPulp.py: 

4. BlockedNQueensProblem.py: Tale modulo contiene il codice per la versione blocked del problema delle n regine (https://www.csplib.org/Problems/prob080/). Sostanzialmente troviamo le stesse
linee di codice del modulo NqueensProblem.py, con alcune aggiunte: infatti la scacchiera verrà inizializzata con alcune celle marcate con 'F' (Forbidden) nelle quali non
potrà essere posizionata alcuna regina, e nei metodi per la propagazione dei vincoli già citati verranno aggiunti dei controlli per evitare di piazzare una regina in una 
cella vietata
