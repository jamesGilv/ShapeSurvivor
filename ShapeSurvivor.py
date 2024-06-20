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
player_image = pygame.image.load('Graphics/player.png').convert_alpha()
player_image = pygame.transform.rotozoom(player_image, 0, PLAYER_SIZE)

bullet_img = pygame.image.load('Graphics/bullet_1.png').convert_alpha()
bullet_img = pygame.transform.rotozoom(bullet_img, 0, BULLET_SCALE)

# Sounds

# Game variables
game_active = True
current_time = 0
start_time = 0
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1000)


# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites_group)
        self.image = player_image
        self.base_player_image = self.image

        self.pos = pos
        self.vec_pos = Vector2(pos)
        self.base_player_rect = self.base_player_image.get_rect(center=pos)
        self.rect = self.base_player_rect.copy()

        self.player_speed = PLAYER_SPEED
        self.shoot = False
        self.shoot_cooldown = 0

        self.health = PLAYER_HEALTH

        self.gun_barrel_offset = pygame.math.Vector2(45, 20)

    def player_turning(self):
        self.mouse_coords = pygame.mouse.get_pos()

        self.x_change_mouse_player = (self.mouse_coords[0] - self.rect.centerx)
        self.y_change_mouse_player = (self.mouse_coords[1] - self.rect.centery)
        self.angle = int(math.degrees(math.atan2(self.y_change_mouse_player, self.x_change_mouse_player)))
        self.angle = (self.angle) % 360 # if this stop working add 360 in the brackets

        self.image = pygame.transform.rotate(self.base_player_image, -self.angle)
        self.rect = self.image.get_rect(center=self.base_player_rect.center)

    def player_input(self):
        self.velocity_x = 0
        self.velocity_y = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.velocity_y = -self.player_speed
        if keys[pygame.K_s]:
            self.velocity_y = self.player_speed
        if keys[pygame.K_d]:
            self.velocity_x = self.player_speed
        if keys[pygame.K_a]:
            self.velocity_x = -self.player_speed

        if self.velocity_x != 0 and self.velocity_y != 0:  # moving diagonally
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)

        if pygame.mouse.get_pressed() == (1, 0, 0) or keys[pygame.K_SPACE]:
            self.shoot = True
            self.is_shooting()

        else:
            self.shoot = False

        if event.type == pygame.KEYUP:
            if pygame.mouse.get_pressed() == (1, 0, 0):
                self.shoot = False

    def is_shooting(self):
        if self.shoot_cooldown == 0 and self.shoot:
            # gun_shot_sound.play()
            spawn_bullet_pos = self.vec_pos + self.gun_barrel_offset.rotate(self.angle)
            self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle)
            self.shoot_cooldown = 10
            bullet_group.add(self.bullet)
            all_sprites_group.add(self.bullet)

    def move(self):
        self.base_player_rect.centerx += self.velocity_x
        # self.check_collision("horizontal")

        self.base_player_rect.centery += self.velocity_y
        # self.check_collision("vertical")

        self.rect.center = self.base_player_rect.center

        self.vec_pos = (self.base_player_rect.centerx, self.base_player_rect.centery)

    def update(self):
        self.player_turning()
        self.player_input()
        self.move()

        if self.shoot_cooldown > 0: # Just shot a bullet
            self.shoot_cooldown -= 1
        if self.shoot:
            self.is_shooting()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.speed = BULLET_SPEED
        self.angle = angle
        self.x_vel = math.cos(self.angle * (2 * math.pi / 360)) * self.speed
        self.y_vel = math.sin(self.angle * (2 * math.pi / 360)) * self.speed
        self.bullet_lifetime = BULLET_LIFETIME
        self.spawn_time = pygame.time.get_ticks()  # gets the specific time that the bullet was created, stays static

    def bullet_movement(self):
        self.x += self.x_vel
        self.y += self.y_vel

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if pygame.time.get_ticks() - self.spawn_time > self.bullet_lifetime:
            self.kill()

    def update(self):
        self.bullet_movement()
        # self.bullet_collisions()


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

        self.hitbox_rect = pygame.Rect(self.x_pos, self.y_pos, self.radius, self.radius)
        self.hitbox_rect.center = self.position

        self.collide = False

    def check_alive(self):
        if self.health <= 0:
            self.alive = False

    def check_collision(self, direction):
        for sprite in enemy_group:
            if sprite.hitbox_rect != self.hitbox_rect:
                if self.get_vector_distance(Vector2(self.hitbox_rect.center), Vector2(sprite.hitbox_rect.center)) < self.radius:
                    # print('collide')
                    self.collide = True
                    if direction == "horizontal":
                        if self.velocity.x > 0:
                            self.hitbox_rect.right = sprite.hitbox_rect.left
                        if self.velocity.x < 0:
                            self.hitbox_rect.left = sprite.hitbox_rect.right
                    if direction == "vertical":
                        if self.velocity.y < 0:
                            self.hitbox_rect.top = sprite.hitbox_rect.bottom
                        if self.velocity.y > 0:
                            self.hitbox_rect.bottom = sprite.hitbox_rect.top

    def get_vector_distance(self, vector_1, vector_2):
        return (vector_1 - vector_2).magnitude()

    def move_shape(self):
        target_vector = Vector2(player.base_player_rect.center)
        target_vec_x = target_vector[0]
        target_vec_y = target_vector[1]
        target_vector = Vector2(target_vec_x, target_vec_y)
        enemy_vector = Vector2(self.hitbox_rect.center)
        distance = self.get_vector_distance(target_vector, enemy_vector)

        if distance > 0:
            self.direction = (target_vector - enemy_vector).normalize()
        else:
            self.direction = Vector2()

        self.velocity = self.speed * self.direction
        self.position += self.velocity
        new_x = self.position.x
        new_y = self.position.y

        self.hitbox_rect.centerx = new_x
        self.hitbox_rect.centery = new_y

        # self.check_collision("horizontal")
        # self.check_collision("vertical")

    def update(self):
        self.move_shape()
        if self.name == "circle":
            pygame.draw.circle(screen, self.colour, (self.hitbox_rect.x, self.hitbox_rect.y), self.radius)
        else:
            draw_shape(self.colour, self.sides, 0, self.hitbox_rect.x, self.hitbox_rect.y, self.radius)


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


player = Player((PLAYER_START_X, PLAYER_START_Y))
# Shape()
# Shape()

while True:
    current_time = pygame.time.get_ticks()

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == enemy_timer:
            Shape()

    pygame.draw.rect(screen, (0, 100, 0), background)
    all_sprites_group.update()
    screen.blit(player.image, player.rect)
    for bullet in bullet_group:
        screen.blit(bullet_img, bullet.rect)
    pygame.display.update()
    clock.tick(FPS)
