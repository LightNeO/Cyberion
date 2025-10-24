import pygame
from hero import Hero
from flying_enemy import FlyingEnemy
from turret_enemy import TurretEnemy
from background import Background
from pytmx.util_pygame import load_pygame
from tile import Tile
from coin import Coin
from shop import Shop
from shop_menu import ShopMenu
from ui import UI
from camera import Camera
import config as Config


class BaseLevel:
    def __init__(self, displaySurface, tmx_path):
        self.displaySurface = displaySurface
        self.level_data = load_pygame(tmx_path, force_reload=True)

        # Sprite groups
        self.visible_sprites = Camera()
        self.hero = pygame.sprite.GroupSingle()
        self.flying_enemies = pygame.sprite.Group()
        self.turret_enemies = pygame.sprite.Group()
        self.platform_tiles = pygame.sprite.Group()
        self.foreground_tiles = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.shops = pygame.sprite.Group()
        self.shop_menus = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.next_level_triggers = pygame.sprite.Group()
        self.quit_triggers = pygame.sprite.Group()
        self.background_tiles = []

        # Level setup
        self._setup_layers()
        self._setup_objects()
        self._setup_player()
        self._setup_enemies()

        # BG and UI
        self.background = Background()
        self.ui = UI(self.displaySurface)

        # Some attributes
        self.coin_count = 0
        self.is_shop_menu_opened = False
        self.last_key_press_time = 0
        self.key_cooldown = 200
        self.quit = False

    def _setup_layers(self):
        # Foreground
        layer_foreground = self.level_data.get_layer_by_name("Foreground")
        for x, y, tile_surface in layer_foreground.tiles():
            tile = Tile((x * Config.TILESIZE, y * Config.TILESIZE), tile_surface)
            self.foreground_tiles.add(tile)
            self.visible_sprites.add(tile)

        # Backgrounds
        for bg_name in ["Background4", "Background3", "Background2", "Background1"]:
            try:
                bg_group = pygame.sprite.Group()
                layer_bg = self.level_data.get_layer_by_name(bg_name)
                for x, y, tile_surface in layer_bg.tiles():
                    tile = Tile(
                        (x * Config.TILESIZE, y * Config.TILESIZE), tile_surface
                    )
                    bg_group.add(tile)
                    self.visible_sprites.add(tile)
                self.background_tiles.append(bg_group)
            except ValueError:
                print(f"'{bg_name}' layer not found in TMX file, skipping.")

        # Platforms
        layer_platforms = self.level_data.get_layer_by_name("Platforms")
        for x, y, tile_surface in layer_platforms.tiles():
            tile = Tile((x * Config.TILESIZE, y * Config.TILESIZE), tile_surface)
            self.platform_tiles.add(tile)
            self.visible_sprites.add(tile)

    def _setup_objects(self):
        try:
            object_layer = self.level_data.get_layer_by_name("Objects")
            for obj in object_layer:
                if obj.name == "Coin":
                    coin = Coin((obj.x, obj.y), obj.image)
                    self.coins.add(coin)
                    self.visible_sprites.add(coin)
                elif obj.name in ["Open1", "Open2", "Open3"]:
                    shop = Shop((obj.x, obj.y), obj.image)
                    self.shops.add(shop)
                    self.visible_sprites.add(shop)
                elif obj.name == "NextLvl":
                    trigger = pygame.sprite.Sprite()
                    trigger.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    self.next_level_triggers.add(trigger)
                elif obj.name == "Quit":
                    trigger = pygame.sprite.Sprite()
                    trigger.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    self.quit_triggers.add(trigger)
        except ValueError:
            print("'Objects' layer not found in TMX file")

    def _setup_player(self):
        raise NotImplementedError("Need to define this method in specific llvl class")

    def _setup_enemies(self):
        raise NotImplementedError("Need to define this method in specific llvl class")
        pass

    def update(self):
        self.hero.update(self)
        self.flying_enemies.update(self)
        self.turret_enemies.update(self)
        self.bullets.update(self)
        self.check_coin_collisions()
        self.check_shop_collision()

        if self.check_next_lvl_collision():
            return True  # Change lvl

        if self.check_quit_collision():
            self.quit = True

        # Remove dead enemies
        for enemy in self.flying_enemies.copy():
            if not enemy.alive:
                self.flying_enemies.remove(enemy)
                self.visible_sprites.remove(enemy)
        
        for enemy in self.turret_enemies.copy():
            if not enemy.alive:
                self.turret_enemies.remove(enemy)
                self.visible_sprites.remove(enemy)

        # Bullet collisions
        for bullet in self.bullets.copy():
            if bullet.bullet_type == "hero":
                # Hero bullets hitting enemies
                flying_hits = pygame.sprite.spritecollide(bullet, self.flying_enemies, False)
                if flying_hits:
                    bullet.kill()
                    for enemy in flying_hits:
                        if enemy.alive and not enemy.is_dying:
                            enemy.die()
                
                turret_hits = pygame.sprite.spritecollide(bullet, self.turret_enemies, False)
                if turret_hits:
                    bullet.kill()
                    for enemy in turret_hits:
                        if enemy.alive and not enemy.is_dying:
                            enemy.die()

    def check_coin_collisions(self):
        collided_coins = pygame.sprite.spritecollide(self.hero.sprite, self.coins, True)
        if collided_coins:
            self.coin_count += len(collided_coins)

    def check_shop_collision(self):
        collided_shop = pygame.sprite.spritecollide(self.hero.sprite, self.shops, False)
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if collided_shop:
            if keys[pygame.K_e] and not self.is_shop_menu_opened:
                if current_time - self.last_key_press_time > self.key_cooldown:
                    self.last_key_press_time = current_time
                    self.open_shop_menu()
            elif keys[pygame.K_q] and self.is_shop_menu_opened:
                if current_time - self.last_key_press_time > self.key_cooldown:
                    self.last_key_press_time = current_time
                    self.close_shop_menu()
            elif self.is_shop_menu_opened:
                if keys[pygame.K_1] and self.coin_count >= 11 and Hero.get_hp() < 5:
                    if current_time - self.last_key_press_time > self.key_cooldown:
                        self.last_key_press_time = current_time
                        self.coin_count -= 11
                        Hero.change_hp(1)
                elif keys[pygame.K_2] and self.coin_count >= 1:
                    if current_time - self.last_key_press_time > self.key_cooldown:
                        self.last_key_press_time = current_time
                        self.coin_count -= 1
                        Hero.change_bullets(1)

    def open_shop_menu(self):
        try:
            object_layer = self.level_data.get_layer_by_name("Objects")
            for obj in object_layer:
                if obj.name == "ShopMenu":
                    shop_menu = ShopMenu((obj.x, obj.y), obj.image)
                    self.shop_menus.add(shop_menu)
                    self.visible_sprites.add(shop_menu)
            self.is_shop_menu_opened = True
        except ValueError:
            print("'ShopMenu' object not found in TMX file")

    def close_shop_menu(self):
        for menu in self.shop_menus:
            menu.kill()
        self.is_shop_menu_opened = False

    def check_next_lvl_collision(self):
        if pygame.sprite.spritecollide(
            self.hero.sprite, self.next_level_triggers, False
        ):
            return True
        return False

    def check_quit_collision(self):
        if pygame.sprite.spritecollide(
            self.hero.sprite, self.quit_triggers, False
        ):
            print("QUIT")
            return True
        return False

    def draw(self):
        self.background.draw(self.displaySurface)
        self.visible_sprites.custom_draw(self.hero.sprite, self.level_data)
        self.ui.show_coins(self.coin_count)
        self.ui.show_hp(Hero.get_hp())
        self.ui.show_bullets(Hero.get_bullets())

    def run(self):
        should_change_level = self.update()
        self.draw()
        return should_change_level


