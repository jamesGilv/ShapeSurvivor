import pygame
from settings import *
import random
from sys import exit
import math
from pygame.math import Vector2

pygame.init()

# Game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Shape Survivors')
clock = pygame.time.Clock()


# Fonts

# Images
background = pygame.Rect(0, 0, WIDTH, HEIGHT)

# Sounds

# Game variables
game_active = True
current_time = 0
start_time = 0


# Classes
class Shape(pygame.sprite.Sprite):
    def __init__(self, name, start_x, start_y):
        super().__init__(all_sprites_group, enemy_group)
        self.alive = True
        self.position = Vector2(start_x, start_y)
        self.x_pos = self.position.x
        self.y_pos = self.position.y
        self.name = name

        self.velocity = Vector2()
        self.direction = Vector2()
        self.direction_list = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        enemy_info = shape_data[self.name]
        self.health = enemy_info["health"]
        self.attack_damage = enemy_info["attack_damage"]
        self.speed = enemy_info["speed"]
        self.sides = enemy_info["sides"]
        self.colour = enemy_info["colour"]
        self.radius = enemy_info["radius"]

        # self.hitbox_rect = draw_shape(self.colour, self.sides, 0, self.x_pos, self.y_pos, self.radius)

    def check_alive(self):
        if self.health <= 0:
            self.alive = False

    def get_vector_distance(self, vector_1, vector_2):
        return (vector_1 - vector_2).magnitude()

    def move_shape(self):
        target_vector = pygame.mouse.get_pos()
        target_vec_x = target_vector[0]
        target_vec_y = target_vector[1]
        target_vector = Vector2(target_vec_x, target_vec_y)
        enemy_vector = Vector2(self.position)
        distance = self.get_vector_distance(target_vector, enemy_vector)

        if distance > 0:
            self.direction = (target_vector - enemy_vector).normalize()
        else:
            self.direction = Vector2()

        self.velocity = self.speed * self.direction
        self.position += self.velocity
        new_x = self.position.x
        new_y = self.position.y
        # self.hitbox_rect.centerx = self.x_pos
        # self.check_collision("horizontal", "hunt")

        # self.base_zombie_rect.centery = self.position.y
        # self.check_collision("vertical", "hunt")

        # self.position = (self.hitbox_rect.centerx, self.hitbox_rect.centery)
        draw_shape(self.colour, self.sides, 0, new_x, new_y, 50)

    def update(self):
        self.move_shape()


# Groups
all_sprites_group = pygame.sprite.Group()
obstacles_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
items_group = pygame.sprite.Group()


def draw_shape(colour, num_sides, tilt_angle, x, y, radius):
    pts = []
    for i in range(num_sides):
        x = x + radius * math.cos(tilt_angle + math.pi * 2 * i / num_sides)
        y = y + radius * math.sin(tilt_angle + math.pi * 2 * i / num_sides)
        pts.append([int(x), int(y)])

    pygame.draw.polygon(screen, colour, pts)


Triangle = Shape("triangle", 10, 10)
# all_sprites_group.add(Triangle)
# draw_shape((0, 0, 255), 3, 0, 500, 500, 100)
# Triangle_rect = pygame.Rect(500, 500, Triangle.width, Triangle.height)
x = 500
y = 500
while True:
    current_time = pygame.time.get_ticks()

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.draw.rect(screen, (60, 255, 60), background)
    all_sprites_group.update()
    # draw_shape((0, 0, 255), 3, 0, x, y, 100)
    # x += 1
    # y -= 1

    pygame.display.update()
    clock.tick(FPS)
