import toga
from toga.style import Pack

# Import sécurisé pour Android et Desktop
try:
    from parrotaudioclient.client import AudioClient
except ImportError:
    from client import AudioClient


class parrotAudioClient(toga.App):
    def startup(self):
        self.audio = AudioClient("192.168.0.86")

        # Conteneur principal
        self.root_box = toga.Box(style=Pack(direction="column", flex=1))

        # --- VUE PRINCIPALE ---
        self.main_box = toga.Box(style=Pack(direction="column", padding=5))
        self.message_label = toga.Label("Réponse du serveur: ")
        self.response_text = toga.MultilineTextInput(style=Pack(flex=1))

        self.main_box.add(self.message_label)
        self.main_box.add(self.response_text)

        # Boutons de la vue principale
        buttons = [
            ("Afficher les musiques", self.show_musics_action),
            ("Ajouter de la musique", self.add_music),
            ("Supprimer de la musique", self.remove_music),
            ("Afficher la file d'attente", self.show_queue),
            ("Lire la musique", self.play_music),
            ("Pause", self.pause_music),
            ("Reprendre", self.resume_music),
            ("Précédent", self.previous_music),
            ("Suivant", self.next_music),
        ]

        for label, callback in buttons:
            self.main_box.add(toga.Button(label, on_press=callback))

        # --- VUE POPUP (DÉDIÉE) ---
        self.popup_box = toga.Box(style=Pack(direction="column", padding=5))

        # Affichage initial
        self.root_box.add(self.main_box)
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.root_box
        self.main_window.show()

    def exec_cmd(self, cmd):
        return self.audio.send(cmd)

    def get_music_list(self):
        output = self.exec_cmd(self.audio.get_status())
        return output.splitlines()[1].split(":")[1].split("|")

    def switch_view(self, new_view):
        """Bascule proprement l'affichage du conteneur racine."""
        self.root_box.clear()
        self.root_box.add(new_view)
        self.main_window.content = self.root_box

    def show_musics_action(self, widget):
        music_list = self.get_music_list()
        self.response_text.value = "\n".join(music_list)

    def add_music(self, widget):
        self.popup_box.clear()

        music_list = self.get_music_list()
        for music in music_list:
            # Capturer correctement la valeur de la variable 'm'
            btn = toga.Button(
                music,
                on_press=lambda w, m=music: self.add_selected_music(m),
            )
            self.popup_box.add(btn)

        cancel_button = toga.Button("Annuler", on_press=self.close_popup)
        self.popup_box.add(cancel_button)

        self.switch_view(self.popup_box)

    def remove_music(self, widget):
        self.popup_box.clear()

        raw_queue = self.exec_cmd(self.audio.show_queue()).split("\n", 1)
        if len(raw_queue) > 1:
            queue_list = raw_queue[1].split("|")
            if queue_list and queue_list[0]:
                for i, music in enumerate(queue_list):
                    btn = toga.Button(
                        music,
                        on_press=lambda w, idx=i: self.remove_index_music(idx),
                    )
                    self.popup_box.add(btn)

        cancel_button = toga.Button("Annuler", on_press=self.close_popup)
        self.popup_box.add(cancel_button)

        self.switch_view(self.popup_box)

    def close_popup(self, widget=None):
        self.popup_box.clear()
        self.switch_view(self.main_box)

    def add_selected_music(self, music):
        feedback = self.exec_cmd(self.audio.add_music(music))
        self.response_text.value = f"Musique ajoutée: {feedback}"
        self.close_popup()

    def remove_index_music(self, index):
        feedback = self.exec_cmd(self.audio.del_music(index))
        self.response_text.value = f"Musique supprimée: {feedback}"
        self.close_popup()

    def show_queue(self, widget):
        queue_list = self.exec_cmd(self.audio.show_queue()).split("|")
        self.response_text.value = "\n".join(queue_list)

    def play_music(self, widget):
        self.response_text.value = self.exec_cmd(self.audio.play())

    def pause_music(self, widget):
        self.response_text.value = self.exec_cmd(self.audio.pause())

    def resume_music(self, widget):
        self.response_text.value = self.exec_cmd(self.audio.resume())

    def previous_music(self, widget):
        self.response_text.value = self.exec_cmd(self.audio.previous_song())

    def next_music(self, widget):
        self.response_text.value = self.exec_cmd(self.audio.next_song())


def main():
    return parrotAudioClient(
        formal_name="parrotAudioClient", app_id="com.example.parrotaudioclient"
    )