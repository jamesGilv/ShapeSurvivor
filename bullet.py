import math

import pygame.transform

from settings import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, game):
        super().__init__()
        self.game = game
        self.image = self.game.bullet_img
        self.image = pygame.transform.rotozoom(self.image, 0, self.game.player.bullet_scale)
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

    def bullet_collisions(self):
        hits = pygame.sprite.groupcollide(self.game.enemy_group, self.game.bullet_group, False, True, hitbox_collide)

        for hit in hits:
            hit.health -= self.game.player.damage

    def draw_bullet(self):
        self.game.display.blit(self.image, self.rect)

    def update(self):
        self.bullet_movement()
        self.bullet_collisions()
        self.draw_bullet()


def hitbox_collide(sprite1, sprite2):
    return sprite1.rect.colliderect(sprite2.rect)