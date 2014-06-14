import pygame
from player import Player
from creep import Creep
import combat
import sys
import random
import menu


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

    menu_entries = ("Start Game", "Load", "Save", "Quit")

    creeps = pygame.sprite.Group()

    playa = Player(screen, field_rect, (50, 50), (0, 0), 0.07, img_playa,
                   img_playa_dead)
    # creeps.add(playa)
    crp = Creep(screen, field_rect, (150, 150), (1, 1), 0.05, img_creep,
                img_creep_dead)

    creeps.add(crp)

    for i in range(5):
        creeps.add(Creep(screen, field_rect, (random.randint(50, 550),
                                              random.randint(50, 550)), (1, 1),
                                              0.05, img_creep, img_creep_dead))

    main_menu = menu.Menu(menu_entries)

    while True:
        time_passed = clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused

            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                flag = False
                for crep in creeps:
                    if crep.mouse_click(pygame.mouse.get_pos()):
                        flag = True
                        combat.Battle.player_start_battle(
                            playa, crep, time_passed)
                if flag == False:
                    playa.moving(pygame.mouse.get_pos())

        if not paused:
            main_menu.deactivate()
            screen.blit(background, (0, 0))

            for crep in creeps:
                crep.update(time_passed, playa)
                crep.draw(time_passed)

            playa.update(time_passed)
            playa.draw(time_passed)

            pygame.display.flip()

        else:
            main_menu.activate()
            main_menu.drawMenu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game()
                else:
                    event_text = main_menu.handleEvent(event)
                    if event_text == "Quit":
                        main_menu.deactivate()
                        exit_game()
                    elif event_text == "Start Game":
                        paused = not paused
                        main_menu.deactivate()
                        print("Start Gane")
                    else:
                        main_menu.deactivate()
                        pass
            pygame.display.flip()




def exit_game():
    sys.exit()


run_game()
