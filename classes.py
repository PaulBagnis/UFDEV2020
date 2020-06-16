import os
import pygame
from functions import collide

# Taille de l'écran du jeu
WIDTH, HEIGHT = 750, 750

# Chargement des images des vaisseaux
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Vaisseaux du joueur
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Classe pour les vaisseaux
class Ship:
    COOLDOWN = 30

    # Constructeur
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_look = None
        self.laser_look = None
        self.lasers = []
        self.cool_down_counter = 0

    # Fonction pour Render le vaisseau sur la fenêtre de jeu (fonction blit() de pygame)
    def draw(self, window):
        window.blit(self.ship_look, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    # Définition du temps entre deux tirs
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    # Méthode qui permet le tir d'un laser
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_look)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    # Déplacement des lasers
    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)
    
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
        self.ship_look = YELLOW_SPACE_SHIP
        self.laser_look = YELLOW_LASER
        # Le mask sert a parcourir les images pour détecter les pixels effectifs des png sur 
        # la surface pour une meilleur gestion des impacts
        self.mask = pygame.mask.from_surface(self.ship_look)
        self.max_health = health

    # Fonction pour Render le vaisseau sur la fenêtre de jeu (Overxrite celle du parent)
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    # Déplacement des lasers sur l'écran
    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    # Barre de vie du joueur
    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_look.get_height() + 10, self.ship_look.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_look.get_height() + 10, self.ship_look.get_width() * (self.health/self.max_health), 10))


# Classe pour les vaisseaux hostiles
class Enemy(Ship):
    COOLDOWN = 30

    # Différentes apparences des vaisseaux
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
                }
    # Constructeur
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_look, self.laser_look = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_look)
        self.max_health = 100

    # Fait de tirer
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_look)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    # Barre de vie des ennemis
    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_look.get_height() + 10, self.ship_look.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_look.get_height() + 10, self.ship_look.get_width() * (self.health/self.max_health), 10))

    # Méthode pour bouger
    def move(self, vel):
        self.y += vel

class Laser:
    # Constructeurs
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    # render des lasers sur l'écran de jeu
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    # Méthode pour le déplacement des lasers
    def move(self, vel):
        self.y += vel

    # Vérification si hors écran
    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    # Vérification si collision
    def collision(self, obj):
        return collide(self, obj)

class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False
