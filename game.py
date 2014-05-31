import pygame
from player import Player
from creep import Creep
import combat
import sys


def run_game():
    SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    FIELD_RECT = pygame.Rect(20, 20, 580, 580)
    clock = pygame.time.Clock()

    background = pygame.image.load('background.jpg').convert_alpha()
    playa_img = pygame.image.load("player.png").convert_alpha()
    creep_img = pygame.image.load("creep.png").convert_alpha()

    creeps = pygame.sprite.Group()

    playa = Player(screen, playa_img, FIELD_RECT, (50, 50), (0, 0), 0.05)
    creeps.add(playa)
    crp = Creep(screen, creep_img, FIELD_RECT, (150, 150), (0, 0), 0.05)
    creeps.add(crp)

    while True:
        time_passed = clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.blit(background, (0, 0))

        for crep in creeps:
            crep.update(time_passed, playa)
            crep.draw()
        pygame.display.flip()


def exit_game():
    sys.exit()


run_game()
