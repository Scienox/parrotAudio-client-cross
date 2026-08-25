import asyncio

class AudioClient:
    def __init__(self, host: str = "localhost", port: int = 5000):
        self.host = host
        self.port = port
    
    async def send_async(self, command: str) -> str:
        """Envoie une commande de façon asynchrone sans bloquer l'UI."""
        try:
            # Connexion asynchrone avec un timeout de 3 secondes
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(self.host, self.port), 
                timeout=3.0
            )
            
            writer.write(command.encode('utf-8'))
            await writer.drain()
            
            data = await asyncio.wait_for(reader.read(1024), timeout=3.0)
            writer.close()
            await writer.wait_closed()
            
            return data.decode('utf-8')
        except asyncio.TimeoutError:
            return "Erreur: Le serveur n'a pas répondu dans les 3 secondes."
        except Exception as e:
            return f"Erreur de connexion: {e}"

    def add_music(self, music: str): return f"add:{music}"
    def del_music(self, index): return f"delete:{index}"
    def show_queue(self): return "show:queue"
    def show_files(self): return "show:files"
    def play(self): return "play"
    def stop(self): return "stop"
    def pause(self): return "pause"
    def resume(self): return "resume"
    def previous_song(self): return "previous"
    def next_song(self): return "next"
    def get_status(self): return "get:status"