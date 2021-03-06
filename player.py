import pygame
from pygame.sprite import Sprite
import vec2d
from vec2d import vec2d
import math
import combat
from pygame import Color
import sys
from bullet import Bullet

# do creep code look pretty


class Player(Sprite):

    def __init__(self, screen, field, init_position, init_direction, speed,
                 img_file, dead_img_file):

        Sprite.__init__(self)
        self.name = 'Nero'

        self.base_image = img_file
        self.image = self.base_image
        self.image_dead = dead_img_file

        self.screen = screen
        self.field = field

        self.pos = vec2d(init_position)
        self.direction = vec2d(init_direction).normalized()
        self.speed = speed

        self.state = self.ALIVE

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
        self.bullets = []

    (ALIVE, DEAD, CHASING, FIGHTING, MOVING) = range(5)

    def update(self, time_passed):
        if self.state == self.FIGHTING:
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] or key[pygame.K_RIGHT] or key[pygame.K_DOWN] or key[pygame.K_UP]:
                self.state = self.ALIVE
            if self.life > 0 and self.chasing_target.life > 0:
                self.change_direction(self.chasing_target.pos)
                self.rotate_image()
                if 50**2 <= (self.chasing_target.pos.x - self.pos.x)**2 + (self.chasing_target.pos.y - self.pos.y) **2:
                    self.move(time_passed)
                combat.Battle.do_battle(self, self.chasing_target, time_passed)
                self.health_bar()
            else:
                if self.life > 0 :
                    self.state = self.ALIVE
                    self.health_bar()
                else:
                    self.state = self.DEAD
            

        if self.state == self.MOVING:
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] or key[pygame.K_RIGHT] or key[pygame.K_DOWN] or key[pygame.K_UP]:
                self.state = self.ALIVE

            if self.get_destination():
                self.state = self.ALIVE
                self.health_bar()
            else:
                self.move(time_passed)
                self.health_bar()

        if self.state == self.CHASING:
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] or key[pygame.K_RIGHT] or key[pygame.K_DOWN] or key[pygame.K_UP]:
                self.state = self.ALIVE

            if self.get_chasing_target():
                self.state = self.FIGHTING
            else:
                self.change_direction(self.chasing_target.pos)
                self.rotate_image()
                self.move(time_passed)
            self.health_bar()

        if self.state == self.ALIVE:
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


            if self.pos != wanted_pos:
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

            self.health_bar()

        elif self.expirience >= self.max_expirience:
            self.levelUp(self.level + 1)

        if self.state == self.DEAD:
            self.reborn_time += time_passed
            if self.reborn_time > 3000:
                self.reborn()

    def get_destination(self):
        if (self.pos.x - self.moving_pos.x) ** 2 + (self.pos.y - self.moving_pos.y) ** 2 <= 10 ** 2:
            return True
        return False

    def health_bar(self):
        health_bar_x = self.pos.x - 50 + self.image_w / 2
        health_bar_y = self.pos.y - 10
        self.screen.fill(Color('red'),
                        (health_bar_x, health_bar_y,
                         self.max_life / self.level, 4))
        self.screen.fill(Color('green'),
                        (health_bar_x, health_bar_y,
                         self.life / self.level, 4))

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

    def draw(self, time_passed):
        print("{0} : {1}".format(self.name, self.pos))
        draw_rect = self.image.get_rect().move(
            self.pos.x - self.image_w / 2,
            self.pos.y - self.image_h / 2)
        self.screen.blit(self.image, draw_rect)

        for bullet in self.bullets:
            if bullet.state == bullet.MOVING:
                bullet.update(time_passed)
                bullet_rect = bullet.image.get_rect().move(
                    bullet.pos.x - bullet.image.get_size()[0]/2,
                    bullet.pos.y - bullet.image.get_size()[1]/2)
                self.screen.blit(bullet.image, bullet_rect)
            elif bullet.state == bullet.DEAD:
                self.bullets.remove(bullet)


    def levelUp(self, level):
        self.level = level
        self.expirience = 0
        self.max_expirience = level * 100
        self.max_life = level * 100
        self.life = self.max_life

        self.attack_power = level * 10
        self.deffence_power = level * 5

        self.money += level * 1000

    def moving(self, pos):
        if self.state != self.DEAD:
            wanted_pos = vec2d(pos)
            self.state = self.MOVING
            self.change_direction(wanted_pos)
            self.rotate_image()
            self.moving_pos = wanted_pos

    def chasing(self, target):
        self.state = self.CHASING
        self.chasing_target = target

    def get_chasing_target(self):
        if (self.chasing_target.pos.x - self.pos.x) ** 2 + (self.chasing_target.pos.y - self.pos.y) ** 2 <= 50 ** 2:
            return True
        return False

    def attack(self, target, time_passed):
        self.bullets.append(Bullet(target, self.pos, 
            pygame.transform.scale(pygame.transform.rotate(pygame.image.load('Nero_bullet.png'),-45), (50, 50))))
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
        self.state = self.FIGHTING
        if damage > 0:
            if self.armor > 0:
                self.armor -= damage * 0.3
                self.life -= damage * 0.7
            self.expirience += 0.10 * self.deffence_power
            if self.life <= 0:
                self.kill(time_passed)
        else:
            self.expirience += 0.20 * self.deffence_power

    def kill(self, time_passed):
        self.state = self.DEAD
        self.life = 0
        self.image = self.image_dead
        self.reborn_time = 0

    def reborn(self):
        self.state = self.ALIVE
        self.life = self.max_life
        self.image = self.base_image
