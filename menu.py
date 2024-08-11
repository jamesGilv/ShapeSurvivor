import pygame
from player import Gunner, Sniper, Wizard, Crossbow


class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 30, 30)
        self.offset = -250

    def draw_cursor(self):
        self.game.draw_text("X", 30, self.cursor_rect.x, self.cursor_rect.y, self.game.WHITE)

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
        self.startx, self.starty = self.mid_w, self.mid_h + 100
        self.start_rect = self.text_rect(self.startx, self.starty, 500, 40)
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 150
        self.credits_rect = self.text_rect(self.creditsx, self.creditsy, 200, 40)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((40, 40, 100))
            self.game.draw_text("Welcome to Shape Survivors", 60, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200, (255, 255, 255))
            if self.state == 'Start':
                self.game.draw_text("Start Game", 40, self.startx, self.starty, (255, 255, 0))
                self.game.draw_text("Credits", 30, self.creditsx, self.creditsy, (255, 255, 255))
            else:
                self.game.draw_text("Start Game", 40, self.startx, self.starty, (255, 255, 255))
                self.game.draw_text("Credits", 30, self.creditsx, self.creditsy, (255, 255, 0))
            self.game.draw_text("Controls:", 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 200, (255, 255, 255))
            self.game.draw_text("Aim: L-Mouse     Confirm: Space     Move: wasd     Upgrade: R-Mouse", 20, self.mid_w, self.mid_h + 250, (255, 255, 255))
            self.game.draw_shape((255, 0, 0), 8, self.mid_w - 25, self.mid_h - 75, 50)
            self.blit_screen()

    def check_mouse(self):
        pos = pygame.mouse.get_pos()
        if self.start_rect.collidepoint(pos[0], pos[1]):
            self.state = 'Start'
        if self.credits_rect.collidepoint(pos[0], pos[1]):
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
            self.game.draw_text("Class Select", 50, self.textx, self.texty, (255, 255, 255))
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
        self.game.draw_text(f"{name}", 40, x, y - 60, (255, 255, 255))
        self.game.draw_text(f'Health: {info["health"]}', 30, x - 120, y - 30, (255, 255, 255))
        self.game.draw_text(f'Damage: {info["damage"]}', 30, x + 120, y - 30, (255, 255, 255))
        self.game.draw_text(f'Speed: {info["speed"]}', 30, x - 120, y, (255, 255, 255))
        self.game.draw_text(f'Cooldown: {info["cooldown"]}', 30, x - 120, y + 30, (255, 255, 255))
        self.game.draw_text(f'Bullet speed: {info["bullet_speed"]}', 30, x + 110, y, (255, 255, 255))
        self.game.draw_text(f'Pierce: {info["pierce"]}', 30, x - 120, y + 60, (255, 255, 255))
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
                self.game.player = Gunner(self.game)
                self.game.start_game()
            elif self.state == 'Wizard':
                self.game.player_class = 'Wizard'
                self.game.player = Wizard(self.game)
                self.game.start_game()
            elif self.state == 'Sniper':
                self.game.player_class = 'Sniper'
                self.game.player = Sniper(self.game)
                self.game.start_game()
            elif self.state == 'Crossbow':
                self.game.player_class = 'Crossbow'
                self.game.player = Crossbow(self.game)
                self.game.start_game()
            self.run_display = False


class LevelMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Damage'
        self.levelx, self.levely = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 6
        self.healthx, self.healthy = self.mid_w - 280, self.mid_h - 50
        self.health_rect = self.text_rect(self.healthx, self.healthy, 300, 50)
        self.speedx, self.speedy = self.mid_w + 80, self.mid_h - 50
        self.speed_rect = self.text_rect(self.speedx, self.speedy, 300, 50)
        self.up_1x, self.up_1y = self.mid_w - 280, self.mid_h + 50
        self.up_1_rect = self.text_rect(self.up_1x, self.up_1y, 300, 50)
        self.up_2x, self.up_2y = self.mid_w + 80, self.mid_h + 50
        self.up_2_rect = self.text_rect(self.up_2x, self.up_2y, 300, 50)
        self.up_3x, self.up_3y = self.mid_w - 280, self.mid_h + 150
        self.up_3_rect = self.text_rect(self.up_3x, self.up_3y, 300, 50)
        self.up_4x, self.up_4y = self.mid_w + 80, self.mid_h + 150
        self.up_4_rect = self.text_rect(self.up_4x, self.up_4y, 300, 50)

        self.itemx, self.itemy = 1200, 50
        self.lifex, self.lifey = 1100, 300
        self.life_rect = self.text_rect(self.lifex, self.lifey, 300, 50)
        self.killx, self.killy = 1100, 400
        self.kill_rect = self.text_rect(self.killx, self.killy, 300, 50)
        self.winx, self.winy = 1100, 500
        self.win_rect = self.text_rect(self.winx, self.winy, 300, 50)
        self.item_data = self.game.item_data

    def display_menu(self):
        self.run_display = True
        info = self.game.player_data[self.game.player_class]
        self.up_1 = info["up_1"]
        self.up_2 = info["up_2"]
        self.up_3 = info["up_3"]
        self.up_4 = info["up_4"]
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((40, 40, 100))
            self.game.draw_text("Select upgrade, space to confirm", 50, self.levelx, self.levely, (255, 255, 255))
            self.game.draw_text(f"Levels remaining: {self.game.player.saved_levels}", 40, self.levelx, self.levely + 50, (255, 255, 255))
            self.draw_level("Health", self.healthx, self.healthy)
            self.draw_level("Speed", self.speedx, self.speedy)
            self.draw_level(self.up_1, self.up_1x, self.up_1y)
            self.draw_level(self.up_2, self.up_2x, self.up_2y)
            self.draw_level(self.up_3, self.up_3x, self.up_3y)
            self.draw_level(self.up_4, self.up_4x, self.up_4y)

            self.draw_item("coin", self.itemx - 40, self.itemy)
            self.draw_level("Extra Life", self.lifex, self.lifey)
            self.draw_level("Clear screen", self.killx, self.killy)
            self.draw_level("Win game", self.winx, self.winy)
            self.game.draw_text(f"{self.game.player.coins}", 40, self.itemx, self.itemy, (255, 255, 255))
            self.draw_item("heart", self.itemx - 40, self.itemy + 40)
            self.game.draw_text(f"{self.game.player.lives}", 40, self.itemx, self.itemy + 40, (255, 255, 255))
            self.game.draw_text("10", 30, self.lifex, self.lifey + 50, (255, 255, 0))
            self.game.draw_text("20", 30, self.killx, self.killy + 50, (255, 255, 0))
            self.game.draw_text("100", 30, self.winx, self.winy + 50, (255, 255, 0))
            self.game.draw_text("Shop", 50, 1100, 200, (255, 255, 255))
            self.blit_screen()

    def draw_item(self, name, x, y):
        info = self.item_data[name]
        image = info["image"].convert_alpha()
        image_rect = image.get_rect(center=(x, y))
        self.game.display.blit(image, image_rect)

    def draw_level(self, name, x, y):
        self.game.draw_text(f"{name}", 40, x, y, (255, 255, 255))
        if self.state == name:
            self.draw_rect(x, y, 300, 50, (255, 255, 0), 5)
        else:
            self.draw_rect(x, y, 300, 50, (255, 255, 255), 5)

    def check_mouse(self):
        current_pos = pygame.mouse.get_pos()
        if self.health_rect.collidepoint(current_pos[0], current_pos[1]):
            self.state = 'Health'
        if self.speed_rect.collidepoint(current_pos[0], current_pos[1]):
            self.state = 'Speed'
        if self.up_1_rect.collidepoint(current_pos[0], current_pos[1]):
            self.state = self.up_1
        if self.up_2_rect.collidepoint(current_pos[0], current_pos[1]):
            self.state = self.up_2
        if self.up_3_rect.collidepoint(current_pos[0], current_pos[1]):
            self.state = self.up_3
        if self.up_4_rect.collidepoint(current_pos[0], current_pos[1]):
            self.state = self.up_4
        if self.life_rect.collidepoint(current_pos[0], current_pos[1]):
            self.state = 'Extra Life'
        if self.kill_rect.collidepoint(current_pos[0], current_pos[1]):
            self.state = 'Clear screen'
        if self.win_rect.collidepoint(current_pos[0], current_pos[1]):
            self.state = 'Win game'

    def check_input(self):
        if pygame.MOUSEMOTION:
            self.check_mouse()
        if self.game.START_KEY or self.game.SPACE_KEY:
            if self.state == 'Extra Life':
                if self.game.player.coins >= 10:
                    self.game.player.lives += 1
                    self.game.player.coins -= 10
            elif self.state == 'Clear screen':
                if self.game.player.coins >= 20:
                    for shape in self.game.enemy_group:
                        shape.kill()
                    self.game.enemy_group.empty()
                    self.game.player.coins -= 20
            elif self.state == 'Win game':
                if self.game.player.coins >= 100:
                    self.game.game_won = True
                    self.run_display = False
                    self.game.ready_to_spawn = False
                    self.game.curr_menu = self.game.end_menu
                    self.game.game_time = pygame.time.get_ticks()
                    self.game.reset_game()
            else:
                if self.state == 'Health':
                    self.game.player.add_health()
                elif self.state == 'Speed':
                    self.game.player.add_speed()
                elif self.state == self.up_1:
                    self.game.player.upgrade_1()
                elif self.state == self.up_2:
                    self.game.player.upgrade_2()
                elif self.state == self.up_3:
                    self.game.player.upgrade_3()
                elif self.state == self.up_4:
                    self.game.player.upgrade_4()
                self.game.player.saved_levels -= 1
                if self.game.player.saved_levels == 0:
                    self.game.playing = True
                    self.game.ready_to_spawn = True
                    self.run_display = False
                self.game.player.level += 1


