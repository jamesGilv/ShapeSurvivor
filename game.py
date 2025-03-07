import math

import pygame

from menu import *
from settings import *
from shape import Shape, Boss, Ring, Turret, get_points


class Game():
    def __init__(self):
        # must initialise pygame when game starts
        pygame.init()

        # bools for menu control
        self.running, self.playing = True, False

        # bools for specific keys
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.SPACE_KEY = False, False, False, False, False
        self.PAUSE_KEY = False

        # dimensions of screen
        self.DISPLAY_W, self.DISPLAY_H = WIDTH, HEIGHT

        # create display to draw on
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))

        # create window for game to be played
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))

        # change text in top right of window
        pygame.display.set_caption('Shape Survivors')

        # clock for time keeping
        self.clock = pygame.time.Clock()

        # colour shortcuts
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)

        # Groups
        self.all_sprites_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.items_group = pygame.sprite.Group()

        # info from settings
        self.player_data = class_data
        self.item_data = item_data
        self.weapon_images = weapon_images
        self.shape_data = shape_data

        # must store different times as game can be played multiple times per window
        self.current_time = 0
        self.start_time = 0
        self.game_time = 0

        # create menus to allow for menu swapping
        self.main_menu = NewMenu(self)
        self.controls = ControlsMenu(self)
        self.credits = Credits(self)
        self.class_select = ClassMenu(self)
        self.level_menu = LevelMenu(self)
        self.evo_menu = EvoScreen(self)
        self.end_menu = EndScreen(self)
        self.pause_menu = PauseMenu(self)
        self.curr_menu = self.main_menu

        # only want to spawn shapes when game is being played, not during menus
        self.ready_to_spawn = False

        # list of available sides
        self.sides = [1, 3, 4]

        # can change colour of new shapes added to list
        self.current_colour = (255, 200, 200)

        # timers
        self.enemy_timer = pygame.USEREVENT + 1
        self.scale_timer = pygame.USEREVENT + 2
        self.boss_timer = pygame.USEREVENT + 3
        self.ring_timer = pygame.USEREVENT + 4
        self.survive_timer = pygame.USEREVENT + 5
        self.power_timer = pygame.USEREVENT + 6
        self.exp_timer = pygame.USEREVENT + 7
        self.invincible_timer = pygame.USEREVENT + 8
        self.speed_timer = pygame.USEREVENT + 9

        self.game_won = False

    def game_loop(self):
        while self.playing:
            # always need current time and to check events when playing
            self.current_time = pygame.time.get_ticks()
            self.check_events()
            if self.BACK_KEY:
                # when backspace pressed while playing, return to main menu and reset game
                self.playing = False
                self.reset_game()
                self.curr_menu = self.main_menu
            if self.PAUSE_KEY:
                # when p pressed while playing, pause game
                self.curr_menu = self.pause_menu
                self.PAUSE_KEY = False
                self.playing = False
            if self.ready_to_spawn:
                # if playing and ready to spawn, can spawn shapes and display user interface (UI)
                self.display.fill((0, 100, 0))
                self.all_sprites_group.update()
                self.display_ui()
                self.window.blit(self.display, (0, 0))
            else:
                self.playing = False

            # need to always be updating sprites, and updating clock a certain number of times per second
            pygame.display.update()
            self.clock.tick(FPS)
            if not self.ready_to_spawn:
                # when playing but not spawning (menus), this means if a button is held down it will appear as one press
                self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            # pygame.QUIT is the red x in the top right corner
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                # KEYDOWN is a key being pressed, check for up, down, backspace, enter, and space
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
                elif event.key == pygame.K_p:
                    self.PAUSE_KEY = True
            # right click will bring up upgrade menu if player has saved levels
            if pygame.mouse.get_pressed() == (0, 0, 1) and self.player.saved_levels > 0:
                # need to pause shape spawning while in menu
                self.ready_to_spawn = False
                # swap to level menu
                self.curr_menu = self.level_menu
            if event.type == self.enemy_timer:
                # will spawn a shape when ready to spawn is true
                if self.ready_to_spawn:
                    # Turret(self)
                    Shape(self)
            if event.type == self.scale_timer:
                # adds new shape to the list, and creates new dictionary entry containing shape data
                new = self.sides[-1] + 1
                self.sides.append(new)
                self.shape_data[new] = {"health": 10*new, "attack_damage": 5*new, "speed": 1,
                                        "colour": self.current_colour, "radius": 20}
                # each shape added gets more red
                if self.current_colour[1] > 0:
                    self.current_colour = (self.current_colour[0], self.current_colour[1]-10, self.current_colour[2]-10)
            if event.type == self.boss_timer:
                # spawn a boss
                Boss(self)
            if event.type == self.ring_timer:
                # spawn a ring of shapes around the player
                self.spawn_ring()
            if event.type == self.survive_timer:
                # when timer is up, kill remaining shapes in ring
                for shape in self.ring_shapes:
                    shape.kill()
            if event.type == self.power_timer:
                # must remove power up from player
                self.player.depower_player()
            if event.type == self.exp_timer:
                # must remove double exp for player
                self.player.level_scale /= 2
            if event.type == self.invincible_timer:
                # remove invincibility from player
                self.player.damage_mult = 1
            if event.type == self.speed_timer:
                # remove super speed from player
                self.player.speed = int(self.player.speed / 2)

    def start_game(self):
        # upon game start, clear all sprites except for player
        self.empty_groups()

        # can now spawn shapes
        self.ready_to_spawn = True

        # must reset player and start timers
        self.player.reset_player()
        self.start_time = pygame.time.get_ticks()
        pygame.time.set_timer(self.enemy_timer, 1500)
        pygame.time.set_timer(self.scale_timer, 30000)
        pygame.time.set_timer(self.boss_timer, 60000)
        pygame.time.set_timer(self.ring_timer, 120000)
        self.playing = True

    def reset_game(self):
        # resets shape data, kills player, and removes timers
        self.sides = [1, 3, 4]
        self.player.reset_player()

        self.empty_groups()

        pygame.time.set_timer(self.enemy_timer, 0)
        pygame.time.set_timer(self.scale_timer, 0)
        pygame.time.set_timer(self.boss_timer, 0)
        pygame.time.set_timer(self.ring_timer, 0)
        self.shape_data = shape_data

    def empty_groups(self):
        # function for killing all current shapes, bullets, items abd renoves them from groups
        for bullet in self.bullet_group:
            bullet.kill()
        for shape in self.enemy_group:
            shape.kill()
        for item in self.items_group:
            item.kill()
        self.bullet_group.empty()
        self.enemy_group.empty()
        self.items_group.empty()

    def reset_keys(self):
        # resets keys to false
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.SPACE_KEY = False, False, False, False, False
        self.PAUSE_KEY = False

    def draw_text(self, text, size, x, y, colour):
        # function for drawing text with variable for position, size, and colour
        font = pygame.font.Font('Font/GummyBear.ttf', size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect(center=(x, y))
        self.display.blit(text_surface, text_rect)

    def display_ui(self):
        # set positions for health, level, timer, coins, and loves
        healthx, healthy = 150, 60
        levelx, levely = 500, 60
        timerx, timery = 800, 60
        coinx, coiny = 1100, 60
        heartx, hearty = 1100, 100
        pausex, pausey = 1180, 570

        # calculate game time in seconds
        self.game_time = int((self.current_time - self.start_time) / 1000) - self.pause_menu.time_paused

        self.display_health_bar()

        # draw health, levels, time, coins, and hearts on screen
        self.draw_text(f"{self.player.health} / {self.player.max_health}", 40, healthx, healthy, self.WHITE)
        self.draw_text(f"Level: {self.player.level}", 40, levelx, levely, self.WHITE)
        self.draw_text(f"Time: {self.game_time}", 40, timerx, timery, self.WHITE)
        self.display_item(coinx, coiny, "coin")
        self.display_item(heartx, hearty, "heart")
        self.draw_text(f"{self.player.coins}", 40, coinx + 40, coiny, self.WHITE)
        self.draw_text(f"{self.player.lives}", 40, heartx + 40, hearty, (255, 0, 0))
        self.draw_text("Pause: P", 40, pausex, pausey, (255, 255, 255))

        # will display saved levels if there are any
        if self.player.saved_levels > 0:
            self.draw_text(f"+{self.player.saved_levels}", 30, levelx, levely + 30, self.WHITE)

    def display_item(self, x, y, name):
        # display items along with their sprite
        info = self.item_data[name]
        image = info["image"].convert_alpha()
        rect = image.get_rect(center=(x, y))
        self.display.blit(image, rect)

    def display_health_bar(self):
        # calculate how much health the player has compared to the max health, show appropriate colour
        ratio = self.player.health / self.player.max_health

        # if max health is less than 1260 (screen width), health bar can get longer across screen
        if 1260 >= self.player.max_health:
            if ratio == 1:
                # for full health just draw one rectangle
                pygame.draw.rect(self.display, (0, 255, 0), (10, 15, self.player.max_health, 20))
            elif ratio >= 0.75:
                # draw black rectangle for max health, then draw health bar on top of it
                pygame.draw.rect(self.display, (0, 0, 0), (10, 15, self.player.max_health, 20))
                # draw health in green if current heath is above 75% max health
                pygame.draw.rect(self.display, (0, 255, 0), (10, 15, self.player.max_health * ratio, 20))
            elif ratio >= 0.25:
                # draw health in yellow if current health is below 75% but above 25% max health
                pygame.draw.rect(self.display, (0, 0, 0), (10, 15, self.player.max_health, 20))
                pygame.draw.rect(self.display, (255, 255, 0), (10, 15, self.player.max_health * ratio, 20))
            else:
                # draw health in red if current health is less than 25% of max health
                pygame.draw.rect(self.display, (0, 0, 0), (10, 15, self.player.max_health, 20))
                pygame.draw.rect(self.display, (255, 0, 0), (10, 15, self.player.max_health * ratio, 20))
            # draw white border around health bar to make it stand out
            pygame.draw.rect(self.display, (255, 255, 255), (10, 15, self.player.max_health, 20), 4)
        else:
            # max health is above 1260, so goes across the entire screen
            if ratio == 1:
                # full health
                pygame.draw.rect(self.display, (0, 255, 0), (10, 15, 1260, 20))
            elif ratio >= 0.75:
                # above 75% is green
                pygame.draw.rect(self.display, (0, 0, 0), (10, 15, 1260, 20))
                pygame.draw.rect(self.display, (0, 255, 0), (10, 15, 1260 * ratio, 20))
            elif ratio >= 0.25:
                # between 25% and 75% is yellow
                pygame.draw.rect(self.display, (0, 0, 0), (10, 15, 1260, 20))
                pygame.draw.rect(self.display, (255, 255, 0), (10, 15, 1260 * ratio, 20))
            else:
                # below 25% is red
                pygame.draw.rect(self.display, (0, 0, 0), (10, 15, 1260, 20))
                pygame.draw.rect(self.display, (255, 0, 0), (10, 15, 1260 * ratio, 20))
            # white border around health bar
            pygame.draw.rect(self.display, (255, 255, 255), (10, 15, 1260, 20), 4)

    def spawn_ring(self):
        # spwans a set amount of shapes in a circle around the player
        radius = 300
        spawns = 16

        # make a group so that it is easier to remove them after set time
        self.ring_shapes = []
        time = 30000
        for i in range(spawns):
            x = self.player.base_player_rect.centerx + radius * math.cos(math.pi * 2 * i / spawns)
            y = self.player.base_player_rect.centery + radius * math.sin(math.pi * 2 * i / spawns)

            # if the shape is off the screen, remove it
            if 0 < x < self.DISPLAY_W and 0 < y < self.DISPLAY_H:
                center = pygame.math.Vector2(x, y)
                spawn = Ring(self, center)
                spawn.points = get_points(spawn.sides, x, y, spawn.radius)
                self.ring_shapes.append(spawn)

        # set a timer for the rings to be removed
        pygame.time.set_timer(self.survive_timer, time, 1)
