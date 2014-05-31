import pygame
from pygame.sprite import Sprite
import vec2d
from vec2d import vec2d
import math


class Player(pygame.sprite.Sprite):

    def __init__(self, img_file, screen, field, init_position, init_direction, speed):
        Sprite.__init__(self)
        self.name = 'Creep'

        self.base_image = img_file
        self.image = self.base_image
        self.screen = screen
        self.field = field

        self.pos = vec2d(init_position)
        self.direction = vec2d(init_direction).normalized()
        self.speed = speed

        self.isAlive = True
        self.isFighting = False

        self.level = 1
        self.expirience = 0
        self.max_expirience = 100

        self.weapon = None
        self.armor = 100

        self.attack_power = 10
        self.deffence_power = 5

        self.life = 100
        self.max_life = 100

        self.money = 1000

    def update(self, game_time):
        if self.isAlive == True:
            if self.isFighting == False:
                key = pygame.key.get_pressed()
                wanted_pos = vec2d(self.pos)
                if key[pygame.K_LEFT]:
                    wanted_pos.x -= 5

                if key[pygame.K_RIGHT]:
                    wanted_pos.x += 5

                if key[pygame.K_UP]:
                    wanted_pos.y -= 5

                if key[pygame.K_DOWN]:
                    wanted_pos.y += 5

                self.change_direction(wanted_pos)
                self.rotate_image()
                self.move(game_time)

        if self.isAlive == False:
            if pygame.time.get_rawtime() - self.reborn_time > 30:
                self.reborn()

        if self.expirience >= self.max_expirience:
                self.levelUp(self.level + 1)

    def change_direction(self, wanted_pos):
        dx = self.pos.x - wanted_pos.x
        dy = self.pos.y - wanted_pos.y
        self.direction = vec2d(-dx, -dy).normalized()

    def rotate_image(self):
        self.image = pygame.transform.rotate(
            self.base_image, -self.direction.angle)

    def move(self, game_time):
        displacement = vec2d(
            self.direction.x * self.speed * game_time,
            self.direction.y * self.speed * game_time)

        self.pos += displacement

    def draw(self):
        draw_pos = self.image.get_rect().move(
            self.pos.x - self.image_w / 2,
            self.pos.y - self.image_h / 2)
        self.screen.blit(self.image, draw_pos)

    def levelUp(self, level):
        self.level = level
        self.expirience = 0
        self.max_expirience = level * 100
        self.max_life = level * 100
        self.life = self.max_life

        self.attack_power = level * 10
        self.deffence_power = level * 5

        self.money += level * 1000

    def Attack(self, target):
        damage = self.attack_power - target.deffence_power
        if damage > 0:
            self.expirience += 0.10 * self.attack_power + 0.10 * damage
            target.deffence(damage)
            # return Hit and damage for display event
        else:
            self.expirience += 0.05 * self.attack_power
            target.deffence(0)
            # return Ressist ----//----

    def deffence(self, damage):
        if damage > 0:
            self.life -= damage
            self.expirience += 0.10 * self.deffence_power
            if self.life <= 0:
                self.kill()
        else:
            self.expirience += 0.20 * self.deffence_power

    def kill(self):
        self.isAlive = False
        self.life = 0
        self.image = pygame.image.load('dead_player.png')

        self.reborn_time = self.time.get_rawtime()

    def reborn(self):
        self.isAlive = True
        self.life = self.max_life
        self.image = pygame.image.load('player.png')
