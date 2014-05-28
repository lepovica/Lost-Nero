import pygame
import player


class Game(object):
    running = True

    def __init__(self, size):
        pygame.init()
        self.screen = pygame.display.set_mode(size)

    def main(self):
        clock = pygame.time.Clock()

        background = pygame.image.load('background.jpg')
        sprites = pygame.sprite.Group()
        self.player = player.Player(sprites)

        while self.running:
            time = clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            sprites.update()
            self.screen.blit(background, (0, 0))
            sprites.draw(self.screen)
            pygame.display.flip()


if __name__ == '__main__':
    Game((600, 600)).main()
