import pygame
import os

# Game setup
WIDTH = 1280
HEIGHT = 600
FPS = 60
TILESIZE = 32

# Colours
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)

# Player settings
PLAYER_START_X = WIDTH / 2
PLAYER_START_Y = HEIGHT / 2
PLAYER_SIZE = 0.35
PLAYER_SPEED = 5
GUN_OFFSET_X = 45
GUN_OFFSET_Y = 20
PLAYER_HEALTH = 100

# Bullet settings
SHOOT_COOLDOWN = 10
BULLET_SCALE = 1.4
BULLET_SPEED = 50
BULLET_LIFETIME = 400
BULLET_DAMAGE = 100

# Enemy settings

shape_data = {
    "circle": {"health": 100, "attack_damage": 10, "speed": 2, "sides": 1, "colour": (0, 200, 255), "radius": 15, "exp": 10},
    "triangle": {"health": 300, "attack_damage": 30, "speed": 2, "sides": 3, "colour": (255, 255, 0), "radius": 30, "exp": 30},
    "square": {"health": 400, "attack_damage": 40, "speed": 1, "sides": 4, "colour": (255, 51, 242), "radius": 30, "exp": 40},
    "pentagon": {"health": 500, "attack_damage": 50, "speed": 1, "sides": 5, "colour": (0, 0, 10), "radius": 20, "exp": 50},
    "hexagon": {"health": 600, "attack_damage": 60, "speed": 1, "sides": 6, "colour": (0, 255, 150), "radius": 20, "exp": 60},
    "septagon": {"health": 700, "attack_damage": 70, "speed": 1, "sides": 7, "colour": (0, 0, 100), "radius": 20, "exp": 70},
    "octagon": {"health": 800, "attack_damage": 80, "speed": 1, "sides": 8, "colour": (255, 0, 0), "radius": 20, "exp": 80},
}
