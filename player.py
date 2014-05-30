import pygame
from pygame.sprite import Sprite

from vec2d import vec2d


class Player(pygame.sprite.Sprite):

    def __init__(self, screen, init_position, init_direction, speed):
        Sprite.__init__(self)
        self.name = 'Nero'

        self.image = pygame.image.load('player.png')
        self.rect = pygame.rect.Rect((50, 50), self.image.get_size())
        self.screen = screen
        
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
        self.time = pygame.time.Clock()

        self.image_w, self.image_h = self.image.get_size()

    def update(self, player_object = None):
        if self.isAlive == True:
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                self.rect.x -= 5
            if key[pygame.K_RIGHT]:
                self.rect.x += 5
            if key[pygame.K_UP]:
                self.rect.y -= 5
            if key[pygame.K_DOWN]:
                self.rect.y += 5
            if key[pygame.K_k]:
                self.kill()

            if self.expirience >= self.max_expirience:
                self.levelUp(self.level + 1)

        if self.isAlive == False:
            if self.time.get_rawtime() - self.reborn_time > 30:
                self.reborn()
            key = pygame.key.get_pressed()
            if key[pygame.K_r]:
                self.reborn()

    def blitme(self):
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
        elif damage <= 0:
            self.expirience += 0.05 * self.attack_power
            target.deffence(0)
            pass
            # return Ressist ----//----

    def kill(self):
        self.isAlive = False
        self.life = 0
        self.image = pygame.image.load('dead_player.png')
        self.rect = pygame.rect.Rect(
            (self.rect.x, self.rect.y), self.image.get_size())
        self.reborn_time = self.time.get_rawtime()

    def deffence(self, damage):
        if damage > 0:
            self.life -= damage
            self.expirience += 0.05 * self.deffence_power
            if self.life <= 0:
                self.kill()
        else:
            self.expirience += 0.10 * self.deffence_power

    def reborn(self):
        self.isAlive = True
        self.life = self.max_life
        self.image = pygame.image.load('player.png')
        self.rect = pygame.rect.Rect(
            (self.rect.x, self.rect.y), self.image.get_size())


