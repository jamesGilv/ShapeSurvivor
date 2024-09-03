import pygame.time
from pygame.math import Vector2
import math
import random
from bullet import Bullet, Grenade, Fire, Arrow, Lightning


class Player(pygame.sprite.Sprite):
    def __init__(self, game, name):
        super().__init__(game.all_sprites_group)
        self.game = game
        self.name = name
        self.class_info = self.game.player_data[self.name]
        self.max_health = self.class_info["health"]
        self.health = self.max_health
        self.damage = self.class_info["damage"]
        self.player_speed = self.class_info["speed"]
        self.fire_delay = self.class_info["cooldown"]
        self.image = self.class_info["player_img"].convert_alpha()
        self.image_scale = self.class_info["player_size"]
        self.image = pygame.transform.rotozoom(self.image, 0, self.image_scale)
        self.base_player_image = self.image
        self.bullet_speed = self.class_info["bullet_speed"]
        self.bullet_lifetime = self.class_info["bullet_lifetime"]
        self.bullet_pierce = self.class_info["pierce"]
        self.bullet_scale = self.class_info["bullet_size"]
        self.stun = self.class_info["stun"]
        self.knockback = 0
        self.evo = 0

        self.pos = (self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2)
        self.vec_pos = Vector2(self.pos)
        self.base_player_rect = self.base_player_image.get_rect(center=self.pos)
        self.rect = self.base_player_rect.copy()

        self.shoot = False
        self.shoot_cooldown = 0

        self.gun_barrel_offset = Vector2(self.class_info["xoffset"], self.class_info["yoffset"])

        self.experience = 0
        self.level = 0
        self.saved_levels = 0
        self.exp_cap = 100
        self.level_scale = 1

        self.coins = 0
        self.lives = 0
        self.not_powered = True

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
            spawn_bullet_pos = self.vec_pos + self.gun_barrel_offset.rotate(self.angle)
            Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.bullet_pierce, self.game)
            self.shoot_cooldown = self.fire_delay

    def move(self):
        self.check_position()
        self.base_player_rect.centerx += self.velocity_x

        self.base_player_rect.centery += self.velocity_y

        self.rect.center = self.base_player_rect.center

        self.vec_pos = (self.base_player_rect.centerx, self.base_player_rect.centery)

    def check_position(self):
        if self.base_player_rect.top > self.game.DISPLAY_H + 100:
            self.base_player_rect.centery = -50
        elif self.base_player_rect.bottom < -100:
            self.base_player_rect.centery = (self.game.DISPLAY_H + 50)
        if self.base_player_rect.left > self.game.DISPLAY_W + 100:
            self.base_player_rect.centerx = -50
        elif self.base_player_rect.right < -100:
            self.base_player_rect.centerx = (self.game.DISPLAY_W + 50)

    def get_damage(self, amount):
        if self.health > 0:
            self.health -= amount
        if self.health < 0:
            self.health = 0

    def check_level(self):
        if self.experience >= self.exp_cap:
            self.experience = (self.experience - self.exp_cap)
            self.exp_cap += 10
            self.saved_levels += 1
        if self.level >= 25 and self.evo == 0:
            self.game.ready_to_spawn = False
            self.game.curr_menu = self.game.evo_menu
        if self.level >= 100:
            self.game.game_won = True
            self.game.curr_menu.run_display = False
            self.game.ready_to_spawn = False
            self.game.curr_menu = self.game.end_menu
            self.game.game_time = pygame.time.get_ticks()
            self.game.reset_game()

    def check_health(self):
        if 0 >= self.health:
            if self.lives == 0:
                self.game.ready_to_spawn = False
                self.game.curr_menu = self.game.end_menu
                self.game.game_time = pygame.time.get_ticks()
                self.game.reset_game()
            else:
                self.lives -= 1
                if self.max_health >= 200:
                    self.max_health = int(self.max_health / 2)
                    self.health = self.max_health
                else:
                    self.max_health = 100
                    self.health = self.max_health

    def add_health(self):
        self.max_health += 50
        self.health += 50

    def add_speed(self):
        self.player_speed += 0.5

    def reset_player(self):
        info = self.class_info
        self.max_health = info["health"]
        self.health = self.max_health
        self.base_player_rect.center = (self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2)
        self.experience = 0
        self.fire_delay = info["cooldown"]
        self.damage = info["damage"]
        self.bullet_pierce = info["pierce"]
        self.player_speed = info["speed"]
        self.bullet_speed = info["bullet_speed"]
        self.bullet_scale = 1
        self.level = 0
        self.lives = 0
        self.coins = 0

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


