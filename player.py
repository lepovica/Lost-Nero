import pygame

import time


class Player(pygame.sprite.Sprite):

    def __init__(self, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load('player.png')
        self.rect = pygame.rect.Rect((50, 50), self.image.get_size())

        self.isAlive = True

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



    def update(self):
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
            if time.time() - self.reborn_time > 30:
                self.reborn()
            key = pygame.key.get_pressed()
            if key[pygame.K_r]:
                self.reborn()



    def levelUp(self, level):
        self.level = level
        self.expirience = 0
        self.max_expirience = level*100
        self.max_life = level*100
        self.life = self.max_life

        self.attack_power = level*10
        self.deffence_power = level*5

        self.money += level*1000

    def Attack(self, target):
        damage = self.attack_power - target.deffence_power
        if damage > 0:
            self.expirience += 0.10*self.attack_power + 0.10*damage
            target.deffence(damage)
            #return Hit and damage for display event
        elif damage <= 0:
            self.expirience += 0.05*self.attack_power
            target.deffence(0)
            pass 
            #return Ressist ----//----

    def kill(self):
        self.isAlive = False
        self.life = 0
        self.image = pygame.image.load('dead_player.png')
        self.rect = pygame.rect.Rect((self.rect.x, self.rect.y), self.image.get_size())
        self.reborn_time = time.time()



    def deffence(self, damage):
        if damage > 0:
            self.life -= damage
            self.expirience += 0.05*self.deffence_power
            if self.life <= 0:
                self.kill()
        else:
            self.expirience += 0.10*self.deffence_power

    def reborn(self):
        self.isAlive = True
        self.life = self.max_life
        self.image = pygame.image.load('player.png')
        self.rect = pygame.rect.Rect((self.rect.x, self.rect.y), self.image.get_size())




            

