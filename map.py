import pygame as pg

_ = False  # empty space
# 1 = wall
mini_map = [
    [1]*40,
    [1]+[_]*38+[1],
    [1]+[_]*38+[1],
    [1]+[_]*38+[1],
    [1]+[_]*38+[1],
    [1]+[_]*38+[1],
    [1]+[_]*15+[1]*10+[_]*13+[1],
    [1]+[_]*15+[1]*10+[_]*13+[1],
    [1]+[_]*15+[1]*10+[_]*13+[1],
    [1]+[_]*38+[1],
    [1]+[_]*38+[1],
    [1]+[_]*38+[1],
    [1]+[_]*10+[1]*20+[_]*8+[1],
    [1]+[_]*10+[1]*20+[_]*8+[1],
    [1]+[_]*10+[1]*20+[_]*8+[1],
    [1]+[_]*38+[1],
    [1]+[_]*38+[1],
    [1]+[_]*38+[1],
    [1]+[_]*38+[1],
    [1]+[_]*38+[1],
    [1]+[_]*38+[1],
    [1]+[_]*38+[1],
    [1]+[_]*38+[1],
    [1]+[_]*38+[1],
    [1]*40,
]


class Map:
    def __init__(self, game):
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}
        self.get_map()

    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, cell in enumerate(row):
                if cell:
                    self.world_map[(i,j)] = cell

    def draw(self):
        [pg.draw.rect(self.game.screen, 'darkgray', (pos[0] * 100,pos[1] * 100, 100, 100), 2)
         for pos in self.world_map]