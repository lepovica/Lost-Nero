import pygame
from vec2d import vec2d
from random import choice

level = 1
display = "screen"
(DROPPED, GETTED) = range(2)
pos = (100, 100)


ITEM_TYPES = ['weapon', 'armor', 'flask']
WEAPONS_ID = ['sword', 'axe', 'staff', 'bow']
ARMORS_ID = [
    'chest', 'shoulders', 'shield', 'gloves', 'boots', 'pants', 'mantle',
    'helmet', 'skirt']
FLASKS_ID = ['healt', 'armor']

SWORD_IMG = list()
AXES_IMG = list()
STAFF_IMG = list()
BOW_IMG = list()

for i in range(47):
    SWORD_IMG.append(pygame.image.load('sw'+str(i+1)+'.png'))
    AXES_IMG.append(pygame.image.load('sw'+str(i+1)+'.png'))
    STAFF_IMG.append(pygame.image.load('sw'+str(i+1)+'.png'))
    BOW_IMG.append(pygame.image.load('sw'+str(i+1)+'.png'))


class Item(pygame.sprite.Sprite):
    (DROPPED, GETTED) = range(2)

    def __init__(self, screen, pos, img_file, item_type,
                 price, attack_power, deffence_power, armor, name, level):

        pygame.sprite.Sprite.__init__(self)
        self.pos = vec2d(pos)
        self.screen = screen
        self.base_image = img_file
        self.image = self.base_image
        self.state = self.DROPPED
        self.type = item_type
        self.attack_power = attack_power
        self.deffence_power = deffence_power
        self.armor = armor
        self.price = price
        self.name = name
        self.level_required = level

    def drop(self, pos):
        self.state = self.DROPPED

    def get(self):
        self.state = self.GETTED

    def draw(self):
        item_rect = self.image.get_rect().move(
            self.pos.x - self.image.get_size()[0] / 2,
            self.pos.y - self.image.get_size()[1] / 2)
        self.screen.blit(self.image, item_rect)



SWORDS = dict()

for img_file in SWORD_IMG:
    i += i + 1

    SWORDS[str(i) + "_sword"] = type(str(i) + "_sword", (Item,), {
                           'pos' : vec2d(pos), 'screen' : display,
                           'base_image' : img_file, 'image' : img_file, 
                           'state' : DROPPED, 'item_type' : ITEM_TYPES[0], 
                           'level_required' : level, 'name' : str(i) + "_sword",
                           'attack_power' : level*20, 'deffence_power' : level*5,
                           'price' : level*100, 'armor' : level*100 })



class Inventory:

    def __init__(self, screen):
        self.screen = screen
        self.bag_page = 0
        self.bag = [[]]
        self.abilities = []


