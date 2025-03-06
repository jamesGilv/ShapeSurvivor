import pygame.time
from pygame.math import Vector2
import math
import random
from bullet import Bullet, Grenade, Magic, Fire, Arrow, PoisonArrow, Lightning


class Player(pygame.sprite.Sprite):
    def __init__(self, game, name):
        # upon creation, add player to all sprites group
        super().__init__(game.all_sprites_group)
        self.game = game

        # gets data for player from settings
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
        self.effect_mult = 1
        self.evo = 0

        # player starts in middle of screen, create hitbox
        self.pos = (self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2)
        self.vec_pos = Vector2(self.pos)
        self.base_player_rect = self.base_player_image.get_rect(center=self.pos)
        self.rect = self.base_player_rect.copy()

        # variables for shooting mechanics
        self.shoot = False
        self.shoot_cooldown = 0

        # must offset bullets from player spawn point
        self.gun_barrel_offset = Vector2(self.class_info["xoffset"], self.class_info["yoffset"])

        # variables for levelling player
        self.experience = 0
        self.level = 0
        self.saved_levels = 0
        self.exp_cap = 100
        self.level_scale = 1

        self.coins = 0
        self.lives = 0

        # variable for item power up
        self.not_powered = True

    def player_turning(self):
        # function for turning player sprite to point at mouse
        self.mouse_coords = pygame.mouse.get_pos()

        self.x_change_mouse_player = (self.mouse_coords[0] - self.rect.centerx)
        self.y_change_mouse_player = (self.mouse_coords[1] - self.rect.centery)
        self.angle = int(math.degrees(math.atan2(self.y_change_mouse_player, self.x_change_mouse_player)))
        self.angle = (self.angle) % 360  # if this stop working add 360 in the brackets

        self.image = pygame.transform.rotate(self.base_player_image, -self.angle)
        self.rect = self.image.get_rect(center=self.base_player_rect.center)

    def player_input(self):
        # determines player velocity based on keyboard inputs
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

        # determines if player is shooting by using left click
        if pygame.mouse.get_pressed() == (1, 0, 0):
            self.shoot = True
            self.is_shooting()
        if pygame.mouse.get_pressed() == (0, 0, 0):
            self.shoot = False

    def is_shooting(self):
        # shoots if player is using left click and there is no cooldown
        if self.shoot_cooldown == 0 and self.shoot:
            spawn_bullet_pos = self.vec_pos + self.gun_barrel_offset.rotate(self.angle)
            Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.bullet_pierce, self.game)
            self.shoot_cooldown = self.fire_delay

    def move(self):
        # screen loops to other side
        self.check_position()

        # add velocity to current position
        self.base_player_rect.centerx += self.velocity_x

        self.base_player_rect.centery += self.velocity_y

        self.rect.center = self.base_player_rect.center

        self.vec_pos = (self.base_player_rect.centerx, self.base_player_rect.centery)

    def check_position(self):
        # if player goes too far in one direction, will emerge on opposite side of screen
        if self.base_player_rect.top > self.game.DISPLAY_H + 100:
            self.base_player_rect.centery = -50
        elif self.base_player_rect.bottom < -100:
            self.base_player_rect.centery = (self.game.DISPLAY_H + 50)
        if self.base_player_rect.left > self.game.DISPLAY_W + 100:
            self.base_player_rect.centerx = -50
        elif self.base_player_rect.right < -100:
            self.base_player_rect.centerx = (self.game.DISPLAY_W + 50)

    def get_damage(self, amount):
        # function for damaging player
        if self.health > 0:
            self.health -= amount
        if self.health < 0:
            self.health = 0

    def check_level(self):
        # checks if experience is enough to level up, and increases exp requirement
        if self.experience >= self.exp_cap:
            self.experience = (self.experience - self.exp_cap)
            self.exp_cap += 10
            self.saved_levels += 1
        # player will evolve at level 25
        if self.level >= 25 and self.evo == 0:
            self.game.ready_to_spawn = False
            self.game.curr_menu = self.game.evo_menu
        # game is won when player reaches level 100
        if self.level >= 100:
            self.game.game_won = True
            self.game.curr_menu.run_display = False
            self.game.ready_to_spawn = False
            self.game.curr_menu = self.game.end_menu
            self.game.game_time = pygame.time.get_ticks()
            self.game.reset_game()

    def check_health(self):
        # if player health reaches 0, can return with if you have extra lives
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
        # adds 50 to current and max health
        self.max_health += 50
        self.health += 50

    def add_speed(self):
        # give player more speed
        self.player_speed += 0.5

    def reset_player(self):
        # reset player stats and position
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

    def double_exp(self):
        # sets 20 second timer where player exp is doubled
        pygame.time.set_timer(self.game.exp_timer, 20000, 1)
        self.level_scale *= 2

    def invincible(self):
        # make player invincible for 5 seconds
        pygame.time.set_timer(self.game.invincible_timer, 5000, 1)
        self.damage_mult = 0

    def super_speed(self):
        # gives player double speed for 10 seconds
        pygame.time.set_timer(self.game.speed_timer, 10000, 1)
        self.speed = int(self.speed * 2)

    def draw_player(self):
        # draw player image inside hitbox
        self.game.display.blit(self.image, self.rect)

    def update(self):
        self.player_turning()
        self.player_input()
        self.move()
        self.check_level()
        self.check_health()
        self.draw_player()

        if self.shoot_cooldown > 0:
            # Just shot a bullet
            self.shoot_cooldown -= 1
        if self.shoot:
            self.is_shooting()


