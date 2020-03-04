#!/usr/bin/env python3

import sys
import pygame
import time
import random


#variables globales => elles sont utilisables dans toutes les fonctions sans avoir besoin de les mettre en argument
#Cette variable permettra de gerer la difficulté du jeu, elle varie entre 1 et 10
DIFFICULTY = 1


#taille de départ du serpent
START_LENGTH = 10

#vitesse du jeu plus la difficulté sera elevée, plus le jeu sera rapide
WAIT	= 0.1 / DIFFICULTY


RADIUS	= 10

#taille de la fenêtre
RES	= [800, 600]

WALL	= []

BUG     = ()

#initialisation de pygame, création d'une fenêtre (ici nommé "snake")
pygame.init()
SCREEN = pygame.display.set_mode(RES)
pygame.display.set_caption("Snake")


#creation du classe Joueur => elle permet de reunir toutes les fonctions propre a ce dernier comme son 
#initialisation, sa mort, ses déplacements ...
class Mob():
    #initailisation du joueur
    def __init__(self):
        #coordonnées x et y => position de la tête sur la map
        self.headx = 100
        self.heady = 100
        #Taille du serpent
        self.length = START_LENGTH
        #tous les maillions du serpent
        self.elements = [[self.headx, self.heady]]

        #ajout de tous mes maillions du serpent
        while len(self.elements) != (self.length - 1):
            self.elements.append([self.headx, self.heady])
        #orientation du joueur
        self.rotate = [RADIUS * 2, 0]
        #affichage de la tête sur la fenêtre
        pygame.draw.circle(SCREEN, (255, 255, 0), (self.headx, self.heady),
            RADIUS)
        pygame.display.flip()

        #fonnction de déplacement du joueur
    def move(self):
        pygame.draw.circle(SCREEN, (0, 0, 0), (self.elements[-1][0],
            self.elements[-1][1]), RADIUS)
        self.elements.pop()
        self.headx += self.rotate[0]
        self.heady += self.rotate[1]
        self.elements = [[self.headx, self.heady]] + self.elements[0:]
        self.check_dead()
        #affichage de tous les maillons du serpent
        for element in self.elements[1:]:
            pygame.draw.circle(SCREEN, (255, 255, 0), (element[0], element[1]),
                RADIUS)
        #affichage de la tête du serpent
        pygame.draw.circle(SCREEN, (0, 255, 0), (self.headx, self.heady),
            RADIUS)
        #affichage à l'écran
        pygame.display.flip()
        self.check_bug()

        #vérification de la mort du joueur
    def check_dead(self):
        if [self.headx, self.heady] in self.elements[1:]:
            exit_dead()
        if [self.headx, self.heady] in WALL:
            exit_dead()

        #vérification permettant de savoir si la tête du serpent est sur une pomme 
    def check_bug(self):
        if (self.headx, self.heady) == BUG:
            self.elements.append(self.elements[-1])
            create_bug()


#Comme son nom l'indique, cette fonction permet de dessiner la map a l'écran
def draw_map():
    for n in range(20, RES[0], 20):
        pygame.draw.circle(SCREEN, (0, 0, 255), (n, 20), 10)
        WALL.append([n, 20])
        pygame.draw.circle(SCREEN,(0, 0, 255),(n, RES[1] - 20), 10)
        WALL.append([n, RES[1] - 20])
    for n in range(20, RES[1], 20):
        pygame.draw.circle(SCREEN, (0, 0, 255),(20, n), 10)
        WALL.append([20, n])
        pygame.draw.circle(SCREEN, (0, 0, 255), (RES[0] - 20, n), 10)
        WALL.append([RES[0] - 20 , n])
    pygame.display.flip()

#fonction permettant de créer un pomme et de la placer aléatoirement sur la map
def create_bug():
    global BUG
    BUG = ()
    while ( list(BUG) in WALL ) or ( list(BUG) in SNAKE.elements) or (not BUG):
        BUG = (random.randrange(40, RES[0] - 40 , 20),
            (random.randrange(40, RES[1] - 40 , 20)))
    #on dessine la pomme
    pygame.draw.circle(SCREEN, (255, 0, 0), BUG, RADIUS)
    #et on l'affiche a l'ecran
    pygame.display.flip()

#boucle principale du jeu, c'est elle qui va tourner indéfiniment tant que le joueur n'a pas perdu/gagné
def event_loop():
    while True:
        #pause permettant la vitesse du jeu ici la variable WAIT est calculé grâce a la fifficulté (voir en haut du fichier)
        time.sleep(WAIT)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #on regarde quelle commande est capté
            #si c'est une flche directionelle on modifie la vitesse
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_DOWN)	and \
                    (SNAKE.rotate != [0, -2*RADIUS]):
                    #on verifie que le joueur n'avance pas deja dans la direction contraire
                    #puis on indique sa nouvelle direction;
                    #on fait la même chose pour les 3 fleches directionelles restantes
                    SNAKE.rotate = [0, 2*RADIUS]
                elif (event.key == pygame.K_UP) and \
                    (SNAKE.rotate != [0, 2*RADIUS]):
                    SNAKE.rotate = [0, -2*RADIUS]
                elif (event.key == pygame.K_RIGHT) and \
                    (SNAKE.rotate != [-2* RADIUS, 0]):
                    SNAKE.rotate = [2*RADIUS, 0]
                elif (event.key == pygame.K_LEFT) and \
                    (SNAKE.rotate != [2* RADIUS, 0]):
                    SNAKE.rotate = [-2*RADIUS, 0]
                #On quitte si on appuie sur echap => fin du jeu
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        #on a appelle la fonction move du joueur afin de le mettre a jour et l'afficher 
        SNAKE.move()

#fin du jeu / mort du joueur
def exit_dead():
    #affichage des stats de la parties sur le terminal
    print("Difficulty:\t%d" % DIFFICULTY)
    print("Bugs eaten:\t%d" % (len(SNAKE.elements) - START_LENGTH + 1))
    print("Score:\t\t%d" % ((len(SNAKE.elements) - START_LENGTH + 1) * DIFFICULTY))
    time.sleep(1)
    pygame.quit()
    sys.exit()
    
#fonction principale
if __name__ == "__main__":
    #creation de la map
    draw_map()
    #creation du joueur
    SNAKE = Mob()
    #creation d'une pomme
    create_bug()
    #boucle principale du jeu
    event_loop()
