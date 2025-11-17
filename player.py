import pygame as pg
import math
from settings import *

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def movement(self):
        keys = pg.key.get_pressed()

        # --- Rotation ---
        if keys[pg.K_a]:
            self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        if keys[pg.K_d]:
            self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        self.angle %= math.tau  # keep in [0, 2pi]

        # --- Movement ---
        dx, dy = 0, 0
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        speed = PLAYER_SPEED * self.game.delta_time

        if keys[pg.K_w]:
            dx += cos_a * speed
            dy += sin_a * speed
        if keys[pg.K_s]:
            dx -= cos_a * speed
            dy -= sin_a * speed

        self.check_wall_collision(dx, dy)

    def check_wall_collision(self, dx, dy):
        """Robust four-point collision for a circle in a tile map."""
        next_x = self.x + dx
        next_y = self.y + dy

        # Points to check: left/right edges for X, top/bottom edges for Y
        points_x = [(next_x + PLAYER_RADIUS, self.y),
                    (next_x - PLAYER_RADIUS, self.y)]
        points_y = [(self.x, next_y + PLAYER_RADIUS),
                    (self.x, next_y - PLAYER_RADIUS)]

        # Optional: add diagonal points to prevent corner clipping
        points_diag = [
            (next_x + PLAYER_RADIUS, next_y + PLAYER_RADIUS),
            (next_x - PLAYER_RADIUS, next_y + PLAYER_RADIUS),
            (next_x + PLAYER_RADIUS, next_y - PLAYER_RADIUS),
            (next_x - PLAYER_RADIUS, next_y - PLAYER_RADIUS),
        ]

        # Horizontal movement
        if all((int(px), int(py)) not in self.game.map.world_map for (px, py) in points_x):
            self.x = next_x

        # Vertical movement
        if all((int(px), int(py)) not in self.game.map.world_map for (px, py) in points_y):
            self.y = next_y

        # Uncomment below to fully prevent corner clipping (optional)
        # if all((int(px), int(py)) not in self.game.map.world_map for (px, py) in points_diag):
        #     self.x = next_x
        #     self.y = next_y

    def update(self):
        self.movement()

    def draw(self, screen):
        # Draw player
        pg.draw.circle(self.game.screen, 'green', (int(self.x * 100), int(self.y * 100)), int(PLAYER_RADIUS * 100))
        # Draw facing direction
        end_x = self.x + math.cos(self.angle)
        end_y = self.y + math.sin(self.angle)
        pg.draw.line(self.game.screen, 'yellow',
                     (int(self.x * 100), int(self.y * 100)),
                     (int(end_x * 100), int(end_y * 100)),
                     2)
