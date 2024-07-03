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
PLAYER_SIZE = 0.25
PLAYER_SPEED = 2
GUN_OFFSET_X = 45
GUN_OFFSET_Y = 20

# Bullet settings
BULLET_LIFETIME = 400

# Player classes
class_data = {
    "Gunner": {"health": 100, "damage": 10, "speed": 2, "cooldown": 20, "player_size": 0.25,
               "player_img": pygame.image.load('Graphics/long gun.png',), "bullet_speed": 80, "bullet_lifetime": 400,
               "pierce": 1, "bullet_size": 1.25, "bullet_img": pygame.image.load('Graphics/bullet_1.png'), "xoffset": 45, "yoffset": 20},
    "Wizard": {"health": 100, "damage": 20, "speed": 2, "cooldown": 50, "player_size": 0.25,
               "player_img": pygame.image.load('Graphics/wizard.png'), "bullet_speed": 40, "bullet_lifetime": 400,
               "pierce": 3, "bullet_size": 1.25, "bullet_img": pygame.image.load('Graphics/bullet_0.png'), "xoffset": 45, "yoffset": 20},
    "Sniper": {"health": 100, "damage": 80, "speed": 3, "cooldown": 100, "player_size": 0.25,
               "player_img": pygame.image.load('Graphics/sniper.png'), "bullet_speed": 80, "bullet_lifetime": 500,
               "pierce": 5, "bullet_size": 2, "bullet_img": pygame.image.load('Graphics/bullet_1.png'), "xoffset": 45, "yoffset": 20},
    "Crossbow": {"health": 100, "damage": 80, "speed": 3, "cooldown": 100, "player_size": 0.25,
               "player_img": pygame.image.load('Graphics/crossbow.png'), "bullet_speed": 20, "bullet_lifetime": 500,
               "pierce": 3, "bullet_size": 0.75, "bullet_img": pygame.image.load('Graphics/arrow.png'), "xoffset": -10, "yoffset": 10}
}

# Enemy settings
shape_data = {
    "circle": {"health": 10, "attack_damage": 15, "speed": 2, "sides": 1, "colour": (0, 200, 255), "radius": 15, "exp": 10},
    "triangle": {"health": 30, "attack_damage": 25, "speed": 2, "sides": 3, "colour": (255, 255, 0), "radius": 30, "exp": 30},
    "square": {"health": 40, "attack_damage": 40, "speed": 1, "sides": 4, "colour": (255, 51, 242), "radius": 30, "exp": 40},
    "pentagon": {"health": 50, "attack_damage": 50, "speed": 1, "sides": 5, "colour": (0, 0, 10), "radius": 25, "exp": 50},
    "hexagon": {"health": 60, "attack_damage": 60, "speed": 1, "sides": 6, "colour": (0, 255, 150), "radius": 25, "exp": 60},
    "septagon": {"health": 70, "attack_damage": 70, "speed": 1, "sides": 7, "colour": (0, 0, 100), "radius": 20, "exp": 70},
    "octagon": {"health": 80, "attack_damage": 80, "speed": 1, "sides": 8, "colour": (255, 0, 0), "radius": 20, "exp": 80},
}
