import pygame


class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 30, 30)
        self.offset = -250

    def draw_cursor(self):
        self.game.draw_text("X", 30, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Start'
        self.startx, self.starty = self.mid_w, self.mid_h + 150
        self.start_rect = pygame.Rect(0, 0, 500, 50)
        self.start_rect.center = (self.startx, self.starty)
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 200
        self.credits_rect = pygame.Rect(0, 0, 100, 40)
        self.credits_rect.center = (self.creditsx, self.creditsy)
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((40, 40, 100))
            self.game.draw_text("Welcome to Shape Survivors", 60, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 100)
            self.game.draw_text("Press space to start", 40, self.startx, self.starty)
            self.game.draw_text("Credits", 30, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.game.draw_shape((255, 0, 0), 8, 0, self.mid_w - 25, self.mid_h - 25, 50)
            self.blit_screen()

    def check_mouse(self):
        pos = pygame.mouse.get_pos()
        if self.start_rect.collidepoint(pos[0], pos[1]):
            self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
            self.state = 'Start'
        if self.credits_rect.collidepoint(pos[0], pos[1]):
            self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
            self.state = 'Credits'

    def move_cursor(self):
        if self.game.DOWN_KEY or self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'

    def check_input(self):
        if pygame.MOUSEMOTION:
            self.check_mouse()
        self.move_cursor()
        if self.game.SPACE_KEY:
            if self.state == 'Start':
                self.game.start_game()
                self.game.playing = True
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            self.run_display = False


class LevelMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Damage'
        self.damagex, self.damagey = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 5
        self.damage_rect = pygame.Rect(0, 0, 200, 40)
        self.damage_rect.center = (self.damagex, self.damagey)
        self.healthx, self.healthy = self.game.DISPLAY_W / 2, self.game.DISPLAY_H * 2 / 5
        self.health_rect = pygame.Rect(0, 0, 200, 40)
        self.health_rect.center = (self.healthx, self.healthy)
        self.speedx, self.speedy = self.game.DISPLAY_W / 2, self.game.DISPLAY_H * 3 / 5
        self.speed_rect = pygame.Rect(0, 0, 200, 40)
        self.speed_rect.center = (self.speedx, self.speedy)
        self.firex, self.firey = self.game.DISPLAY_W / 2, self.game.DISPLAY_H * 4 / 5
        self.fire_rect = pygame.Rect(0, 0, 200, 40)
        self.fire_rect.center = (self.firex, self.firey)
        self.offset = -100
        self.cursor_rect.midtop = (self.damagex + self.offset, self.damagey)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((40, 40, 100))
            self.game.draw_text("Damage", 40, self.damagex, self.damagey)
            self.game.draw_text("Health", 40, self.healthx, self.healthy)
            self.game.draw_text("Speed", 40, self.speedx, self.speedy)
            self.game.draw_text("Fire rate", 40, self.firex, self.firey)
            self.draw_cursor()
            self.blit_screen()

    def check_mouse(self):
        current_pos = pygame.mouse.get_pos()
        if self.damage_rect.collidepoint(current_pos[0], current_pos[1]):
            self.cursor_rect.midtop = (self.damagex + self.offset, self.damagey)
            self.state = 'Damage'
        if self.health_rect.collidepoint(current_pos[0], current_pos[1]):
            self.cursor_rect.midtop = (self.healthx + self.offset, self.healthy)
            self.state = 'Health'
        if self.speed_rect.collidepoint(current_pos[0], current_pos[1]):
            self.cursor_rect.midtop = (self.speedx + self.offset, self.speedy)
            self.state = 'Speed'
        if self.fire_rect.collidepoint(current_pos[0], current_pos[1]):
            self.cursor_rect.midtop = (self.firex + self.offset, self.firey)
            self.state = 'Fire'

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Damage':
                self.cursor_rect.midtop = (self.healthx + self.offset, self.healthy)
                self.state = 'Health'
            elif self.state == 'Health':
                self.cursor_rect.midtop = (self.speedx + self.offset, self.speedy)
                self.state = 'Speed'
            elif self.state == 'Speed':
                self.cursor_rect.midtop = (self.firex + self.offset, self.firey)
                self.state = 'Fire'
            elif self.state == 'Fire':
                self.cursor_rect.midtop = (self.damagex + self.offset, self.damagey)
                self.state = 'Damage'
        elif self.game.UP_KEY:
            if self.state == 'Damage':
                self.cursor_rect.midtop = (self.firex + self.offset, self.firey)
                self.state = 'Fire'
            elif self.state == 'Health':
                self.cursor_rect.midtop = (self.damagex + self.offset, self.damagey)
                self.state = 'Damage'
            elif self.state == 'Speed':
                self.cursor_rect.midtop = (self.healthx + self.offset, self.healthy)
                self.state = 'Health'
            elif self.state == 'Fire':
                self.cursor_rect.midtop = (self.speedx + self.offset, self.speedy)
                self.state = 'Speed'

    def check_input(self):
        if pygame.MOUSEMOTION:
            self.check_mouse()
        self.move_cursor()
        if self.game.START_KEY or self.game.SPACE_KEY:
            if self.state == 'Damage':
                self.game.player.add_damage()
                self.game.playing = True
            elif self.state == 'Health':
                self.game.player.add_health()
                self.game.playing = True
            elif self.state == 'Speed':
                self.game.player.add_speed()
                self.game.playing = True
            elif self.state == 'Fire':
                self.game.player.add_fire()
                self.game.playing = True
        self.game.ready_to_spawn = True
        self.run_display = False


class EndScreen(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.game_overx, self.game_overy = self.mid_w, self.mid_h - 50
        self.textx, self.texty = self.mid_w, self.mid_h
        self.levelx, self.levely = self.mid_w - 300, self.mid_h + 100
        self.timerx, self.timery = self.mid_w + 250, self.mid_h + 100

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.SPACE_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill((40, 40, 100))
            self.game.draw_text("GAME OVER", 60, self.game_overx, self.game_overy)
            self.game.draw_text("Press space to return to main menu", 40, self.textx, self.texty)
            self.game.draw_text(f"Level: {self.game.player.level}", 40, self.levelx, self.levely)
            self.game.draw_text(f"Time survived: {int((self.game.game_time - self.game.start_time) / 1000)}s", 40, self.timerx, self.timery)
            self.blit_screen()


class Credits(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("Credits", 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text("Made by me", 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.blit_screen()
