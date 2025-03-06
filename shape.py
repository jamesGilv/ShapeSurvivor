import pygame
import random
import math
from pygame.math import Vector2
from item import Coin, Heart, Doubler, Magnet, Power, Bomb#, DoubleExp, Invincible, Speed


def get_points(sides, center_x, center_y, radius):
    # returns a list of points based on number of sides
    pts = []
    for i in range(sides):
        angle = math.pi * 2 * i / sides - math.pi / 4
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        pts.append([int(x), int(y)])
    return pts


def get_vector_distance(vector_1, vector_2):
    # returns distance between two objects
    return (vector_1 - vector_2).magnitude()


class Shape(pygame.sprite.Sprite):
    def __init__(self, game):
        # upon creation, add to enemy and all sprites groups
        super().__init__(game.all_sprites_group, game.enemy_group)
        self.game = game
        self.alive = True
        self.stun = 0

        # upon creation, select random shape from current shapes
        shape = random.choice(list(game.shape_data.items()))
        self.sides = shape[0]
        self.health = shape[1]["health"]
        self.attack_damage = shape[1]["attack_damage"]
        self.speed = shape[1]["speed"]
        self.colour = shape[1]["colour"]
        self.radius = shape[1]["radius"]
        self.exp = self.health

        # determine spawn point then create points for drawing it
        self.position = self.get_position()
        self.points = get_points(self.sides, self.x_pos, self.y_pos, self.radius)

        # vectors used for movement
        self.velocity = Vector2()
        self.direction = Vector2()

        # determine hitbox based on shape
        self.get_rect(self.sides, self.x_pos, self.y_pos, self.radius)

        # status effects
        self.on_fire = False
        self.poison = False

    def check_alive(self):
        # if health is below 0, kill it, give experience, and drop an item
        if self.health <= 0:
            self.alive = False
            self.game.player.experience += int(self.exp * self.game.player.level_scale)
            self.drop_item()
            self.kill()

    def get_position(self):
        # shapes are placed a random distance from the player
        values = [-300, -250, -200, 200, 250, 300]
        player_x = self.game.player.base_player_rect.centerx
        player_y = self.game.player.base_player_rect.centery
        self.x_pos = player_x + random.choice(values)
        self.y_pos = player_y + random.choice(values)
        return Vector2(self.x_pos, self.y_pos)

    def get_rect(self, sides, x, y, rad):
        # gives different sized hitboxes based on number of sides
        match sides:
            case sides if sides == 1:
                self.rect = pygame.Rect(x, y, rad * 2, rad * 2)
            case sides if sides == 3:
                self.rect = pygame.Rect(x, y, rad * 1.5, rad * 1.5)
            case sides if sides == 4:
                self.rect = pygame.Rect(x, y, rad * 1.7, rad * 1.7)
            case _:
                self.rect = pygame.Rect(x - rad, y, rad * 2, rad * 2)

    def drop_item(self):
        # generate a random number when killed to determine which item to drop
        num = random.randint(0, 100)
        match num:
            case num if 75 < num < 85:
                Coin(self.rect.centerx, self.rect.centery, self.game)
            case num if 85 < num < 90:
                Heart(self.rect.centerx, self.rect.centery, self.game)
            case num if num == 91:
                Doubler(self.rect.centerx, self.rect.centery, self.game)
            case num if 92 < num < 95:
                Magnet(self.rect.centerx, self.rect.centery, self.game)
            case num if num == 95:
                Power(self.rect.centerx, self.rect.centery, self.game)
            # case num if num == 96:
            #     DoubleExp(self.rect.centerx, self.rect.centery, self.game)
            # case num if num == 97:
            #     Invincible(self.rect.centerx, self.rect.centery, self.game)
            # case num if num == 98:
            #     Speed(self.rect.centerx, self.rect.centery, self.game)
            case num if num > 98:
                Bomb(self.rect.centerx, self.rect.centery, self.game)
            case _:
                pass

    def move_shape(self):
        # shapes move towards player at a set speed
        target_vector = Vector2(self.game.player.base_player_rect.center)
        target_vec_x = target_vector[0]
        target_vec_y = target_vector[1]
        target_vector = Vector2(target_vec_x, target_vec_y)
        enemy_vector = Vector2(self.rect.center)
        distance = get_vector_distance(target_vector, enemy_vector)

        if distance > 0:
            self.direction = (target_vector - enemy_vector).normalize()
        else:
            self.direction = Vector2()

        # adds velocity to current position
        self.velocity = self.speed * self.direction
        self.position += self.velocity
        new_x = self.position.x
        new_y = self.position.y

        self.x_pos = new_x
        self.y_pos = new_y
        self.rect.center = (new_x, new_y)

        # must move shape also
        for point in self.points:
            point[0] += self.velocity[0]
            point[1] += self.velocity[1]

    def check_player_collision(self):
        # if shape hits player it dies and damages the player
        if pygame.Rect.colliderect(self.rect, self.game.player.base_player_rect):  # player and enemy collides
            self.kill()
            self.game.player.get_damage(self.attack_damage)

    def check_status(self):
        # check if shape is stunned, on fire, or poisoned
        if self.stun > 0:
            self.stun -= 1
        else:
            self.move_shape()
        if self.on_fire:
            self.health -= int(self.game.player.damage * 0.1 * self.game.player.effect_mult)
        if self.poison:
            self.health -= int(self.health * 0.1 * self.game.player.effect_mult)

    def draw_shape(self):
        # must draw circles differently from other shapes
        if self.sides == 1:
            pygame.draw.circle(self.game.display, self.colour, (self.x_pos, self.y_pos), self.radius)
        else:
            pygame.draw.polygon(self.game.display, self.colour, self.points)
        # pygame.draw.rect(self.game.display, (100, 0, 0), self.rect, 5) # draw hitboxes

    def update(self):
        self.check_status()
        self.check_alive()
        self.check_player_collision()
        self.draw_shape()


