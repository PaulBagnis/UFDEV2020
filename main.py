import pygame
import os
import time
import random

from classes import *
from functions import *
pygame.font.init()

mydb = mysql.connector.connect(host="localhost", user="root", passwd="", db="doom")
mycursor = mydb.cursor()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doom Space")

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

# Bonus
global life_bonus
life_bonus = 0
global dmg_bonus
dmg_bonus = 0

# Selected Ship
global select_ship_player
select_ship_player = 1

# Credits
money = getCredits()

def main() :
    # print("Tout marche !")
    # scores = getScores()
    # for score in scores :
    #     print(score)
    # print(select_ship_player)
    # print(life_bonus)
    # print(dmg_bonus)
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    # CHANGER CA EN FONCTION DU VAISSEAU CHOISI et BONUS
    player_vel = 5
    laser_vel = 5

    player = Player(300, 630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0,0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT: # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)

def select_ship() :
    # print(getScores())
    main_font = pygame.font.SysFont("comicsans", 70)
    back_font = pygame.font.SysFont("comicsans", 30)
    run = True
    # Les boutons
    select_ship_1 =  button((255,255,255), 550, 150, 150, 50, 'Select')
    select_ship_2 =  button((255,255,255), 550, 350, 150, 50, 'Select')
    select_ship_3 =  button((255,255,255), 550, 550, 150, 50, 'Select')
    def redraw_window():
        select_ship_1.draw(WIN, (0,0,0))
        select_ship_2.draw(WIN, (0,0,0))
        select_ship_3.draw(WIN, (0,0,0))
        money_label = main_font.render(f"Credits: {money}", 1, (255,255,255))
        WIN.blit(money_label, (10, 10))
    while run:
        WIN.blit(BG, (0,0))
        # les titres
        title_label = main_font.render("Select Ship Menu", 1, (255,255,255))
        back_label = back_font.render("Hit space to go back to main menu", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 30))
        WIN.blit(back_label, (WIDTH/2 - back_label.get_width()/2, 700))
        redraw_window()
        pygame.display.update()
        global select_ship_player
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if select_ship_1.isOver(pos):
                    select_ship_player += 1
                    main_menu()
                if select_ship_2.isOver(pos):
                    select_ship_player += 2
                    main_menu()
                if select_ship_3.isOver(pos):
                    select_ship_player += 3
                    main_menu()
    pygame.quit()

def select_bonus() :
    # print("in bonus menu")
    main_font = pygame.font.SysFont("comicsans", 70)
    back_font = pygame.font.SysFont("comicsans", 30)
    run = True
    select_life_bonus =  button((255,255,255), 550, 250, 180, 50, 'Buy One')
    select_dmg_bonus =  button((255,255,255), 550, 450, 180, 50, 'Buy One')
    def redraw_window():
        select_life_bonus.draw(WIN, (0,0,0))
        select_dmg_bonus.draw(WIN, (0,0,0))
        money_label = main_font.render(f"Credits: {money}", 1, (255,255,255))
        WIN.blit(money_label, (10, 10))
    while run:
        WIN.blit(BG, (0,0))
        title_label = main_font.render("Select Bonus Menu", 1, (255,255,255))
        back_label = back_font.render("Hit space to go back to main menu", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 120))
        WIN.blit(back_label, (WIDTH/2 - back_label.get_width()/2, 600))
        redraw_window()
        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if select_life_bonus.isOver(pos):
                    global life_bonus
                    life_bonus += 1
                if select_dmg_bonus.isOver(pos):
                    global dmg_bonus
                    dmg_bonus += 1
    pygame.quit()

def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    second_font = pygame.font.SysFont("comicsans", 50)
    run = True
    while run:
        WIN.blit(BG, (0,0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255,255,255))
        select_label = second_font.render("Press A to select a ship.", 1, (255,255,255))
        bonus_label = second_font.render("Press E to select bonuses.", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 250))
        WIN.blit(select_label, (WIDTH/2 - select_label.get_width()/2, 400))
        WIN.blit(bonus_label, (WIDTH/2 - bonus_label.get_width()/2, 550))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    select_ship()
                if event.key == pygame.K_e:
                    select_bonus()
    pygame.quit()


main_menu()