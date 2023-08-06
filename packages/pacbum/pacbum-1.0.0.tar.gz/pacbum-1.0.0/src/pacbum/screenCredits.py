#! /usr/bin/env python
import pygame
import time
from pacbum.background import *
from pacbum.textClass import *
import pacbum.menuPacBum
from pygame.locals import *
from sys import exit



#Cria a tela dos créditos
def screenCredits():

    #Inicia os objetos na tela de créditos
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1300, 700), 0, 32)
    pygame.display.set_caption('PAC BUM! > Creditos')

    #Definição do background.
    bg = background()
    bg.image = "images/bg_credits_pb.png"
    bg.rect = [0,0,1300,1300]


    #Laço de update da tela de cŕeditos
    clock = pygame.time.Clock()
    while True:

        #Desenha o plano de fundo
        draw_background(screen, bg)


        #Habilita que a janela seja fechada no "x"
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        #Habilita que a janela retorne para o menu principal ao "ESC" ser teclado.
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_r]:
            menuPacBum.mainMenu()

        #Atualiza a tela de acordo com o laço principal
        pygame.display.update()
        #Clock máximo do update.
        time_passed = clock.tick(30)

#screenCredits()

