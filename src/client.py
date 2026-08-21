import socket

class AudioClient:
    """Client pour envoyer des commandes à un serveur audio distant."""
    
    def __init__(self, host: str = "localhost", port: int = 5000):
        """
        Initialise le client.
        
        Args:
            host (str): Adresse IP du serveur
            port (int): Port du serveur
        """
        self.host = host
        self.port = port
    
    def send(self, command: str) -> str:
        """
        Envoie une commande au serveur.
        
        Args:
            command (str): Commande à envoyer
            
        Returns:
            str: Réponse du serveur
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # On définit un délai d'attente de 3 secondes
                sock.settimeout(3.0)
                sock.connect((self.host, self.port))
                sock.send(command.encode('utf-8'))
                response = sock.recv(1024).decode('utf-8')
                return response
        except socket.timeout:
            return "Erreur: Le serveur n'a pas répondu dans les 3 secondes."
        except Exception as e:
            return f"Erreur: {e}"
        
    def add_music(self, music: str):
        return f"add:{music}"
    
    def show_queue(self):
        return "show:queue"
    
    def show_files(self):
        return "show:files"

    def play(self):
        return "play"

    def stop(self):
        return "stop"

    def pause(self):
        return "pause"

    def resume(self):
        return "resume"

    def previous_song(self):
        return "previous"

    def next_song(self):
        return "next"

    def set_playlist(self, playlist_name):
        return f"set:playlist:{playlist_name}"

    def get_status(self):
        return "get:status"

    def get_volume(self):
        return "get:volume"

    def set_volume(self, volume):
        return f"set:volume:{volume}"
        
    def start_cli(self):
        while True:
            raw_cmd = input("Entrez une commande (PLAY, STOP, PAUSE, RESUME) ou 'exit' pour quitter: ")
            cmd = raw_cmd.strip()
            
            if cmd.lower() == 'exit':
                break
            elif cmd.lower() == "add music":
                music = input("Musique à ajouter: ")
                cmd = self.add_music(music)
            elif cmd.lower() == "show queue":
                cmd = self.show_queue()
            elif cmd == "show files":
                cmd = self.show_files()
            elif cmd == "get status":
                cmd = self.get_status()
            elif cmd == "set playlist":
                playlist_name = input("Nom de la playlist: ")
                cmd = self.set_playlist(playlist_name)
            elif cmd == "get volume":
                cmd = self.get_volume()
            elif cmd == "set volume":
                volume = input("Niveau de volume (0-100): ")
                cmd = self.set_volume(volume)
            elif cmd == "":
                cmd = " "
                
            response = self.send(cmd)
            print(f"Réponse du serveur: {response}")

    def start_gui(self):
        from gui import AudioClientGUI
        AudioClientGUI().run()
