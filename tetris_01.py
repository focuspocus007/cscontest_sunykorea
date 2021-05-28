import pygame
import random
import os
from time import time
import re
import pygame_menu

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()
user_name = ""
# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 200  # meaning 300 // 10 = 30 width per block
play_height = 440  # meaning 600 // 20 = 20 height per blo ck
block_size = 20

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

fall_time = 0
# SHAPE FORMATS

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (128, 0, 128), (255, 127, 0), (255, 0, 127)]
# index 0 - 6 represent shape
score = 0

class Piece(object):
    rows = 22  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # number from 0-3


def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for x in range(10)] for x in range(22)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):

    accepted_positions = [[(j, i) for j in range(
        10) if grid[i][j] == (0, 0, 0)] for i in range(22)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True


def check_lost(positions):
    global score
    for pos in positions:
        x, y = pos
        if y < 1:
            print("user:",user_name)
            with open("scoreboard.txt", 'w') as f:
                
                f.write(str(user_name)+":"+str(score))
            return True
    return False


def get_shape():
    global shapes, shape_colors

    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2),
                         top_left_y + play_height/2 - label.get_height()/2))


def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i*block_size),
                         (sx + play_width, sy + i * block_size))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy),
                             (sx + j * block_size, sy + play_height))  # vertical lines


def clear_rows(grid, locked):
    # need to see if row is clear the shift every other row above down one
    global score
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            # add positions to remove from locked
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
        score += 1
        print(score)



def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]
    # score_label = font.render('SCORE:' + str(score), 1, (255,255,255))
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.Surface.fill(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size))
                pygame.draw.rect(surface, (0, 0, 0),
                                 (sx + j*block_size, sy + i*block_size, block_size, block_size), 5)

    surface.blit(label, (sx + 10, sy - 30))
    # surface.blit(score_label, (sx, sy - 150))


def draw_score(increaseScore, surface):
    font = pygame.font.SysFont('comicsans', 30)

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    score_label = font.render('SCORE:' + str(increaseScore), 1, (255,255,255))
    surface.blit(score_label, (sx, sy - 150))

