import pygame
from player import *
import random
from item import Magnet, Doubler, Power, Bomb


class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True

    def text_rect(self, x, y, width, height):
        # function for creating hitboxes for text
        rect = pygame.Rect(0, 0, width, height)
        rect.center = (x, y)
        return rect

    def draw_rect(self, x, y, width, height, colour, radius):
        # function for drawing rect easily
        rect = pygame.Rect(0, 0, width, height)
        rect.center = (x, y)
        pygame.draw.rect(self.game.display, colour, rect, radius)

    def blit_screen(self):
        # displays screen
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    # basic menu
    def __init__(self, game):
        Menu.__init__(self, game)
        # set start to be default option
        self.state = 'Start'
        # set placements for text and creates hitboxes
        self.startx, self.starty = self.mid_w, self.mid_h + 100
        self.start_rect = self.text_rect(self.startx, self.starty, 500, 40)

        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 150
        self.credits_rect = self.text_rect(self.creditsx, self.creditsy, 200, 40)

        # creates points to draw octagon
        self.pts = []
        for i in range(8):
            x = 640 + 100 * math.cos(math.pi * 2 * i / 8)
            y = 260 + 100 * math.sin(math.pi * 2 * i / 8)
            self.pts.append([int(x), int(y)])

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            # must check for player inputs
            self.game.check_events()
            self.check_input()

            # sets background colour as blue
            self.game.display.fill((40, 40, 100))

            # drawing text on screen
            self.game.draw_text("Welcome to Shape Survivors", 60, self.mid_w, self.mid_h - 200, (255, 255, 255))
            # draws text yellow if selected, otherwise white
            if self.state == 'Start':
                self.game.draw_text("Start Game", 40, self.startx, self.starty, (255, 255, 0))
                self.game.draw_text("Credits", 30, self.creditsx, self.creditsy, (255, 255, 255))
            else:
                self.game.draw_text("Start Game", 40, self.startx, self.starty, (255, 255, 255))
                self.game.draw_text("Credits", 30, self.creditsx, self.creditsy, (255, 255, 0))

            self.game.draw_text("Controls:", 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 200, (255, 255, 255))
            self.game.draw_text("Aim: L-Mouse     Confirm: Space     Move: wasd     Upgrade: R-Mouse", 20, self.mid_w,
                                self.mid_h + 250, (255, 255, 255))

            # draws red octagon
            pygame.draw.polygon(self.game.display, (255, 0, 0), self.pts)

            # displays screen
            self.blit_screen()

    def check_mouse(self):
        # function for checking if mouse is touching buttons
        pos = pygame.mouse.get_pos()
        if self.start_rect.collidepoint(pos[0], pos[1]):
            self.state = 'Start'
        if self.credits_rect.collidepoint(pos[0], pos[1]):
            self.state = 'Credits'

    def check_input(self):
        # checks for mouse movement and option confirmation
        if pygame.MOUSEMOTION:
            self.check_mouse()
        if self.game.SPACE_KEY:
            if self.state == 'Start':
                self.game.curr_menu = self.game.class_select
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            self.run_display = False


class NewMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        # no options are highlighted by default
        self.state = None

        # set locations for text, hitboxes, and sets health
        self.titlex, self.titley = self.game.DISPLAY_W / 2, 100
        self.startx, self.starty = self.game.DISPLAY_W / 4, self.game.DISPLAY_H / 3
        self.start_rect = self.text_rect(self.startx, self.starty, 250, 35)
        self.start_health = 100

        self.controlx, self.controly = self.game.DISPLAY_W * 3 / 4, self.game.DISPLAY_H / 3
        self.control_rect = self.text_rect(self.controlx, self.controly, 190, 35)
        self.control_health = 100

        self.creditx, self.credity = self.game.DISPLAY_W / 4, self.game.DISPLAY_H * 4 / 5
        self.credit_rect = self.text_rect(self.creditx, self.credity, 150, 35)
        self.credit_health = 100

        self.classx, self.classy = self.game.DISPLAY_W * 3 / 4, self.game.DISPLAY_H * 4 / 5
        self.class_rect = self.text_rect(self.classx, self.classy, 250, 35)
        self.class_health = 100

        # creates gunner as default player
        self.game.player_class = 'Gunner'
        self.game.player = Gunner(self.game)

    def display_menu(self):
        # when returning to main menu, must reset health of options
        self.reset_health()
        self.run_display = True

        # need to reset player when returning to menu
        if self.game.player_class == 'Gunner':
            self.game.player.kill()
            self.game.player = Gunner(self.game)
        elif self.game.player_class == 'Sniper':
            self.game.player.kill()
            self.game.player = Sniper(self.game)
        if self.game.player_class == 'Wizard':
            self.game.player.kill()
            self.game.player = Wizard(self.game)
        if self.game.player_class == 'Crossbow':
            self.game.player.kill()
            self.game.player = Crossbow(self.game)
        self.game.player.reset_player()

        while self.run_display:
            # need to check for button presses
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 100, 0))
            self.game.draw_text("Welcome to Shape Survivors", 60, self.titlex, self.titley, (255, 255, 255))

            self.game.all_sprites_group.update() # need to update player and bullet sprites

            # draw health of options
            self.draw_rect(self.startx, self.starty + 30, self.start_health, 20, (0, 255, 0), 10)
            self.draw_rect(self.startx, self.starty + 30, 100, 20, (0, 0, 0), 3)

            self.draw_rect(self.controlx, self.controly + 30, self.control_health, 20, (0, 255, 0), 10)
            self.draw_rect(self.controlx, self.controly + 30, 100, 20, (0, 0, 0), 3)

            self.draw_rect(self.creditx, self.credity + 30, self.credit_health, 20, (0, 255, 0), 10)
            self.draw_rect(self.creditx, self.credity + 30, 100, 20, (0, 0, 0), 3)

            self.draw_rect(self.classx, self.classy + 30, self.class_health, 20, (0, 255, 0), 10)
            self.draw_rect(self.classx, self.classy + 30, 100, 20, (0, 0, 0), 3)

            # highlights text when mouse is touching it
            if self.state == 'Start':
                self.game.draw_text("Start Game", 40, self.startx, self.starty, (255, 255, 0))
                self.game.draw_text("Controls", 40, self.controlx, self.controly, (255, 255, 255))
                self.game.draw_text("Credits", 40, self.creditx, self.credity, (255, 255, 255))
                self.game.draw_text("Class select", 40, self.classx, self.classy, (255, 255, 255))
            elif self.state == 'Controls':
                self.game.draw_text("Start Game", 40, self.startx, self.starty, (255, 255, 255))
                self.game.draw_text("Controls", 40, self.controlx, self.controly, (255, 255, 0))
                self.game.draw_text("Credits", 40, self.creditx, self.credity, (255, 255, 255))
                self.game.draw_text("Class select", 40, self.classx, self.classy, (255, 255, 255))
            elif self.state == 'Credits':
                self.game.draw_text("Start Game", 40, self.startx, self.starty, (255, 255, 255))
                self.game.draw_text("Controls", 40, self.controlx, self.controly, (255, 255, 255))
                self.game.draw_text("Credits", 40, self.creditx, self.credity, (255, 255, 0))
                self.game.draw_text("Class select", 40, self.classx, self.classy, (255, 255, 255))
            elif self.state == 'Class':
                self.game.draw_text("Start Game", 40, self.startx, self.starty, (255, 255, 255))
                self.game.draw_text("Controls", 40, self.controlx, self.controly, (255, 255, 255))
                self.game.draw_text("Credits", 40, self.creditx, self.credity, (255, 255, 255))
                self.game.draw_text("Class select", 40, self.classx, self.classy, (255, 255, 0))
            else:
                self.game.draw_text("Start Game", 40, self.startx, self.starty, (255, 255, 255))
                self.game.draw_text("Controls", 40, self.controlx, self.controly, (255, 255, 255))
                self.game.draw_text("Credits", 40, self.creditx, self.credity, (255, 255, 255))
                self.game.draw_text("Class select", 40, self.classx, self.classy, (255, 255, 255))
            self.blit_screen()

        # by setting this to None once the menu is no longer being displayed, all options will be white when returning
        self.state = None

    def reset_health(self):
        # reset health of all options
        self.start_health = 100
        self.control_health = 100
        self.credit_health = 100
        self.class_health = 100

    def check_mouse(self):
        # check if mouse is over an option
        pos = pygame.mouse.get_pos()
        if self.start_rect.collidepoint(pos[0], pos[1]):
            self.state = 'Start'
        if self.control_rect.collidepoint(pos[0], pos[1]):
            self.state = 'Controls'
        if self.credit_rect.collidepoint(pos[0], pos[1]):
            self.state = 'Credits'
        if self.class_rect.collidepoint(pos[0], pos[1]):
            self.state = 'Class'

    def check_health(self):
        # for each bullet, check if it collides with hitbox and deals damage
        # also need to check if hitbox is killed, same as selecting that option
        for bullet in self.game.bullet_group:
            if self.start_rect.colliderect(bullet.rect):
                self.start_health -= self.game.player.damage
                bullet.kill()
                if self.start_health <= 0:
                    self.game.start_game()
                    self.run_display = False
            elif self.control_rect.colliderect(bullet.rect):
                self.control_health -= self.game.player.damage
                bullet.kill()
                if self.control_health <= 0:
                    self.game.curr_menu = self.game.controls
                    self.run_display = False
            elif self.credit_rect.colliderect(bullet.rect):
                self.credit_health -= self.game.player.damage
                bullet.kill()
                if self.credit_health <= 0:
                    self.game.curr_menu = self.game.credits
                    self.run_display = False
            elif self.class_rect.colliderect(bullet.rect):
                self.class_health -= self.game.player.damage
                bullet.kill()
                if self.class_health <= 0:
                    self.game.curr_menu = self.game.class_select
                    self.run_display = False

    def check_input(self):
        # checks for mouse and keyboard inputs
        self.check_health()
        if pygame.MOUSEMOTION:
            self.check_mouse()
        if pygame.MOUSEBUTTONDOWN:
            self.game.player.is_shooting()
        if self.game.SPACE_KEY:
            if self.state == 'Start':
                self.game.start_game()
                # self.game.curr_menu = self.game.class_select
            elif self.state == 'Controls':
                self.game.curr_menu = self.game.controls
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            elif self.state == 'Class':
                self.game.curr_menu = self.game.class_select
            self.run_display = False


class ControlsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        # set positions for text
        self.controlx, self.controly = self.game.DISPLAY_W / 2, 100
        self.upx, self.upy = self.game.DISPLAY_W / 4 - 90, self.game.DISPLAY_H / 3 + 35
        self.downx, self.downy = self.game.DISPLAY_W / 4 - 90, self.game.DISPLAY_H / 3 + 70
        self.leftx, self.lefty = self.game.DISPLAY_W / 4 + 90, self.game.DISPLAY_H / 3 + 35
        self.rightx, self.righty = self.game.DISPLAY_W / 4 + 90, self.game.DISPLAY_H / 3 + 70
        self.movex, self.movey = self.game.DISPLAY_W / 4, self.game.DISPLAY_H / 3

        self.mousex, self.mousey = self.game.DISPLAY_W * 3 / 4, self.game.DISPLAY_H / 3
        self.shootx, self.shooty = self.game.DISPLAY_W * 3 / 4, self.game.DISPLAY_H / 3 + 35
        self.upgradex, self.upgradey = self.game.DISPLAY_W * 3 / 4, self.game.DISPLAY_H / 3 + 70

        self.menux, self.menuy = self.game.DISPLAY_W / 2, self.game.DISPLAY_H * 3 / 4
        self.confirmx, self.confirmy = self.game.DISPLAY_W / 2, self.game.DISPLAY_H * 3 / 4 + 35
        self.returnx, self.returny = self.game.DISPLAY_W / 2, self.game.DISPLAY_H * 3 / 4 + 70

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            # must check if player has pressed backspace to return to main menu
            self.game.check_events()
            self.check_input()
            self.game.display.fill((40, 40, 100))

            # text for movement
            self.game.draw_text("Controls:", 60, self.controlx, self.controly, (255, 255, 255))
            self.game.draw_text("Up: W", 40, self.upx, self.upy, (255, 255, 255))
            self.game.draw_text("Down: S", 40, self.downx, self.downy, (255, 255, 255))
            self.game.draw_text("Left: A", 40, self.leftx, self.lefty, (255, 255, 255))
            self.game.draw_text("Right: D", 40, self.rightx, self.righty, (255, 255, 255))
            self.game.draw_text("Movement", 40, self.movex, self.movey, (255, 255, 255))
            self.draw_rect(self.movex, self.movey + 35, 450, 150, (255, 255, 255), 5)

            # text for mouse
            self.game.draw_text("Mouse", 40, self.mousex, self.mousey, (255, 255, 255))
            self.game.draw_text("Shoot: Left Click", 40, self.shootx, self.shooty, (255, 255, 255))
            self.game.draw_text("Upgrade: Right Click", 40, self.upgradex, self.upgradey, (255, 255, 255))
            self.draw_rect(self.mousex, self.mousey + 35, 450, 150, (255, 255, 255), 5)

            # text for menus
            self.game.draw_text("Menus", 40, self.menux, self.menuy, (255, 255, 255))
            self.game.draw_text("Confirm: Space", 40, self.confirmx, self.confirmy, (255, 255, 255))
            self.game.draw_text("Return: Backspace", 40, self.returnx, self.returny, (255, 255, 255))
            self.draw_rect(self.menux, self.menuy + 35, 450, 150, (255, 255, 255), 5)
            self.blit_screen()

    def check_input(self):
        # check is backspace has been pressed
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False


class ClassMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        # gunner is selected by default
        self.state = 'Gunner'

        # set positions for text and hitboxes
        self.textx, self.texty = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 8
        self.gunx, self.guny = self.game.DISPLAY_W * 3 / 10, self.game.DISPLAY_H * 2 / 5
        self.gun_rect = self.text_rect(self.gunx, self.guny, 500, 200)
        self.wizx, self.wizy = self.game.DISPLAY_W * 3 / 10, self.game.DISPLAY_H * 4 / 5 - 28
        self.wiz_rect = self.text_rect(self.wizx, self.wizy, 500, 200)
        self.sniperx, self.snipery = self.game.DISPLAY_W * 7 / 10, self.game.DISPLAY_H * 2 / 5
        self.sniper_rect = self.text_rect(self.sniperx, self.snipery, 500, 200)
        self.crossx, self.crossy = self.game.DISPLAY_W * 7 / 10, self.game.DISPLAY_H * 4 / 5 - 28
        self.cross_rect = self.text_rect(self.crossx, self.crossy, 500, 200)

        self.returnx, self.returny = self.game.DISPLAY_W / 6, self.game.DISPLAY_H / 8
        self.confirmx, self.confirmy = self.game.DISPLAY_W * 5 / 6, self.game.DISPLAY_H / 8

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            # need to check for class selection and confirmation
            self.game.check_events()
            self.check_input()
            self.game.display.fill((40, 40, 100))
            self.game.draw_text("Class Select", 50, self.textx, self.texty, (255, 255, 255))
            self.game.draw_text("Return: Backspace", 30, self.returnx, self.returny, (255, 255, 255))
            self.game.draw_text("Confirm: Space", 30, self.confirmx, self.confirmy, (255, 255, 255))

            # display all four classes
            self.display_class("Gunner", self.gunx, self.guny)
            self.display_class("Wizard", self.wizx, self.wizy)
            self.display_class("Sniper", self.sniperx, self.snipery)
            self.display_class("Crossbow", self.crossx, self.crossy)
            self.blit_screen()

    def display_class(self, name, x, y):
        # function for displaying classes
        # yellow rectangle is drawn if selected, otherwise white
        if self.state == name:
            self.draw_rect(x, y, 500, 200, (255, 255, 0), 5)
        else:
            self.draw_rect(x, y, 500, 200, (255, 255, 255), 5)

        # retrieve class information from settings
        info = self.game.player_data[name]
        image = info["player_img"].convert_alpha()
        # must scale image before displaying it
        image = pygame.transform.rotozoom(image, 0, info["player_size"])
        # place image in specific position in rectangle
        img_rect = image.get_rect(center=(x + 120, y + 50))

        # displays class information, showing which class player is currently
        if self.game.player.name == name:
            self.game.draw_text(f"{name} (current)", 40, x, y - 60, (255, 255, 255))
        else:
            self.game.draw_text(f"{name}", 40, x, y - 60, (255, 255, 255))
        self.game.draw_text(f'Health: {info["health"]}', 30, x - 120, y - 30, (255, 255, 255))
        self.game.draw_text(f'Damage: {info["damage"]}', 30, x + 120, y - 30, (255, 255, 255))
        self.game.draw_text(f'Speed: {info["speed"]}', 30, x - 120, y, (255, 255, 255))
        self.game.draw_text(f'Cooldown: {info["cooldown"]}', 30, x - 120, y + 30, (255, 255, 255))
        self.game.draw_text(f'Bullet speed: {info["bullet_speed"]}', 30, x + 110, y, (255, 255, 255))
        self.game.draw_text(f'Pierce: {info["pierce"]}', 30, x - 120, y + 60, (255, 255, 255))
        self.game.display.blit(image, img_rect)

    def check_mouse(self):
        # check if mouse is selecting class
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
        # check mouse and keyboard inputs
        if pygame.MOUSEMOTION:
            self.check_mouse()
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        if self.game.SPACE_KEY:
            # need to spawn in new class in current position while removing current class
            pos = self.game.player.base_player_rect.center
            self.game.player.kill()
            if self.state == 'Gunner':
                self.game.player_class = 'Gunner'
                self.game.player = Gunner(self.game)
            elif self.state == 'Wizard':
                self.game.player_class = 'Wizard'
                self.game.player = Wizard(self.game)
            elif self.state == 'Sniper':
                self.game.player_class = 'Sniper'
                self.game.player = Sniper(self.game)
            elif self.state == 'Crossbow':
                self.game.player_class = 'Crossbow'
                self.game.player = Crossbow(self.game)
            self.game.player.base_player_rect.center = pos
            self.game.curr_menu = self.game.main_menu
            self.run_display = False


class LevelMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        # damage upgrade is selected by default
        self.state = 'Damage'

        # set postions for upgrades and hitboxes
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

        # set positions for shop items and hitboxes
        self.itemx, self.itemy = 1200, 50
        self.lifex, self.lifey = 1100, 300
        self.life_rect = self.text_rect(self.lifex, self.lifey, 300, 50)
        self.killx, self.killy = 1100, 400
        self.kill_rect = self.text_rect(self.killx, self.killy, 300, 50)
        self.dropx, self.dropy = 1100, 500
        self.drop_rect = self.text_rect(self.dropx, self.dropy, 300, 50)
        # self.winx, self.winy = 1100, 500
        # self.win_rect = self.text_rect(self.winx, self.winy, 300, 50)
        self.item_data = self.game.item_data

    def display_menu(self):
        self.run_display = True
        info = self.game.player_data[self.game.player_class]
        # retrieve class specific upgrades
        self.up_1 = info["up_1"]
        self.up_2 = info["up_2"]
        self.up_3 = info["up_3"]
        self.up_4 = info["up_4"]
        while self.run_display:
            # check for upgrade selection and confirmation
            self.game.check_events()
            self.check_input()
            self.game.display.fill((40, 40, 100))
            self.game.draw_text("Select upgrade, space to confirm", 50, self.levelx, self.levely, (255, 255, 255))

            # shows remaining levels to spend
            self.game.draw_text(f"Levels remaining: {self.game.player.saved_levels}", 40, self.levelx, self.levely + 50, (255, 255, 255))

            # displays upgrades
            self.draw_level("Health", self.healthx, self.healthy)
            self.draw_level("Speed", self.speedx, self.speedy)
            self.draw_level(self.up_1, self.up_1x, self.up_1y)
            self.draw_level(self.up_2, self.up_2x, self.up_2y)
            self.draw_level(self.up_3, self.up_3x, self.up_3y)
            self.draw_level(self.up_4, self.up_4x, self.up_4y)

            # draw shop with pictures and costs
            self.draw_item("coin", self.itemx - 40, self.itemy)
            self.draw_level("Extra Life", self.lifex, self.lifey)
            self.draw_level("Clear screen", self.killx, self.killy)
            self.draw_level("Random drop", self.dropx, self.dropy)
            self.game.draw_text(f"{self.game.player.coins}", 40, self.itemx, self.itemy, (255, 255, 255))
            self.draw_item("heart", self.itemx - 40, self.itemy + 40)
            self.game.draw_text(f"{self.game.player.lives}", 40, self.itemx, self.itemy + 40, (255, 255, 255))
            self.game.draw_text("10", 30, self.lifex, self.lifey + 50, (255, 255, 0))
            self.game.draw_text("20", 30, self.killx, self.killy + 50, (255, 255, 0))
            self.game.draw_text("40", 30, self.dropx, self.dropy + 50, (255, 255, 0))
            self.game.draw_text("Shop", 50, 1100, 250, (255, 255, 255))

            # draw rectangle around shop
            rect = pygame.Rect(900, 200, (self.game.DISPLAY_W-900), (self.game.DISPLAY_H-200))
            pygame.draw.rect(self.game.display, (255, 255, 255), rect, 5)
            self.blit_screen()

    def draw_item(self, name, x, y):
        # function for drawing items
        info = self.item_data[name]
        image = info["image"].convert_alpha()
        image_rect = image.get_rect(center=(x, y))
        self.game.display.blit(image, image_rect)

    def draw_level(self, name, x, y):
        # function for drawing levels with yellow rectangle if selected, otherwise white
        self.game.draw_text(f"{name}", 40, x, y, (255, 255, 255))
        if self.state == name:
            self.draw_rect(x, y, 300, 50, (255, 255, 0), 5)
        else:
            self.draw_rect(x, y, 300, 50, (255, 255, 255), 5)

    def check_mouse(self):
        # check mouse position to see what has been selected
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
        if self.drop_rect.collidepoint(current_pos[0], current_pos[1]):
            self.state = 'Random drop'

    def check_input(self):
        # checks for mouse and keyboard inputs
        if pygame.MOUSEMOTION:
            self.check_mouse()
        if self.game.START_KEY or self.game.SPACE_KEY:
            # checks if shop items have been bought
            if self.state == 'Extra Life':  # gives extra life
                if self.game.player.coins >= 10:
                    self.game.player.lives += 1
                    self.game.player.coins -= 10
            elif self.state == 'Clear screen':  # kills all enemies
                if self.game.player.coins >= 20:
                    for shape in self.game.enemy_group:
                        shape.kill()
                    self.game.enemy_group.empty()
                    self.game.player.coins -= 20
            elif self.state == 'Random drop':  # spawns random item
                if self.game.player.coins >= 40:
                    num = random.randint(0, 3)
                    match num:
                        case num if num == 0:
                            Doubler(self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2, self.game)
                        case num if num == 1:
                            Magnet(self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2, self.game)
                        case num if num == 2:
                            Power(self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2, self.game)
                        case num if num == 3:
                            Bomb(self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2, self.game)
                    self.game.player.coins -= 40
            # elif self.state == 'Win game':
            #     if self.game.player.coins >= 100:
            #         self.game.game_won = True
            #         self.run_display = False
            #         self.game.ready_to_spawn = False
            #         self.game.curr_menu = self.game.end_menu
            #         self.game.game_time = pygame.time.get_ticks()
            #         self.game.reset_game()
            else:
                # checks which upgrade has been selected
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
                # checks if all levels have been spent and returns to game
                if self.game.player.saved_levels == 0:
                    self.game.playing = True
                    self.game.ready_to_spawn = True
                    self.run_display = False
                self.game.player.level += 1  # add 1 to player level


