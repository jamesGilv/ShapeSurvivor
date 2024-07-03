import math

import pygame.transform

from settings import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, pierce, game):
        super().__init__()
        self.game = game
        self.image = self.game.player.class_info["bullet_img"].convert_alpha()
        self.image_scale = self.game.player.class_info["bullet_size"]
        self.image = pygame.transform.rotozoom(self.image, -angle, self.image_scale * self.game.player.bullet_scale)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.speed = self.game.player.bullet_speed
        self.angle = angle
        self.x_vel = math.cos(self.angle * (2 * math.pi / 360)) * self.speed
        self.y_vel = math.sin(self.angle * (2 * math.pi / 360)) * self.speed
        self.bullet_lifetime = self.game.player.bullet_lifetime
        self.bullet_pierce = pierce
        self.spawn_time = pygame.time.get_ticks()  # gets the specific time that the bullet was created, stays static

    def bullet_movement(self):
        self.x += self.x_vel
        self.y += self.y_vel

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if pygame.time.get_ticks() - self.spawn_time > self.bullet_lifetime or self.bullet_pierce == 0:
            self.kill()

    def bullet_collisions(self):
        hits = pygame.sprite.groupcollide(self.game.enemy_group, self.game.bullet_group, False, False, hitbox_collide)

        for hit in hits:
            hit.health -= self.game.player.damage

    def draw_bullet(self):
        self.game.display.blit(self.image, self.rect)

    def update(self):
        self.bullet_movement()
        self.bullet_collisions()
        self.draw_bullet()


def hitbox_collide(sprite1, sprite2):
    collision = sprite1.rect.colliderect(sprite2.rect)
    if collision:
        if sprite2.bullet_pierce == 1:
            sprite2.kill()
        else:
            sprite2.bullet_pierce -= 1
    return collision
