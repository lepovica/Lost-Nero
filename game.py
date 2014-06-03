import pygame
from player import Player
from creep import Creep
import combat
import sys



def run_game():
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
    crp = Creep(screen, field_rect, (450, 450), (1, 1), 0.05, img_creep,
                img_creep_dead)

    creeps.add(crp)

    for i in range(10):
        creeps.add(Creep(screen, field_rect, (150, 150), (1, 1), 0.05, 
            img_creep, img_creep_dead))

    while True:
        time_passed = clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            for crep in creeps:
                if crep.mouse_click(pygame.mouse.get_pos()):
                    combat.player_start_battle(playa, crep, time_passed)
                else:
                    playa.moving(pygame.mouse.get_pos())
                # crep.mouse_click(pygame.mouse.get_pos(), playa, time_passed)

        screen.blit(background, (0, 0))

        playa.update(time_passed)
        playa.draw()

        for crep in creeps:
            crep.update(time_passed, playa)
            crep.draw()
        pygame.display.flip()


def exit_game():
    sys.exit()


run_game()
