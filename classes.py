import pygame

# Classe pour les vaisseaux
class Ship:
    # Constructeur
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_look = None
        self.laser_look = None
        self.lasers = []

    # Fonction pour Render le vaisseau sur la fenêtre de jeu (fonction blit() de pygame)
    def draw(self, window):
        window.blit(self.ship_look, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    # Getters // Setters
    def get_width(self):
        return self.ship_look.get_width()

    def get_height(self):
        return self.ship_look.get_height()

# Classe pour le joueur
class Player(Ship):
    # Constructeur
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_look = None
        self.laser_look = None
        self.max_health = health

    # Fonction pour Render le vaisseau sur la fenêtre de jeu (Overxrite celle du parent)
    def draw(self, window):
        super().draw(window)

# Classe pour les vaisseaux hostiles
class Enemy(Ship):
    # Constructeur
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_look = None
        self.laser_look = None

# Classe pour les vaisseaux Boss
class Boss(Ship):
    # Constructeur
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_look = None
        self.laser_look = None
