#! /usr/bin/env python
import pygame
import time
#não esquecer de recolocar os "pacbum.algumacoisa" antes dos imports!
from pacbum.menuArrow import *
from FGAme import *
from pacbum.colectScreen import *
from pacbum.screenCredits import *
from pacbum.background import *
from pygame.locals import *
from sys import exit

#Inicializa o menu principal
def mainMenu():

    rodar  = pygame
    rodar.init()
    bg_sound = play("Blob-Monsters-on-the-Loose")

    #inicializa os objetos do menu principal
    pygame.font.init()
    screen = pygame.display.set_mode((1300, 700), 0, 32)
    pygame.display.set_caption('PAC BUM! > Menu Principal')

    #Definição do background.
    bg = background()
    bg.image = "images/bg_menu_pb.png"
    bg.rect = [0,0,1300,1300]



    init = pygame.image.load('images/start_bt.png').convert_alpha()
    options = pygame.image.load('images/options_bt.png').convert_alpha()
    credits = pygame.image.load('images/credits_bt.png').convert_alpha()
    exit = pygame.image.load('images/exit_bt.png').convert_alpha()


    #textos que aparecem no menu principal
    list_text = list()
    textVersion = textScreen()
    textVersion.text = "V - 0.1.5"
    textVersion.pygamePosition = [1210,675]
    add_text(list_text, textVersion)

    arrow = 0
    #Clock e laço de update do menu principal
    clock = pygame.time.Clock()

    menu = True
    while menu:

        #Desenha o plano de fundo.
        draw_background(screen, bg)

        if arrow == 0:
            screen.blit(init,(500,325),[300,0,300,300])
        else:
            screen.blit(init,(500,325),[0,0,300,300])

        if arrow == 1:
            screen.blit(options,(475, 425),[300,0,300,300])
        else:
            screen.blit(options,(475, 425),[0,0,300,300])

        if arrow == 2:
            screen.blit(credits,(480, 525),[300,0,300,300])
        else:
            screen.blit(credits,(480, 525),[0,0,300,300])

        if arrow == 3:
            screen.blit(exit,(525, 625),[300,0,300,300])
        else:
            screen.blit(exit,(525, 625),[0,0,300,300])

        #Desenha os textos da tela.
        draw_text(screen, list_text)

        #Habilita que a janela seja fechada pelo "x"
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()


        #Habilita os controles do jogo pelo teclado
        pressed_keys = pygame.key.get_pressed()

        #Comandos da seta de controle do menu principal
        #Para cima
        if pressed_keys[K_UP]:
            select_sound = play("UI_Quirky27")
            arrow -= 1
            time.sleep(1/7)
            if arrow < 0:
                arrow = 3


        #Para baixo
        if pressed_keys[K_DOWN]:
            select_sound = play("UI_Quirky27")
            arrow += 1
            time.sleep(1/7)
            if arrow > 3:
                arrow = 0

        #Confrima opção
        if pressed_keys[K_RETURN]:
            play("PowerUp10")
            if arrow == 0:
                bg_sound.stop()
                colectScreen()
                menu = False
            elif arrow == 1:
                print('1')
            elif arrow == 2:
                bg_sound.stop()
                screenCredits()
                menu = False
            if arrow == 3:
                menu = False
                pygame.quit()
                exit()

        #Atualização dos objetos na tela
        pygame.display.update()

        #Clock máximo do uptade
        time_passed = clock.tick(30)


#mainMenu()