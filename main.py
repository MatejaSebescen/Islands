import pygame
from settings import *
from sprites import *
import requests


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.lives = MAX_LIVES
        self.state = 0

    def new(self):
        self.req = requests.get('https://jobfair.nordeus.com/jf24-fullstack-challenge/test')
       # file = open('islands.txt', 'r')
        #file.read()
        self.board = Board(self.req.text)
        self.board.display_board()
        self.menu = Menu()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()

    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.board.draw(self.screen)
        self.menu.draw(self.screen)

        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                mx //= TILESIZE
                my //= TILESIZE

                if self.state == 0:
                    if event.button == 1 and self.board.is_inside(mx, my) and self.board.map_values[
                        (mx, my)].islandNum != -1 and self.lives != 0 and self.board.map_values[(mx, my)].color != RED:
                        print(str(self.board.averageHeight(mx, my)))
                        # print(self.board.isWinner(mx, my))
                        if not self.board.isWinner(mx, my):
                            print("Not Best Island")
                            if self.lives > 0:
                                self.lives -= 1
                                if self.lives == 0:
                                    self.state = 1
                                    self.menu.text = "Game Over..."
                                    self.menu.restart_text = "Click Anywhere to restart"
                                    self.menu.isVisible = True
                            if self.board.placed_X < MAX_LIVES:
                                self.board.placed_X += 1
                            self.board.player_score -= LOSE_POINTS
                        else:
                            print("Best Island")
                            self.state = 2
                            self.board.player_score += WIN_POINTS
                            self.menu.text = "You win!"
                            self.menu.restart_text = "Click Anywhere to continue"
                            self.menu.isVisible = True
                    elif event.button == 1 and self.lives == 0:
                        print("Game Over")
                elif self.state == 1:
                    if event.button == 1:
                        self.lives = MAX_LIVES
                        self.board.placed_X = 0
                        self.board.player_score = 0
                        self.menu.isVisible = False
                        self.req = requests.get('https://jobfair.nordeus.com/jf24-fullstack-challenge/test')
                        self.board.callNewMap(self.req.text)
                        self.state = 0
                elif self.state == 2:
                    if event.button == 1:
                        self.menu.isVisible = False
                        self.req = requests.get('https://jobfair.nordeus.com/jf24-fullstack-challenge/test')
                        self.board.callNewMap(self.req.text)
                        self.state = 0


game = Game()
while True:
    game.new()
    game.run()
