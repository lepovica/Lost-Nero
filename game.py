import pygame
from player import Player
from creep import Creep
import combat
import sys
from menu import *
import random


def run_game():
    flag = False
    paused = True
    SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    field_rect = pygame.Rect(20, 20, 580, 580)
    clock = pygame.time.Clock()

    background = pygame.image.load('background.jpg')

    img_playa = pygame.image.load('player.png')
    img_playa_dead = pygame.image.load('dead_player.png')
    img_creep = pygame.image.load('creep.png')
    img_creep_dead = pygame.image.load('dead_creep.png')

    creeps = pygame.sprite.Group()

    playa = Player(screen, field_rect, (50, 50), (0, 0), 0.07, img_playa,
                   img_playa_dead)
    # creeps.add(playa)
    crp = Creep(screen, field_rect, (150, 150), (1, 1), 0.05, img_creep,
                img_creep_dead)

    creeps.add(crp)

    for i in range(10):
        creeps.add(Creep(screen, field_rect, (random.randint(50, 550),
                                              random.randint(
                                                  50, 550)), (1, 1), 0.05,
                         img_creep, img_creep_dead))

    main_menu_items = ("Start Game", "Load Game", "Save Game", "Quit")

    main_menu = Menu(main_menu_items)
    main_menu.drawMenu()

    while True:
        time_passed = clock.tick(30)
        text = ""
        for event in pygame.event.get():
            text = main_menu.handleEvent(event)
            if event.type == pygame.QUIT:
                exit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused

            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                for crep in creeps:
                    if crep.mouse_click(pygame.mouse.get_pos()):
                        flag = True
                        combat.Battle.player_start_battle(
                            playa, crep, time_passed)
                    else:
                        flag = False

                if flag == False:
                    playa.moving(pygame.mouse.get_pos())

        if not paused:
            screen.blit(background, (0, 0))

            for crep in creeps:
                crep.update(time_passed, playa)
                crep.draw(time_passed)

            playa.update(time_passed)
            playa.draw(time_passed)

        else:
            main_menu.activate()
            main_menu.drawMenu()
            if text == "Quit":
                exit_game()
            elif text == "Start Game":
                paused = not paused
                main_menu.deactivate()
            elif text == "Load Game":
                pass
                # load_game()
            elif text == "Save Game":
                pass
                # save_game()

        pygame.display.flip()


def exit_game():
    sys.exit()


run_game()
