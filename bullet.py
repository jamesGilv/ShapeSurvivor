import math
import random
from settings import *


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, pierce, game):
        # when created, each projectile is added to the all sprites group and bullet group
        super().__init__(game.all_sprites_group, game.bullet_group)
        self.game = game
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

        # must determine trajectory of bullet based on which direction it was fired
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
        # moves bullet by adding velocity to position then moves its hitbox
        self.x += self.x_vel
        self.y += self.y_vel

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # if bullet is alive for too long it will die
        if pygame.time.get_ticks() - self.spawn_time > self.bullet_lifetime:
            self.kill()

    def bullet_collisions(self):
        # uses function to determine if bullets hit enemies
        hits = pygame.sprite.groupcollide(self.game.enemy_group, self.game.bullet_group, False, False, hitbox_collide)

        # when enemy is hit, stun and damage it
        for hit in hits:
            hit.stun += self.game.player.stun
            hit.health -= self.game.player.damage

    def draw_bullet(self):
        # draws image of the projectile in its hitbox
        self.game.display.blit(self.image, self.rect)

    def update(self):
        # moves projectile, checks for collisions, and draws it
        self.bullet_movement()
        self.bullet_collisions()
        self.draw_bullet()


class Bullet(Projectile):
    def __init__(self, x, y, angle, pierce, game):
        Projectile.__init__(self, x, y, angle, pierce, game)
        # retrieves image of bullet and resizes and rotates it
        self.image = self.game.weapon_images["bullet_img"].convert_alpha()
        self.image_scale = self.game.player.class_info["bullet_size"]
        self.image = pygame.transform.rotozoom(self.image, -angle, self.image_scale * self.game.player.bullet_scale)

        # set hitbox for bullet
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # sets values for knockback of bullet
        self.knockback_x = self.game.player.knockback * self.x_vel
        self.knockback_y = self.game.player.knockback * self.y_vel
        self.knockback = pygame.math.Vector2(self.knockback_x, self.knockback_y)

    def bullet_collisions(self):
        # uses function to determine if bullets hit enemies
        hits = pygame.sprite.groupcollide(self.game.enemy_group, self.game.bullet_group, False, False, hitbox_collide)

        # for each enemy hit, it damages it and knocks it back
        for hit in hits:
            hit.health -= self.game.player.damage
            if hit.health > 0:
                hit.position += self.knockback
                for point in hit.points:
                    point[0] += self.knockback_x
                    point[1] += self.knockback_y


class Grenade(Projectile):
    def __init__(self, x, y, angle, game):
        Projectile.__init__(self, x, y, angle, 1, game)
        # gets image of bullet and resizes and rotates it
        self.image = self.game.weapon_images["grenade_img"].convert_alpha()
        self.image_scale = self.game.player.class_info["bullet_size"]
        self.image = pygame.transform.rotozoom(self.image, -angle, 0.5 * self.game.player.bullet_scale)

        # sets hitbox for grenade
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def bullet_collisions(self):
        # uses function to determine if grenade hit enemies
        hits = pygame.sprite.groupcollide(self.game.enemy_group, self.game.bullet_group, False, True)

        # if the grenade hits something, it creates an explosion
        if len(hits) > 0:
            for hit in hits:
                hit.stun += self.game.player.stun
            Explosion(self.x, self.y, self.game)


class Magic(Projectile):
    def __init__(self, x, y, angle, pierce, game):
        Projectile.__init__(self, x, y, angle, pierce, game)
        # gets image for magic and resizes and rotates it
        self.image = self.game.weapon_images["magic_img"].convert_alpha()
        self.image_scale = self.game.player.class_info["bullet_size"]
        self.image = pygame.transform.rotozoom(self.image, -angle, self.image_scale * self.game.player.bullet_scale)

        # sets hitbox for magic
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Fire(Projectile):
    def __init__(self, x, y, angle, pierce, game):
        Projectile.__init__(self, x, y, angle, pierce, game)
        # gets image for fire and resizes and rotates it
        self.image = self.game.weapon_images["fire_img"].convert_alpha()
        self.image_scale = self.game.player.class_info["bullet_size"]
        self.image = pygame.transform.rotozoom(self.image, -angle, self.image_scale * self.game.player.bullet_scale)

        # cerates hitbox for fire
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def bullet_collisions(self):
        # uses function to determine if bullets hit enemies
        hits = pygame.sprite.groupcollide(self.game.enemy_group, self.game.bullet_group, False, False, hitbox_collide)

        # if fire hits an enemy, must be set on fire, and change colour of it
        for hit in hits:
            hit.on_fire = True
            if hit.poison:
                hit.colour = (200, 240, 44)
            else:
                hit.colour = (245, 139, 0)
            hit.stun += self.game.player.stun
            hit.health -= self.game.player.damage