class Gunner(Player):
    def __init__(self, game):
        Player.__init__(self, game, "Gunner")
        self.base_player_rect = self.base_player_rect.scale_by(0.35)

    def upgrade_1(self):
        # give gunner 5 bullet speed
        self.bullet_speed += 5

    def upgrade_2(self):
        # reduce fire delay by 1
        if self.fire_delay > 1:
            self.fire_delay -= 1
        else:
            self.fire_delay = 1

    def upgrade_3(self):
        # increase knockback by 0.1
        self.knockback += 0.1

    def upgrade_4(self):
        # increase exp earned by 20%
        self.level_scale += 0.2

    def is_shooting(self):
        # if cooldown is 0 and player is using left click, shoot
        if self.shoot_cooldown == 0 and self.shoot:
            spawn_bullet_pos = self.vec_pos + self.gun_barrel_offset.rotate(self.angle)
            Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.bullet_pierce, self.game)
            self.shoot_cooldown = self.fire_delay

    def power_player(self):
        # powers gunner up for 10 seconds by tripling damage and adding 3 more pierce
        if self.not_powered:  # stops multiple power ups being activated at once
            pygame.time.set_timer(self.game.power_timer, 10000, 1)
            self.damage *= 3
            self.bullet_pierce += 3
            self.not_powered = False

    def depower_player(self):
        # removes power up after 10 seconds
        self.damage /= 3
        self.bullet_pierce -= 3
        self.not_powered = True


class DualGunner(Gunner):
    def __init__(self, game):
        Gunner.__init__(self, game)

        # get new image for dual gunner
        self.dual_gun_img = self.class_info["evo1_img"].convert_alpha()
        self.base_player_image = pygame.transform.rotozoom(self.dual_gun_img, 0, self.image_scale)

    def is_shooting(self):
        # shoots 2 bullets per shot instead of 1
        if self.shoot_cooldown == 0 and self.shoot:
            spawn_2 = self.vec_pos + Vector2(-10, 0)
            spawn_bullet_pos = self.vec_pos + self.gun_barrel_offset.rotate(self.angle)
            Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.bullet_pierce, self.game)
            spawn_bullet_2 = spawn_2 + self.gun_barrel_offset.rotate(self.angle)
            Bullet(spawn_bullet_2[0], spawn_bullet_2[1], self.angle, self.bullet_pierce, self.game)
            self.shoot_cooldown = self.fire_delay


class Shotgun(Gunner):
    def __init__(self, game):
        Gunner.__init__(self, game)
        # increase fire delay and damage for shotgun
        self.fire_delay = 20
        self.damage = 50

    def is_shooting(self):
        if self.shoot_cooldown == 0 and self.shoot:
            spawn_bullet_pos = self.vec_pos + self.gun_barrel_offset.rotate(self.angle)
            # generate 4 random angles so bullets go in different directions
            angles = random.sample(range(1, 40), 4)
            Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.bullet_pierce, self.game)
            Bullet(spawn_bullet_pos[0] + 5, spawn_bullet_pos[1], self.angle + angles[0], self.bullet_pierce, self.game)
            Bullet(spawn_bullet_pos[0] - 5, spawn_bullet_pos[1], self.angle + angles[1], self.bullet_pierce, self.game)
            Bullet(spawn_bullet_pos[0] + 10, spawn_bullet_pos[1], self.angle + angles[2], self.bullet_pierce, self.game)
            Bullet(spawn_bullet_pos[0] - 10, spawn_bullet_pos[1], self.angle + angles[3], self.bullet_pierce, self.game)
            self.shoot_cooldown = self.fire_delay


