import math
import random
from settings import *


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, pierce, game):
        super().__init__(game.all_sprites_group, game.bullet_group)
        self.game = game
        self.image = self.game.player.class_info["bullet_img"].convert_alpha()
        self.image_scale = self.game.player.class_info["bullet_size"]
        self.image = pygame.transform.rotozoom(self.image, -angle, self.image_scale * self.game.player.bullet_scale)
        self.rect = self.image.get_rect()
        # if 30 < angle <= 60:
        #     self.x = x - 40
        #     self.y = y
        #     self.rect.topleft = (self.x, self.y)
        # elif 60 < angle <= 100:
        #     self.x = x - 60
        #     self.y = y
        #     self.rect.midtop = (self.x, self.y)
        # elif 100 < angle <= 120:
        #     self.x = x - 90
        #     self.y = y - 10
        #     self.rect.topleft = (self.x, self.y)
        # elif 120 < angle <= 150:
        #     self.x = x - 100
        #     self.y = y - 50
        #     self.rect.midright = (self.x, self.y)
        # elif 150 < angle <= 180:
        #     self.x = x - 100
        #     self.y = y - 50
        #     self.rect.midright = (self.x, self.y)
        # elif 180 < angle <= 200:
        #     self.x = x - 120
        #     self.y = y - 70
        #     self.rect.midright = (self.x, self.y)
        # elif 200 < angle <= 250:
        #     self.x = x - 40
        #     self.y = y - 90
        #     self.rect.midbottom = (self.x, self.y)
        # elif 250 < angle <= 300:
        #     self.x = x - 20
        #     self.y = y - 100
        #     self.rect.midbottom = (self.x, self.y)
        # elif 300 < angle <= 330:
        #     self.x = x
        #     self.y = y - 80
        #     self.rect.midleft = (self.x, self.y)
        # elif 330 < angle <= 360:
        #     self.x = x
        #     self.y = y - 30
        #     self.rect.midleft = (self.x, self.y)
        # elif angle <= 30:
        #     self.x = x
        #     self.y = y
        #     self.rect.midleft = (self.x, self.y)

        self.x = x
        self.y = y
        self.rect.center = (x, y)
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

    def bullet_collisions(self):
        hits = pygame.sprite.groupcollide(self.game.enemy_group, self.game.bullet_group, False, False, hitbox_collide)

        for hit in hits:
            hit.stun += self.game.player.stun
            hit.health -= self.game.player.damage

    def draw_bullet(self):
        self.game.display.blit(self.image, self.rect)

    def update(self):
        self.bullet_movement()
        self.bullet_collisions()
        self.draw_bullet()


class Bullet(Projectile):
    def __init__(self, x, y, angle, pierce, game):
        Projectile.__init__(self, x, y, angle, pierce, game)
        self.knockback_x = self.game.player.knockback * self.x_vel
        self.knockback_y = self.game.player.knockback * self.y_vel
        self.knockback = pygame.math.Vector2(self.knockback_x, self.knockback_y)

    def bullet_collisions(self):
        hits = pygame.sprite.groupcollide(self.game.enemy_group, self.game.bullet_group, False, False, hitbox_collide)

        for hit in hits:
            hit.health -= self.game.player.damage
            if hit.health > 0 :
                hit.position += self.knockback


class Grenade(Projectile):
    def __init__(self, x, y, angle, game):
        Projectile.__init__(self, x, y, angle, 1, game)
        self.image = self.game.player.class_info["grenade"].convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.5)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def bullet_collisions(self):
        hits = pygame.sprite.groupcollide(self.game.enemy_group, self.game.bullet_group, False, True)

        if len(hits) > 0:
            for hit in hits:
                hit.stun += self.game.player.stun
            Explosion(self.x, self.y, self.game)


class Fire(Projectile):
    def __init__(self, x, y, angle, pierce, game):
        Projectile.__init__(self, x, y, angle, pierce, game)
        self.image = self.game.player.class_info["fire_img"].convert_alpha()

    def bullet_collisions(self):
        hits = pygame.sprite.groupcollide(self.game.enemy_group, self.game.bullet_group, False, False, hitbox_collide)

        for hit in hits:
            hit.on_fire = True
            hit.stun += self.game.player.stun
            hit.health -= self.game.player.damage


class Arrow(Projectile):
    def __init__(self, x, y, angle, pierce, game):
        Projectile.__init__(self, x, y, angle, pierce, game)


class Lightning(Projectile):
    def __init__(self, x, y, angle, game):
        Projectile.__init__(self, x, y, angle, 1, game)

    def bullet_collisions(self):
        hits = pygame.sprite.groupcollide(self.game.enemy_group, self.game.bullet_group, False, True)

        if len(hits) > 0:
            current = list(hits)[0]
            current.health -= self.game.player.damage
            current.stun += self.game.player.stun
            new_list = self.game.enemy_group.copy()
            new_list.remove(current)
            closest = self.closest_shape(new_list, current)
            if current.position.distance_to(closest.position) < 150:
                chain = True
                pygame.draw.line(self.game.display, (0, 253, 253), current.position, closest.position, 10)
                closest.stun += self.game.player.stun
                closest.health -= self.game.player.damage * self.game.player.effect_mult
                while chain:
                    current = closest
                    new_list.remove(closest)
                    closest = self.closest_shape(new_list, current)
                    if current.position.distance_to(closest.position) < 150:
                        pygame.draw.line(self.game.display, (0, 253, 253), current.position, closest.position, 5)
                        closest.stun += self.game.player.stun
                        closest.health -= self.game.player.damage * self.game.player.effect_mult
                    else:
                        chain = False

    def closest_shape(self, targets, current):
        shape = min([s for s in targets], key=lambda s: pow(s.rect.centerx - current.rect.centerx, 2) + pow(s.rect.centery - current.rect.centery, 2))
        return shape


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        super().__init__(game.all_sprites_group)
        self.x = x
        self.y = y
        self.radius = 30
        self.colour = (245, 109, 0)
        self.game = game
        self.image = self.game.player.class_info["exp"].convert_alpha()
        self.angle = random.randint(0, 180)
        self.image = pygame.transform.rotozoom(self.image, self.angle, 3)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.life = 5

    def draw_explosion(self):
        self.game.display.blit(self.image, self.rect)

    def check_collision(self):
        if self.life == 5:
            hits = pygame.sprite.spritecollide(self, self.game.enemy_group, False)
            for hit in hits:
                hit.health -= self.game.player.damage

    def update(self):
        self.draw_explosion()
        self.check_collision()
        if self.life > 0:
            self.life -= 1
        else:
            self.kill()


def hitbox_collide(sprite1, sprite2):
    collision = sprite1.rect.colliderect(sprite2.rect)
    if collision:
        sprite2.bullet_pierce -= 1
        if sprite2.bullet_pierce == 0:
            sprite2.kill()
    return collision
