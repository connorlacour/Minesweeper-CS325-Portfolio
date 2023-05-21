import sys
import math
import random
import numpy as np
import pygame as game
from pygame.locals import *


# revealed_array guide:
#   0 = empty
#   1 = num revealed

# cells_array guide:
#   -1 = bomb
#   0+ = value is equal to number of adjacent bombs

def make_2d_array():
    w = 22
    h = 22
    arr = [[0 for x in range(w)] for y in range(h)]
    # print(arr)
    return arr


class Board:
    def __init__(self, size, difficulty):
        """
        surface is the screen on which the game is drawn
        size is the number of rows & columns (ie. a size of 10 would be 10x10 rows x columns
        difficulty is the number of bombs generated.
        """
        self.draw_time = game.time.get_ticks()
        self.cool_down = 160
        self.surface = game.display.set_mode((600, 600))
        self.flag_array = []
        self.lose = False
        self.win = False

        self.size = size
        self.difficulty = difficulty

        self.main()

    def main(self):
        # initialize basic screen components
        game.init()
        game.display.set_caption('Welcome to Minesweeper')

        player_lost = False

        # fill background with off-white
        background = game.Surface(self.surface.get_size())
        background = background.convert()
        background.fill((200, 200, 200))

        # Blit background to the screen
        self.surface.blit(background, (0, 0))
        game.display.flip()

        # draw lines
        self.draw_board()

        # generate blank array
        cells_array = make_2d_array()

        # generate array to track whether or not a cell has been revealed
        # 0 = hidden
        # 1 = revealed
        # all cells begin hidden
        revealed_array = make_2d_array()

        # generate bomb positions
        self.generate_bombs(cells_array)

        # generate clue positions
        # MUST occur after generate_bombs is called
        self.generate_clues(cells_array)

        # draws all cells, for testing purposes only
        # self.draw_all_cells(cells_array)

        # Event loop to maintain game until window is closed or game ends
        while 1:

            for event in game.event.get():
                if event.type == game.QUIT:
                    return
                if self.lose is False:
                    if self.win is False:
                        self.mouse_click(cells_array, revealed_array)
                else:
                    pressed_keys = game.key.get_pressed()
                    if pressed_keys[K_SPACE]:
                        self.lose = False
                        self.flag_array = []
                        self.main()
                if self.check_for_win(cells_array, revealed_array):
                    self.win = True
                    self.display_win_message()
                    pressed_keys = game.key.get_pressed()
                    if pressed_keys[K_SPACE]:
                        self.win = False
                        self.flag_array = []
                        self.main()

            game.display.update()

    def mouse_click(self, cells_array, revealed_array):
        # if left mouse button clicked, reveal cell
        if game.mouse.get_pressed(3) == (True, False, False):
            mouse_pos = game.mouse.get_pos()
            x_mouse = int((mouse_pos[0] - 25) // 25)
            y_mouse = int((mouse_pos[1] - 25) // 25)

            if 0 <= x_mouse <= 21 and 0 <= y_mouse <= 21:
                # check if revealed
                # if not revealed, call draw_one_cell with index
                if revealed_array[x_mouse][y_mouse] == 0:
                    self.draw_one_cell(x_mouse, y_mouse, cells_array)
                    revealed_array[x_mouse][y_mouse] = 1

                    # if clicked zero, reveal other bordering zeros
                    if cells_array[x_mouse][y_mouse] == 0:
                        self.check_for_zeros(cells_array, revealed_array, x_mouse, y_mouse)

            else:
                print('oops you clicked off the board!')

        # flag on right click
        if game.mouse.get_pressed(3) == (False, False, True):
            mouse_pos = game.mouse.get_pos()
            x_mouse = int((mouse_pos[0] - 25) // 25)
            y_mouse = int((mouse_pos[1] - 25) // 25)

            # if on the board:
            if 0 <= x_mouse <= 21 and 0 <= y_mouse <= 21:

                now = game.time.get_ticks()
                # if enough time has passed, we can append.
                # otherwise, we append several dozen per click
                if now - self.draw_time >= self.cool_down:
                    # check if revealed
                    # if not revealed, call append to flag_array and mark as revealed
                    self.draw_time = now
                    if revealed_array[x_mouse][y_mouse] == 0:
                        self.flag_array.append([x_mouse, y_mouse])
                        self.draw_flag(x_mouse, y_mouse)
                        revealed_array[x_mouse][y_mouse] = 1

                    # un-flag if already flagged
                    else:
                        for i in range(0, len(self.flag_array)):
                            if self.flag_array[i][0] == x_mouse and self.flag_array[i][1] == y_mouse:
                                del self.flag_array[i]
                                self.draw_empty(x_mouse, y_mouse)
                                revealed_array[x_mouse][y_mouse] = 0

            else:
                print('oops you clicked off the board!')

    def draw_board(self):

        dark_grey = (50, 50, 50)

        # draw outline
        r = Rect(25, 25, 550, 550)
        game.draw.rect(surface=self.surface, color=dark_grey, rect=r, width=1)

        # draw grid
        x_start = 25
        y = 50
        x_end = 574

        y_start = 25
        x = 50
        y_end = 574

        for i in range(0, 21):
            x_start_pos = (x_start, y)
            x_end_pos = (x_end, y)
            y_start_pos = (x, y_start)
            y_end_pos = (x, y_end)

            game.draw.line(surface=self.surface, color=dark_grey, start_pos=x_start_pos, end_pos=x_end_pos)
            game.draw.line(surface=self.surface, color=dark_grey, start_pos=y_start_pos, end_pos=y_end_pos)

            y += 25
            x += 25

    def draw_one_cell(self, x_index, y_index, cells_array):

        dark_grey = (50, 50, 50)
        medium_grey = (140, 140, 140)
        red = (255, 0, 0)

        font = game.font.SysFont(None, 24)

        # calculate center of bomb circle based on index of array
        def circle_center(index_x, index_y):
            c = (37.5 + (index_x * 25), 37.5 + (index_y * 25))
            return c

        def text_center(x, y):
            c = (34.5 + (x * 25), 30.9 + (y * 25))
            return c

        # draw bomb
        if cells_array[x_index][y_index] == -1:
            center = circle_center(x_index, y_index)

            x_pos = (x_index * 25) + 26
            y_pos = (y_index * 25) + 26
            r = Rect(x_pos, y_pos, 24, 24)

            game.draw.rect(surface=self.surface, color=red, rect=r)
            game.draw.circle(surface=self.surface, color=dark_grey, center=center, radius=8)

            # player loses
            self.lose = True
            self.display_loss_message()

        # draw empty space
        elif cells_array[x_index][y_index] == 0:
            x_pos = (x_index * 25) + 26
            y_pos = (y_index * 25) + 26
            r = Rect(x_pos, y_pos, 24, 24)
            game.draw.rect(surface=self.surface, color=medium_grey, rect=r)

        # display value of clue
        else:
            x_pos = (x_index * 25) + 26
            y_pos = (y_index * 25) + 26
            r = Rect(x_pos, y_pos, 24, 24)
            center = text_center(x_index, y_index)

            # val = text to be displayed
            val = str(cells_array[x_index][y_index])

            # draw 1 as blue
            if val == '1':
                game.draw.rect(surface=self.surface, color=medium_grey, rect=r)
                img = font.render(val, True, (0, 0, 255))
                self.surface.blit(img, center)

            # draw 2 as red
            elif val == '2':
                game.draw.rect(surface=self.surface, color=medium_grey, rect=r)
                img = font.render(val, True, (255, 0, 0))
                self.surface.blit(img, center)

            # draw 3 as green
            elif val == '3':
                game.draw.rect(surface=self.surface, color=medium_grey, rect=r)
                img = font.render(val, True, (0, 255, 0))
                self.surface.blit(img, center)

            # draw 4 as indigo
            elif val == '4':
                game.draw.rect(surface=self.surface, color=medium_grey, rect=r)
                img = font.render(val, True, (51, 0, 153))
                self.surface.blit(img, center)

            # draw 5 as maroon
            elif val == '5':
                game.draw.rect(surface=self.surface, color=medium_grey, rect=r)
                img = font.render(val, True, (128, 21, 0))
                self.surface.blit(img, center)

            # draw 6 as turquoise
            elif val == '6':
                game.draw.rect(surface=self.surface, color=medium_grey, rect=r)
                img = font.render(val, True, (51, 255, 221))
                self.surface.blit(img, center)

            # draw 7 as black
            elif val == '7':
                game.draw.rect(surface=self.surface, color=medium_grey, rect=r)
                img = font.render(val, True, (240, 240, 240))
                self.surface.blit(img, center)

            # draw 8 as grey
            else:
                game.draw.rect(surface=self.surface, color=medium_grey, rect=r)
                img = font.render(val, True, (140, 140, 140))
                self.surface.blit(img, center)

    def draw_flag(self, x_index, y_index):
        medium_grey = (140, 140, 140)

        x_pos = (x_index * 25) + 26
        y_pos = (y_index * 25) + 26
        r = Rect(x_pos, y_pos, 24, 24)

        def flag_center(x, y):
            c = (30 + (x * 25), 30 + (y * 25))
            return c

        center = flag_center(x_index, y_index)

        # load flag image
        player_img = game.image.load('minesweeper_flag_1.png').convert()
        player_img = game.transform.scale(player_img, (18, 18))
        player_img.set_colorkey((255, 255, 255))

        game.draw.rect(surface=self.surface, color=medium_grey, rect=r)
        self.surface.blit(player_img, center)

    def draw_empty(self, x_index, y_index):

        light_grey = (200, 200, 200)

        x_pos = (x_index * 25) + 26
        y_pos = (y_index * 25) + 26
        r = Rect(x_pos, y_pos, 24, 24)
        game.draw.rect(surface=self.surface, color=light_grey, rect=r)

    def check_for_zeros(self, cells_array, revealed_array, x_pos, y_pos):

        adjacent_cells = self.generate_adjacent_cells(x_pos, y_pos)

        for i in range(0, len(adjacent_cells)):

            if revealed_array[adjacent_cells[i][0]][adjacent_cells[i][1]] != 1:
                if cells_array[adjacent_cells[i][0]][adjacent_cells[i][1]] > 0:
                    self.draw_one_cell(adjacent_cells[i][0], adjacent_cells[i][1], cells_array)
                    revealed_array[adjacent_cells[i][0]][adjacent_cells[i][1]] = 1

                elif cells_array[adjacent_cells[i][0]][adjacent_cells[i][1]] == 0:
                    self.draw_one_cell(adjacent_cells[i][0], adjacent_cells[i][1], cells_array)
                    revealed_array[adjacent_cells[i][0]][adjacent_cells[i][1]] = 1
                    self.check_for_zeros(cells_array, revealed_array, adjacent_cells[i][0], adjacent_cells[i][1])

    def generate_adjacent_cells(self, x_pos, y_pos):
        l = self.size - 1

        adjacent_cells_array = []
        if y_pos != 0:
            if x_pos != 0:
                adjacent_cells_array.append([x_pos - 1, y_pos - 1])
            adjacent_cells_array.append([x_pos, y_pos - 1])
            if x_pos != l:
                adjacent_cells_array.append([x_pos + 1, y_pos - 1])

        if x_pos != 0:
            adjacent_cells_array.append([x_pos - 1, y_pos])
        if x_pos != l:
            adjacent_cells_array.append([x_pos + 1, y_pos])

        if y_pos != l:
            if x_pos != 0:
                adjacent_cells_array.append([x_pos - 1, y_pos + 1])
            adjacent_cells_array.append([x_pos, y_pos + 1])
            if x_pos != l:
                adjacent_cells_array.append([x_pos + 1, y_pos + 1])

        return adjacent_cells_array

    def generate_bombs(self, array):
        no_of_bombs = self.difficulty

        for b in range(0, no_of_bombs):
            pos_x = random.randint(0, 21)
            pos_y = random.randint(0, 21)

            # if bomb already exists here, step back one in the loop and try again
            # this ensures we always generate the same number of bombs per game
            if array[pos_x][pos_y] == -1:
                b -= 1
            else:
                array[pos_x][pos_y] = -1

        return array

    def generate_clues(self, array):
        l = self.size

        # for each cell
        for i in range(0, l):
            for j in range(0, l):
                # check for bomb, 0 = no bomb
                if array[i][j] == 0:

                    # generate adjacent cells to be checked
                    adjacent_cells = self.generate_adjacent_cells(i, j)
                    clue_count = 0

                    # for each cell, calculate number of bombs in adjacent cells
                    for g in range(0, len(adjacent_cells)):

                        # if value at adjacent cell is -1, we found a bomb
                        # if bomb is adjacent, increment the count
                        if array[adjacent_cells[g][0]][adjacent_cells[g][1]] == -1:
                            clue_count += 1

                    array[i][j] = clue_count

        return array

    def check_for_win(self, cells_array, revealed_array):

        # loop the board
        for i in range(0, self.size):
            for j in range(0, self.size):

                # if cell is not a bomb
                # if it is a bomb, it does not need to be flagged
                if cells_array[i][j] >= 0:

                    # if cell is not revealed, not a win state
                    if revealed_array[i][j] != 1:
                        return False

                    cell_coord = [i, j]
                    # if non-bomb cell is flagged, not a win state
                    if cell_coord in self.flag_array:
                        return False
        # if not returned False, return True for win
        return True

    def display_win_message(self):
        black = (10, 10, 10)
        light_grey = (215, 215, 215)
        white = (255, 255, 255)

        x_index = 115
        y_index = 280

        font = game.font.SysFont(None, 34)
        font2 = game.font.SysFont(None, 25)

        outer_rect = Rect(x_index, y_index, 375, 85)
        inner_rect = Rect(x_index + 5, y_index + 5, 365, 75)
        center = (x_index + 125, y_index + 30)
        center2 = (x_index + 80, y_index + 55)

        # val = text to be displayed
        val = 'You Won!!'
        val2 = 'press space to play again'

        img = font.render(val, True, black)
        img2 = font2.render(val2, True, black)

        game.draw.rect(surface=self.surface, color=light_grey, rect=outer_rect)
        game.draw.rect(surface=self.surface, color=white, rect=inner_rect)

        self.surface.blit(img2, center2)
        self.surface.blit(img, center)

    def display_loss_message(self):
        black = (10, 10, 10)
        medium_grey = (140, 140, 140)
        white = (255, 255, 255)

        x_index = 115
        y_index = 280

        font = game.font.SysFont(None, 25)

        outer_rect = Rect(x_index, y_index, 375, 85)
        inner_rect = Rect(x_index + 5, y_index + 5, 365, 75)
        center = (x_index + 141, y_index + 28)
        center2 = (x_index + 19, y_index + 42)

        # val = text to be displayed
        val = 'You lost!'
        val2 = 'If you would like to try again, press ''space'''

        img = font.render(val, True, black)
        img2 = font.render(val2, True, black)
        game.draw.rect(surface=self.surface, color=medium_grey, rect=outer_rect)
        game.draw.rect(surface=self.surface, color=white, rect=inner_rect)
        self.surface.blit(img, center)
        self.surface.blit(img2, center2)

    def draw_all_cells(self, array):

        dark_grey = (50, 50, 50)
        darker_grey = (20, 20, 20)

        font = game.font.SysFont(None, 24)

        # calculate center of bomb circle based on index of array
        def circle_center(index_x, index_y):
            c = (37.5 + (index_x * 25), 37.5 + (index_y * 25))
            return c

        def text_center(index_x, index_y):
            c = (32.5 + (index_x * 25), 32.5 + (index_y * 25))
            return c

        # if bomb, draw circle
        # else, draw text = val of array at index
        for i in range(0, len(array)):
            for j in range(0, len(array)):

                if array[i][j] == -1:
                    center = circle_center(i, j)
                    game.draw.circle(surface=self.surface, color=dark_grey, center=center, radius=8)

                else:
                    center = text_center(i, j)
                    val = str(array[i][j])
                    img = font.render(val, True, (255, 0, 0))
                    self.surface.blit(img, center)


Minesweeper = Board(22, 99)