class Sniper(Player):
    def __init__(self, game):
        Player.__init__(self, game, "Sniper")
        self.base_player_rect = self.base_player_rect.scale_by(0.35)

    def upgrade_1(self):
        # lets sniper hit one more enemy
        self.bullet_pierce += 1

    def upgrade_2(self):
        # increase size of sniper bullet
        self.bullet_scale += 0.2

    def upgrade_3(self):
        # increase sniper damage by 10
        self.damage += 10

    def upgrade_4(self):
        # increase knockback by 0.1
        self.knockback += 0.1

    def is_shooting(self):
        # fires a bullet when left mouse is clicked and cooldown is 0
        if self.shoot_cooldown == 0 and self.shoot:
            spawn_bullet_pos = self.vec_pos + self.gun_barrel_offset.rotate(self.angle)
            Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.bullet_pierce, self.game)
            self.shoot_cooldown = self.fire_delay

    def power_player(self):
        # powers sniper class up for 10 seconds by tripling damage, adding 3 pierce, and halving fire delay
        if self.not_powered:  # stops multiple power ups being used at once
            pygame.time.set_timer(self.game.power_timer, 10000, 1)
            self.damage *= 3
            self.bullet_pierce += 3
            self.fire_delay /= 2
            self.not_powered = False

    def depower_player(self):
        # removes power up after 10 seconds
        self.damage /= 3
        self.bullet_pierce -= 3
        self.fire_delay *= 2
        self.not_powered = True


class CoverFire(Sniper):
    def __init__(self, game):
        Sniper.__init__(self, game)

    def is_shooting(self):
        # fires an additional bullet behind, to the left, and to the right of the player
        if self.shoot_cooldown == 0 and self.shoot:
            spawn_bullet_pos = self.vec_pos + self.gun_barrel_offset.rotate(self.angle)
            Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.bullet_pierce, self.game)
            Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle - 90, self.bullet_pierce, self.game)
            Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle - 180, self.bullet_pierce, self.game)
            Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle - 270, self.bullet_pierce, self.game)
            self.shoot_cooldown = self.fire_delay


class GrenadeLauncher(Sniper):
    def __init__(self, game):
        Sniper.__init__(self, game)

        # reduce cooldown for grenade launcher to 50
        self.shoot_cooldown = 50

    def is_shooting(self):
        if self.shoot_cooldown == 0 and self.shoot:
            spawn_bullet_pos = self.vec_pos + self.gun_barrel_offset.rotate(self.angle)
            Grenade(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.game)
            self.shoot_cooldown = self.fire_delay


class Wizard(Player):
    def __init__(self, game):
        Player.__init__(self, game, "Wizard")
        self.base_player_rect = self.base_player_rect.scale_by(0.5)

        # variable for damage done by status effects like fire and poison
        self.effect_mult = 1

    def upgrade_1(self):
        # increases stun by 5
        self.stun += 5

    def upgrade_2(self):
        # increases magic size by 0.2
        self.bullet_scale += 0.2

    def upgrade_3(self):
        # increases damage by 10
        self.damage += 10

    def upgrade_4(self):
        # increases damage done by status effects by 0.1
        self.effect_mult += 0.1

    def is_shooting(self):
        # fires magic if left click used and cooldown is 0
        if self.shoot_cooldown == 0 and self.shoot:
            spawn_bullet_pos = self.vec_pos + self.gun_barrel_offset.rotate(self.angle)
            Magic(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.bullet_pierce, self.game)
            self.shoot_cooldown = self.fire_delay

    def power_player(self):
        # powers wizard up for 10 seconds by tripling damage, adding 3 pierce, and halving fire delay
        if self.not_powered:  # stops multiple power ups being used at once
            pygame.time.set_timer(self.game.power_timer, 10000, 1)
            self.damage *= 3
            self.bullet_pierce += 3
            self.fire_delay /= 2
            self.not_powered = False

    def depower_player(self):
        # removes power up after 10 seconds
        self.damage /= 3
        self.bullet_pierce -= 3
        self.fire_delay *= 2
        self.not_powered = True


