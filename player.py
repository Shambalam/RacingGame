import pygame as pg
import math
from settings import *

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE

        # Movement physics
        self.velocity = 0.0
        self.acceleration = 5
        self.friction = 2
        self.max_speed = 50
        self.max_reverse = -2
        self.brake_force = 4
        self.drift_factor = 2

        # Camera
        self.camera_x = self.x
        self.camera_y = self.y
        self.camera_distance = 2.0  # tiles behind
        self.camera_lerp = 0.1      # smoothing factor

        # Sprite
        self.car_image = pg.image.load("resources/textures/car.png").convert_alpha()
        self.sprite_angle = 0.0  # current visual rotation
        self.max_sprite_angle = 45  # degrees
        self.sprite_turn_speed = 180  # degrees per second
        self.sprite_return_speed = 240  # degrees per second

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
        self.angle %= math.tau

        # --- Acceleration / deceleration ---
        if keys[pg.K_w]:
            self.velocity += self.acceleration * self.game.delta_time
        elif keys[pg.K_s]:
            self.velocity -= self.acceleration * self.game.delta_time
        else:
            # Natural friction
            if self.velocity > 0:
                self.velocity -= self.friction * self.game.delta_time
                if self.velocity < 0: self.velocity = 0
            elif self.velocity < 0:
                self.velocity += self.friction * self.game.delta_time
                if self.velocity > 0: self.velocity = 0

        # --- Braking ---
        if keys[pg.K_SPACE]:
            if self.velocity > 0:
                self.velocity -= self.brake_force * self.game.delta_time
                if self.velocity < 0: self.velocity = 0
            elif self.velocity < 0:
                self.velocity += self.brake_force * self.game.delta_time
                if self.velocity > 0: self.velocity = 0

        # Clamp velocity
        self.velocity = max(min(self.velocity, self.max_speed), self.max_reverse)

        # --- Movement vector ---
        dx = math.cos(self.angle) * self.velocity * self.game.delta_time
        dy = math.sin(self.angle) * self.velocity * self.game.delta_time

        # --- Drifting while braking + turning ---
        if keys[pg.K_SPACE] and (keys[pg.K_a] or keys[pg.K_d]):
            side_dx = math.cos(self.angle + math.pi/2) * self.drift_factor * self.game.delta_time
            side_dy = math.sin(self.angle + math.pi/2) * self.drift_factor * self.game.delta_time
            if keys[pg.K_a]:
                dx -= side_dx
                dy -= side_dy
            if keys[pg.K_d]:
                dx += side_dx
                dy += side_dy

        keys = pg.key.get_pressed()
        dt = self.game.delta_time  # convert to seconds

        # --- Steering visual offset ---
        if keys[pg.K_a]:
            self.sprite_angle -= self.sprite_turn_speed * dt
        elif keys[pg.K_d]:
            self.sprite_angle += self.sprite_turn_speed * dt
        else:
            # Return to center when no input
            if self.sprite_angle > 0:
                self.sprite_angle -= self.sprite_return_speed * dt
                if self.sprite_angle < 0:
                    self.sprite_angle = 0
            elif self.sprite_angle < 0:
                self.sprite_angle += self.sprite_return_speed * dt
                if self.sprite_angle > 0:
                    self.sprite_angle = 0

        # Clamp between -45 and +45 degrees
        self.sprite_angle = max(-self.max_sprite_angle,
                                min(self.sprite_angle, self.max_sprite_angle))

        # Apply collision
        self.check_wall_collision(dx, dy)

        # --- Update camera ---
        cam_target_x = self.x - math.cos(self.angle) * self.camera_distance
        cam_target_y = self.y - math.sin(self.angle) * self.camera_distance
        self.camera_x += (cam_target_x - self.camera_x) * self.camera_lerp
        self.camera_y += (cam_target_y - self.camera_y) * self.camera_lerp

    def check_wall_collision(self, dx, dy):
        next_x = self.x + dx
        next_y = self.y + dy

        # Four-point collision
        points_x = [(next_x + PLAYER_RADIUS, self.y), (next_x - PLAYER_RADIUS, self.y)]
        points_y = [(self.x, next_y + PLAYER_RADIUS), (self.x, next_y - PLAYER_RADIUS)]
        points_diag = [
            (next_x + PLAYER_RADIUS, next_y + PLAYER_RADIUS),
            (next_x - PLAYER_RADIUS, next_y + PLAYER_RADIUS),
            (next_x + PLAYER_RADIUS, next_y - PLAYER_RADIUS),
            (next_x - PLAYER_RADIUS, next_y - PLAYER_RADIUS),
        ]

        if all((int(px), int(py)) not in self.game.map.world_map for (px, py) in points_x):
            self.x = next_x
        if all((int(px), int(py)) not in self.game.map.world_map for (px, py) in points_y):
            self.y = next_y
        # Optional diagonal check
        if all((int(px), int(py)) not in self.game.map.world_map for (px, py) in points_diag):
            self.x = next_x
            self.y = next_y

    def draw(self, screen):
        # Rotate the sprite around its center
        rotated = pg.transform.rotate(self.car_image, -self.sprite_angle)
        print(self.sprite_angle)
        rect = rotated.get_rect(center=(HALF_WIDTH, HALF_HEIGHT + 250))

        screen.blit(rotated, rect)

    def update(self):
        self.movement()
