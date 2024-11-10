# ChaosLogger - Keylogging Tool

## Descrizione
ChaosLogger è un keylogger che permette di catturare e salvare le sequenze di tasti premuti su un computer. Il progetto è stato realizzato da Francesco Bulla per scopi di ricerca e include una modalità stealth di base, crittografia dei dati raccolti e la possibilità di salvare i dati localmente. Questo keylogger è progettato principalmente per sistemi Windows, con l'obiettivo di nascondere l'esecuzione del processo il più possibile.

## Caratteristiche
- **Modalità Stealth**: Nasconde la finestra della console su Windows e la rinomina con un titolo generico per evitare sospetti.
- **Crittografia dei Dati**: Le sequenze di tasti catturate vengono crittografate utilizzando la libreria `cryptography` per garantire la sicurezza dei dati.
- **Salvataggio Periodico**: I dati raccolti vengono salvati periodicamente su un file di log, con un intervallo di tempo casuale per evitare pattern prevedibili.

## Requisiti
- Python 3.6+
- Librerie Python:
  - `keyboard`: Per catturare gli eventi della tastiera.
  - `cryptography`: Per crittografare le sequenze di tasti.
  - `psutil`: Per verificare i processi attivi.
  - `ctypes`: Per nascondere la finestra della console su Windows.
  - `threading`, `logging`, `os`, `time`, `random`: Librerie standard di Python.

## Installazione
1. Clona questo repository:
   ```sh
   git clone <repository-url>
   ```
2. Installa le dipendenze necessarie utilizzando `pip`:
   ```sh
   pip install keyboard cryptography psutil
   ```

## Utilizzo
1. Esegui lo script `ChaosLogger`:
   ```sh
   python chaos_logger.py
   ```
2. La registrazione delle sequenze di tasti partirà automaticamente e verrà eseguita in modalità stealth su Windows.
3. Per fermare la registrazione, premi `Invio` o utilizza `Ctrl+C` nella console.

## Avvertenze
- **Permessi di Amministratore**: La libreria `keyboard` potrebbe richiedere permessi di amministratore per funzionare correttamente su alcuni sistemi operativi.
- **Compatibilità**: La funzionalità di modalità stealth è implementata solo per Windows. Su altri sistemi operativi, il keylogger funzionerà senza nascondere la console.
- **Rilevabilità**: Anche con la modalità stealth, un buon software antivirus potrebbe rilevare e bloccare l'esecuzione del keylogger.

## Avvertenza Etica
Questo progetto è stato sviluppato esclusivamente per scopi di ricerca e studio. L'uso non autorizzato di keylogger è illegale e può comportare gravi conseguenze legali. Assicurati di utilizzare questo strumento solo su dispositivi di tua proprietà o su cui hai ottenuto autorizzazione esplicita per effettuare test di sicurezza.

## Problemi Comuni
- **Errore `ModuleNotFoundError`**: Se il modulo `keyboard` non è installato, assicurati di installarlo utilizzando il comando `pip install keyboard`.
- **Permessi Insufficienti**: Se riscontri errori relativi ai permessi, prova a eseguire il programma con privilegi di amministratore (`sudo` su Linux).

## Contributi
Le contribuzioni sono benvenute. Se desideri migliorare il progetto, sentiti libero di aprire una pull request o segnalare un problema.

## Licenza
Questo progetto è distribuito sotto la licenza MIT. .

 