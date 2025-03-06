import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, game, name):
        # upon creation, add to item and all sprites group
        super().__init__(game.all_sprites_group, game.items_group)
        self.x = x
        self.y = y
        self.game = game

        # get image from game settings
        self.name = name
        self.item_info = self.game.item_data[self.name]
        self.image = self.item_info["image"].convert_alpha()
        self.image_scale = self.item_info["size"]
        self.image = pygame.transform.rotozoom(self.image, 0, self.image_scale)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw_item(self):
        self.game.display.blit(self.image, self.rect)

    def update(self):
        self.check_collision()
        self.draw_item()


class Coin(Item):
    def __init__(self, x, y, game):
        Item.__init__(self, x, y, game, "coin")
        self.attract = False
        self.speed = self.game.player.player_speed

    def check_collision(self):
        # give player 5 coins
        if pygame.Rect.colliderect(self.rect, self.game.player.base_player_rect):
            self.kill()
            self.game.player.coins += 5

    def attract_to_player(self):
        # attracts to player when coin magnet grabbed, getting faster
        target_vector = pygame.math.Vector2(self.game.player.base_player_rect.center)
        target_vec_x = target_vector[0]
        target_vec_y = target_vector[1]
        target_vector = pygame.math.Vector2(target_vec_x, target_vec_y)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        distance = (target_vector - enemy_vector).magnitude()

        if distance > 0:
            direction = (target_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2()

        velocity = self.game.player.player_speed * 2 * direction
        self.rect.centerx += velocity.x
        self.rect.centery += velocity.y
        self.speed += 1

    def update(self):
        if self.attract:
            self.attract_to_player()
        self.check_collision()
        self.draw_item()


class Heart(Item):
    def __init__(self, x, y, game):
        Item.__init__(self, x, y, game, "heart")

    def check_collision(self):
        # heal player for up to 20 health
        if pygame.Rect.colliderect(self.rect, self.game.player.base_player_rect):
            self.kill()
            if self.game.player.health > (self.game.player.max_health - 20):
                self.game.player.health = self.game.player.max_health
            else:
                self.game.player.health += 20


class Doubler(Item):
    def __init__(self, x, y, game):
        Item.__init__(self, x, y, game, "doubler")

    def check_collision(self):
        # doubles the players coins
        if pygame.Rect.colliderect(self.rect, self.game.player.base_player_rect):
            self.kill()
            self.game.player.coins *= 2


class Magnet(Item):
    def __init__(self, x, y, game):
        Item.__init__(self, x, y, game, "magnet")

    def check_collision(self):
        # makes all coins attracted to player
        if pygame.Rect.colliderect(self.rect, self.game.player.base_player_rect):
            self.kill()
            for item in self.game.items_group:
                if item.name == "coin":
                    item.attract = True


class Power(Item):
    def __init__(self, x, y, game):
        Item.__init__(self, x, y, game, "power")

    def check_collision(self):
        # gives player unique powers based on class
        if pygame.Rect.colliderect(self.rect, self.game.player.base_player_rect):
            self.kill()
            self.game.player.power_player()


class Bomb(Item):
    def __init__(self, x, y, game):
        Item.__init__(self, x, y, game, "bomb")

    def check_collision(self):
        # damages and stuns all enemies
        if pygame.Rect.colliderect(self.rect, self.game.player.base_player_rect):
            self.kill()
            for enemy in self.game.enemy_group:
                enemy.health -= 50
                enemy.stun += 5

# need to make images
# class DoubleExp(Item):
#     def __init__(self, x, y, game):
#         Item.__init__(self, x, y, game, "exp")
#
#     def check_collision(self):
#         if pygame.Rect.colliderect(self.rect, self.game.player.base_player_rect):
#             self.kill()
#             self.game.player.double_exp()
#
#
# class Invincible(Item):
#     def __init__(self, x, y, game):
#         Item.__init__(self, x, y, game, "invincible")
#
#     def check_collision(self):
#         if pygame.Rect.colliderect(self.rect, self.game.player.base_player_rect):
#             self.kill()
#             self.game.player.invincible()
#
#
# class Speed(Item):
#     def __init__(self, x, y, game):
#         Item.__init__(self, x, y, game, "speed")
#
#     def check_collision(self):
#         if pygame.Rect.colliderect(self.rect, self.game.player.base_player_rect):
#             self.kill()
#             self.game.player.super_speed()