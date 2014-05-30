import pygame
import player
import creep
import combat


class Game(object):
    running = True

    def __init__(self, size):
        pygame.init()
        self.screen = pygame.display.set_mode(size)

    def main(self):
        clock = pygame.time.Clock()

        background = pygame.image.load('background.jpg')
        
        self.creeps = []

        self.player = player.Player(self.screen, (50, 50), (200, 200), 0.1)

        self.creeps.append(creep.Creep(self.screen, (150, 150), (200, 200), 0.1))


        while self.running:
            time = clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return


            self.screen.blit(background, (0, 0))
            self.player.update()
            self.player.blitme()

            for c in self.creeps:
                c.update(time, self.player)
                c.blitme()

            pygame.display.flip()


if __name__ == '__main__':
    Game((600, 600)).main()
