# imports
import pygame
import random


# constants
APPLE_COLOR = pygame.Color("firebrick3")
SNAKE_COLOR = pygame.Color("coral2")
TILE_COLOR = pygame.Color("limegreen")


'''
board object which contains and manages an array of tiles
@author ~~
'''
class Board:
    '''
    initialization method which sets up the board,
    and fills it with tiles using the appropriate parameters.

    @param screen_x, screen_y   -> screen dimensions in pixels
    @param tile_size            -> width / height of one tile in pixels

    @instance x_tiles, y_tiles  -> board dimensions in tiles
    @instance board             -> array of tiles
    '''
    def __init__(self, screen_x, screen_y, tile_size):
        # initializing board! (is just an array of tiles)
        self.board = []

        # specific number of tiles
        self.x_tiles = (int) (screen_x / tile_size) - 1
        self.y_tiles = (int) (screen_y / tile_size) - 1

        # distance between board and screen edges
        self.x_diff = (screen_x - (self.x_tiles * tile_size))
        self.y_diff = (screen_y - (self.y_tiles * tile_size))
        
        # initialize the tiles in the board
        for y in range(self.y_tiles-1):
            for x in range(self.x_tiles-1):
                self.board.append(
                        self.Tile(
                            x * tile_size + self.x_diff, 
                            y * tile_size + self.y_diff,
                            tile_size,
                            TILE_COLOR
                        ))

    # update method to tick through all the tiles
    def update(self): 
        for tile in self.board: tile.update()

    '''
    getter which returns the tile located at the given coordinate

    @param x, y -> xy coordinates of tile to be indexed
    @return -> tile being indexed
    '''
    def get_tile(self, x, y): return self.board[x + y * (self.x_tiles - 1)]

    '''
    method which searches through every tile, looking for empty spaces

    @return -> True if no empty tiles, False if empty spaces (not full)
    '''
    def is_full(self):
        for tile in self.board:
            if tile.occupied == "empty": return False
        return True

    # simple method which goes through and renders all the tiles
    def render(self, screen): 
        for tile in self: tile.render(screen)

    # mutator which finds a random location to place an apple
    def place_apple(self):
        x, y = random.randint(0, self.x_tiles-2), random.randint(0, self.y_tiles-2)
        # loop ensures the apple is on an empty tile
        while not self.get_tile(x, y).status == "empty":
            x = random.randint(0, self.x_tiles-2)
            y = random.randint(0, self.y_tiles-2)
        # good to place an apple, which stays indefinitely!
        self.get_tile(x, y).occupy("apple", 0)

    '''
    iterator methods which pulls tiles directly from the board array,
    so that a Board object can be iterated through!

    @return -> every Tile in the board
    '''
    def __iter__(self):
        self.i = 0
        return self
    def __next__(self):
        if self.i >= len(self.board): raise StopIteration
        tile = self.board[self.i]
        self.i += 1
        return tile


    '''
    a board is composed of tiles, each of which has its own coordinates
    and sizes relative to the screen, a status to indicate what's on 
    the tile, as well as the colors to make the tile.

    back refers to the tile's background,
    occ refers to the tile's occupance.

    the status of the tile details its occupancy,
    and is one of three options, detailed below:
        - apple: an apple is on the tile (yum!)
        - snake: part of the snake is on the tile
        - empty: nothing on the tile
    '''
    class Tile:
        '''
        initialization method to set up the tile. every tile starts empty,
        and therefore doesn't need an occ_color (which is set to back_color).

        @param x, y         -> screen coordinates of the tile in pixels
        @param size         -> size of the tile in pixels
        @param back_color   -> initial tile color

        @instance back_rect, occ_rect   -> pygame rect objects
        @instance back_color, occ_color -> pygame color (rgb)
        @instance status                -> status of the tile (see header)
        '''
        def __init__(self, x, y, size, back_color):
            self.back_rect = pygame.Rect(x, y, size, size)
            self.occ_rect = pygame.Rect(x+4, y+4, size-8, size-8)
            self.back_color = back_color
            self.empty()

        # when the tile is occupied by something (ie snake) which needs 
        # to disappear after a while, we use update()
        def update(self):
            if self.life > 0:
                self.life -= 1
                if self.life <= 0: self.empty()

        # simple mutator which makes the tile empty
        def empty(self):
            self.life = 0
            self.status = "empty"
            self.occ_color = self.back_color

        # simple mutator which changes the background color of the tile
        def set_back_color(self, color): self.back_color = color

        # render method to put the tile on the screen
        def render(self, screen):
            # draws the tile
            pygame.draw.rect(screen, self.back_color, self.back_rect)
            # draws a frame for the tile
            pygame.draw.rect(screen, pygame.Color("black"), self.back_rect, 1)
            # draws object on the tile (if one exists)
            if self.status != "empty":
                pygame.draw.rect(screen, self.occ_color, self.occ_rect)

        '''
        mutator which applies either the snake or apple status to the tile

        @param color    -> new color for the occupied tile
        @param status   -> new status of the tile
            !! must be either "snake" or "apple" !!
        '''
        def occupy(self, status, length):
            self.status = status
            if status == "snake": 
                self.occ_color = SNAKE_COLOR
                self.life = length
            if status == "apple": 
                self.occ_color = APPLE_COLOR
                self.life = 0
