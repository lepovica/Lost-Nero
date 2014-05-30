import pygame
from pygame.sprite import Sprite

from vec2d import vec2d
import math


class Creep(pygame.sprite.Sprite):

    def __init__(self, screen, init_position, init_direction, speed):
        Sprite.__init__(self)
        self.name = 'Creep'

        self.image = pygame.image.load('creep.png')
        self.rect = pygame.rect.Rect(init_position, self.image.get_size())
        self.screen = screen

        self.pos = vec2d(init_position)
        self.direction = vec2d(init_direction).normalized()
        self.speed = speed

        self.isAlive = True
        self.isFighting = True

        self.weapon = None
        self.armor = 100

        self.attack_power = 10
        self.deffence_power = 5

        self.life = 100
        self.max_life = 100

        self.time = pygame.time.Clock()

        self.image_w, self.image_h = self.image.get_size()


    def update(self, game_time, target):
        if self.isAlive == True:
            if self.isFighting == True:
                self.go_after(target, game_time) 
            else:
                self.move_around() #attack nearby -->move_around().detect()

        if self.isAlive == False:
            if self.time.get_rawtime() - self.reborn_time > 30:
                self.reborn()

    def move_around(self):
        pass
    # vec2d !!!
    def detect_target(self, target):
        if (target.pos.x - self.pos.x)**2 + (target.pos.y - self.pos.y)**2 <= 10**2:
            return True

    def go_after(self, target, game_time):
        if self.detect_target(target):

            self.change_direction_to_target(game_time, target)

            self.image = pygame.transform.rotate(
                 self.image, -self.direction.angle)
            self.rect = pygame.rect.Rect(self.pos, self.image.get_size())

            displacement = vec2d(    
                self.direction.x * self.speed * game_time,
                self.direction.y * self.speed * game_time)
            
            self.pos += displacement
            self.rect = pygame.rect.Rect(self.pos, self.image.get_size())

    def change_direction_to_target(self, game_time, target):
        (dir_x, dir_y) = (target.pos.x - self.posx,
            target.pos.y - self.pos.y)
        # Compute the angle
        angle = math.atan(float(dir_x)/float(dir_y))
        # Make angle in degrees
        angle *= 180/math.pi
        # Flip angle if target is behind
        if dy < 0:
           angle += 180

        self.direction.rotate(angle)

    def blitme(self):
        draw_pos = self.image.get_rect().move(
            self.pos.x - self.image_w / 2, 
            self.pos.y - self.image_h / 2)
        self.screen.blit(self.image, draw_pos)

    def Attack(self, target):
        damage = self.attack_power - target.deffence_power
        if damage > 0:
            target.deffence(damage)
            # return Hit and damage for display event
        elif damage <= 0:
            target.deffence(0)
            pass
            # return Ressist ----//----

    def kill(self):
        self.isAlive = False
        self.life = 0
        self.image = pygame.image.load('dead_player.png')
        self.rect = pygame.rect.Rect(self.pos, self.image.get_size())
        self.reborn_time = self.time.get_rawtime()

    def deffence(self, damage):
        if damage > 0:
            self.life -= damage
            if self.life <= 0:
                self.kill()
        else:
            pass

    def reborn(self):
        self.isAlive = True
        self.life = self.max_life
        self.image = pygame.image.load('creep.png')
        self.rect = pygame.rect.Rect(self.pos, self.image.get_size())


