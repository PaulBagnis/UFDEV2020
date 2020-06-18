import pygame
import os
import time
import random

from classes import *
from functions import *

pygame.init()
pygame.font.init()
pygame.mixer.init()

mydb = mysql.connector.connect(
    host="localhost", user="root", passwd="", db="doom")
mycursor = mydb.cursor()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doom Space")

# Background
BG = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "background.jpg")), (WIDTH, HEIGHT))
BG2 = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))
son = pygame.mixer.Sound('doom.wav')
# Bonus
global life_bonus
life_bonus = getBonusLife()
global vel_bonus
vel_bonus = getBonusLife()

# Selected Ship
global select_ship_player
select_ship_player = 0


def main():
    global life_bonus
    global vel_bonus
    # print("Tout marche !")
    # scores = getScores()
    # for score in scores :
    #     print(score)
    print(select_ship_player)
    print(life_bonus)
    print(vel_bonus)
    run = True
    FPS = 60
    level = 0
    lives = 5 + life_bonus
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)
    money = getCredits()
    start_money = money

    enemies = []
    wave_length = 5

    # CHANGER CA EN FONCTION DU VAISSEAU CHOISI et BONUS
    player_vel = 5 + vel_bonus
    laser_vel = 5

    # ICI CONDITION POUR VAISSEAU CHOISI
    if select_ship_player == 2:
        player = Player(300, 630, XWING_SPACE_SHIP)
    elif select_ship_player == 3:
        player = Player(300, 630, BADASS_SPACE_SHIP)
    else:
        player = Player(300, 630, STANDARD_SPACE_SHIP)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0, 0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        credits_label = main_font.render(
            f"Credits: {money}", 1, (255, 255, 255))
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        WIN.blit(credits_label, (WIDTH/2 - credits_label.get_width()/2, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            won_money = money - start_money
            lost_label = lost_font.render("You Lost!!", 1, (255, 255, 255))
            cred_label = lost_font.render(
                f"You won {won_money} credits !!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))
            WIN.blit(cred_label, (WIDTH/2 - cred_label.get_width()/2, 500))
            life_bonus = 0
            vel_bonus = 0
            updateBonus(vel_bonus, life_bonus)
            updateCredits(money)

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        son.play(loops=-1, maxtime=0, fade_ms=0)
        son.set_volume(0.1)
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            i = 0
            level += 1
            wave_length += 2
            # Mettre tout ca dans un if pour les différents niveaux
            if level % 3 == 0:
                for i in range(wave_length):
                    random_chances = random.randrange(0, 100)
                    if random_chances % 4 == 0:
                        enemy = Enemy(random.randrange(
                            50, WIDTH-100), random.randrange(-1500, -100), "7", 100, 1, 20)
                    elif random_chances % 2 == 0:
                        enemy = Enemy(random.randrange(
                            50, WIDTH-100), random.randrange(-1500, -100), "8", 100, 1, 30)
                    else:
                        enemy = Enemy(random.randrange(
                            50, WIDTH-100), random.randrange(-1500, -100), "9", 100, 1, 40)
                    enemies.append(enemy)
                    i += 1
            elif level % 2 == 0:
                for i in range(wave_length):
                    random_chances = random.randrange(0, 100)
                    if random_chances % 4 == 0:
                        enemy = Enemy(random.randrange(
                            50, WIDTH-100), random.randrange(-1500, -100), "4", 100, 1, 20)
                    elif random_chances % 2 == 0:
                        enemy = Enemy(random.randrange(
                            50, WIDTH-100), random.randrange(-1500, -100), "5", 100, 1, 30)
                    else:
                        enemy = Enemy(random.randrange(
                            50, WIDTH-100), random.randrange(-1500, -100), "6", 100, 1, 40)
                    enemies.append(enemy)
                    i += 1
            elif level % 1 == 0:
                for i in range(wave_length):
                    random_chances = random.randrange(0, 100)
                    if random_chances % 4 == 0:
                        enemy = Enemy(random.randrange(
                            50, WIDTH-100), random.randrange(-1500, -100), "1", 100, 1, 20)
                    elif random_chances % 2 == 0:
                        enemy = Enemy(random.randrange(
                            50, WIDTH-100), random.randrange(-1500, -100), "2", 100, 1, 30)
                    else:
                        enemy = Enemy(random.randrange(
                            50, WIDTH-100), random.randrange(-1500, -100), "3", 100, 1, 40)
                    enemies.append(enemy)
                    i += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                life_bonus = 0
                vel_bonus = 0
                updateCredits(money)
                updateBonus(vel_bonus, life_bonus)
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    life_bonus = 0
                    vel_bonus = 0
                    updateCredits(money)
                    updateBonus(vel_bonus, life_bonus)
                    main_menu()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:  # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:  # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:  # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move()
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        if player.move_lasers(-laser_vel, enemies) == 1:
            money += 10


def select_ship():
    global select_ship_player
    money = getCredits()
    main_font = pygame.font.SysFont("comicsans", 70)
    back_font = pygame.font.SysFont("comicsans", 30)
    run = True
    # Les boutons
    select_ship_1 = button((255, 255, 255), 550, 150, 150, 50, 'Select')
    select_ship_2 = button((255, 255, 255), 550, 350, 150, 50, 'Select')
    select_ship_3 = button((255, 255, 255), 550, 550, 150, 50, 'Select')

    def redraw_window():
        select_ship_1.draw(WIN, (0, 0, 0))
        select_ship_2.draw(WIN, (0, 0, 0))
        select_ship_3.draw(WIN, (0, 0, 0))
        money_label = back_font.render(f"Credits: {money}", 1, (255, 255, 255))
        WIN.blit(money_label, (10, 10))
    while run:
        WIN.blit(BG2, (0, 0))
        WIN.blit(STANDARD_SPACE_SHIP, (230, 150))
        WIN.blit(XWING_SPACE_SHIP, (220, 330))
        WIN.blit(BADASS_SPACE_SHIP, (200, 500))
        # les titres
        title_label = main_font.render("Select Ship Menu", 1, (255, 255, 255))
        back_label = back_font.render(
            "Hit space to go back to main menu", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 30))
        WIN.blit(back_label, (WIDTH/2 - back_label.get_width()/2, 700))
        redraw_window()
        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                updateCredits(money)
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


def select_bonus():
    global life_bonus
    global vel_bonus
    money = getCredits()
    main_font = pygame.font.SysFont("comicsans", 70)
    back_font = pygame.font.SysFont("comicsans", 30)
    run = True
    select_life_bonus = button((255, 255, 255), 550, 250, 180, 50, 'Buy One')
    select_dmg_bonus = button((255, 255, 255), 550, 450, 180, 50, 'Buy One')

    def redraw_window():
        select_life_bonus.draw(WIN, (0, 0, 0))
        select_dmg_bonus.draw(WIN, (0, 0, 0))
        life_label = main_font.render(f"x{life_bonus}", 1, (255, 255, 255))
        vel_label = main_font.render(f"x{vel_bonus}", 1, (255, 255, 255))
        money_label = back_font.render(f"Credits: {money}", 1, (255, 255, 255))
        WIN.blit(money_label, (10, 10))
        WIN.blit(life_label, (450, 250))
        WIN.blit(vel_label, (450, 450))
    while run:
        WIN.blit(BG2, (0, 0))
        WIN.blit(LIFE_BONUS, (230, 230))
        WIN.blit(RAGE_BONUS, (230, 420))
        title_label = main_font.render("Select Bonus Menu", 1, (255, 255, 255))
        price_label = back_font.render("50 credits each", 1, (255, 255, 255))
        back_label = back_font.render(
            "Hit space to go back to main menu", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 100))
        WIN.blit(price_label, (WIDTH/2 - price_label.get_width()/2, 160))
        WIN.blit(back_label, (WIDTH/2 - back_label.get_width()/2, 600))
        redraw_window()
        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                updateCredits(money)
                updateBonus(vel_bonus, life_bonus)
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    updateBonus(vel_bonus, life_bonus)
                    updateCredits(money)
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if select_life_bonus.isOver(pos):
                    life_bonus += 1
                    money -= 50
                if select_dmg_bonus.isOver(pos):
                    vel_bonus += 1
                    money -= 50
    pygame.quit()


def info_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    second_font = pygame.font.SysFont("comicsans", 50)
    third_font = pygame.font.SysFont("comicsans", 30)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("How to Play Doom", 1, (255, 255, 255))
        one_label = second_font.render(
            "Press Q to go left", 1, (255, 255, 255))
        two_label = second_font.render(
            "Press D to go right", 1, (255, 255, 255))
        three_label = second_font.render(
            "Press A to go up", 1, (255, 255, 255))
        four_label = second_font.render(
            "Press S to go down", 1, (255, 255, 255))
        five_label = second_font.render(
            "Press SPACE to SHOOT !", 1, (255, 255, 255))
        six_label = second_font.render("ENJOY !", 1, (255, 255, 255))
        end_label = third_font.render(
            "Press Esc to come back to main Menu", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 50))
        WIN.blit(one_label, (WIDTH/2 - one_label.get_width()/2, 150))
        WIN.blit(two_label, (WIDTH/2 - two_label.get_width()/2, 250))
        WIN.blit(three_label, (WIDTH/2 - three_label.get_width()/2, 350))
        WIN.blit(four_label, (WIDTH/2 - four_label.get_width()/2, 450))
        WIN.blit(five_label, (WIDTH/2 - five_label.get_width()/2, 550))
        WIN.blit(six_label, (WIDTH/2 - six_label.get_width()/2, 650))
        WIN.blit(end_label, (WIDTH/2 - end_label.get_width()/2, 700))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
    pygame.quit()


