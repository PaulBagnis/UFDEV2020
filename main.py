import pygame
import os
import time
import random

from classes import *
from functions import *

mydb = mysql.connector.connect(host="localhost", user="root", passwd="", db="doom")
mycursor = mydb.cursor()

def main() :
    print("Tout marche !")
    moe = Player(100, 100)
    moe2 = Enemy(100, 100)
    moe3 = Boss(100, 100)

    scores = getScores()
    for score in scores :
        print(score)
    
main()