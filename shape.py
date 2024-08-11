import pygame
import random
from pygame.math import Vector2
from item import Coin, Heart


class Shape(pygame.sprite.Sprite):
    def __init__(self, game, side, boss):
        super().__init__(game.all_sprites_group, game.enemy_group)
        self.game = game
        self.alive = True
        self.stun = 0
        self.x_pos = random.randint(-100, self.game.DISPLAY_W + 100)
        self.y_pos = random.randint(-100, self.game.DISPLAY_W + 100)
        self.position = Vector2(self.x_pos, self.y_pos)
        while self.get_vector_distance(self.position, self.game.player.pos) < 300:
            self.x_pos = random.randint(-100, self.game.DISPLAY_W + 100)
            self.y_pos = random.randint(-100, self.game.DISPLAY_W + 100)
            self.position = Vector2(self.x_pos, self.y_pos)

        self.sides = side

        self.velocity = Vector2()
        self.direction = Vector2()
        self.direction_list = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        enemy_info = self.game.shape_data[self.sides]
        self.health = enemy_info["health"] * (int(1 + (self.game.player.level / 5)))
        self.attack_damage = enemy_info["attack_damage"]
        self.speed = enemy_info["speed"]
        self.colour = enemy_info["colour"]
        self.radius = enemy_info["radius"]
        self.exp = enemy_info["exp"]

        if boss:
            self.x_pos = random.choice([-100, self.game.DISPLAY_W + 100])
            self.y_pos = random.choice([-100, self.game.DISPLAY_H + 100])
            self.position = Vector2(self.x_pos, self.y_pos)
            self.health *= 5
            self.radius *= 2
            self.exp *= 2

        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.radius * 2, self.radius * 2)
        self.rect.center = self.position

        self.collide = False
        self.on_fire = False

    def check_alive(self):
        if self.health <= 0:
            self.alive = False
            self.game.player.experience += int(self.exp * self.game.player.level_scale)
            drop = self.get_drop()
            if drop < 40:
                Coin(self.rect.centerx, self.rect.centery, self.game)
            elif drop > 90:
                Heart(self.rect.centerx, self.rect.centery, self.game)
            self.kill()

    def get_drop(self):
        return random.randint(0, 100)

    def check_collision(self, direction):
        for sprite in self.game.enemy_group:
            if sprite.hitbox_rect != self.rect:
                if self.get_vector_distance(self.position, sprite.position) < self.radius:
                    self.collide = True
                    if direction == "horizontal":
                        if self.velocity.x > 0:
                            self.rect.centerx -= self.radius / 2
                            sprite.rect.centerx += self.radius / 2
                        if self.velocity.x < 0:
                            self.rect.centerx += self.radius / 2
                            sprite.rect.centerx -= self.radius / 2
                    if direction == "vertical":
                        if self.velocity.y < 0:
                            self.rect.centery -= self.radius / 2
                            sprite.rect.centery += self.radius / 2
                        if self.velocity.y > 0:
                            self.rect.centery += self.radius / 2
                            sprite.rect.centery = self.radius / 2

    def get_vector_distance(self, vector_1, vector_2):
        return (vector_1 - vector_2).magnitude()

    def move_shape(self):
        if self.stun == 0:
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
        if self.on_fire:
            self.colour = (245, 139, 0)
            self.health -= int(self.game.player.damage * 0.1)

    def update(self):
        if self.alive:
            self.check_status()
            self.check_alive()
            self.move_shape()
            self.check_player_collision()
            if self.sides == 1:
                pygame.draw.circle(self.game.display, self.colour, (self.rect.x, self.rect.y), self.radius)
            else:
                self.game.draw_shape(self.colour, self.sides, self.rect.x, self.rect.y, self.radius)

