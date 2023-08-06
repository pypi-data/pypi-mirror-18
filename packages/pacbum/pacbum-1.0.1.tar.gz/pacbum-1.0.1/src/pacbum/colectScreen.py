#! /usr/bin/env python
import pygame
import time
from datetime import datetime
import pacbum.menuPacBum
from FGAme import *
from pacbum.pacBum import *
from pacbum.textClass import *
from pacbum.environment import *
from pacbum.background import *
from pacbum.objects import *
from pacbum.colectScreen_2 import *
from pygame.locals import *
from sys import exit


def time_end(time_for_game, pacbum):

    if time_for_game >= 60:
        pacbum.position = [3000, 3000]
        return True
    else:
        return False


# cria a faze
def colectScreen():

    #Inicializa a tela.
    pygame.font.init()
    screen = pygame.display.set_mode((1260, 840), 0, 32)
    pygame.display.set_caption('PAC BUM! > Fase 1')

    #Inicializa o plano de fundo.
    bg = background()
    bg.image = "images/bg_colect_screen.png"
    bg.rect[0] = 1890


    #Inicializa os textos da tela
    text_list = list()
    title = textScreen()
    title.text  = "Fase 1 - Velho Oeste"
    title.pygamePosition = [50,755]


    score = textScreen()
    score.pygamePosition = [450,750]

    vidas = textScreen()
    vidas.pygamePosition = [450, 775]

    time_g = textScreen()
    time_g.pygamePosition = [450, 800]

    bombs = textScreen()
    bombs.pygamePosition = [650, 750]



    add_text(text_list, vidas)
    add_text(text_list, title)
    add_text(text_list, score)
    add_text(text_list, bombs)
    add_text(text_list, time_g)

    #Inicializa os objetos da tela.
    world = environment()
    PacBum = pacBum()
    PacBum.gravity = world.gravity

    #Cow skull
    skull = obj_game()
    skull.image = "images/cow_skull.png"
    skull.pygameS = pygame.image.load(skull.image).convert_alpha()
    skull.inScreen = False
    skull.position = [1500, 600]
    skull.rect = [0,0,125,125]
    skull.mass = 100
    skull.split_range = 10
    skull.who_touch = "skull"
    skull.vel_in_x = 5

    #Pac bomb
    bomb = obj_game()
    bomb.image = "images/pac_bomb.png"
    bomb.pygameS = pygame.image.load(bomb.image).convert_alpha()
    bomb.inScreen = False
    bomb.position = [1500, 600]
    bomb.rect = [0,0,125,125]
    bomb.mass = 300
    bomb.split_range = 10
    bomb.who_touch = "bomb"
    bomb.vel_in_x = 5

    #Super points
    spoints = obj_game()
    spoints.image = "images/pac_super_points.png"
    spoints.pygameS = pygame.image.load(spoints.image).convert_alpha()
    spoints.inScreen = False
    spoints.position = [1500, 550]
    spoints.rect = [0,0,125,125]
    spoints.mass = 50
    spoints.split_range = 20
    spoints.who_touch = "spoint"
    spoints.vel_in_x = 5

    #Vida
    lifes = obj_game()
    lifes.image = "images/pac_life.png"
    lifes.pygameS = pygame.image.load(lifes.image).convert_alpha()
    lifes.inScreen = False
    lifes.position = [1500, 550]
    lifes.mass = 200
    lifes.rect = [0,0,125,125]
    lifes.split_range = 5
    lifes.who_touch = "life"
    lifes.vel_in_x = 5

    #Veneno
    venon = obj_game()
    venon.image = "images/pac_venon.png"
    venon.pygameS = pygame.image.load(venon.image).convert_alpha()
    venon.inScreen = False
    venon.mass = 10
    venon.position = [1500, 550]
    venon.rect = [0,0,125,125]
    venon.split_range = 5
    venon.who_touch = "venon"
    venon.vel_in_x = 5

    #Flag Dead Pacbum
    flagdead = obj_game()
    flagdead.image = "images/flag_dead.png"
    flagdead.pygameS  = pygame.image.load(flagdead.image).convert_alpha()
    flagdead.inScreen = False
    flagdead.position = [600, 100]

    #Flag Next Level
    flagnextlevel = obj_game()
    flagnextlevel.image = "images/flag_next_level.png"
    flagnextlevel.pygameS = pygame.image.load(flagnextlevel.image).convert_alpha()
    flagnextlevel.inScreen = False
    flagnextlevel.position = [600, 100]

    #1º Objeto => Nº 0
    add_objects(world, skull)
    #2º Objeto => Nº 1
    add_objects(world, bomb)
    #3º Objeto => Nº 2
    add_objects(world, spoints)
    #4º Objeto => Nº 3
    add_objects(world, lifes)
    #5º Objeto => Nº 4
    add_objects(world, venon)
    #6º Objeto => Nº 5
    add_objects(world, flagdead)
    #7º Objeto => Nº 6
    add_objects(world, flagnextlevel)

    add_friction(world, 0.007)
    add_friction(world, 0.001)

    obj_inScreen(world)
    #Clock e laço de update da faze
    clock = pygame.time.Clock()

    #Pega um tempo inicial
    time_for_game = 0
    time_now  = datetime.now()
    second = time_now.second
    aux = second + 1

    bg_sound_phase = play("Clunky-Old-Time-Piano")
    while True:

        #Desenha o plano de fundo
        draw_background(screen, bg)


        #Pega o tempo e atualiza

        if second == 0:
            aux = second + 1

        if second == aux:
            if time_for_game < 60:
                time_for_game += 1
                aux = second + 1

            else:
                time_for_game = 60

        #Define os textos atualizados
        score.text = "Score: " + str(int(PacBum.points))
        vidas.text = "Vidas: " + str(int(PacBum.lifes))
        time_g.text = "Tempo: " + str(int(time_for_game))
        bombs.text = "Bombas: " + str(int(PacBum.bombs))

        #Desenha os objetos na tela
        draw_text(screen, text_list)
        draw_pacbum(screen, PacBum)
        draw_and_update_objects(screen, world)

        #Confere se o pac bum está morto
        if pacbum_is_dead(PacBum):
            screen.blit(flagdead.pygameS,(300,200))
            bg_sound_phase.stop()

        #Confere o tempo
        if time_end(time_for_game, PacBum) and PacBum.dead is not True:
            screen.blit(flagnextlevel.pygameS,(300,200))
            if pressed_keys[K_SPACE]:
                bg_sound_phase.stop()
                PacBum.friction_tax = 0
                PacBum.position = [625,570]
                play("PowerUp10")
                break


        #Habilita que a tela seja fechada no "x"
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        #Habilita as teclas para o controle
        pressed_keys = pygame.key.get_pressed()

        #ANDAR PARA FRENTE
        if pressed_keys[K_RIGHT]:
            animation_pacBum(PacBum)
            forward_colectScreen(PacBum)

            #Atualiza a posição da camera
            #Mover a camera para frente
            if PacBum.position[0] > 1000:

                if bg.rect[0] < 2500:
                    bg.for_rect_background = PacBum.vel_in_x
                    bg.rect[0] += bg.for_rect_background
                else:
                    bg.rect[0] = 2500


        #ANDAR PARA TRÁS
        if pressed_keys[K_LEFT]:
            animation_pacBum(PacBum)
            backward_colectScreen(PacBum)

            #Atualiza a posição da camera
            #Mover a camera para trás
            if PacBum.position[0] < 300 :

                if bg.rect[0] > 100:
                    bg.for_rect_background = PacBum.vel_in_x
                    bg.rect[0] -= bg.for_rect_background
                else:
                    bg.rect[0] = 100

        #SUBIR
        if pressed_keys[K_UP]:

            if PacBum.position[1] != 470:
                PacBum.friction_tax = world.friction[1]
                PacBum.position[1] = 470
                PacBum.vel_in_x = 15

            else:
                pass

        #DESCER
        if pressed_keys[K_DOWN]:

            if PacBum.position[1] != 570:
                PacBum.friction_tax = world.friction[0]
                PacBum.position[1] = 570
                PacBum.vel_in_x = 15
            else:
                pass

        #VOLTAR PARA O MENU
        if pressed_keys[K_r]:
            bg_sound_phase.stop()
            menuPacBum.mainMenu()

        #update da cena
        pygame.display.update()
        update_colisions(world, PacBum)

        #Faz um update para o proximo laço
        time_now  = datetime.now()
        second = time_now.second


        #clock máximo do update
        time_passed = clock.tick(30)

    colectScreen_2(PacBum)



