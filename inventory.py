import pygame
from vec2d import vec2d
from random import choice



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

SWORDS = dict()

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








class Cell(pygame.sprite.Sprite):
    def __init__(self, screen, pos, item = None, background = None):
        pygame.sprite.Sprite.__init__(self)
        self.pos = vec2d(pos)
        self.item = item
        self.screen = screen
        self.background = background
        self.side = 50

    def is_empty(self):
        return self.item == None

    def draw():
        if self.background == None:
            self.background = Color('Black')
        cell_rect = self.background.get_rect()

        cell_rect.move(
                self.pos.x - self.image.get_size()[0] / 2,
                self.pos.y - self.image.get_size()[1] / 2)
        self.screen.blit(self.image, item_rect)


class Inventory:

    (WEAPON, SHIELD, CHEST, SHOULDERS, SHIELD, GLOVES,
        BOOTS, PANTS, MANTLE, HELMET, SKIRT,) = range(11)

    def __init__(self, screen, texture):
        self.texture = texture
        self.left_top = vec2d(0, 540)
        self.hight = 60
        self.wide = 600
        self.screen = screen
        self.bag_pages = 1
        self.bag = [[]]
        self.start_pos_bag = vec2d(0, 0)
        # initial of bag
        self.inverntory = list()
        self.start_pos_inventory = vec2d(0, 0)
        for i in range(11):
            current_pos = self.start_pos_inventory
            self.inverntory.append(Cell(self.screen, current_pos))
            current_pos.x += 60
        self.bar = []
        self.start_pos_bar = vec2d(5, 545)
        for i in range(9):
            current_pos = self.start_pos_bar
            self.bar.append(Cell(self.screen, current_pos)) 
            current_pos.x += 60


    def add_item_bag(self, item):
        if self.bag_pages <= 3:
            if len(self.bag[self.bag_pages]) == 9 and self.bag_pages < 3:
                self.bag_pages += 1
            else:
                return
            item.state = item.GETTED
            cell_position = (self.bag_pages, len(self.bag[self.bag_pages]))
            self.bag[self.bag_pages].apeend(Cell(self.screen, cell_position,
                                            item, background))


    def remove_item_bag(self, item):
        deleting_pos = (item.pos.x, item.pos.y)
        self.bag[deleting_pos[0]].pop(deleting_pos[1])
        item.state = item.DROPPED


    def add_item_inventory(self, pos_inventory, item):
        if self.inverntory[pos_inventory] == None:
            self.inverntory[pos_inventory] = item
        else:
            self.remove_item_inventory(pos_inventory)
            self.inverntory.insert(pos_inventory, item)

    def remove_item_inventory(self, pos_inventory):
        if self.inverntory[pos_inventory] != None:
            removed_item = self.inverntory[pos_inventory]
            self.inverntory[pos_inventory] = None
            self.add_item_bag(removed_item)

    def draw(self):
        step_h, step_w = self.texture.get_size()
        step_h_counter = 0
        step_w_counter = 0
        while step_w_counter <= self.wide:
            while step_h_counter <= self.hight:
                self.screen.blit(self.texture,
                    self.left_top + vec2d(step_w_counter, step_h_counter))
                step_h_counter += step_h
            step_w_counter += step_w
            step_h_counter = 0


    def load_items(self):
        for img_file in SWORD_IMG:
            i += i + 1

            SWORDS[str(i) + "_sword"] = type(str(i) + "_sword", (Item,), {
                                   'pos' : vec2d(0, 0), 'screen' : self.screen,
                                   'base_image' : img_file, 'image' : img_file, 
                                   'state' : 0, 'item_type' : ITEM_TYPES[0], 
                                   'level_required' : level, 
                                   'name' : str(i) + "_sword",
                                   'attack_power' : level*20, 
                                   'deffence_power' : level*5,
                                   'price' : level*100, 'armor' : level*100 })

            # load more items..



    def draw_inventory(self):
        for cell in self.inverntory:
            cell.draw()
            cell.item.draw()

            

    def draw_bar(self):
        for cell in self.bar:
            cell.draw()
            cell.item.draw()



    def draw_bag(self):
        pass



