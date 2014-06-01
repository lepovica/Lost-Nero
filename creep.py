import pygame
from pygame.sprite import Sprite
from random import randint

from vec2d import vec2d
import math


class Creep(Sprite):

    def __init__(self, screen, field, init_position, init_direction, speed):
        Sprite.__init__(self)
        self.name = 'Creep'

        self.base_image = pygame.image.load('creep.png')
        self.image = self.base_image
        self.screen = screen
        self.field = field

        self.pos = vec2d(init_position)
        self.direction = vec2d(init_direction).normalized()
        self.speed = speed

        self.isAlive = True

        self.armor = 100

        self.attack_power = 10
        self.deffence_power = 5

        self.life = 100
        self.image_w, self.image_h = self.image.get_size()

    def update(self, time_passed, target):
        if self.isAlive == True:
            if self.check_target(target.pos):
                self.get_direction(target.pos)
            else:
                self.change_direction(target, time_passed)

            self.rotate_image()
            self.move(time_passed)

            self.image_w, self.image_h = self.image.get_size()
            bounds_rect = self.field.inflate(-self.image_w, -self.image_h)

            if self.pos.x < bounds_rect.left:
                self.pos.x = bounds_rect.left
                self.direction.x *= -1
            elif self.pos.x > bounds_rect.right:
                self.pos.x = bounds_rect.right
                self.direction.x *= -1
            elif self.pos.y < bounds_rect.top:
                self.pos.y = bounds_rect.top
                self.direction.y *= -1
            elif self.pos.y > bounds_rect.bottom:
                self.pos.y = bounds_rect.bottom
                self.direction.y *= -1
        if self.isAlive == False:
            if pygame.time.get_rawtime() - self.reborn_time > 30:
                self.reborn()

    _counter = 0

    def change_direction(self, target, time_passed):
        self._counter += time_passed
        if self._counter > randint(400, 500):
            self.direction.rotate(45 * randint(-1, 1))
            self._counter = 0

    def check_target(self, target):
        if 10 ** 2 <= (target.x - self.pos.x) ** 2 + (target.y - self.pos.y) ** 2 <= 50 ** 2:
            print("ZOMBIE")
            return True
        return False

    def rotate_image(self):
        self.image = pygame.transform.rotate(
            self.base_image, -self.direction.angle)

    def move(self, time_passed):
        displacement = vec2d(
            self.direction.x * self.speed * time_passed,
            self.direction.y * self.speed * time_passed)

        self.pos += displacement

    def get_direction(self, wanted_pos):
        dx = self.pos.x - wanted_pos.x
        dy = self.pos.y - wanted_pos.y
        self.direction = vec2d(-dx, -dy).normalized()

    def draw(self):
        print("{0} : {1}".format(self.name, self.pos))
        draw_rect = self.image.get_rect().move(
            self.pos.x - self.image_w / 2,
            self.pos.y - self.image_h / 2)
        self.screen.blit(self.image, self.pos)

    def Attack(self, target):
        damage = self.attack_power - target.deffence_power
        if damage > 0:
            target.deffence(damage)
            # return Hit and damage for display event
        else:
            target.deffence(0)
            # return Ressist ----//----

    def deffence(self, damage):
        if damage > 0:
            self.life -= damage
            if self.life <= 0:
                self.kill()

    def kill(self):
        self.isAlive = False
        self.life = 0
        self.image = pygame.image.load('dead_player.png').convert_alpha()
        self.reborn_time = pygame.time.get_rawtime()

    def reborn(self):
        self.isAlive = True
        self.life = self.max_life
        self.image = pygame.image.load('creep.png').convert_alpha()
