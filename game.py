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

    creeps = pygame.sprite.Group()

    playa = Player(screen, field_rect, (50, 50), (0, 0), 0.07)
    # creeps.add(playa)
    crp = Creep(screen, field_rect, (150, 150), (1, 1), 0.05)
    creeps.add(crp)

    # for i in range(10):
    #     creeps.add(Creep(screen, field_rect, (150, 150), (1, 1), 0.05))

    while True:
        time_passed = clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

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
