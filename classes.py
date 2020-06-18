import os
import pygame
from functions import collide

# Taille de l'écran du jeu
WIDTH, HEIGHT = 750, 750

# Declaration de la taille du screen
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Tutorial")

# Load images

# Enemies
RED_ENEMY = pygame.image.load(os.path.join("assets", "cacodemon.png"))
AFRIT_ENEMY = pygame.image.load(os.path.join("assets", "Afrit.png"))
SOUL_ENEMY = pygame.image.load(os.path.join("assets", "lostsoul.png"))
L_ENEMY = pygame.image.load(os.path.join("assets", "s1.png"))
M_ENEMY = pygame.image.load(os.path.join("assets", "s2.png"))
N_ENEMY = pygame.image.load(os.path.join("assets", "s3.png"))
O_ENEMY = pygame.image.load(os.path.join("assets", "s4.png"))
P_ENEMY = pygame.image.load(os.path.join("assets", "s5.png"))
Q_ENEMY = pygame.image.load(os.path.join("assets", "s6.png"))


# Player player
STANDARD_SPACE_SHIP = pygame.image.load(os.path.join("assets", "ship.png"))
XWING_SPACE_SHIP = pygame.image.load(os.path.join("assets", "ship2.png"))
BADASS_SPACE_SHIP = pygame.image.load(os.path.join("assets", "ship3.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "laser3.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "bfg.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "laser1.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "laser2.png"))

# Bonus
RAGE_BONUS = pygame.image.load(os.path.join("assets", "rage.png"))
LIFE_BONUS = pygame.image.load(os.path.join("assets", "fak.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "background.jpg")), (WIDTH, HEIGHT))
pygame.mixer.init()

son = pygame.mixer.Sound('doom.wav')

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
    COOLDOWN = 30
    # Constructeur

    def __init__(self, x, y, look, health=100):
        super().__init__(x, y, health)
        self.ship_look = look
        self.laser_look = GREEN_LASER
        # Le mask sert a parcourir les images pour détecter les pixels effectifs des png sur
        # la surface pour une meilleur gestion des impacts
        self.mask = pygame.mask.from_surface(self.ship_look)
        self.max_health = health
        self.cool_down_counter = 0

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
                return 0
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                            return 1

    # Définition du temps entre deux tirs
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    # Barre de vie du joueur
    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y +
                                               self.ship_look.get_height() + 10, self.ship_look.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_look.get_height() +
                                               10, self.ship_look.get_width() * (self.health/self.max_health), 10))


# Classe pour les vaisseaux hostiles
class Enemy(Ship):
    # Différentes apparences des vaisseaux
    COLOR_MAP = {
        "1": (RED_ENEMY, RED_LASER),
        "2": (AFRIT_ENEMY, YELLOW_LASER),
        "3": (SOUL_ENEMY, BLUE_LASER),
        "4": (L_ENEMY, RED_LASER),
        "5": (M_ENEMY, YELLOW_LASER),
        "6": (N_ENEMY, BLUE_LASER),
        "7": (O_ENEMY, RED_LASER),
        "8": (P_ENEMY, YELLOW_LASER),
        "9": (Q_ENEMY, BLUE_LASER),
    }
    # Constructeur

    def __init__(self, x, y, color, health, vel, cd):
        super().__init__(x, y)
        self.ship_look, self.laser_look = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_look)
        self.health = health
        self.max_health = 100
        self.vel = vel
        self.cool_down_counter = 0
        self.cd = cd

    # Définition du temps entre deux tirs
    def cooldown(self):
        if self.cool_down_counter >= self.cd:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    # Fait de tirer
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_look)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    # Barre de vie des ennemis
    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y +
                                               self.ship_look.get_height() + 10, self.ship_look.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_look.get_height() +
                                               10, self.ship_look.get_width() * (self.health/self.max_health), 10))

    # Méthode pour bouger
    def move(self):
        self.y += self.vel


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

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y -
                                            2, self.width+4, self.height+4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y,
                                           self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                            self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False
