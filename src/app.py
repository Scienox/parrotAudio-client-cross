import toga
from toga.style import Pack
from client import AudioClient

class parrotAudioClient(toga.App):
    def startup(self):
        self.audio = AudioClient("192.168.0.86")

        # Conteneur racine unique
        self.root_box = toga.Box(style=Pack(direction="column", flex=1))

        # --- VUE PRINCIPALE ---
        self.main_box = toga.Box(style=Pack(direction="column", padding=5))
        self.message_label = toga.Label('Réponse du serveur: ')
        self.response_text = toga.MultilineTextInput()

        self.show_musics_button = toga.Button('Afficher les musiques', on_press=self.show_musics_action)
        self.add_music_button = toga.Button('Ajouter de la musique', on_press=self.add_music)
        self.remove_music_button = toga.Button('Supprimer de la musique', on_press=self.remove_music)
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
        self.main_box.add(self.remove_music_button)
        self.main_box.add(self.show_queue_button)
        self.main_box.add(self.play_music_button)
        self.main_box.add(self.pause_music_button)
        self.main_box.add(self.resume_music_button)
        self.main_box.add(self.previous_music_button)
        self.main_box.add(self.next_music_button)

        # --- VUE POPUP ---
        self.popup_box = toga.Box(style=Pack(direction="column", padding=5))

        # Affichage initial : Vue principale
        self.root_box.add(self.main_box)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.root_box
        self.main_window.show()

    def exec_cmd(self, cmd):
        feedback = self.audio.send(cmd)
        return feedback

    def get_music_list(self):
        return self.exec_cmd(self.audio.get_status()).splitlines()[1].split(':')[1].split('|')

    def show_musics_action(self, widget):
        music_list = self.get_music_list()
        self.response_text.value = '\n'.join(music for music in music_list)

    def switch_view(self, new_view):
        """Remplace le contenu du conteneur racine par la nouvelle vue."""
        self.root_box.clear()
        self.root_box.add(new_view)

    def add_music(self, widget):
        # 1. Réinitialiser la popup box
        self.popup_box.clear()

        # 2. Générer la liste des boutons
        music_list = self.get_music_list()
        for music in music_list:
            button = toga.Button(
                music, 
                on_press=lambda widget, m=music: self.add_selected_music(m)
            )
            self.popup_box.add(button)

        # 3. Ajouter le bouton d'annulation
        cancel_button = toga.Button('Annuler', on_press=self.close_popup)
        self.popup_box.add(cancel_button)

        # 4. Basculer l'affichage vers la popup box
        self.switch_view(self.popup_box)

    def remove_music(self, widget):
        # 1. Réinitialiser la popup box
        self.popup_box.clear()
        # 2. Générer la liste des boutons
        queue_list = self.exec_cmd(self.audio.show_queue()).split(':\n')[1].split('|')
        for i, music in enumerate(queue_list):
            button = toga.Button(
                music,
                on_press=lambda widget, index=i: self.remove_index_music(index)
            )
            self.popup_box.add(button)
        
        # 3. Ajouter le bouton d'annulation
        cancel_button = toga.Button('Annuler', on_press=self.close_popup)
        self.popup_box.add(cancel_button)
        # 4. Basculer l'affichage vers la popup box
        self.switch_view(self.popup_box)

    def close_popup(self, widget=None):
        # Réinitialiser la popup box et revenir à la vue principale
        self.popup_box.clear()
        self.switch_view(self.main_box)

    def add_selected_music(self, music):
        feedback = self.exec_cmd(self.audio.add_music(music))
        self.response_text.value = f"Musique ajoutée: {feedback}"
        self.close_popup()

    def show_queue(self, widget):
        queue_list = self.exec_cmd(self.audio.show_queue()).split('|')
        queue = "\n".join(music for music in queue_list)
        self.response_text.value = queue

    def remove_index_music(self, index):
        # Supprimer la musique à l'index spécifié
        feedback = self.exec_cmd(self.audio.del_music(index))
        self.response_text.value = f"Musique supprimée: {feedback}"
        self.close_popup()

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