# imports
import pygame
import time

from board import Board
from player import Player
from text import Text


# constants
SCREEN_X = 800
SCREEN_Y = 400
TILE_SIZE = 32
START_LENGTH = 3
DIFFICULTY = 10


# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y)) 
pygame.display.set_caption("Silly Snakes (of doom) II 🐍🐍")
clock = pygame.time.Clock()
pygame.key.set_repeat()

# font setup
header = pygame.font.Font("Arial.ttf", 28)
standard = pygame.font.Font("Arial.ttf", 20)
small = pygame.font.Font("Arial.ttf", 16)

mid_x = SCREEN_X / 2
mid_y = SCREEN_Y / 2
white = pygame.Color("white")
gameover_text = Text(header, "Game Over!", mid_x, mid_y - 24, white)

highscore = open("highscore", 'r').read()
highscore = highscore[:len(highscore)]
highscore_text = Text(standard, "High Score: " + highscore, mid_x, mid_y + 24, white)
newhighscore_text = Text(standard, "New High Score!!", mid_x, mid_y + 72, white)

# set up pieces
board = Board(SCREEN_X, SCREEN_Y, TILE_SIZE)
board.place_apple()
player = Player(1,1,1,START_LENGTH) # start at coord (1,1) facing east
mode = "play"
visible = True # for blinking stuff


# game loop
running = True
tics = 0
while running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    # handle blinking objects
    if tics % 5 == 0: visible = not visible

    match mode:
        case "play":
            # refresh the screen
            screen.fill("black")

            # keep the score up to date
            score = player.length - START_LENGTH
            score_text = Text(small,
                              "Score: " + str(score),
                              board.x_diff, 16, white)
            score_text.render(screen)

            # render the board
            board.render(screen)

            # update pieces
            if not player.alive: mode = "game over"
            player.update(board, pygame.key.get_pressed())
            board.update()

        case "game over":
            # handle the game over screen
            screen.fill("black")
            score_text = Text(standard, 
                              "Score: " + str(score),
                              mid_x, mid_y + 48, white)
            gameover_text.render(screen)
            highscore_text.render(screen)
            score_text.render(screen)

            # check if new high score
            if score > int(highscore): 
                if visible: newhighscore_text.set_alpha(255)
                else: newhighscore_text.set_alpha(0)
                open("highscore", 'w').write(str(score))
                newhighscore_text.render(screen)

    # utility shtuff
    pygame.display.flip()
    clock.tick(DIFFICULTY) 
    tics += 1

# close and exit
pygame.quit()
exit(0)