def main_menu():
    doom_font = pygame.font.SysFont("comicsans", 150)
    title_font = pygame.font.SysFont("comicsans", 70)
    second_font = pygame.font.SysFont("comicsans", 50)
    third_font = pygame.font.SysFont("comicsans", 30)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        doom_label = doom_font.render("DOOM", 1, (255, 0, 0))
        title_label = title_font.render(
            "Press the mouse to begin...", 1, (255, 255, 255))
        select_label = second_font.render(
            "Press A to select a ship.", 1, (255, 255, 255))
        bonus_label = second_font.render(
            "Press E to select bonuses.", 1, (255, 255, 255))
        info_label = second_font.render(
            "Press I to get Informations.", 1, (255, 255, 255))
        end_label = third_font.render(
            "Press Esc to come back to main Menu", 1, (255, 255, 255))
        WIN.blit(doom_label, (WIDTH/2 - doom_label.get_width()/2, 80))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 250))
        WIN.blit(select_label, (WIDTH/2 - select_label.get_width()/2, 350))
        WIN.blit(bonus_label, (WIDTH/2 - bonus_label.get_width()/2, 450))
        WIN.blit(info_label, (WIDTH/2 - info_label.get_width()/2, 550))
        WIN.blit(end_label, (WIDTH/2 - end_label.get_width()/2, 650))
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
                if event.key == pygame.K_i:
                    info_menu()
    pygame.quit()


main_menu()
