import pygame
import random
import ssl
import csv

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


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
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape

class Piece(object):  # *
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_pos={}):  # *

    #make a 10x20 grid via nested list
    #grid[list[]]
    #each item in list[] is a tuple representing a color
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    #i=row (y), j=column (x)
    #locked_pos{} is dictionary of {(x,y):color}
    #if (j,i) grid position is in locked_pos{}, set grid[i][j] to color specified for that locked_pos{} item
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j,i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):

    #obtain the square positions that the tetromino occupies on the grid

    positions = []

    #retrieve index representing the tetromino orientation
    #remember modulous retrieves the remainder, so format will always be one of the orientations of a tetronmio
    #remember a tetromino is a nested list, so format will be one of the lists inside a tetromino list [[format]]
    #format will be an int indicating the index of the tetromino orientation

    '''
    example with L tetromino which has (4) orientations
    0%4 = 0, 1%4 = 1, 2%4 = 2, 3%4 = 3, 4%4 = 0, 5%4 = 1, 6%4 = 2, 7%4 = 3, 8%4 = 0, 9%4 = 1
    '''

    format = shape.shape[shape.rotation % len(shape.shape)]

    # sift through the tetronmino orientation matrix[], append coordinates of tetromino to positions[], return positions[]
    # for each line (row) look at each item in line
    # i tracks index of column (y)
    # j tracks index of row (x)
    # if it's a '0' there's a block, 
        # get current x value of the shape and add j to it
        # get current y value of the shape and add i to it
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    #offset positions
    #move everything left and up

    '''
    Looking at the tetromino, notice how the piece is offset in the middle of the matrix.
    This offset moves the piece up and left inside its matrix so each piece is being referenced from the same spot within the matrix.
    Don't over think it, but it does make sense about needing to reference the piece from the same top left spot

    ['.....',
      '..0..',
      '.000.',
      '.....',
      '.....']

    '''

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):

    #check if tetromino occupies valid grid space
    #get list of grid squares that are not occupied by a tetromino
    #get list of grid squares the current tetromino occupies
    #compare lists

    #get spaces that don't have a block in it
    #flatten list
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    #get positions taken up by piece
    formatted = convert_shape_format(shape)

    #for each formatted position, check if position is an accepted position, and position is within the grid
    #when a piece starts at top of screen the piece will be outside of grid, only want to check for valid positions when piece falls within the grid
    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    #check if any locked_positions{} are above the grid
    #if so, game is over
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape():
    #randomly choose a tetronmino to play
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(surface, text, size, color):
    #draw title
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    #draw grid lines 
    for i in range(len(grid)):
        #draw horizontal lines
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx+play_width, sy+ i*block_size))
        for j in range(len(grid[i])):
            #draw vertical lines
            pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy),(sx + j*block_size, sy + play_height))


def clear_rows(grid, locked):
    #remember, locked represents the locked_positions{} dict of {(x,y):color}
    
    #keep track of how many rows are cleared
    inc = 0

    #starting from the bottom and moving upwards, check if there's a row with no black squares (i.e. a full row)
    #increase inc by (1) for each full row
    #use ind to track what the topmost full row is (this will be used to move all rows above the topmost full row down the grid)
    #get position of each square in the full row and delete that positon from locked_positions{}
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue

    #shift every row down by the number of rows cleared
    if inc > 0:
        #for every key in locked{}, sort the keys by the y value of the keys
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            #if y of key is less than (i.e. above) the top most full row, that grid's position needs to move down on the grid (i.e. the y position increases by the number of cleared rows) 
            #create new key based the row that's being moved down
            #add new key to dictionary, set new key to color of old key
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))


def update_score(nscore):
    score = max_score()

    #if score at end of game is greater than current high scrore, note down new high score in scores.txt
    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def max_score():
    #get the max score from the score.txt file
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score


def draw_window(surface, grid, score=0, last_score = 0):
    surface.fill((0, 0, 0))

    pygame.font.init()

    #title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255, 255, 255))
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    # current score
    font = pygame.font.SysFont('comicsans', 20)
    label = font.render('Score: ' + str(score), 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    surface.blit(label, (sx + 20, sy + 160))

    # last score
    label = font.render('High Score: ' + last_score, 1, (255,255,255))

    sx = top_left_x - 200
    sy = top_left_y + 200

    surface.blit(label, (sx + 10, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

    draw_grid(surface, grid)
    #pygame.display.update()


def main(win):  # *
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0 #track how long since last loop ran
    fall_speed = 0.57 #how long it takes before each tetromino falls again, decrease this number to have the tetrominos fall faster
    level_time = 0
    score = 0

    #for as long as the game is running
    #game loop
    while run:

        #constantly update grid
        grid = create_grid(locked_positions)

        #track how long since last loop ran, add that time to fall_time(), ensures game runs at same pace on every OS
        #get_rawtime(): the number of milliseconds that have passed between the previous two calls to Clock.tick()  
        fall_time += clock.get_rawtime() 
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005

        #move piece down screen one row
        # check if piece moves into invalid space (i.e. grid square already occupied) or piece hits the bottom of the grid
        #if yes, set change_piece to true to go through logic that indicates current_piece is done and need to start new piece
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()


            #remember, if player moves piece down into an occupied grid square, the piece will move back to its previous grid square
            #in the next run loop, the piece will move down one row, set change_pice to true, and then the change_piece logic will execute.
            #in other words, the player moving the piece into an occupied grid square will be taken care of in the next run loop, not this current run loop.

            #left : move piece to the left
            #right: move piece to the right
            #down: move piece down
            #up: add 1 to current_piece rotation to choose piece orientation
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        #get all grid squares the tetromino currently occupies
        #will return list[] of grid squares tetromino occupies
        shape_pos = convert_shape_format(current_piece)

        #for each grid square tetromino occupies, change the grid square to the tetromino's color
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        #if a shape hits an occupied grid square or hits the ground a new peice starts (i.e. change_piece == True)
        # add the grid squares that the tetromino now occupies to locked_positions{}
            #grid squares will be the key for the dict{} item
            #value of dict{} item will be the color of the tetromino
        #change current_piece to the next_piece
        # get a new piece for next_piece
        # change_piece is set back to false so don't start a new piece down the board
        # calculate score based on if any rows clear, and add 10pts for each row cleared
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        #draw window
        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        #check for lost game
        if check_lost(locked_positions):
            draw_text_middle(win, "YOU LOST!", 80, (255,255,255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)

#starting menu when program starts
def main_menu(win):  # *
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle(win, 'Press Any Key To Play', 60, (255,255,255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()

#start the pygame
win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)