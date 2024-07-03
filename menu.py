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

    def text_rect(self, x, y, width, height):
        rect = pygame.Rect(0, 0, width, height)
        rect.center = (x, y)
        return rect

    def draw_rect(self, x, y, width, height, colour, radius):
        rect = pygame.Rect(0, 0, width, height)
        rect.center = (x, y)
        pygame.draw.rect(self.game.display, colour, rect, radius)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Start'
        self.startx, self.starty = self.mid_w, self.mid_h + 150
        self.start_rect = self.text_rect(self.startx, self.starty, 500, 40)
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 200
        self.credits_rect = self.text_rect(self.creditsx, self.creditsy, 200, 40)
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
                self.game.curr_menu = self.game.class_select
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            self.run_display = False


class ClassMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Gunner'
        self.textx, self.texty = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 8
        self.gunx, self.guny = self.game.DISPLAY_W * 3 / 10, self.game.DISPLAY_H * 2 / 5
        self.gun_rect = self.text_rect(self.gunx, self.guny, 500, 200)
        self.wizx, self.wizy = self.game.DISPLAY_W * 3 / 10, self.game.DISPLAY_H * 4 / 5 - 28
        self.wiz_rect = self.text_rect(self.wizx, self.wizy, 500, 200)
        self.sniperx, self.snipery = self.game.DISPLAY_W * 7 / 10, self.game.DISPLAY_H * 2 / 5
        self.sniper_rect = self.text_rect(self.sniperx, self.snipery, 500, 200)
        self.crossx, self.crossy = self.game.DISPLAY_W * 7 / 10, self.game.DISPLAY_H * 4 / 5 - 28
        self.cross_rect = self.text_rect(self.crossx, self.crossy, 500, 200)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((40, 40, 100))
            self.game.draw_text("Class Select", 50, self.textx, self.texty)
            self.display_class("Gunner", self.gunx, self.guny)
            self.display_class("Wizard", self.wizx, self.wizy)
            self.display_class("Sniper", self.sniperx, self.snipery)
            self.display_class("Crossbow", self.crossx, self.crossy)
            self.blit_screen()

    def display_class(self, name, x, y):
        if self.state == name:
            self.draw_rect(x, y, 500, 200, (255, 255, 0), 5)
        else:
            self.draw_rect(x, y, 500, 200, (255, 255, 255), 5)
        info = self.game.player_data[name]
        image = info["player_img"].convert_alpha()
        image = pygame.transform.rotozoom(image, 0, info["player_size"])
        img_rect = image.get_rect(center=(x + 120, y + 50))
        self.game.draw_text(f"{name}", 40, x, y - 60)
        self.game.draw_text(f'Health: {info["health"]}', 30, x - 120, y - 30)
        self.game.draw_text(f'Damage: {info["damage"]}', 30, x + 120, y - 30)
        self.game.draw_text(f'Speed: {info["speed"]}', 30, x - 120, y)
        self.game.draw_text(f'Cooldown: {info["cooldown"]}', 30, x - 120, y + 30)
        self.game.draw_text(f'Bullet speed: {info["bullet_speed"]}', 30, x + 110, y)
        self.game.draw_text(f'Pierce: {info["pierce"]}', 30, x - 120, y + 60)
        self.game.display.blit(image, img_rect)


    def check_mouse(self):
        pos = pygame.mouse.get_pos()
        if self.gun_rect.collidepoint(pos[0], pos[1]):
            self.state = 'Gunner'
        if self.wiz_rect.collidepoint(pos[0], pos[1]):
            self.state = 'Wizard'
        if self.sniper_rect.collidepoint(pos[0], pos[1]):
            self.state = 'Sniper'
        if self.cross_rect.collidepoint(pos[0], pos[1]):
            self.state = 'Crossbow'

    def check_input(self):
        if pygame.MOUSEMOTION:
            self.check_mouse()
        if self.game.SPACE_KEY:
            if self.state == 'Gunner':
                self.game.player_class = 'Gunner'
                self.game.start_game()
            elif self.state == 'Wizard':
                self.game.player_class = 'Wizard'
                self.game.start_game()
            elif self.state == 'Sniper':
                self.game.player_class = 'Sniper'
                self.game.start_game()
            elif self.state == 'Crossbow':
                self.game.player_class = 'Crossbow'
                self.game.start_game()
            self.run_display = False




class LevelMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Damage'
        self.levelx, self.levely = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 5
        self.damagex, self.damagey = self.game.DISPLAY_W / 3, self.game.DISPLAY_H * 3 / 8
        self.damage_rect = self.text_rect(self.damagex, self.damagey, 200, 40)
        self.healthx, self.healthy = self.game.DISPLAY_W / 3, self.game.DISPLAY_H * 5 / 8
        self.health_rect = self.text_rect(self.healthx, self.healthy, 200, 40)
        self.speedx, self.speedy = self.game.DISPLAY_W / 3, self.game.DISPLAY_H * 7 / 8
        self.speed_rect = self.text_rect(self.speedx, self.speedy, 200, 40)
        self.firex, self.firey = self.game.DISPLAY_W * 2 / 3, self.game.DISPLAY_H * 3 / 8
        self.fire_rect = self.text_rect(self.firex, self.firey, 200, 40)
        self.scalex, self.scaley = self.game.DISPLAY_W * 2 / 3, self.game.DISPLAY_H * 5 / 8
        self.scale_rect = self.text_rect(self.scalex, self.scaley, 200, 40)
        self.expx, self.expy = self.game.DISPLAY_W * 2 / 3, self.game.DISPLAY_H * 7 / 8
        self.exp_rect = self.text_rect(self.expx, self.expy, 200, 40)
        self.offset = -100
        self.cursor_rect.midtop = (self.damagex + self.offset, self.damagey)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((40, 40, 100))
            self.game.draw_text("Select upgrade, space to confirm", 50, self.levelx, self.levely)
            self.game.draw_text("Damage", 40, self.damagex, self.damagey)
            self.game.draw_text("Health", 40, self.healthx, self.healthy)
            self.game.draw_text("Speed", 40, self.speedx, self.speedy)
            self.game.draw_text("Fire rate", 40, self.firex, self.firey)
            self.game.draw_text("Bullet size", 40, self.scalex, self.scaley)
            self.game.draw_text("Exp scale", 40, self.expx, self.expy)
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
        if self.scale_rect.collidepoint(current_pos[0], current_pos[1]):
            self.cursor_rect.midtop = (self.scalex + self.offset - 20, self.scaley)
            self.state = 'Scale'
        if self.exp_rect.collidepoint(current_pos[0], current_pos[1]):
            self.cursor_rect.midtop = (self.expx + self.offset, self.expy)
            self.state = 'Exp'


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
        # self.move_cursor()
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
            elif self.state == 'Scale':
                self.game.player.bigger_bullet()
                self.game.playing = True
            elif self.state == 'Exp':
                self.game.player.add_exp_scale()
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
