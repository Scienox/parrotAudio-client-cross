import toga
from toga.style import Pack
from client import AudioClient

class parrotAudioClient(toga.App):
    def startup(self):
        self.audio = AudioClient("192.168.0.86")
        self.main_box = toga.Box(style=Pack(direction="column", padding=5))
        self.message_label = toga.Label('Réponse du serveur: ')
        self.response_text = toga.MultilineTextInput()
        self.show_musics_button = toga.Button('Afficher les musiques', on_press=self.show_musics)
        self.add_music_button = toga.Button('Ajouter de la musique', on_press=self.add_music)
        self.show_queue_button = toga.Button('Afficher la file d\'attente', on_press=self.show_queue)
        self.play_music_button = toga.Button('Lire la musique', on_press=self.play_music)
        self.pause_music_button = toga.Button('Pause', on_press=self.pause_music)
        self.resume_music_button = toga.Button('Reprendre', on_press=self.resume_music)

        self.previous_music_button = toga.Button('Précédent', on_press=self.previous_music)
        self.next_music_button = toga.Button('Suivant', on_press=self.next_music)

        self.main_box.add(self.message_label)
        self.main_box.add(self.response_text)
        self.main_box.add(self.show_musics_button)
        self.main_box.add(self.add_music_button)
        self.main_box.add(self.show_queue_button)
        self.main_box.add(self.play_music_button)
        self.main_box.add(self.pause_music_button)
        self.main_box.add(self.resume_music_button)

        self.main_box.add(self.previous_music_button)
        self.main_box.add(self.next_music_button)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()

    def exec_cmd(self, cmd):
        feedback = self.audio.send(cmd)
        return feedback

    def show_musics(self):
        music_list = self.exec_cmd(self.audio.get_status()).splitlines()[1].split(':')[1].split('|')
        return '\n'.join(music for music in music_list)

    def add_music(self, widget):
        self.show_music_popup()

    def show_music_popup(self):
        music_list = self.show_musics().splitlines()
        box = toga.Box(style=Pack(direction="column", padding=5))

        for music in music_list:
            button = toga.Button(music, on_press=lambda widget, music=music: self.add_selected_music(music))
            box.add(button)

        close_button = toga.Button('Annuler', on_press=self.close_popup)
        box.add(close_button)

        if hasattr(self, 'popup_box'):
            self.main_box.remove(self.popup_box)

        self.popup_box = box
        self.main_box.add(self.popup_box)

    def close_popup(self, widget=None):
        if hasattr(self, 'popup_box'):
            self.main_box.remove(self.popup_box)
            del self.popup_box

    def add_selected_music(self, music):
        feedback = self.exec_cmd(self.audio.add_music(music))
        self.response_text.value = f"Musique ajoutée: {feedback}"
        self.close_popup()

    def show_queue(self, widget):
        queue_list = self.exec_cmd(self.audio.show_queue()).split('|')
        queue = "\n".join(music for music in queue_list)
        self.response_text.value = queue

    def play_music(self, widget):
        feedback = self.exec_cmd(self.audio.play())
        self.response_text.value = feedback

    def pause_music(self, widget):
        feedback = self.exec_cmd(self.audio.pause())
        self.response_text.value = feedback

    def resume_music(self, widget):
        feedback = self.exec_cmd(self.audio.resume())
        self.response_text.value = feedback

    def previous_music(self, widget):
        feedback = self.exec_cmd(self.audio.previous_song())
        self.response_text.value = feedback

    def next_music(self, widget):
        feedback = self.exec_cmd(self.audio.next_song())
        self.response_text.value = feedback


def main():
    return parrotAudioClient(formal_name="parrotAudioClient", app_id="com.example.parrotaudioclient")

if __name__ == "__main__":
    main().main_loop()
