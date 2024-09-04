import pygame
import random
from pygame.math import Vector2
from item import Coin, Heart, Doubler, Magnet, Power, Bomb


class Shape(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__(game.all_sprites_group, game.enemy_group)
        self.game = game
        self.alive = True
        self.stun = 0
        shape = random.choice(list(game.shape_data.items()))
        self.sides = shape[0]
        self.health = shape[1]["health"]
        self.attack_damage = shape[1]["attack_damage"]
        self.speed = shape[1]["speed"]
        self.colour = shape[1]["colour"]
        self.radius = shape[1]["radius"]
        self.exp = self.health

        self.position = self.get_position()

        self.velocity = Vector2()
        self.direction = Vector2()

        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.radius * 2, self.radius * 2)
        self.rect.center = self.position

        self.on_fire = False

    def check_alive(self):
        if self.health <= 0:
            self.alive = False
            self.game.player.experience += int(self.exp * self.game.player.level_scale)
            self.drop_item()
            self.kill()

    def get_position(self):
        values = [-300, -250, -200, 200, 250, 300]
        player_x = self.game.player.base_player_rect.centerx
        player_y = self.game.player.base_player_rect.centery
        self.x_pos = player_x + random.choice(values)
        self.y_pos = player_y + random.choice(values)
        return Vector2(self.x_pos, self.y_pos)

    def drop_item(self):
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
            case num if 95 < num < 98:
                Power(self.rect.centerx, self.rect.centery, self.game)
            case num if num > 98:
                Bomb(self.rect.centerx, self.rect.centery, self.game)
            case _:
                pass

    def get_vector_distance(self, vector_1, vector_2):
        return (vector_1 - vector_2).magnitude()

    def move_shape(self):
        target_vector = Vector2(self.game.player.base_player_rect.center)
        target_vec_x = target_vector[0]
        target_vec_y = target_vector[1]
        target_vector = Vector2(target_vec_x, target_vec_y)
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

    def check_player_collision(self):
        if pygame.Rect.colliderect(self.rect, self.game.player.base_player_rect):  # player and enemy collides
            self.kill()
            self.game.player.get_damage(self.attack_damage)

    def check_status(self):
        if self.stun > 0:
            self.stun -= 1
        else:
            self.move_shape()
        if self.on_fire:
            self.colour = (245, 139, 0)
            self.health -= int(self.game.player.damage * 0.1 * self.game.player.effect_mult)

    def draw_shape(self):
        if self.sides == 1:
            pygame.draw.circle(self.game.display, self.colour, (self.rect.x, self.rect.y), self.radius)
        else:
            self.game.draw_shape(self.colour, self.sides, self.rect.x, self.rect.y, self.radius)

    def update(self):
        if self.alive:
            self.check_status()
            self.check_alive()
            self.move_shape()
            self.check_player_collision()
            self.draw_shape()


class Boss(Shape):
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


class Ring(Shape):
    def __init__(self, game, pos):
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
            self.game.draw_shape(self.colour, self.sides, self.rect.x, self.rect.y, self.radius)

