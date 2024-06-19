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
PLAYER_START_X = 1000
PLAYER_START_Y = 900
PLAYER_SIZE = 0.35
PLAYER_SPEED = 10
GUN_OFFSET_X = 45
GUN_OFFSET_Y = 20
PLAYER_HEALTH = 100

# Bullet settings
SHOOT_COOLDOWN = 10
BULLET_SCALE = 1.4
BULLET_SPEED = 50
BULLET_LIFETIME = 750
BULLET_DAMAGE = 10

# Enemy settings

shape_data = {
    "circle": {"health": 100, "attack_damage": 20, "speed": 5, "sides": 1, "colour": (0, 0, 255), "radius": 10},
    "triangle": {"health": 200, "attack_damage": 30, "speed": 5, "sides": 3, "colour": (0, 125, 125), "radius": 10},
}
