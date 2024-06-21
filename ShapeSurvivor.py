import pygame
from settings import *
import random
from sys import exit
import math
from pygame.math import Vector2

pygame.init()

# Game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Shape Survivors')
clock = pygame.time.Clock()


# Fonts
font = pygame.font.Font('Font/GummyBear.ttf', 60)
small_font = pygame.font.Font('Font/GummyBear.ttf', 40)
level_font = pygame.font.Font('Font/bakemono_stereo/Bakemono-Stereo-Regular-trial.ttf', 40)

# Images
background = pygame.Rect(0, 0, WIDTH, HEIGHT)
player_image = pygame.image.load('Graphics/player.png').convert_alpha()
player_image = pygame.transform.rotozoom(player_image, 0, PLAYER_SIZE)

bullet_img = pygame.image.load('Graphics/bullet_1.png').convert_alpha()
bullet_img = pygame.transform.rotozoom(bullet_img, 0, BULLET_SCALE)

# Sounds

# Game variables
game_active = True
ready_to_spawn = True
upgrade_select = False
current_time = 0
start_time = 0
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1000)


# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites_group)
        self.image = player_image
        self.base_player_image = self.image

        self.pos = pos
        self.vec_pos = Vector2(pos)
        self.base_player_rect = self.base_player_image.get_rect(center=pos)
        self.rect = self.base_player_rect.copy()

        self.player_speed = PLAYER_SPEED
        self.shoot = False
        self.shoot_cooldown = 0
        self.fire_delay = SHOOT_COOLDOWN

        self.health = PLAYER_HEALTH

        self.gun_barrel_offset = pygame.math.Vector2(45, 20)

        self.damage = BULLET_DAMAGE
        self.experience = 0

    def player_turning(self):
        self.mouse_coords = pygame.mouse.get_pos()

        self.x_change_mouse_player = (self.mouse_coords[0] - self.rect.centerx)
        self.y_change_mouse_player = (self.mouse_coords[1] - self.rect.centery)
        self.angle = int(math.degrees(math.atan2(self.y_change_mouse_player, self.x_change_mouse_player)))
        self.angle = (self.angle) % 360 # if this stop working add 360 in the brackets

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

        if pygame.mouse.get_pressed() == (1, 0, 0) or keys[pygame.K_SPACE]:
            self.shoot = True
            self.is_shooting()
        else:
            self.shoot = False

        if event.type == pygame.KEYUP:
            if pygame.mouse.get_pressed() == (1, 0, 0):
                self.shoot = False

    def is_shooting(self):
        if self.shoot_cooldown == 0 and self.shoot:
            # gun_shot_sound.play()
            spawn_bullet_pos = self.vec_pos + self.gun_barrel_offset.rotate(self.angle)
            self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle)
            self.shoot_cooldown = self.fire_delay
            bullet_group.add(self.bullet)
            all_sprites_group.add(self.bullet)

    def move(self):
        self.base_player_rect.centerx += self.velocity_x
        # self.check_collision("horizontal")

        self.base_player_rect.centery += self.velocity_y
        # self.check_collision("vertical")

        self.rect.center = self.base_player_rect.center

        self.vec_pos = (self.base_player_rect.centerx, self.base_player_rect.centery)

    def get_damage(self, amount):
        self.health -= amount

    def check_level(self):
        if self.experience >= 100:
            level_up()

    def update(self):
        self.player_turning()
        self.player_input()
        self.move()
        self.check_level()

        if self.shoot_cooldown > 0: # Just shot a bullet
            self.shoot_cooldown -= 1
        if self.shoot:
            self.is_shooting()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = bullet_img
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
        hits = pygame.sprite.groupcollide(enemy_group, bullet_group, False, True, hitbox_collide)

        for hit in hits:
            hit.health -= player.damage

    def update(self):
        self.bullet_movement()
        self.bullet_collisions()