class Gunner(Player):
    def __init__(self, game):
        Player.__init__(self, game, "Gunner")
        self.dual_gun_img = self.class_info["evo1_img"].convert_alpha()
        self.base_player_rect = self.base_player_rect.scale_by(0.35)

    def upgrade_1(self):
        self.bullet_speed += 5

    def upgrade_2(self):
        if self.fire_delay > 1:
            self.fire_delay -= 1
        else:
            self.fire_delay = 1

    def upgrade_3(self):
        self.knockback += 0.1

    def upgrade_4(self):
        self.level_scale += 0.2

    def check_evo(self):
        if self.evo == 1:
            self.base_player_image = pygame.transform.rotozoom(self.dual_gun_img, 0, self.image_scale)
        elif self.evo == 2:
            self.fire_delay = 20
            self.damage = 50

    def is_shooting(self):
        if self.shoot_cooldown == 0 and self.shoot:
            spawn_bullet_pos = self.vec_pos + self.gun_barrel_offset.rotate(self.angle)
            if self.evo == 0:
                Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.bullet_pierce, self.game)
            elif self.evo == 1:
                Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.bullet_pierce, self.game)
                spawn_2 = self.vec_pos + Vector2(20, 0) + self.gun_barrel_offset.rotate(self.angle)
                Bullet(spawn_2[0], spawn_2[1], self.angle, self.bullet_pierce, self.game)
            elif self.evo == 2:
                angles = random.sample(range(1, 40), 4)
                Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.bullet_pierce, self.game)
                Bullet(spawn_bullet_pos[0] + 5, spawn_bullet_pos[1], self.angle + angles[0], self.bullet_pierce, self.game)
                Bullet(spawn_bullet_pos[0] - 5, spawn_bullet_pos[1], self.angle + angles[1], self.bullet_pierce, self.game)
                Bullet(spawn_bullet_pos[0] + 10, spawn_bullet_pos[1], self.angle + angles[2], self.bullet_pierce, self.game)
                Bullet(spawn_bullet_pos[0] - 10, spawn_bullet_pos[1], self.angle + angles[3], self.bullet_pierce, self.game)
            self.shoot_cooldown = self.fire_delay

    def power_player(self):
        if self.not_powered:
            pygame.time.set_timer(self.game.power_timer, 10000, 1)
            self.damage *= 3
            self.bullet_pierce += 3
            self.not_powered = False

    def depower_player(self):
        self.damage /= 3
        self.bullet_pierce -= 3
        self.not_powered = True


class Sniper(Player):
    def __init__(self, game):
        Player.__init__(self, game, "Sniper")
        self.base_player_rect = self.base_player_rect.scale_by(0.35)

    def upgrade_1(self):
        self.bullet_pierce += 1

    def upgrade_2(self):
        self.bullet_scale += 0.2

    def upgrade_3(self):
        self.damage += 10

    def upgrade_4(self):
        self.knockback += 0.1

    def check_evo(self):
        if self.evo == 2:
            self.shoot_cooldown = 50

    def is_shooting(self):
        if self.shoot_cooldown == 0 and self.shoot:
            spawn_bullet_pos = self.vec_pos + self.gun_barrel_offset.rotate(self.angle)
            if self.evo == 0:
                Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.bullet_pierce, self.game)
            elif self.evo == 1:
                Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.bullet_pierce, self.game)
                Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle - 90, self.bullet_pierce, self.game)
                Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle - 180, self.bullet_pierce, self.game)
                Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle - 270, self.bullet_pierce, self.game)
            elif self.evo == 2:
                Grenade(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.game)
            self.shoot_cooldown = self.fire_delay

    def power_player(self):
        if self.not_powered:
            pygame.time.set_timer(self.game.power_timer, 10000, 1)
            self.damage *= 3
            self.bullet_pierce += 3
            self.fire_delay /= 2
            self.not_powered = False

    def depower_player(self):
        self.damage /= 3
        self.bullet_pierce -= 3
        self.fire_delay *= 2
        self.not_powered = True

