import pygame
import random
from pygame.math import Vector2


class Shape(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__(game.all_sprites_group, game.enemy_group)
        self.game = game
        self.alive = True
        self.x_pos = random.randint(-100, self.game.DISPLAY_W / 2 + 100)
        self.y_pos = random.randint(-100, self.game.DISPLAY_W / 2 + 100)
        self.position = Vector2(self.x_pos, self.y_pos)
        while self.get_vector_distance(self.position, self.game.player.pos) < 300:
            self.x_pos = random.randint(-100, self.game.DISPLAY_W / 2 + 100)
            self.y_pos = random.randint(-100, self.game.DISPLAY_W / 2 + 100)
            self.position = Vector2(self.x_pos, self.y_pos)

        self.name = random.choice(["circle", "triangle", "square", "pentagon", "hexagon", "septagon", "octagon"])

        self.velocity = Vector2()
        self.direction = Vector2()
        self.direction_list = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        enemy_info = self.game.shape_data[self.name]
        self.health = enemy_info["health"] + self.game.player.level * 5
        self.attack_damage = enemy_info["attack_damage"]
        self.speed = enemy_info["speed"]
        self.sides = enemy_info["sides"]
        self.colour = enemy_info["colour"]
        self.radius = enemy_info["radius"]
        self.exp = enemy_info["exp"]

        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.radius * 2, self.radius * 2)
        self.rect.center = self.position

        self.collide = False

    def check_alive(self):
        if self.health <= 0:
            self.alive = False
            self.game.player.experience += self.exp
            self.kill()

    def check_collision(self, direction):
        for sprite in self.game.enemy_group:
            if sprite.hitbox_rect != self.rect:
                if self.get_vector_distance(self.position, sprite.position) < self.radius:
                    # print('collide')
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

    def update(self):
        if self.alive:
            self.check_alive()
            self.move_shape()
            self.check_player_collision()
            if self.name == "circle":
                pygame.draw.circle(self.game.display, self.colour, (self.rect.x, self.rect.y), self.radius)
            else:
                self.game.draw_shape(self.colour, self.sides, 0, self.rect.x, self.rect.y, self.radius)