class EvoScreen(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.evox, self.evoy = self.mid_w, self.game.DISPLAY_H / 6
        self.up_1x, self.up_1y = self.mid_w - 270, self.mid_h
        self.up_1_rect = self.text_rect(self.up_1x, self.up_1y, 500, 200)
        self.up_2x, self.up_2y = self.mid_w + 270, self.mid_h
        self.up_2_rect = self.text_rect(self.up_2x, self.up_2y, 500, 200)

    def display_menu(self):
        info = self.game.player_data[self.game.player_class]
        self.state = info["evo_1"]
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((40, 40, 100))
            self.game.draw_text("Select Evolution", 50, self.evox, self.evoy, (255, 255, 255))
            self.game.draw_text(f"{self.game.player_class} evolutions", 40, self.evox, self.evoy + 50, (255, 255, 255))
            self.display_evo(1, info["evo_1"], info["desc_1"], self.up_1x, self.up_1y)
            self.display_evo(2, info["evo_2"], info["desc_2"], self.up_2x, self.up_2y)
            self.blit_screen()

    def display_evo(self, state, upgrade, desc, x, y):
        if self.state == state:
            self.draw_rect(x, y, 500, 200, (255, 255, 0), 5)
        else:
            self.draw_rect(x, y, 500, 200, (255, 255, 255), 5)
        self.game.draw_text(upgrade, 30, x, y, (255, 255, 255))
        self.game.draw_text(desc, 30, x, y + 40, (255, 255, 255))

    def check_mouse(self):
        pos = pygame.mouse.get_pos()
        if self.up_1_rect.collidepoint(pos[0], pos[1]):
            self.state = 1
        if self.up_2_rect.collidepoint(pos[0], pos[1]):
            self.state = 2

    def check_input(self):
        if pygame.MOUSEMOTION:
            self.check_mouse()
        if self.game.SPACE_KEY:
            if self.state == 1:
                self.game.player.evo = 1
            else:
                self.game.player.evo = 2
            self.game.player.check_evo()
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
            if self.game.game_won:
                self.game.draw_text("YOU WIN", 60, self.game_overx, self.game_overy, (255, 255, 255))
            else:
                self.game.draw_text("GAME OVER", 60, self.game_overx, self.game_overy, (255, 255, 255))
            self.game.draw_text("Press space to return to main menu", 40, self.textx, self.texty, (255, 255, 255))
            self.game.draw_text(f"Level: {self.game.player.level}", 40, self.levelx, self.levely, (255, 255, 255))
            self.game.draw_text(f"Time survived: {int((self.game.game_time - self.game.start_time) / 1000)}s", 40, self.timerx, self.timery, (255, 255, 255))
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
            self.game.draw_text("Credits", 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20, (255, 255, 255))
            self.game.draw_text("Made by me", 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10, (255, 255, 255))
            self.blit_screen()
