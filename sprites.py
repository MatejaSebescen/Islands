import random

import pygame
from settings import *


class Tile:
    def __init__(self, x, y, color, level):
        self.x, self.y = x * TILESIZE, y * TILESIZE
        self.color = color
        self.level = level
        if level == 0:
            self.islandNum = -1
        else:
            self.islandNum = 0
            self.setTileColor()

    def setTileColor(self):
        if 0 < self.level < 300:
            self.color = LVL200
        elif 300 <= self.level < 400:
            self.color = LVL300
        elif 400 <= self.level < 500:
            self.color = LVL400
        elif 500 <= self.level < 600:
            self.color = LVL500
        elif 600 <= self.level < 700:
            self.color = LVL600
        elif 700 <= self.level < 800:
            self.color = LVL700
        elif 800 <= self.level < 900:
            self.color = LVL800
        elif 900 <= self.level < 950:
            self.color = LVL900
        elif self.level >= 950:
            self.color = LVL950

    def draw(self, board_surface):
        pygame.draw.rect(board_surface, self.color, (self.x, self.y, TILESIZE, TILESIZE))

    def __repr__(self):
        return str(self.level)


class Board:
    def __init__(self, request_text):
        self.map_values = {}
        self.board_surface = pygame.Surface((WIDTH, HEIGHT))
        self.parseRequest(request_text)
        self.NumOfIslands = 0
        self.islands = []
        self.toCheck = []
        self.findIslands()

        self.best_average = 0
        self.best_islands = []
        self.calculateAverages()
        self.placed_X = 0

        self.player_score = 0

        pygame.font.init()
        self.text_size = TEXT_SIZE
        self.my_font = pygame.font.SysFont('Calibri', self.text_size)
        self.score_text = "Score: " + str(self.player_score)
        self.text_surface = self.my_font.render(self.score_text, True, WHITE)

    def parseRequest(self, request_text):
        print(request_text)
        substring = request_text.split()
        for i in range(0, ROWS):
            for j in range(0, COLS - 3):
                self.map_values.__setitem__((i, j), Tile(i, j, BGCOLOUR, int(substring[i + j * (COLS - 3)])))
        for i in range(0, ROWS):
            for j in range(COLS - 3, COLS):
                self.map_values.__setitem__((i, j), Tile(i, j, BGCOLOUR, 0))

    #  print(self.map_values)

    def findIslands(self):
        for tile in self.map_values:
            if self.map_values[tile].islandNum == 0:
                self.NumOfIslands += 1
                self.islands.insert(self.NumOfIslands - 1, set())
                self.toCheck.append(tile)
                while self.toCheck:
                    self.setIslandNumber(self.toCheck.pop())

    def setIslandNumber(self, tile):
        self.map_values[tile].islandNum = self.NumOfIslands
        if self.is_inside(tile[0] - 1, tile[1]) and self.map_values[(tile[0] - 1, tile[1])].islandNum == 0 and (
                tile[0] - 1, tile[1]) not in self.toCheck:
            self.toCheck.append((tile[0] - 1, tile[1]))
        if self.is_inside(tile[0] + 1, tile[1]) and self.map_values[(tile[0] + 1, tile[1])].islandNum == 0 and (
                tile[0] + 1, tile[1]) not in self.toCheck:
            self.toCheck.append((tile[0] + 1, tile[1]))
        if self.is_inside(tile[0], tile[1] - 1) and self.map_values[(tile[0], tile[1] - 1)].islandNum == 0 and (
                tile[0], tile[1] - 1) not in self.toCheck:
            self.toCheck.append((tile[0], tile[1] - 1))
        if self.is_inside(tile[0], tile[1] + 1) and self.map_values[(tile[0], tile[1] + 1)].islandNum == 0 and (
                tile[0], tile[1] + 1) not in self.toCheck:
            self.toCheck.append((tile[0], tile[1] + 1))
        self.islands[self.NumOfIslands - 1].add(tile)

    def averageHeight(self, x, y):
        average = 0
        num_of_tiles = 0
        target_island = self.map_values[(x, y)].islandNum
        for island in self.islands[target_island - 1]:
            average += self.map_values[island].level
            num_of_tiles += 1
        average /= num_of_tiles
        return average

    def calculateAverages(self):
        for islandNum in range(0, len(self.islands)):
            average = 0
            tile_nums = 0
            for tile in self.islands[islandNum]:
                average += self.map_values[tile].level
                tile_nums += 1
            average /= tile_nums
            if average == self.best_average:
                self.best_islands.append(islandNum + 1)
            elif average > self.best_average:
                self.best_islands.clear()
                self.best_average = average
                self.best_islands.append(islandNum + 1)
        print(self.best_islands)

    def isWinner(self, x, y):
        if self.map_values[(x, y)].islandNum in self.best_islands:
            for islands in self.islands[self.map_values[(x, y)].islandNum-1]:
                self.map_values[islands].color = GREEN
            return True
        else:
            for islands in self.islands[self.map_values[(x, y)].islandNum-1]:
                self.map_values[islands].color = RED
            return False

    @staticmethod
    def is_inside(x, y):
        return 0 <= x < ROWS and 0 <= y < (COLS - 3)

    def draw(self, screen):
        for row in self.map_values:
            self.map_values.get(row).draw(self.board_surface)
        for i in range(0, WIDTH):
            self.board_surface.set_at((i, (COLS - 3) * TILESIZE), BLACK)
            self.board_surface.set_at((i, (COLS - 3) * TILESIZE + 1), BLACK)
            self.board_surface.set_at((i, (COLS - 3) * TILESIZE + 2), BLACK)
            self.board_surface.set_at((i, COLS * TILESIZE), BGCOLOUR)
            self.board_surface.set_at((i, COLS * TILESIZE + 1), BGCOLOUR)
            self.board_surface.set_at((i, COLS * TILESIZE + 2), BGCOLOUR)
        self.board_surface.blit(tile_score_menu, (0,(COLS - 3) * TILESIZE + 6))
        self.placeX()
        self.score_text = "Score: " + str(self.player_score)
        self.text_surface = self.my_font.render(self.score_text, True, WHITE)
        screen.blit(self.board_surface, (0, 0))
        text_rect = self.text_surface.get_rect(center=(15, HEIGHT - 1.5 * TILESIZE))
        text_rect.x = TILESIZE/2
        screen.blit(self.text_surface, text_rect)

    def placeX(self):
        for i in range(0, self.placed_X):
            self.board_surface.blit(tile_X, ((ROWS - 3) * TILESIZE - i * TILESIZE * 3, (COLS - 3) * TILESIZE + 6))

    def display_board(self):
        pass
        # curr_x, curr_y = 0, 0
        # for row in self.map_values:
        #     print(self.map_values.get(row), end=" ")
        #     temp_x, temp_y = row
        #     if temp_x != curr_x:
        #         print("\n", end="")
        #         curr_x = temp_x

    def callNewMap(self, request_text):
        self.map_values.clear()
        self.parseRequest(request_text)
        self.NumOfIslands = 0
        self.islands.clear()
        self.toCheck.clear()
        self.findIslands()

        self.best_average = 0
        self.best_islands.clear()
        self.calculateAverages()


class Menu:
    def __init__(self):
        self.text = "Game Over"
        self.restart_text = "Click Anywhere to Continue"
        self.isVisible = False
        self.board_surface = pygame.Surface(tile_menu.get_size())

        pygame.font.init()
        self.text_size = TEXT_SIZE + 5
        self.my_font = pygame.font.SysFont('Calibri', self.text_size)

    def draw(self, screen):
        if self.isVisible:
            self.board_surface.blit(tile_menu, (0,0))
            screen.blit(self.board_surface, self.board_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2 + TILESIZE)))
            self.text_surface = self.my_font.render(self.text, True, WHITE)
            screen.blit(self.text_surface, self.text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2)))
            self.text_surface = self.my_font.render(self.restart_text, True, WHITE)
            screen.blit(self.text_surface, self.text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2 + self.text_size + 9)))
