import pygame
import os

# Game setup
WIDTH = 1280
HEIGHT = 600
FPS = 60

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

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
    "Gunner": {"health": 200, "damage": 20, "speed": 3, "cooldown": 15, "player_size": 0.25,
               "player_img": pygame.image.load('Graphics/long gun.png', ), "bullet_speed": 40, "bullet_lifetime": 400,
               "pierce": 1, "bullet_size": 1.25, "bullet_img": pygame.image.load('Graphics/bullet_1.png'),
               "xoffset": 45, "yoffset": 20, "stun": 0, "up_1": "Bullet speed", "up_2": "Fire rate",
               "evo_1": "Dual Wield", "evo_2": "Shotgun", "desc_1": "Fire two guns at once",
               "desc_2": "Fire a large spread of bullets", "evo1_img": pygame.image.load('Graphics/dual gun.png'),
               "evo2_img": pygame.image.load('Graphics/long gun.png')},
    "Wizard": {"health": 100, "damage": 30, "speed": 2, "cooldown": 30, "player_size": 0.25,
               "player_img": pygame.image.load('Graphics/wizard.png'), "bullet_speed": 40, "bullet_lifetime": 400,
               "pierce": 3, "bullet_size": 1.25, "bullet_img": pygame.image.load('Graphics/bullet_0.png'),
               "xoffset": 45, "yoffset": 20, "stun": 10, "up_1": "Stun", "up_2": "Magic size",
               "evo_1": "Fire Mage", "evo_2": "Electric Mage", "desc_1": "Set enemies on fire",
               "desc_2": "Lightning chains to enemies", "evo1_img": pygame.image.load('Graphics/fire_mage.png'),
               "evo2_img": pygame.image.load('Graphics/e_wiz.png'), "fire_img": pygame.image.load('Graphics/fire.png')},
    "Sniper": {"health": 100, "damage": 80, "speed": 4, "cooldown": 80, "player_size": 0.25,
               "player_img": pygame.image.load('Graphics/sniper.png'), "bullet_speed": 80, "bullet_lifetime": 500,
               "pierce": 5, "bullet_size": 2, "bullet_img": pygame.image.load('Graphics/bullet_1.png'), "xoffset": 45,
               "yoffset": 20, "stun": 0, "up_1": "Pierce", "up_2": "Bullet size",
               "evo_1": "Cover Fire", "evo_2": "Grenade Launcher", "desc_1": "Shoot in four directions",
               "desc_2": "Fire an explosive grenade", "evo1_img": pygame.image.load('Graphics/sniper.png'),
               "evo2_img": pygame.image.load('Graphics/sniper.png')},
    "Crossbow": {"health": 150, "damage": 80, "speed": 3, "cooldown": 50, "player_size": 0.25,
                 "player_img": pygame.image.load('Graphics/crossbow.png'), "bullet_speed": 20, "bullet_lifetime": 500,
                 "pierce": 3, "bullet_size": 0.75, "bullet_img": pygame.image.load('Graphics/arrow.png'),
                 "xoffset": -20, "yoffset": 0, "stun": 10, "up_1": "Stun", "up_2": "Arrow speed",
                 "evo_1": "Triple Shot", "evo_2": "Big Bolt", "desc_1": "Fire three arrows",
                 "desc_2": "Fire a large bolt", "evo1_img": pygame.image.load('Graphics/crossbow.png'),
                 "evo2_img": pygame.image.load('Graphics/crossbow.png')}
}

# Enemy settings
shape_data = {
    1: {"health": 10, "attack_damage": 15, "speed": 2, "colour": (0, 200, 255), "radius": 15, "exp": 10},
    3: {"health": 30, "attack_damage": 25, "speed": 2, "colour": (255, 255, 0), "radius": 30, "exp": 30},
    4: {"health": 40, "attack_damage": 40, "speed": 1, "colour": (255, 51, 242), "radius": 30, "exp": 40},
    5: {"health": 50, "attack_damage": 50, "speed": 1, "colour": (0, 0, 10), "radius": 25, "exp": 50},
    6: {"health": 60, "attack_damage": 60, "speed": 1, "colour": (0, 255, 150), "radius": 25, "exp": 60},
    7: {"health": 70, "attack_damage": 70, "speed": 1, "colour": (0, 0, 100), "radius": 20, "exp": 70},
    8: {"health": 80, "attack_damage": 80, "speed": 1, "colour": (255, 0, 0), "radius": 20, "exp": 80},
    9: {"health": 90, "attack_damage": 90, "speed": 1, "colour": (192, 0, 240), "radius": 20, "exp": 90},
    10: {"health": 100, "attack_damage": 100, "speed": 1, "colour": (101, 0, 127), "radius": 20, "exp": 100}
}

# Item settings
item_data = {
    "coin": {"image": pygame.image.load('Graphics/coin.png'), "size": 0.5},
    "heart": {"image": pygame.image.load('Graphics/heart.png'), "size": 0.5}
}
