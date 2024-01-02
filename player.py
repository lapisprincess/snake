# imports
import pygame

from board import Board


'''
cartesian coordinates translate to int, represented below:
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
'''


'''
player object to keep track of where the player is, and render the player
directly on the board. 

NOTE: if I wanted to be cleaner with my code, this class would only hold
the player's information, getting and manipulating it. python's high level
design allows me to just directly render it onto the board! huzzah!

@author ~~
'''
class Player:
    # class variables
    left_down = False   # True when pressed, 
    right_down = False  # False when released.

    '''

    
    @instance/param x, y        -> head xy coord in tiles
    @instance/param direction   -> cartesian direction (code detailed above)
    @instance/param alive       -> determines game over status
    @instance/param length      -> length of snake; determines score
    '''
    def __init__(self, x, y, direction, start_length):
        self.x = x
        self.y = y
        self.direction = direction
        self.alive = True
        self.length = start_length

    '''
    method to update the player's position, manage keystrokes,
    and check collisions.
    
    @param board    -> a reference to the board the player exists on
    @param keys     -> pygame's list of currently held keys
    '''
    def update(self, board, keys):
        # handle movement
        if keys[pygame.K_LEFT] and not self.left_down:
            self.turn_left()
            self.left_down = True
        elif not keys[pygame.K_LEFT]: self.left_down = False
        if keys[pygame.K_RIGHT] and not self.right_down:
            self.turn_right()
            self.right_down = True
        elif not keys[pygame.K_LEFT]: self.right_down = False
        self.move()

        # handle border collision
        if self.x < 0 or self.x >= board.x_tiles - 1: 
            self.alive = False
            return
        if self.y < 0 or self.y >= board.y_tiles - 1:
            self.alive = False
            return

        # handle tile occupations
        tile = board.get_tile(self.x, self.y).status
        if tile == "snake": self.alive = False # bumped into itself :(
        if tile == "apple": # yum! 🍎
            board.place_apple()
            self.length += 1

        # add the snake!
        board.get_tile(self.x, self.y).occupy("snake", self.length)


    # simple turn methods to adjust the player's direction,
    # staying within bounds.
    def turn_left(self):
        self.direction -= 1
        if self.direction <= -1: self.direction = 3
    def turn_right(self):
        self.direction += 1
        if self.direction >= 4: self.direction = 0

    # move the snake based on direction.
    # (see index above for int to direction conversion)
    def move(self):
        match self.direction:
            case 0: self.y -= 1 # NORTH
            case 1: self.x += 1 # EAST
            case 2: self.y += 1 # SOUTH
            case 3: self.x -= 1 # WEST
