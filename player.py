import pygame
from pygame.sprite import Sprite
import vec2d
from vec2d import vec2d
import math
import combat


class Player(Sprite):

    def __init__(self, screen, field, init_position, init_direction, speed):
        Sprite.__init__(self)
        self.name = 'Nero'

        self.base_image = pygame.image.load('player.png')
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
        self.image_w, self.image_h = self.image.get_size()
        self.reborn_time = 0

    def update(self, time_passed):
        if self.isAlive == True:
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

        elif self.expirience >= self.max_expirience:
            self.levelUp(self.level + 1)

        if self.isAlive == False:
            self.reborn_time += time_passed
            if self.reborn_time > 3000:
                self.reborn()

    def change_direction(self, wanted_pos):
        dx = self.pos.x - wanted_pos.x
        dy = self.pos.y - wanted_pos.y
        self.direction = vec2d(-dx, -dy).normalized()

    def rotate_image(self):
        self.image = pygame.transform.rotate(
            self.base_image, -self.direction.angle)

    def move(self, time_passed):
        displacement = vec2d(
            self.direction.x * self.speed * time_passed,
            self.direction.y * self.speed * time_passed)

        self.pos += displacement

    def draw(self):
        print("{0} : {1}".format(self.name, self.pos))
        draw_rect = self.image.get_rect().move(
            self.pos.x - self.image_w / 2,
            self.pos.y - self.image_h / 2)
        self.screen.blit(self.image, self.pos)

    def levelUp(self, level):
        self.level = level
        self.expirience = 0
        self.max_expirience = level * 100
        self.max_life = level * 100
        self.life = self.max_life

        self.attack_power = level * 10
        self.deffence_power = level * 5

        self.money += level * 1000

    def Attack(self, target, time_passed):
        damage = self.attack_power - target.deffence_power
        if damage > 0:
            self.expirience += 0.10 * self.attack_power + 0.10 * damage
            target.deffence(damage, time_passed)
            # return Hit and damage for display event
        else:
            self.expirience += 0.05 * self.attack_power
            target.deffence(0, time_passed)
            # return Ressist ----//----

    def deffence(self, damage, time_passed):
        if damage > 0:
            if self.armor > 0 :
                self.armor -= damage*0.3
                self.life -= damage*0.7
            self.expirience += 0.10 * self.deffence_power
            if self.life <= 0:
                self.kill(time_passed)
        else:
            self.expirience += 0.20 * self.deffence_power

    def kill(self, time_passed):
        self.isAlive = False
        self.life = 0
        self.image = pygame.image.load('dead_player.png')

        self.reborn_time = 0

    def reborn(self):
        self.isAlive = True
        self.life = self.max_life
        self.image = pygame.image.load('player.png')
     
