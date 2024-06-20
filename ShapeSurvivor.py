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
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1000)


# Classes
class Shape(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites_group, enemy_group)
        self.alive = True
        self.x_pos = random.randint(-100, WIDTH + 100)
        self.y_pos = random.randint(-100, HEIGHT + 100)
        self.position = Vector2(self.x_pos, self.y_pos)
        self.name = random.choice(["circle", "triangle", "square", "pentagon", "hexagon", "septagon", "octagon"])

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
        if self.name == "circle":
            pygame.draw.circle(screen, self.colour, (new_x, new_y), self.radius)
        else:
            draw_shape(self.colour, self.sides, 0, new_x, new_y, self.radius)

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


while True:
    current_time = pygame.time.get_ticks()

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == enemy_timer:
            Shape()

    pygame.draw.rect(screen, (60, 255, 60), background)
    all_sprites_group.update()

    pygame.display.update()
    clock.tick(FPS)