class Level0(BaseLevel):
    def __init__(self, displaySurface):
        tmx_path = Config.LEVELS_PATH + "level_0/level.tmx"
        super().__init__(displaySurface, tmx_path)

    def _setup_player(self):
        hero_sprite = Hero((500, 300), face_right=True)
        self.hero.add(hero_sprite)
        self.visible_sprites.add(hero_sprite)

    def _setup_enemies(self):
        pass


class Level1(BaseLevel):
    def __init__(self, displaySurface):
        tmx_path = Config.LEVELS_PATH + "level_1/level.tmx"
        super().__init__(displaySurface, tmx_path)

    def _setup_player(self):
        hero_sprite = Hero((50, 50), face_right=True)
        self.hero.add(hero_sprite)
        self.visible_sprites.add(hero_sprite)

    def _setup_enemies(self):
        enemy1 = FlyingEnemy((200, 200), 200, move_right=True)
        self.flying_enemies.add(enemy1)
        self.visible_sprites.add(enemy1)

        enemy2 = FlyingEnemy((800, 400), 500, move_right=True)
        self.flying_enemies.add(enemy2)
        self.visible_sprites.add(enemy2)

        turret1 = TurretEnemy((400, 464), 0, False)
        self.turret_enemies.add(turret1)
        self.visible_sprites.add(turret1)


class Level2(BaseLevel):
    def __init__(self, displaySurface):
        tmx_path = Config.LEVELS_PATH + "level_2/level.tmx"
        super().__init__(displaySurface, tmx_path)

    def _setup_player(self):
        hero_sprite = Hero((100, 300), face_right=True)
        self.hero.add(hero_sprite)
        self.visible_sprites.add(hero_sprite)

    def _setup_enemies(self):
        pass