def draw_window(surface):
    surface.fill((0, 0, 0))
    # Tetris Title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width /
                         2 - (label.get_width() / 2), 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.Surface.fill(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size))
            pygame.draw.rect(surface, (0, 0, 0), (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 5)

    # draw grid and border
    draw_grid(surface, 22, 10)
    pygame.draw.rect(surface, (255, 255, 255), (top_left_x,
                                            top_left_y, play_width, play_height), 1) 
    # pygame.display.update()


def main():
    global grid
    global fall_time

    locked_positions = {}  # (x,y):(255,0,0)
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    INCREMENT = 5
    start_time = time()
    fall_speed = 0.25
    # Sound
    pygame.mixer.init()
    mySound = pygame.mixer.Sound( "music.wav" )
    mySound.set_volume(0.7)
    mySound.play(-1)
    while run:
        
        end_time = time()

        # Speed Increase as Time passes (5 sec)
        if (end_time - start_time >= INCREMENT):
            start_time = end_time
            print("start:", start_time, "end:", end_time)
            if (fall_speed != 0):
                fall_speed = fall_speed - 0.01
                print("IF fall_speed:", fall_speed)
            else: 
                fall_speed = 0
                print("ELSE fall_speed:", fall_speed)

        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        # PIECE FALLING CODE
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + \
                        1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - \
                            1 % len(current_piece.shape)

                if event.key == pygame.K_DOWN:
                    # move shape down
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                if event.key == pygame.K_SPACE:
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    print(convert_shape_format(current_piece))  # todo fix

                if event.key == pygame.K_ESCAPE:
                    run = False
                    main_menu()
        shape_pos = convert_shape_format(current_piece)

        # add piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # IF PIECE HIT GROUND
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            # call four times to check for multiple clear rows
            clear_rows(grid, locked_positions)

        draw_window(win)
        draw_next_shape(next_piece, win)
        draw_score(score, win)
        pygame.display.update()

        # Check if user lost
        if check_lost(locked_positions):
            run = False

    draw_text_middle("You Lost", 40, (255, 255, 255), win)
    pygame.display.update()
    pygame.time.delay(2000)


def set_difficulty(value, difficulty):
    global fall_time
    if difficulty == 1:
        fall_time = 0.3
    elif difficulty == 2:
        fall_time = 0.5
    elif difficulty == 3:
        fall_time = 0.7

def scoreBoard():
    run = True
    while run:
        win.fill((0, 0, 0))
        # font = pygame.font.SysFont('comicsans', 60, bold=True)
        # label = font.render('PRESS ESC TO GO BACK', 1, (255, 255, 255))
        # surface.blit(label, (120),(100))

        # s_width = 800
        # s_height = 700
                         
        draw_text_middle('PRESS ESC TO GO BACK', 20, (255, 255, 255), win)
        # draw_text_middle('KING OF TETRIS', 50, (255, 255, 255), win)
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()

def getUserID(value):
    global user_name 
    user_name = value


def getUserScore():
    userScore = []
    
    f = open("scoreBoard.txt", 'r')
    while True:
        line = f.readline()
        if not line: break
        print(line)
        userScore.append(line)
    f.close()

    #SORT RESULT
    
    finalRank = []
    for each in userScore:
        print(each)
        rankScore = ""
        userName = ""
        for x in reversed(each):
            if x.isdigit():
                print(type(rankScore), type(x))
                rankScore += str(x)
            else:
                userName += str(x)
            #reverse the integers that were reversed because of the reversed for loop
        rankScore = str(rankScore[::-1])
        print("rankscore",rankScore)

        userName = userName[::-1]
        print("username",userName)

        finalRank.append((int(rankScore), userName.rstrip(":\n")))
        
        finalRank.sort(reverse=True, key=lambda tup: tup[0])

        
        print(finalRank)
    return finalRank

pygame.init()
win = pygame.display.set_mode((s_width, s_height))
surface = pygame.display.set_mode((800, 700))
menu = pygame_menu.Menu(700, 600, 'Team 2 TETRIS',
                        theme=pygame_menu.themes.THEME_DARK)
menu.add.text_input('Name :', default='enter your name', onchange=getUserID)
menu.add.selector(
    'Difficulty :', [('Hard', 1), ('Normal', 2), ('Easy', 3)], onchange=set_difficulty)
menu.add.button('Play', main)
menu.add.button('Quit', pygame_menu.events.EXIT)


ranking = getUserScore()
# HELP = "\n GOD OF TETRIS [RANKING]\n\n",ranking[0],\
#         "\n"\
#         "Press ENTER to access a Sub-Menu or use an option \n"\
#         "Press UP/DOWN to move through Menu \n"\
#         "Press LEFT/RIGHT to move through Selectors.\n"

if len(ranking) >= 3:
    SCORE_GUIDE = f"\nGOD OF TETRIS [RANKING]\n SCORE,NAME\n1st : {ranking[0][0], ranking[0][1]}\n2nd : {ranking[1][0], ranking[1][1]}\n3rd : {ranking[2][0], ranking[2][1]}\n"
    print("SCORE_GUIDE",SCORE_GUIDE)
    menu.add_label(SCORE_GUIDE, max_char=-1, font_size=20)
if len(ranking) == 2:
    SCORE_GUIDE = f"\nGOD OF TETRIS [RANKING]\n SCORE,NAME\n1st : {ranking[0][0], ranking[0][1]}\n2nd : {ranking[1][0], ranking[1][1]}\n"
    print("SCORE_GUIDE",SCORE_GUIDE)
    menu.add_label(SCORE_GUIDE, max_char=-1, font_size=20)
if len(ranking) == 1:
    SCORE_GUIDE = f"\nGOD OF TETRIS [RANKING]\n SCORE,NAME\n1st : {ranking[0][0], ranking[0][1]}\n"
    print("SCORE_GUIDE",SCORE_GUIDE)
    menu.add_label(SCORE_GUIDE, max_char=-1, font_size=20)
if len(ranking) == 0:
    SCORE_GUIDE = "\nYOU ARE THE FIRST PLAYER! \n PLAY AND BECOME THE FIRST RANKER!"
    print("SCORE_GUIDE",SCORE_GUIDE)
    menu.add_label(SCORE_GUIDE, max_char=-1, font_size=20)

menu.mainloop(surface)

# 
# pygame.display.set_caption('Tetris')

# main_menu()  # start game
