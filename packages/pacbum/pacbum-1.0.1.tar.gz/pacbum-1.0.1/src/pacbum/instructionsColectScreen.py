#! /usr/bin/env python
import pygame
import time
from pacbum.colectScreen import *
from pacbum.background import *
from pygame.locals import *
from pacbum.menuPacBum import *
from sys import exit

#Inicializa o menu principal
def instructionsColectScreen():



    #inicializa os objetos do menu principal
    pygame.font.init()
    screen = pygame.display.set_mode((1300, 700), 0, 32)
    pygame.display.set_caption('PAC BUM! > Instructions ColectScreen')

    #Definição do background.
    bg = background()
    bg.image = "images/bg_instructions_pb.png"
    bg.rect = [0,0,1300,1300]

    #Clock e laço de update do menu principal
    clock = pygame.time.Clock()

    menu = True
    while menu:

        #Desenha o plano de fundo.
        draw_background(screen, bg)


        #Habilita que a janela seja fechada pelo "x"
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()


        #Habilita os controles do jogo pelo teclado
        pressed_keys = pygame.key.get_pressed()

        #Comandos da seta de controle do menu principal

        #Confrima opção
        if pressed_keys[K_SPACE]:
            colectScreen()

        #Atualização dos objetos na tela
        pygame.display.update()

        #Clock máximo do uptade
        time_passed = clock.tick(30)