class Boss(Shape):
    def __init__(self, game):
        Shape.__init__(self, game)

        # boss spawns in a random corner
        self.x_pos = random.choice([-100, self.game.DISPLAY_W + 100])
        self.y_pos = random.choice([-100, self.game.DISPLAY_H + 100])
        self.position = Vector2(self.x_pos, self.y_pos)

        # boss is always strongest shape
        shape = list(game.shape_data.items())[-1]
        self.sides = shape[0]
        self.health = 5 * shape[1]["health"]
        self.attack_damage = shape[1]["attack_damage"]
        self.speed = shape[1]["speed"]
        self.colour = shape[1]["colour"]
        self.radius = 40
        self.exp = 2 * self.health

        # get points for drawing shape then hitbox
        self.points = get_points(self.sides, self.x_pos, self.y_pos, self.radius)
        self.rect = pygame.Rect(self.x_pos - self.radius, self.y_pos - self.radius,
                                self.radius * 1.75, self.radius * 1.75)

    def move_shape(self):
        # boss moves to player at set speed
        target_vector = Vector2(self.game.player.base_player_rect.center)
        target_vec_x = target_vector[0]
        target_vec_y = target_vector[1]
        target_vector = Vector2(target_vec_x, target_vec_y)
        enemy_vector = Vector2(self.rect.center)
        distance = get_vector_distance(target_vector, enemy_vector)

        if distance > 0:
            self.direction = (target_vector - enemy_vector).normalize()
        else:
            self.direction = Vector2()

        # add position to velocity
        self.velocity = self.speed * self.direction
        self.position += self.velocity
        new_x = self.position.x
        new_y = self.position.y

        self.x_pos = new_x
        self.y_pos = new_y
        self.rect.center = (new_x, new_y)

        # move points for drawing
        for point in self.points:
            point[0] += self.velocity[0]
            point[1] += self.velocity[1]


