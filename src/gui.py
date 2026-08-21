import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
from client import AudioClient

class AudioClientGUI:
    def __init__(self, root):
        self.root = root
        self.client = AudioClient(host="192.168.0.86")
        self.create_widgets()

    def create_widgets(self):
        self.message_label = tk.Label(self.root, text="Réponse du serveur: ")
        self.message_label.pack()

        self.response_text = scrolledtext.ScrolledText(self.root, height=10)
        self.response_text.pack()

        self.add_music_button = tk.Button(self.root, text="Ajouter de la musique", command=self.add_music)
        self.add_music_button.pack()

        self.show_queue_button = tk.Button(self.root, text="Afficher la file d'attente", command=self.show_queue)
        self.show_queue_button.pack()

        self.play_music_button = tk.Button(self.root, text="Lire la musique", command=self.play_music)
        self.play_music_button.pack()

    def add_music(self):
        if not self.client:
            messagebox.showerror("Erreur", "Veuillez vous connecter au serveur d'abord.")
            return
        music = simpledialog.askstring("Ajouter de la musique", "Musique à ajouter: ")
        if music:
            command = self.client.add_music(music)
            response = self.client.send(command)
            self.message_label.config(text=f"Réponse du serveur: {response}")
            self.response_text.insert(tk.END, f"Ajout de la musique: {response}\n")

    def show_queue(self):
        command = self.client.show_queue()
        response = self.client.send(command)
        self.message_label.config(text=f"Réponse du serveur: {response}")
        self.response_text.insert(tk.END, f"File d'attente: {response}\n")

    def play_music(self):
        command = self.client.play()
        response = self.client.send(command)
        self.message_label.config(text=f"Réponse du serveur: {response}")
        self.response_text.insert(tk.END, f"Lecture de la musique: {response}\n")