class Shape(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites_group, enemy_group)
        self.alive = True
        self.x_pos = random.randint(-100, WIDTH + 100)
        self.y_pos = random.randint(-100, HEIGHT + 100)
        self.position = Vector2(self.x_pos, self.y_pos)
        self.name = random.choice(["circle", "triangle", "square", "pentagon", "hexagon", "septagon", "octagon"])

        self.velocity = Vector2()
        self.direction = Vector2()
        self.direction_list = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        enemy_info = shape_data[self.name]
        self.health = enemy_info["health"]
        self.attack_damage = enemy_info["attack_damage"]
        self.speed = enemy_info["speed"]
        self.sides = enemy_info["sides"]
        self.colour = enemy_info["colour"]
        self.radius = enemy_info["radius"]
        self.exp = enemy_info["exp"]

        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.radius, self.radius)
        self.rect.center = self.position

        self.collide = False

    def check_alive(self):
        if self.health <= 0:
            self.alive = False
            player.experience += self.exp
            self.kill()

    def check_collision(self, direction):
        for sprite in enemy_group:
            if sprite.hitbox_rect != self.rect:
                if self.get_vector_distance(self.position, sprite.position) < self.radius:
                    # print('collide')
                    self.collide = True
                    if direction == "horizontal":
                        if self.velocity.x > 0:
                            self.rect.centerx -= self.radius/2
                            sprite.rect.centerx += self.radius/2
                        if self.velocity.x < 0:
                            self.rect.centerx += self.radius/2
                            sprite.rect.centerx -= self.radius/2
                    if direction == "vertical":
                        if self.velocity.y < 0:
                            self.rect.centery -= self.radius/2
                            sprite.rect.centery += self.radius/2
                        if self.velocity.y > 0:
                            self.rect.centery += self.radius / 2
                            sprite.rect.centery= self.radius / 2
    def get_vector_distance(self, vector_1, vector_2):
        return (vector_1 - vector_2).magnitude()

    def move_shape(self):
        target_vector = Vector2(player.base_player_rect.center)
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
        if pygame.Rect.colliderect(self.rect, player.base_player_rect): # player and enemy collides
            self.kill()
            player.get_damage(self.attack_damage)

    def update(self):
        if self.alive:
            self.check_alive()
            self.move_shape()
            self.check_player_collision()
            if self.name == "circle":
                pygame.draw.circle(screen, self.colour, (self.rect.x, self.rect.y), self.radius)
            else:
                draw_shape(self.colour, self.sides, 0, self.rect.x, self.rect.y, self.radius)


# Groups
all_sprites_group = pygame.sprite.Group()
obstacles_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
items_group = pygame.sprite.Group()

def hitbox_collide(sprite1, sprite2):
    return sprite1.rect.colliderect(sprite2.rect)

def draw_shape(colour, num_sides, tilt_angle, x, y, radius):
    pts = []
    for i in range(num_sides):
        x = x + radius * math.cos(tilt_angle + math.pi * 2 * i / num_sides)
        y = y + radius * math.sin(tilt_angle + math.pi * 2 * i / num_sides)
        pts.append([int(x), int(y)])

    pygame.draw.polygon(screen, colour, pts)

def level_up():
    global upgrade_select
    upgrade_select = True
    global ready_to_spawn
    ready_to_spawn = False
    screen.fill((0, 100, 200))

    level_text = level_font.render("Level up, select upgrade", True, WHITE)
    upgrade_text = level_font.render("For damage: d. For health: h. For speed: s. For firerate: f", True, WHITE)

    screen.blit(level_text, ((WIDTH - level_text.get_width())/2, HEIGHT/2 - 100))
    screen.blit(upgrade_text, ((WIDTH - upgrade_text.get_width())/2, HEIGHT/2 + 100))

def display_end_screen():
    screen.fill((40, 40, 40))
    draw_shape((255, 0, 0), 8, 0, WIDTH/2 - 25, HEIGHT/2 - 25, 50)
    game_over_surface = font.render("GAME OVER", True, WHITE)
    text_surface = small_font.render("Press space to play again", True, WHITE)

    screen.blit(game_over_surface, ((WIDTH - game_over_surface.get_width())/2, HEIGHT/2 - 100))
    screen.blit(text_surface, ((WIDTH - text_surface.get_width())/2, HEIGHT/2 + 100))

def end_game():
    global game_active
    game_active = False
    for item in items_group:
        item.kill()
    for enemy in enemy_group:
        enemy.kill()
    enemy_group.empty()
    items_group.empty()

player = Player((PLAYER_START_X, PLAYER_START_Y))
# Shape()
# Shape()

while True:
    current_time = pygame.time.get_ticks()
    if player.health <= 0:
        end_game()

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if not game_active and keys[pygame.K_SPACE]:
            player.health = 100
            game_active = True
            start_time = pygame.time.get_ticks()
        if game_active:
            if not ready_to_spawn: # level up screen
                if keys[pygame.K_d]:
                    player.damage += 10
                    ready_to_spawn = True
                    player.experience = 0
                if keys[pygame.K_h]:
                    player.health += 20
                    ready_to_spawn = True
                    player.experience = 0
                if keys[pygame.K_s]:
                    player.player_speed += 1
                    ready_to_spawn = True
                    player.experience = 0
                if keys[pygame.K_f]:
                    player.fire_delay -= 1
                    ready_to_spawn = True
                    player.experience = 0

            if event.type == enemy_timer:
                Shape()

    if game_active:
        if ready_to_spawn:
            pygame.draw.rect(screen, (0, 100, 0), background)
            all_sprites_group.update()
            screen.blit(player.image, player.rect)
            for bullet in bullet_group:
                screen.blit(bullet_img, bullet.rect)
    else:
        end_game()
        display_end_screen()

    pygame.display.update()
    clock.tick(FPS)
