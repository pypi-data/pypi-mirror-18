#! /usr/bin/env python
import pygame
import time
from datetime import datetime
import pacbum.menuPacBum
from FGAme import *
from pacbum.pacBum import *
from pacbum.textClass import *
from pacbum.environment2 import *
from pacbum.background import *
from pacbum.objects import *
from pygame.locals import *
from sys import exit

def time_end(time_for_game, pacbum):

    if time_for_game >= 60:
        pacbum.position = [3000, 3000]
        return True
    else:
        return False

def animation_water(screen, world):

    animation_obj2(world.objects[8])
    screen.blit(world.objects[8].pygameS,(world.objects[8].position),world.objects[8].rect)

def colectScreen_2(pacbum):

    #Inicializa a tela.
    pygame.font.init()
    screen = pygame.display.set_mode((1260, 840), 0, 32)
    pygame.display.set_caption('PAC BUM! > Fase 2')

    #Inicializa o plano de fundo.
    bg = background()
    bg.image = "images/bg_colect_screen_2.png"
    bg.rect[0] = 1890

    #Inicializa o som da fase
    bg_sound_phase = play("Spooky-Island")

    #Inicializa os textos da tela
    text_list = list()
    title = textScreen()
    title.text  = "Fase 2 - Periodo Jurassico"
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
    world = environment2()
    PacBum = pacbum
    PacBum.gravity = world.gravity
    PacBum.image = 'images/suit_pc_fw.png'
    PacBum.pygameS = pygame.image.load(PacBum.image).convert_alpha()
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

    #Life screen colect 2
    lifes = obj_game()
    lifes.image = "images/life_c2_pb.png"
    lifes.pygameS = pygame.image.load(lifes.image).convert_alpha()
    lifes.inScreen = False
    lifes.position = [1500, 600]
    lifes.rect = [0,0,125,125]
    lifes.mass = 100
    lifes.split_range = 10
    lifes.who_touch = "life"
    lifes.vel_in_x = 5

    #Super points collect 2
    super_points_c2_pb = obj_game()
    super_points_c2_pb.image = "images/super_points_c2_pb.png"
    super_points_c2_pb.pygameS = pygame.image.load(super_points_c2_pb.image).convert_alpha()
    super_points_c2_pb.inScreen = False
    super_points_c2_pb.position = [1500, 600]
    super_points_c2_pb.rect = [0,0,125,125]
    super_points_c2_pb.mass = 300
    super_points_c2_pb.split_range = 10
    super_points_c2_pb.who_touch = "spoint"
    super_points_c2_pb.vel_in_x = 5

    #riacho
    water = obj_game()
    water.image = "images/water_c2_pb.png"
    water.pygameS = pygame.image.load(water.image).convert_alpha()
    water.inScreen = False
    water.position = [0, 670]
    water.rect = [0,0,3774,64]
    water.mass = 50
    water.split_range = 20
    water.who_touch = "nothing"
    water.vel_in_x = 5

    #Pedra de fogo
    firestone = obj_game()
    firestone.image = "images/fire_stone_c2_pb.png"
    firestone.pygameS = pygame.image.load(firestone.image).convert_alpha()
    firestone.inScreen = False
    firestone.position = [1500, 550]
    firestone.mass = 200
    firestone.rect = [0,0,125,125]
    firestone.split_range = 5
    firestone.who_touch = "firestone"
    firestone.vel_in_x = 5

    #Bomba de coco
    coconutbomb = obj_game()
    coconutbomb.image = "images/coconut_bomb_c2_pb.png"
    coconutbomb.pygameS = pygame.image.load(coconutbomb.image).convert_alpha()
    coconutbomb.inScreen = False
    coconutbomb.mass = 10
    coconutbomb.position = [1500, 550]
    coconutbomb.rect = [0,0,125,125]
    coconutbomb.split_range = 5
    coconutbomb.who_touch = "bomb"
    coconutbomb.vel_in_x = 5

    #veneno de coco
    coconutvenom = obj_game()
    coconutvenom.image = "images/coconut_venom_c2_pb.png"
    coconutvenom.pygameS = pygame.image.load(coconutvenom.image).convert_alpha()
    coconutvenom.inScreen = False
    coconutvenom.mass = 10
    coconutvenom.position = [1500, 550]
    coconutvenom.rect = [0,0,125,125]
    coconutvenom.split_range = 5
    coconutvenom.who_touch = "venon"
    coconutvenom.vel_in_x = 5

    #alien
    alien = obj_game()
    alien.image = "images/alien_c2_pb.png"
    alien.pygameS = pygame.image.load(alien.image).convert_alpha()
    alien.inScreen = False
    alien.mass = 10
    alien.position = [1500, 550]
    alien.rect = [0,0,125,125]
    alien.split_range = 5
    alien.who_touch = "alien"
    alien.vel_in_x = 5

    #explosao
    explos = obj_game()
    explos.image = "images/coconut_venom_c2_pb.png"
    explos.pygameS = pygame.image.load(explos.image).convert_alpha()
    explos.inScreen = False
    explos.mass = 10
    explos.position = [1500, 550]
    explos.rect = [0,0,125,125]
    explos.split_range = 5
    explos.who_touch = "venon"
    explos.vel_in_x = 5

    #dino anfíbio
    dino = obj_game()
    dino.image = "images/amphibian_dino_c2_pb.png"
    dino.pygameS = pygame.image.load(dino.image).convert_alpha()
    dino.inScreen = False
    dino.mass = 10
    dino.position = [1500, 550]
    dino.rect = [0,0,125,125]
    dino.split_range = 5
    dino.who_touch = "dino"
    dino.vel_in_x = 5

    add_objects2(world, lifes)
    add_objects2(world, super_points_c2_pb)
    add_objects2(world, firestone)
    add_objects2(world, coconutbomb)
    add_objects2(world, coconutvenom)
    add_objects2(world, alien)
    add_objects2(world, dino)
    add_objects2(world, explos)
    add_objects2(world, water)
    add_objects2(world, flagdead)
    add_objects2(world, flagnextlevel)
    obj_inScreen2(world)


    #Clock e laço de update da faze
    clock = pygame.time.Clock()

    #Pega um tempo inicial
    time_for_game = 0
    time_now  = datetime.now()
    second = time_now.second
    aux = second + 1
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
        draw_and_update_objects2(screen, world)
        animation_water(screen, world)

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
            forward_colectScreen2(PacBum)

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
            backward_colectScreen2(PacBum)

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

            if PacBum.position[1] != 450:
                PacBum.position[1] = 450
                PacBum.vel_in_x = 10
            else:
                pass

        #DESCER
        if pressed_keys[K_DOWN]:

            if PacBum.position[1] != 570:
                PacBum.position[1] = 570
                PacBum.vel_in_x = 10
            else:
                pass

        #VOLTAR PARA O MENU
        if pressed_keys[K_r]:
            bg_sound_phase.stop()
            menuPacBum.mainMenu()

        #update da cena
        pygame.display.update()
        update_colisions2(world, PacBum)

        #Faz um update para o proximo laço
        time_now  = datetime.now()
        second = time_now.second


        #clock máximo do update
        time_passed = clock.tick(30)

    menuPacBum.mainMenu()