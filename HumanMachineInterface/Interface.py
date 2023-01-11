import random
import threading
import time
import tkinter as tk

# import HumanMachineInterface.Interface

animate_now = False
is_shown = False


class Interface:
    """
    GUI shown when started
    """

    def __init__(self, min_size, max_size, num_sticks):
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

    def animate(self):
        if not self.is_animated:
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
        while True:
            if not animate_now and self.is_animated:
                self.stop()
            if animate_now and not self.is_animated:
                self.animate()
            time.sleep(1)