class FireWizard(Wizard):
    def __init__(self, game):
        Wizard.__init__(self, game)

        # fire wizard has different sprite to wizard
        self.image = self.class_info["evo1_img"].convert_alpha()
        self.base_player_image = pygame.transform.rotozoom(self.image, 0, self.image_scale)

    def is_shooting(self):
        # shoots fire if left click is pressed and cooldown is 0
        if self.shoot_cooldown == 0 and self.shoot:
            spawn_bullet_pos = self.vec_pos + self.gun_barrel_offset.rotate(self.angle)
            Fire(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.bullet_pierce, self.game)
            self.shoot_cooldown = self.fire_delay


class EWizard(Wizard):
    def __init__(self, game):
        Wizard.__init__(self, game)

        # electro wizard has different sprite to wizard
        self.image = self.class_info["evo2_img"].convert_alpha()
        self.base_player_image = pygame.transform.rotozoom(self.image, 0, self.image_scale)

    def is_shooting(self):
        # shoots lightning if cooldown is 0 and player presses left click
        if self.shoot_cooldown == 0 and self.shoot:
            spawn_bullet_pos = self.vec_pos + self.gun_barrel_offset.rotate(self.angle)
            Lightning(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.game)
            self.shoot_cooldown = self.fire_delay


class Crossbow(Player):
    def __init__(self, game):
        Player.__init__(self, game, "Crossbow")
        self.base_player_rect = self.base_player_rect.scale_by(0.5)
        self.effect_mult = 1

    def upgrade_1(self):
        # increase stun by 5
        self.stun += 5

    def upgrade_2(self):
        # increase arrow speed by 5
        self.bullet_speed += 5

    def upgrade_3(self):
        # allows arrow to hit one more enemy
        self.bullet_pierce += 1

    def upgrade_4(self):
        # increases damage done by status effects
        self.effect_mult += 0.1

    def is_shooting(self):
        # shoots arrow if left click held and cooldown is 0
        if self.shoot_cooldown == 0 and self.shoot:
            spawn_bullet_pos = self.vec_pos + self.gun_barrel_offset.rotate(self.angle)
            Arrow(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.bullet_pierce, self.game)
            self.shoot_cooldown = self.fire_delay

    def power_player(self):
        # powers up crossbow for 10 seconds by tripling damage, adding 3 pierce
        if self.not_powered:  # stops multiple power ups being actiavted at once
            pygame.time.set_timer(self.game.power_timer, 10000, 1)
            self.damage *= 3
            self.bullet_pierce += 3
            self.not_powered = False

    def depower_player(self):
        # removes power up after 10 seconds
        self.damage /= 3
        self.bullet_pierce -= 3
        self.not_powered = True


class TripleShot(Crossbow):
    def __init__(self, game):
        Crossbow.__init__(self, game)

    def is_shooting(self):
        # shoots three arrows per shot
        if self.shoot_cooldown == 0 and self.shoot:
            spawn_bullet_pos = self.vec_pos + self.gun_barrel_offset.rotate(self.angle)
            Arrow(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.bullet_pierce, self.game)
            Arrow(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle - 10, self.bullet_pierce, self.game)
            Arrow(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle + 10, self.bullet_pierce, self.game)
            self.shoot_cooldown = self.fire_delay


class MagicBag(Crossbow):
    def __init__(self, game):
        Crossbow.__init__(self, game)
        
    def is_shooting(self):
        # random choice between poison arrow, fire, lightning, and grenade
        if self.shoot_cooldown == 0 and self.shoot:
            spawn_bullet_pos = self.vec_pos + self.gun_barrel_offset.rotate(self.angle)
            ran = random.choice([0, 1, 2, 3])
            match ran:
                case ran if ran == 0:
                    PoisonArrow(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.bullet_pierce, self.game)
                case ran if ran == 1:
                    Fire(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.bullet_pierce, self.game)
                case ran if ran == 2:
                    Lightning(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.game)
                case ran if ran == 3:
                    Grenade(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.game)
            self.shoot_cooldown = self.fire_delay

