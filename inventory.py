import pygame
from vec2d import vec2d
from random import choice

TYPES = {'weapon': 0, 'armor': 1, 'flask': 2}
WEAPONS = ['sword', 'axe', 'staff', 'bow']
ARMORS = [
    'chest', 'shoulders', 'shield', 'gloves', 'boots', 'pants', 'mantle',
    'helmet', 'skirt']
FLASKS = ['healt', 'armor']
WEP_IMG = [2]
ARM_IMG = [3]
FLA_IMG = [4]


class Item(pygame.sprite.Sprite):
    (DROPPED, GETTED) = range(2)

    def __init__(self, screen, pos, img_file, item_type,
                 price, attack_power, deffence_power, armor, name, level):

        pygame.sprite.Sprite.__init__(self)
        self.pos = vec2d(pos)
        self.screen = screen
        self.image = img_file
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
        bullet_rect = bullet.image.get_rect().move(
            bullet.pos.x - bullet.image.get_size()[0] / 2,
            bullet.pos.y - bullet.image.get_size()[1] / 2)
        self.screen.blit(self.image, bullet_rect)


class Inventory:

    def __init__(self, screen):
        self.screen = screen
        self.bag_page = 0
        self.bag = [[]]
        self.abilities = []


def generate_item(pos, screen, level):
    item_type = choice(TYPES.values())
    if item_type == 0:
        print(0)
        name = choice(WEAPONS)
        img_file = choice(WEP_IMG)
        price = level * 100
        attack_power = level * 20
        deffence_power = level * 5
        armor = level * 20

        item = Item(screen, pos, img_file, item_type,
                    price, attack_power, deffence_power, armor, name, level)
        return item
    elif item_type == 1:
        print(1)
        name = choice(ARMORS)
        img_file = choice(ARM_IMG)
        price = level * 100
        attack_power = level * 5
        deffence_power = level * 20
        armor = level * 30

        item = Item(screen, pos, img_file, item_type,
                    price, attack_power, deffence_power, armor, name, level)
        return item
    elif item_type == 2:
        print(2)
        name = choice(FLASKS)
        img_file = choice(FLA_IMG)
        price = level * 100
        attack_power = 0
        deffence_power = 0
        armor = 0

        item = Item(screen, pos, img_file, item_type,
                    price, attack_power, deffence_power, armor, name, level)
        return item

item = generate_item((1,4), 2, 3)
print (item)