class Arrow(Projectile):
    def __init__(self, x, y, angle, pierce, game):
        Projectile.__init__(self, x, y, angle, pierce, game)
        # gets image for arrow and resizes and rotates it
        self.image = self.game.weapon_images["arrow_img"].convert_alpha()
        self.image_scale = self.game.player.class_info["bullet_size"]
        self.image = pygame.transform.rotozoom(self.image, -angle, self.image_scale * self.game.player.bullet_scale)

        # creates hitbox for arrow
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class PoisonArrow(Arrow):
    def __init__(self, x, y, angle, pierce, game):
        Arrow.__init__(self, x, y, angle, pierce, game)
        # sets poison damage
        self.poison = int(1 * self.game.player.effect_mult)

    def bullet_collisions(self):
        # uses function to determine if arrow hit enemies
        hits = pygame.sprite.groupcollide(self.game.enemy_group, self.game.bullet_group, False, False, hitbox_collide)

        # must poison each enemy hit and changes its colour
        for hit in hits:
            hit.poison = True
            if hit.on_fire:
                hit.colour = (200, 240, 44)
            else:
                hit.colour = (109, 240, 44)
            hit.stun += self.game.player.stun
            hit.speed = 1
            hit.health -= self.game.player.damage


class Lightning(Projectile):
    def __init__(self, x, y, angle, game):
        Projectile.__init__(self, x, y, angle, 1, game)
        # gets image for lightning and rotates and resizes it
        self.image = self.game.weapon_images["magic_img"].convert_alpha()
        self.image_scale = self.game.player.class_info["bullet_size"]
        self.image = pygame.transform.rotozoom(self.image, -angle, self.image_scale * self.game.player.bullet_scale)

        # creates hitbox for lightning
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def bullet_collisions(self):
        # uses function to determine if lightning hit enemies
        hits = pygame.sprite.groupcollide(self.game.enemy_group, self.game.bullet_group, False, True)

        # lightning chains to enemies if they are close enough
        if len(hits) > 0:
            # need to make sure it does not count itself as closest enemy
            current = list(hits)[0]
            current.health -= self.game.player.damage
            current.stun += self.game.player.stun

            # copies list of enemies but removes enemy that was just hit
            new_list = self.game.enemy_group.copy()
            new_list.remove(current)

            # finds closest shape to current one
            closest = self.closest_shape(new_list, current)

            # need to stop loop if no enemy is close
            if closest is None:
                return

            if current.position.distance_to(closest.position) < 150:
                # if enemy is close enough it will chain and draw a blue line
                chain = True
                pygame.draw.line(self.game.display, (0, 253, 253), current.position, closest.position, 10)
                closest.stun += self.game.player.stun
                closest.health -= self.game.player.damage * self.game.player.effect_mult
                while chain:
                    # removes current enemy from copied list
                    current = closest
                    new_list.remove(closest)
                    # finds closest shape to current
                    closest = self.closest_shape(new_list, current)
                    if closest is None:
                        # chain stops if no enemies are present
                        chain = False
                    elif current.position.distance_to(closest.position) < 150:
                        # chain stops if no enemies are close
                        pygame.draw.line(self.game.display, (0, 253, 253), current.position, closest.position, 5)
                        closest.stun += self.game.player.stun
                        closest.health -= self.game.player.damage * self.game.player.effect_mult
                    else:
                        chain = False

    def closest_shape(self, targets, current):
        # function for finding closest shape
        if not targets:
            return None

        # finds distance to all shapes and returns nearest shape
        shape = min(targets, key=lambda s: pow(s.rect.centerx - current.rect.centerx, 2) + pow(s.rect.centery - current.rect.centery, 2))
        return shape


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        super().__init__(game.all_sprites_group)
        # sets position of explosion, including radius
        self.x = x
        self.y = y
        self.radius = 30
        self.colour = (245, 109, 0)
        self.game = game

        # gets image of explosion
        self.image = self.game.weapon_images["explosion_img"].convert_alpha()

        # explosion is rotated by random angle so it is not the same each time
        self.angle = random.randint(0, 180)
        self.image = pygame.transform.rotozoom(self.image, self.angle, 3)

        # creates hitbox for explosion
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # sets lifetime for explosion so it does not disappear immediately
        self.life = 5

    def draw_explosion(self):
        # draws explosion
        self.game.display.blit(self.image, self.rect)

    def check_collision(self):
        # collides with enemies if it has just exploded
        if self.life == 5:
            hits = pygame.sprite.spritecollide(self, self.game.enemy_group, False)
            for hit in hits:
                hit.health -= self.game.player.damage

    def update(self):
        # must decrease life each update
        self.draw_explosion()
        self.check_collision()
        if self.life > 0:
            self.life -= 1
        else:
            self.kill()


def hitbox_collide(sprite1, sprite2):
    # function for determining collision between projectile and shape
    collision = sprite1.rect.colliderect(sprite2.rect)
    if collision:
        # reduce pierce of projectile and remove it if it reaches zero
        sprite2.bullet_pierce -= 1
        if sprite2.bullet_pierce == 0:
            sprite2.kill()
    return collision
