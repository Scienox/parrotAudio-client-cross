import toga
from toga.style import Pack
from client import AudioClient

class parrotAudioClient(toga.App):
    def startup(self):
        self.audio = AudioClient("192.168.0.86")
        main_box = toga.Box(style=Pack(direction="column", padding=5))
        self.message_label = toga.Label('Réponse du serveur: ')
        self.response_text = toga.MultilineTextInput()
        self.add_music_button = toga.Button('Ajouter de la musique', on_press=self.add_music)
        self.show_queue_button = toga.Button('Afficher la file d\'attente', on_press=self.show_queue)
        self.play_music_button = toga.Button('Lire la musique', on_press=self.play_music)
        self.pause_music_button = toga.Button('Pause', on_press=self.pause_music)
        self.resume_music_button = toga.Button('Reprendre', on_press=self.resume_music)

        self.previous_music_button = toga.Button('Précédent', on_press=self.previous_music)
        self.next_music_button = toga.Button('Suivant', on_press=self.next_music)

        main_box.add(self.message_label)
        main_box.add(self.response_text)
        main_box.add(self.add_music_button)
        main_box.add(self.show_queue_button)
        main_box.add(self.play_music_button)
        main_box.add(self.pause_music_button)
        main_box.add(self.resume_music_button)

        main_box.add(self.previous_music_button)
        main_box.add(self.next_music_button)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def add_music(self, widget):
        self.response_text.value = "Ajouter de la musique"

    def show_queue(self, widget):
        self.response_text.value = "Afficher la file d'attente"

    def play_music(self, widget):
        feedback = self.audio.send(self.audio.play())
        self.response_text.value = feedback

    def pause_music(self, widget):
        feedback = self.audio.send(self.audio.pause())
        self.response_text.value = feedback

    def resume_music(self, widget):
        feedback = self.audio.send(self.audio.resume())
        self.response_text.value = feedback

    def previous_music(self, widget):
        feedback = self.audio.send(self.audio.previous_song())
        self.response_text.value = feedback

    def next_music(self, widget):
        feedback = self.audio.send(self.audio.next_song())
        self.response_text.value = feedback


def main():
    return parrotAudioClient(formal_name="parrotAudioClient", app_id="com.example.parrotaudioclient")

if __name__ == "__main__":
    main().main_loop()
