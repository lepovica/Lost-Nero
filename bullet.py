import pygame
from pygame.sprite import Sprite
from vec2d import vec2d

class Bullet(Sprite):

    def __init__(self, target, pos, img_file):
        Sprite.__init__(self)
        self.pos = vec2d(pos)
        self.base_image = img_file
        self.image = self.base_image
        self.speed = 0.5
        self.target = target
        self.state = self.MOVING

    (MOVING, DEAD) = range(2)

    def update(self, time_passed):
        if (self.target.pos.x - self.pos.x)**2 + (self.target.pos.y - self.pos.y)**2 <= 10**2:
            self.state = self.DEAD
        else:
            self.change_direction()
            self.move(time_passed)
            self.rotate_image()
            

    def change_direction(self):
        self.direction = self.get_direction(self.target.pos)


    def get_direction(self, wanted_pos):
        dx = self.pos.x - wanted_pos.x
        dy = self.pos.y - wanted_pos.y
        return vec2d(-dx, -dy).normalized()

    def rotate_image(self):
        self.image = pygame.transform.rotate(
            self.base_image, -self.direction.angle)

    def move(self, time_passed):
        displacement = vec2d(
            self.direction.x * self.speed * time_passed,
            self.direction.y * self.speed * time_passed)

        self.pos += displacement