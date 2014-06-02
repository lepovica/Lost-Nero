import pygame
import combat
from pygame.sprite import Sprite
from random import randint

from vec2d import vec2d
import math


class Creep(Sprite):

    def __init__(self, screen, field, init_position, init_direction, speed,
                 img_file, dead_img_file):
        Sprite.__init__(self)
        self.name = 'Creep'

        self.base_image = img_file
        self.image = self.base_image
        self.image_dead = dead_img_file

        self.screen = screen
        self.field = field

        self.pos = vec2d(init_position)
        self.direction = vec2d(init_direction).normalized()
        self.speed = speed

        self.isAlive = True

        self.attack_power = 10
        self.deffence_power = 5

        self.life = 100
        self.max_life = 100
        self.image_w, self.image_h = self.image.get_size()
        self.reborn_time = 0

    def update(self, time_passed, target):
        if self.isAlive == True:
            if self.check_target(target, time_passed):
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
            self.reborn_time += time_passed
            if self.reborn_time > 3000:
                self.reborn()

    _counter = 0

    def change_direction(self, target, time_passed):
        self._counter += time_passed
        if self._counter > randint(400, 500):
            self.direction.rotate(45 * randint(-1, 1))
            self._counter = 0

    def check_target(self, target, time_passed):
        target_dist = (target.pos.x - self.pos.x) ** 2 + \
            (target.pos.y - self.pos.y) ** 2
        if 10 ** 2 <= target_dist <= 50 ** 2 and target.isAlive == True:
            return True
        elif target_dist <= 10 ** 2 and target.isAlive == True:
            combat.start_battle(self, target, time_passed)

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

    def Attack(self, target, time_passed):
        damage = self.attack_power - target.deffence_power
        if damage > 0:
            target.deffence(damage, time_passed)
            # return Hit and damage for display event
        else:
            target.deffence(0, time_passed)
            # return Ressist ----//----

    def deffence(self, damage, time_passed):
        if damage > 0:
            self.life -= damage
            if self.life <= 0:
                self.kill(time_passed)

    def kill(self, time_passed):
        self.isAlive = False
        self.life = 0
        self.image = self.image_dead

        self.reborn_time = 0

    def reborn(self):
        self.isAlive = True
        self.life = self.max_life
        self.image = self.base_image
