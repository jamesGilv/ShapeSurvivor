import math
from menu import *
from settings import *
from shape import Shape, Boss


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
        self.bullet_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.items_group = pygame.sprite.Group()

        self.player_data = class_data
        self.item_data = item_data

        self.current_time = 0
        self.start_time = 0
        self.game_time = 0

        self.main_menu = MainMenu(self)
        self.credits = Credits(self)
        self.class_select = ClassMenu(self)
        self.level_menu = LevelMenu(self)
        self.evo_menu = EvoScreen(self)
        self.end_menu = EndScreen(self)
        self.curr_menu = self.main_menu

        self.ready_to_spawn = False

        self.shape_data = shape_data
        self.sides = [1, 3, 4]
        self.current_colour = (255, 200, 200)

        self.enemy_timer = pygame.USEREVENT + 1
        self.scale_timer = pygame.USEREVENT + 2
        self.boss_timer = pygame.USEREVENT + 3
        self.ring_timer = pygame.USEREVENT + 4
        self.survive_timer = pygame.USEREVENT + 5
        self.power_timer = pygame.USEREVENT + 6

        self.game_won = False

    def game_loop(self):
        while self.playing:
            self.current_time = pygame.time.get_ticks()
            self.check_events()
            if self.BACK_KEY:
                self.playing = False
                self.reset_game()
                self.curr_menu = self.main_menu
            if self.ready_to_spawn:
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
            if pygame.mouse.get_pressed() == (0, 0, 1) and self.player.saved_levels > 0:
                self.ready_to_spawn = False
                self.curr_menu = self.level_menu
            if event.type == self.enemy_timer:
                if self.ready_to_spawn:
                    Shape(self, random.choice(self.sides))
            if event.type == self.scale_timer:
                new = self.sides[-1] + 1
                self.sides.append(new)
                self.shape_data[new] = {"health": 10*new, "attack_damage": 5*new, "speed": 1,
                                        "colour": self.current_colour, "radius": 20}
                if self.current_colour[1] > 0:
                    self.current_colour = (self.current_colour[0], self.current_colour[1]-10, self.current_colour[2]-10)
            if event.type == self.boss_timer:
                Boss(self, self.sides[-1])
            if event.type == self.ring_timer:
                self.spawn_ring()
            if event.type == self.survive_timer:
                for shape in self.ring_shapes:
                    shape.kill()
            if event.type == self.power_timer:
                self.player.depower_player()

    def start_game(self):
        for bullet in self.bullet_group:
            bullet.kill()
        for shape in self.enemy_group:
            shape.kill()
        for item in self.items_group:
            item.kill()
        self.bullet_group.empty()
        self.enemy_group.empty()
        self.items_group.empty()
        self.ready_to_spawn = True
        self.player.reset_player()
        self.start_time = pygame.time.get_ticks()
        pygame.time.set_timer(self.enemy_timer, 1000)
        pygame.time.set_timer(self.scale_timer, 30000)
        pygame.time.set_timer(self.boss_timer, 60000)
        pygame.time.set_timer(self.ring_timer, 120000)
        self.playing = True

    def reset_game(self):
        self.sides = [1, 3, 4]
        self.player.kill()
        pygame.time.set_timer(self.enemy_timer, 0)
        pygame.time.set_timer(self.scale_timer, 0)
        pygame.time.set_timer(self.boss_timer, 0)
        pygame.time.set_timer(self.ring_timer, 0)
        self.shape_data = shape_data


    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.SPACE_KEY = False, False, False, False, False

    def draw_text(self, text, size, x, y, colour):
        font = pygame.font.Font('Font/GummyBear.ttf', size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect(center=(x, y))
        self.display.blit(text_surface, text_rect)

    def draw_shape(self, colour, num_sides, x, y, radius):
        pts = []
        for i in range(num_sides):
            x = x + radius * math.cos(math.pi * 2 * i / num_sides)
            y = y + radius * math.sin(math.pi * 2 * i / num_sides)
            pts.append([int(x), int(y)])

        pygame.draw.polygon(self.display, colour, pts)

    def display_ui(self):
        healthx, healthy = 150, 60
        levelx, levely = 500, 60
        timerx, timery = 800, 60
        coinx, coiny = 1100, 60
        heartx, hearty = 1100, 100
        game_time = int((self.current_time - self.start_time) / 1000)

        self.display_health_bar()
        self.draw_text(f"{self.player.health} / {self.player.max_health}", 40, healthx, healthy, self.WHITE)
        self.draw_text(f"Level: {self.player.level}", 40, levelx, levely, self.WHITE)
        self.draw_text(f"Time: {game_time}", 40, timerx, timery, self.WHITE)
        self.display_item(coinx, coiny, "coin")
        self.display_item(heartx, hearty, "heart")
        self.draw_text(f"{self.player.coins}", 40, coinx + 40, coiny, self.WHITE)
        self.draw_text(f"{self.player.lives}", 40, heartx + 40, hearty, (255, 0, 0))
        if self.player.saved_levels > 0:
            self.draw_text(f"+{self.player.saved_levels}", 30, levelx, levely + 30, self.WHITE)

    def display_item(self, x, y, name):
        info = self.item_data[name]
        image = info["image"].convert_alpha()
        rect = image.get_rect(center=(x, y))
        self.display.blit(image, rect)

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
                pygame.draw.rect(self.display, (0, 0, 0), (10, 15, 1260, 20))
                pygame.draw.rect(self.display, (0, 255, 0), (10, 15, 1260 * ratio, 20))
            elif ratio >= 0.25:
                pygame.draw.rect(self.display, (0, 0, 0), (10, 15, 1260, 20))
                pygame.draw.rect(self.display, (255, 255, 0), (10, 15, 1260 * ratio, 20))
            else:
                pygame.draw.rect(self.display, (0, 0, 0), (10, 15, 1260, 20))
                pygame.draw.rect(self.display, (255, 0, 0), (10, 15, 1260 * ratio, 20))
            pygame.draw.rect(self.display, (255, 255, 255), (10, 15, 1260, 20), 4)

    def spawn_ring(self):
        radius = 400
        spawns = 16
        self.ring_shapes = []
        time = 30000
        for i in range(spawns):
            x = self.player.base_player_rect.centerx + radius * math.cos(math.pi * 2 * i / spawns)
            y = self.player.base_player_rect.centery + radius * math.sin(math.pi * 2 * i / spawns)
            if 0 < x < self.DISPLAY_W and 0 < y < self.DISPLAY_H:
                center = pygame.math.Vector2(x, y)
                spawn = Shape(self, self.sides[-1])
                spawn.speed = 0
                spawn.position = center
                self.ring_shapes.append(spawn)
        pygame.time.set_timer(self.survive_timer, time, 1)