class EvoScreen(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        # set positions and hitboxes for evolutions
        self.evox, self.evoy = self.mid_w, self.game.DISPLAY_H / 6
        self.up_1x, self.up_1y = self.mid_w - 270, self.mid_h
        self.up_1_rect = self.text_rect(self.up_1x, self.up_1y, 500, 200)
        self.up_2x, self.up_2y = self.mid_w + 270, self.mid_h
        self.up_2_rect = self.text_rect(self.up_2x, self.up_2y, 500, 200)

    def display_menu(self):
        info = self.game.player_data[self.game.player_class]
        # evolution 1 is selected by default
        self.state = info["evo_1"]
        self.run_display = True
        while self.run_display:
            # checks for player inputs
            self.game.check_events()
            self.check_input()
            self.game.display.fill((40, 40, 100))
            self.game.draw_text("Select Evolution", 50, self.evox, self.evoy, (255, 255, 255))
            self.game.draw_text(f"{self.game.player_class} evolutions", 40, self.evox, self.evoy + 50, (255, 255, 255))

            # displays evolutions using function
            self.display_evo(1, info["evo_1"], info["desc_1"], self.up_1x, self.up_1y)
            self.display_evo(2, info["evo_2"], info["desc_2"], self.up_2x, self.up_2y)
            self.blit_screen()

    def display_evo(self, state, upgrade, desc, x, y):
        # displays yellow rectangle if evolution is selected, otherwise white
        if self.state == state:
            self.draw_rect(x, y, 500, 200, (255, 255, 0), 5)
        else:
            self.draw_rect(x, y, 500, 200, (255, 255, 255), 5)
        # draws text for upgrade and its description
        self.game.draw_text(upgrade, 30, x, y, (255, 255, 255))
        self.game.draw_text(desc, 30, x, y + 40, (255, 255, 255))

    def check_mouse(self):
        # checks if mouse is hovering over option
        pos = pygame.mouse.get_pos()
        if self.up_1_rect.collidepoint(pos[0], pos[1]):
            self.state = 1
        if self.up_2_rect.collidepoint(pos[0], pos[1]):
            self.state = 2

    def spawn_evo(self, evo):
        # selects correct evolution, copying current stats
        player_class = self.game.player_class
        match player_class:
            case player_class if player_class == 'Gunner':
                if evo == 1:
                    new_player = DualGunner(self.game)
                else:
                    new_player = Shotgun(self.game)
                self.copy_gunner(self.game.player, new_player)
            case player_class if player_class == 'Sniper':
                if evo == 1:
                    new_player = CoverFire(self.game)
                else:
                    new_player = GrenadeLauncher(self.game)
                self.copy_sniper(self.game.player, new_player)
            case player_class if player_class == 'Wizard':
                if evo == 1:
                    new_player = FireWizard(self.game)
                else:
                    new_player = EWizard(self.game)
                self.copy_wizard(self.game.player, new_player)
            case player_class if player_class == 'Crossbow':
                if evo == 1:
                    new_player = TripleShot(self.game)
                else:
                    new_player = MagicBag(self.game)
                self.copy_crossbow(self.game.player, new_player)
        self.copy_player(self.game.player, new_player)
        self.game.player.kill()
        self.game.player = new_player

    def copy_player(self, current, new):
        # copies current stats to evolution
        new.max_health = current.max_health
        new.health = current.health
        new.player_speed = current.player_speed
        new.vec_pos = current.vec_pos
        new.shoot_cooldown = current.shoot_cooldown
        new.experience = current.experience
        new.level = current.level
        new.exp_cap = current.exp_cap
        new.coins = current.coins
        new.lives = current.lives
        new.not_powered = current.not_powered
        new.evo = current.evo

    def copy_gunner(self, current, new):
        # copies unique stats for gunner class
        new.fire_delay = current.fire_delay
        new.bullet_speed = current.bullet_speed
        new.knockback = current.knockback
        new.level_scale = current.level_scale

    def copy_sniper(self, current, new):
        # copies unique stats for sniper class
        new.damage = current.damage
        new.bullet_pierce = current.bullet_pierce
        new.bullet_scale = current.bullet_scale
        new.knockback = current.knockback

    def copy_wizard(self, current, new):
        # copies unique stats for wizard class
        new.damage = current.damage
        new.bullet_scale = current.bullet_scale
        new.stun = current.stun
        new.effect_mult = current.effect_mult

    def copy_crossbow(self, current, new):
        # copies unique stats for crossbow class
        new.bullet_pierce = current.bullet_pierce
        new.bullet_speed = current.bullet_speed
        new.stun = current.stun
        new.effect_mult = current.effect_mult

    def check_input(self):
        # checks for mouse and keyboard inputs
        if pygame.MOUSEMOTION:
            self.check_mouse()
        if self.game.SPACE_KEY:
            if self.state == 1:
                self.game.player.evo = 1
            else:
                self.game.player.evo = 2
            self.spawn_evo(self.game.player.evo)
            self.game.playing = True
            self.game.ready_to_spawn = True
            self.run_display = False


class EndScreen(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        # set positions for text
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

            # displays message based on whether player has won or lost
            if self.game.game_won:
                self.game.draw_text("YOU WIN", 60, self.game_overx, self.game_overy, (255, 255, 255))
            else:
                self.game.draw_text("GAME OVER", 60, self.game_overx, self.game_overy, (255, 255, 255))

            # displays stats for game played
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
            # check if player returns to main menu
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False

            # displays credits
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("Credits", 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20, (255, 255, 255))
            self.game.draw_text("Made by me", 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10, (255, 255, 255))
            self.blit_screen()


class PauseMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.pausex, self.pausey = self.mid_w, self.mid_h

        # must keep track of how long game is paused for to accurately display game time
        self.time_paused = 0

    def display_menu(self):
        self.run_display = True

        # must stop new shapes from spawning when paused
        self.game.ready_to_spawn = False

        # find exact time game is paused
        self.pause_time = pygame.time.get_ticks()

        while self.run_display:
            # need to check for player to resume game
            self.game.check_events()
            self.check_input()
            self.game.draw_text("Paused", 150, self.pausex, self.pausey, (255, 20, 0))
            self.game.draw_text("Press p to resume", 100, self.pausex, self.pausey + 150, (255, 20, 0))
            self.blit_screen()

    def check_input(self):
        # only input that matters is unpausing the game by pressing p
        if self.game.PAUSE_KEY:
            # can calculate how long game has been paused for if we know when it was paused and unpaused
            resume_time = pygame.time.get_ticks()
            # add to total time paused
            self.time_paused += int((resume_time - self.pause_time) / 1000)

            self.game.ready_to_spawn = True
            self.run_display = False
            self.game.playing = True