class Turret(Shape):
    def __init__(self, game):
        Shape.__init__(self, game)
        self.x_pos = random.choice([-100, self.game.DISPLAY_W + 100])
        self.y_pos = random.choice([-100, self.game.DISPLAY_H + 100])
        self.position = Vector2(self.x_pos, self.y_pos)
        shape = list(game.shape_data.items())[-1]
        self.sides = shape[0]
        self.health = 5 * shape[1]["health"]
        self.attack_damage = shape[1]["attack_damage"]
        self.speed = shape[1]["speed"]
        self.colour = shape[1]["colour"]
        self.radius = 40
        self.exp = 2 * self.health
        self.bullet_speed = 3
        self.shoot_cooldown = 0
        self.fire_delay = 20
        self.turret_rect = pygame.Rect(self.x_pos, self.y_pos, 100, 20)
        self.turret_rect.midleft = (self.x_pos, self.y_pos)
        # use self.direction to aim at player, shoot projectile (new class), is base shape with turret on top, draw base then turret
        # also need to rotate turret position and base potentially

    def move_shape(self):
        target_vector = Vector2(self.game.player.base_player_rect.center)
        target_vec_x = target_vector[0]
        x_change = (target_vec_x - self.rect.centerx)
        target_vec_y = target_vector[1]
        y_change = (target_vec_y - self.rect.centery)
        # target_vector = Vector2(target_vec_x, target_vec_y)
        self.angle = int(math.degrees(math.atan2(y_change, x_change)))
        self.angle = (self.angle) % 360
        # need to rotate rectangle about center
        enemy_vector = Vector2(self.rect.center)
        distance = self.get_vector_distance(target_vector, enemy_vector)

        if distance > 0:
            self.direction = (target_vector - enemy_vector).normalize()
        else:
            self.direction = Vector2()

        self.velocity = self.speed * self.direction
        self.position += self.velocity
        new_x = self.position.x
        new_y = self.position.y

        self.rect.centerx = new_x
        self.rect.centery = new_y

    def shoot(self):
        if self.shoot_cooldown == 0:
            Projectile(self.x_pos, self.y_pos, self.angle, self.game)
            self.shoot_cooldown += self.fire_delay
        else:
            self.shoot_cooldown -= 1

    def draw_shape(self):
        self.game.draw_shape(self.colour, self.sides, self.rect.x, self.rect.y, self.radius)
        pygame.draw.rect(self.game.display, (100, 0, 0), self.rect, 5)
        # pygame.draw.circle(self.game.display, (0, 100, 0), self.rect.center, 10)
        # draw barrel, also need to rotate it around central point when moving
        # pygame.draw.rect(self.game.display, (10, 10, 100), self.turret_rect, 50)

    def update(self):
        self.check_status()
        self.check_alive()
        # self.shoot()
        self.check_player_collision()
        self.draw_shape()


class Projectile(Shape):
    def __init__(self, x, y, angle, game):
        Shape.__init__(self, game)
        shape = list(game.shape_data.items())[0]  # always a circular projectile
        self.sides = shape[0]
        self.health = shape[1]["health"]
        self.attack_damage = shape[1]["attack_damage"]
        self.speed = shape[1]["speed"]
        self.colour = shape[1]["colour"]
        self.radius = shape[1]["radius"]
        self.exp = self.health
        self.x_pos = x
        self.y_pos = y
        self.position = Vector2(x, y)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 300
        self.speed = 3
        self.angle = angle
        self.x_vel = math.cos(self.angle * (2 * math.pi / 360)) * self.speed
        self.y_vel = math.sin(self.angle * (2 * math.pi / 360)) * self.speed

    def move_shape(self):
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel

        self.rect.x = int(self.x_pos)
        self.rect.y = int(self.y_pos)

        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()

    def update(self):
        self.check_status()
        self.check_alive()
        self.check_player_collision()
        self.draw_shape()


class Ring(Shape):
    def __init__(self, game, pos):
        # ring is a shape that does not move
        Shape.__init__(self, game)
        shape = list(game.shape_data.items())[-1]
        self.sides = shape[0]
        self.health = shape[1]["health"]
        self.attack_damage = shape[1]["attack_damage"]
        self.speed = 0
        self.colour = shape[1]["colour"]
        self.radius = shape[1]["radius"]
        self.exp = self.health
        self.position = pos

    def update(self):
        if self.alive:
            self.check_status()
            self.check_alive()
            self.check_player_collision()
            self.draw_shape()

