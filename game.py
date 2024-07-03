import pygame
import math
from menu import *
from settings import *
from player import Player
from shape import Shape


class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.SPACE_KEY = False, False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = WIDTH, HEIGHT
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        pygame.display.set_caption('Shape Survivors')
        self.clock = pygame.time.Clock()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)

        # Groups
        self.all_sprites_group = pygame.sprite.Group()
        self.obstacles_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.items_group = pygame.sprite.Group()

        self.player_data = class_data
        self.player_class = 'Gunner'

        self.current_time = 0
        self.start_time = 0
        self.game_time = 0

        self.main_menu = MainMenu(self)
        self.credits = Credits(self)
        self.class_select = ClassMenu(self)
        self.level_menu = LevelMenu(self)
        self.end_menu = EndScreen(self)
        self.curr_menu = self.main_menu

        self.ready_to_spawn = False

        self.shape_data = shape_data

        self.enemy_timer = pygame.USEREVENT + 1
        self.game_scale = 2
        pygame.time.set_timer(self.enemy_timer, int(2000 / self.game_scale))

    def game_loop(self):
        while self.playing:
            self.current_time = pygame.time.get_ticks()
            self.check_events()
            if self.BACK_KEY:
                self.playing = False
                self.player.kill()
                self.curr_menu = self.main_menu
            if self.ready_to_spawn:
                while self.game_scale < 40:
                    self.game_scale += 0.1
                self.display.fill((0, 100, 0))
                self.all_sprites_group.update()
                self.display_ui()
                self.window.blit(self.display, (0, 0))
            else:
                self.playing = False
            pygame.display.update()
            self.clock.tick(FPS)
            if not self.ready_to_spawn:
                self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                elif event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                elif event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                elif event.key == pygame.K_RETURN:
                    self.START_KEY = True
                elif event.key == pygame.K_SPACE:
                    self.SPACE_KEY = True
            if event.type == self.enemy_timer:
                if self.ready_to_spawn:
                    Shape(self)

    def start_game(self):
        for bullet in self.bullet_group:
            bullet.kill()
        for shape in self.enemy_group:
            shape.kill()
        self.bullet_group.empty()
        self.enemy_group.empty()
        self.ready_to_spawn = True
        self.player = Player(self, (PLAYER_START_X, PLAYER_START_Y), self.player_class)
        self.player.reset_player()
        self.start_time = pygame.time.get_ticks()
        self.playing = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.SPACE_KEY = False, False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font('Font/GummyBear.ttf', size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=(x, y))
        self.display.blit(text_surface, text_rect)

    def draw_shape(self, colour, num_sides, tilt_angle, x, y, radius):
        pts = []
        for i in range(num_sides):
            x = x + radius * math.cos(tilt_angle + math.pi * 2 * i / num_sides)
            y = y + radius * math.sin(tilt_angle + math.pi * 2 * i / num_sides)
            pts.append([int(x), int(y)])

        pygame.draw.polygon(self.display, colour, pts)

    def display_ui(self):
        healthx, healthy = 150, 60
        levelx, levely = 1000, 60
        timerx, timery = self.DISPLAY_W / 2, 60
        game_time = int((self.current_time - self.start_time) / 1000)

        self.display_health_bar()
        self.draw_text(f"{self.player.health} / {self.player.max_health}", 40, healthx, healthy)
        self.draw_text(f"Level: {self.player.level}", 40, levelx, levely)
        self.draw_text(f"Time: {game_time}", 40, timerx, timery)

    def display_health_bar(self):
        ratio = self.player.health / self.player.max_health
        if 1260 >= self.player.max_health:
            if ratio == 1:
                pygame.draw.rect(self.display, (0, 255, 0), (10, 15, self.player.max_health, 20))
            elif ratio >= 0.75:
                pygame.draw.rect(self.display, (0, 0, 0), (10, 15, self.player.max_health, 20))
                pygame.draw.rect(self.display, (0, 255, 0), (10, 15, self.player.max_health * ratio, 20))
            elif ratio >= 0.25:
                pygame.draw.rect(self.display, (0, 0, 0), (10, 15, self.player.max_health, 20))
                pygame.draw.rect(self.display, (255, 255, 0), (10, 15, self.player.max_health * ratio, 20))
            else:
                pygame.draw.rect(self.display, (0, 0, 0), (10, 15, self.player.max_health, 20))
                pygame.draw.rect(self.display, (255, 0, 0), (10, 15, self.player.max_health * ratio, 20))
            pygame.draw.rect(self.display, (255, 255, 255), (10, 15, self.player.max_health, 20), 4)
        else:
            if ratio == 1:
                pygame.draw.rect(self.display, (0, 255, 0), (10, 15, 1260, 20))
            elif ratio >= 0.75:
                pygame.draw.rect(self.display, (0, 0, 0), (10, 15, self.player.max_health, 20))
                pygame.draw.rect(self.display, (0, 255, 0), (10, 15, self.player.max_health * ratio, 20))
            elif ratio >= 0.25:
                pygame.draw.rect(self.display, (0, 0, 0), (10, 15, self.player.max_health, 20))
                pygame.draw.rect(self.display, (255, 255, 0), (10, 15, self.player.max_health * ratio, 20))
            else:
                pygame.draw.rect(self.display, (0, 0, 0), (10, 15, self.player.max_health, 20))
                pygame.draw.rect(self.display, (255, 0, 0), (10, 15, self.player.max_health * ratio, 20))
            pygame.draw.rect(self.display, (255, 255, 255), (10, 15, 1260, 20), 4)
