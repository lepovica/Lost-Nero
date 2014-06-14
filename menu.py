import pygame


class MenuItem (pygame.font.Font):
    '''
    The Menu Item should be derived from the pygame Font class
    '''
    def __init__(self,text, position,font_size=36, antialias = 1, color = (255, 255, 255), background=None):
        pygame.font.Font.__init__(self,None, font_size)
        self.text = text
        if background == None:
            self.text_surface = self.render(self.text,antialias,(255,255,255))
        else:
            self.text_surface = self.render(self.text,antialias,(255,255,255),background)
        self.position=self.text_surface.get_rect(centerx=position[0],centery=position[1])
    def get_pos(self):
        return self.position
    def get_text(self):
        return self.text
    def get_surface(self):
        return self.text_surface


class Menu:


    def __init__(self,menuEntries, menuCenter = None):
        '''
        The constructer uses a list of string for the menu entries,
        which need  to be created
        and a menu center if non is defined, the center of the screen is used
        '''
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.background = pygame.Surface(screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))
        self.active=False

        if pygame.font:
            font_size = 36
            fontSpace= 4
            # loads the standard font with a size of 36 pixels
            # font = pygame.font.Font(None, font_size)

            # calculate the height and startpoint of the menu
            # leave a space between each menu entry
            menuHeight = (font_size+fontSpace)*len(menuEntries)
            startY = self.background.get_height()/2 - menuHeight/2  

            #listOfTextPositions=list()
            self.menuEntries = list()
            for menuEntry in menuEntries:
                centerX=self.background.get_width()/2
                centerY = startY+font_size+fontSpace
                newEnty = MenuItem(menuEntry,(centerX,centerY))
                self.menuEntries.append(newEnty)
                self.background.blit(newEnty.get_surface(), newEnty.get_pos())
                startY=startY+font_size+fontSpace

    def drawMenu(self):
        self.active=True            
        screen = pygame.display.get_surface()
        screen.blit(self.background, (0, 0))

    def isActive(self):
        return self.active
    def activate(self,):
        self.active = True
    def deactivate(self):
        self.active = False
    def handleEvent(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.isActive():
            # initiate with menu Item 0
            curItem = 0
            # get x and y of the current event 
            eventX = event.pos[0]
            eventY = event.pos[1]
            # for each text position 
            for menuItem in self.menuEntries:
                text_rect = menuItem.get_pos()
                #check if current event is in the text area 
                if text_rect.collidepoint(eventX, eventY):
                    return menuItem.get_text
                    

