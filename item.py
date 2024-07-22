import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, game, name):
        super().__init__(game.all_sprites_group, game.items_group)
        self.x = x
        self.y = y
        self.game = game
        self.name = name
        self.item_info = self.game.item_data[self.name]
        self.image = self.item_info["image"].convert_alpha()
        self.image_scale = self.item_info["size"]
        self.image = pygame.transform.rotozoom(self.image, 0, self.image_scale)
        self.rect = self.image.get_rect(center=(self.x, self.y))


class Coin(Item):
    def __init__(self, x, y, game):
        Item.__init__(self, x, y, game, "coin")

    def check_collision(self):
        if pygame.Rect.colliderect(self.rect, self.game.player.rect):
            self.kill()
            self.game.player.coins += 1

    def draw_item(self):
        self.game.display.blit(self.image, self.rect)

    def update(self):
        self.check_collision()
        self.draw_item()


class Heart(Item):
    def __init__(self, x, y, game):
        Item.__init__(self, x, y, game, "heart")

    def check_collision(self):
        if pygame.Rect.colliderect(self.rect, self.game.player.rect):
            self.kill()
            if self.game.player.health > (self.game.player.max_health - 20):
                self.game.player.health = self.game.player.max_health
            else:
                self.game.player.health += 20

    def draw_item(self):
        self.game.display.blit(self.image, self.rect)

    def update(self):
        self.check_collision()
        self.draw_item()
