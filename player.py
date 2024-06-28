import pygame.time

from settings import *
from pygame.math import Vector2
import math
from bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__(game.all_sprites_group)
        self.game = game
        self.image = self.game.player_image
        self.base_player_image = self.image

        self.pos = pos
        self.vec_pos = Vector2(pos)
        self.base_player_rect = self.base_player_image.get_rect(center=pos)
        self.rect = self.base_player_rect.copy()

        self.player_speed = PLAYER_SPEED
        self.shoot = False
        self.shoot_cooldown = 0
        self.fire_delay = SHOOT_COOLDOWN

        self.max_health = PLAYER_HEALTH
        self.health = self.max_health

        self.gun_barrel_offset = pygame.math.Vector2(45, 20)

        self.damage = BULLET_DAMAGE
        self.bullet_scale = 1
        self.experience = 0
        self.level = 0
        self.exp_cap = 100
        self.level_scale = 1

    def player_turning(self):
        self.mouse_coords = pygame.mouse.get_pos()

        self.x_change_mouse_player = (self.mouse_coords[0] - self.rect.centerx)
        self.y_change_mouse_player = (self.mouse_coords[1] - self.rect.centery)
        self.angle = int(math.degrees(math.atan2(self.y_change_mouse_player, self.x_change_mouse_player)))
        self.angle = (self.angle) % 360  # if this stop working add 360 in the brackets

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
        if pygame.mouse.get_pressed() == (1, 0, 0):
            self.shoot = True
            self.is_shooting()
        if pygame.mouse.get_pressed() == (0, 0, 0):
            self.shoot = False

    def is_shooting(self):
        if self.shoot_cooldown == 0 and self.shoot:
            # gun_shot_sound.play()
            spawn_bullet_pos = self.vec_pos + self.gun_barrel_offset.rotate(self.angle)
            self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.game)
            self.shoot_cooldown = self.fire_delay
            self.game.bullet_group.add(self.bullet)
            self.game.all_sprites_group.add(self.bullet)

    def move(self):
        self.base_player_rect.centerx += self.velocity_x

        self.base_player_rect.centery += self.velocity_y

        self.rect.center = self.base_player_rect.center

        self.vec_pos = (self.base_player_rect.centerx, self.base_player_rect.centery)

    def get_damage(self, amount):
        if self.health > 0:
            self.health -= amount
        if self.health < 0:
            self.health = 0

    def check_level(self):
        if self.experience >= self.exp_cap:
            self.game.ready_to_spawn = False
            self.game.curr_menu = self.game.level_menu

    def check_health(self):
        if 0 >= self.health:
            self.game.ready_to_spawn = False
            self.game.curr_menu = self.game.end_menu
            self.game.game_time = pygame.time.get_ticks()

    def add_damage(self):
        self.damage += 10
        self.give_level()

    def add_health(self):
        if self.health == self.max_health or self.health > (self.max_health - 20):
            self.max_health += 20
            self.health += 20
        else:
            self.health += 20
        self.give_level()

    def add_speed(self):
        self.player_speed += 0.5
        self.give_level()

    def add_fire(self):
        if self.fire_delay > 1:
            self.fire_delay -= 1
        else:
            self.fire_delay = 1
        self.give_level()

    def bigger_bullet(self):
        self.bullet_scale += 0.5
        self.give_level()

    def add_exp_scale(self):
        self.level_scale += 0.5
        self.give_level()

    def give_level(self):
        self.level += 1
        self.experience = 0
        self.exp_cap += 10

    def reset_player(self):
        self.max_health = PLAYER_HEALTH
        self.health = self.max_health
        self.base_player_rect.center = (WIDTH / 2, HEIGHT / 2)
        self.experience = 0
        self.fire_delay = SHOOT_COOLDOWN
        self.damage = BULLET_DAMAGE
        self.player_speed = PLAYER_SPEED
        self.level = 0

    def draw_player(self):
        self.game.display.blit(self.image, self.rect)

    def update(self):
        self.player_turning()
        self.player_input()
        self.move()
        self.check_level()
        self.check_health()
        self.draw_player()

        if self.shoot_cooldown > 0:  # Just shot a bullet
            self.shoot_cooldown -= 1
        if self.shoot:
            self.is_shooting()