class Wizard(Player):
    def __init__(self, game):
        Player.__init__(self, game, "Wizard")
        self.fire_img = self.class_info["evo1_img"].convert_alpha()
        self.ewiz_img = self.class_info["evo2_img"].convert_alpha()
        self.base_player_rect = self.base_player_rect.scale_by(0.5)
        self.effect_mult = 1

    def upgrade_1(self):
        self.stun += 5

    def upgrade_2(self):
        self.bullet_scale += 0.2

    def upgrade_3(self):
        self.damage += 10

    def upgrade_4(self):
        self.effect_mult += 0.1

    def check_evo(self):
        if self.evo == 1:
            self.image = self.fire_img
        elif self.evo == 2:
            self.image = self.ewiz_img
        self.base_player_image = pygame.transform.rotozoom(self.image, 0, self.image_scale)

    def is_shooting(self):
        if self.shoot_cooldown == 0 and self.shoot:
            spawn_bullet_pos = self.vec_pos + self.gun_barrel_offset.rotate(self.angle)
            if self.evo == 0:
                Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.bullet_pierce, self.game)
            elif self.evo == 1:
                Fire(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.bullet_pierce, self.game)
            elif self.evo == 2:
                Lightning(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.game)
            self.shoot_cooldown = self.fire_delay

    def power_player(self):
        if self.not_powered:
            pygame.time.set_timer(self.game.power_timer, 10000, 1)
            self.damage *= 3
            self.bullet_pierce += 3
            self.fire_delay /= 2
            self.not_powered = False

    def depower_player(self):
        self.damage /= 3
        self.bullet_pierce -= 3
        self.fire_delay *= 2
        self.not_powered = True


class Crossbow(Player):
    def __init__(self, game):
        Player.__init__(self, game, "Crossbow")
        self.base_player_rect = self.base_player_rect.scale_by(0.5)

    def upgrade_1(self):
        self.stun += 5

    def upgrade_2(self):
        self.bullet_speed += 5

    def upgrade_3(self):
        self.bullet_pierce += 1

    def upgrade_4(self):
        if self.fire_delay > 1:
            self.fire_delay -= 1
        else:
            self.fire_delay = 1

    def check_evo(self):
        if self.evo == 2:
            self.bullet_scale = 2
            self.gun_barrel_offset = Vector2(-20, -10)

    def is_shooting(self):
        if self.shoot_cooldown == 0 and self.shoot:
            spawn_bullet_pos = self.base_player_rect.center + self.gun_barrel_offset.rotate(self.angle)
            if self.evo == 0:
                Arrow(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.bullet_pierce, self.game)
            elif self.evo == 1:
                Arrow(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.bullet_pierce, self.game)
                Arrow(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle - 10, self.bullet_pierce, self.game)
                Arrow(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle + 10, self.bullet_pierce, self.game)
            elif self.evo == 2:
                self.bullet_scale = 2
                self.gun_barrel_offset = Vector2(-20, -10)
                spawn_bullet_pos = self.vec_pos + self.gun_barrel_offset.rotate(self.angle)
                Arrow(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, 10, self.game)
            self.shoot_cooldown = self.fire_delay

    def power_player(self):
        if self.not_powered:
            pygame.time.set_timer(self.game.power_timer, 10000, 1)
            self.damage *= 3
            self.bullet_pierce += 3
            self.not_powered = False

    def depower_player(self):
        self.damage /= 3
        self.bullet_pierce -= 3
        self.not_powered = True

