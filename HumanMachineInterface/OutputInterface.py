# In-project modules
import random
import threading
import time

from HumanMachineInterface.IOInterface import *
from HumanMachineInterface.IOMode import *
import tkinter as tk

speech = ""
is_shown = False


class OutputInterface(IOInterface):
    """
    Output Interface: \n
    Performs all machine to human operations: output actions
    """

    def __init__(self, min_size, max_size, num_sticks, language: str = "fr-FR"):
        super(OutputInterface, self).__init__(IOMode.OUTPUT, language)
        self.root = tk.Tk()
        self.root.attributes("-topmost", True)
        self.min_size = min_size
        self.max_size = max_size
        self.num_sticks = num_sticks
        self.is_animated = False

        # Créer un canvas pour afficher les bâtonnets
        self.canvas = tk.Canvas(self.root, width=350, height=200)
        self.canvas.pack()

        # Afficher les bâtonnets au démarrage
        self.sticks = []
        for i in range(self.num_sticks):
            x1 = 50 + (i * 20) + i * 7
            y1 = 100 - self.min_size
            x2 = 70 + (i * 20) + i * 7
            y2 = 100 + self.min_size
            stick = self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue", width=0)
            self.sticks.append(stick)

        # Démarrer l'animation
        # self.animate()

    def speak(self, text: str):
        """
        Speak information(s) with installed voices \n
        :param text: Information to be spoken
        """
        self.animate()
        super(OutputInterface, self).speak(text)
        self.stop()

    def play_video(self, videoPath: str):
        """
        Play a video file \n
        :param videoPath: Path to th video file
        """
        super(OutputInterface, self).play_video(videoPath)

    def animate(self):
        while not is_shown:
            pass

        self.is_animated = True

        # Modifier la taille de chaque bâtonnet de manière aléatoire
        for i, stick in enumerate(self.sticks):
            size = random.uniform(self.min_size, self.max_size)
            x1 = 50 + (i * 20) + i * 7
            y1 = 100 - size
            x2 = 70 + (i * 20) + i * 7
            y2 = 100 + size
            self.canvas.coords(stick, x1, y1, x2, y2)

        # Répéter l'animation toutes les 100 millisecondes
        self.root.after(100, self.animate)

    def stop(self):
        if self.is_animated:
            self.is_animated = False

        # Arrêter l'animation en annulant l'appel de la méthode "animate" programmé avec "after"
        self.root.after_cancel(self.root.after_idle(self.animate))

        # Remettre chaque bâtonnet à sa taille minimale
        for i, stick in enumerate(self.sticks):
            x1 = 50 + (i * 20) + i * 7
            y1 = 100 - self.min_size
            x2 = 70 + (i * 20) + i * 7
            y2 = 100 + self.min_size
            self.canvas.coords(stick, x1, y1, x2, y2)

    def show(self):
        global is_shown
        # Watchman pour gérer l'animation en fonction des ordres envoyés par les autres modules
        wait_for_order_thread = threading.Thread(target=self.wait_for_order)
        wait_for_order_thread.start()
        is_shown = True
        # Démarrer la boucle d'événements de tkinter
        self.root.mainloop()

    def wait_for_order(self):
        global speech
        while True:
            if speech != "" and not self.is_animated:
                self.speak(speech)
                speech = ""
            time.sleep(1)
