# imports
import pygame

'''
text object to simplify all of pygame's text stuff
@author ~~
'''
class Text:
    '''
    
    @param font
    @param text
    @param x, y
    @param color

    @instance renderobj -> the text object to be rendered
    @instance rect      -> the space which this object takes up
    '''
    def __init__(self, font, text, x, y, color):
        self.renderobj = font.render(text, True, color)
        self.rect = self.renderobj.get_rect()
        self.rect.center = (x, y)

    # method to  blits the text onto the screen! (is magic)
    def render(self, screen):
        screen.blit(self.renderobj, self.rect)

    # set the oppacity of the text.
    def set_alpha(self, alpha):
        self.renderobj.set_alpha(alpha)
