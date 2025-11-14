import pygame
import config as Config
from sprite_sheet import SpriteSheet
from bullet import Bullet
import os


class Hero(pygame.sprite.Sprite):
    def __init__(self, position, face_right, sound_manager):
        super().__init__()
        self.layer = Config.LAYER_MAIN
        self.sound_manager = sound_manager
        idle_sprite_paths = [
            Config.SPRITESHEET_PATH + "sprites/player/idle/idle-1.png",
            Config.SPRITESHEET_PATH + "sprites/player/idle/idle-2.png",
            Config.SPRITESHEET_PATH + "sprites/player/idle/idle-3.png",
            Config.SPRITESHEET_PATH + "sprites/player/idle/idle-4.png",
        ]
        run_sprite_paths = [
            Config.SPRITESHEET_PATH + "sprites/player/run/run-1.png",
            Config.SPRITESHEET_PATH + "sprites/player/run/run-2.png",
            Config.SPRITESHEET_PATH + "sprites/player/run/run-3.png",
            Config.SPRITESHEET_PATH + "sprites/player/run/run-4.png",
            Config.SPRITESHEET_PATH + "sprites/player/run/run-5.png",
            Config.SPRITESHEET_PATH + "sprites/player/run/run-6.png",
            Config.SPRITESHEET_PATH + "sprites/player/run/run-7.png",
            Config.SPRITESHEET_PATH + "sprites/player/run/run-8.png",
        ]
        attack_sprite_paths = [
            Config.SPRITESHEET_PATH + "sprites/player/shoot/shoot.png",
        ]
        run_shoot_sprite_paths = [
            Config.SPRITESHEET_PATH + "sprites/player/run-shoot/run-shoot-1.png",
            Config.SPRITESHEET_PATH + "sprites/player/run-shoot/run-shoot-2.png",
            Config.SPRITESHEET_PATH + "sprites/player/run-shoot/run-shoot-3.png",
            Config.SPRITESHEET_PATH + "sprites/player/run-shoot/run-shoot-4.png",
            Config.SPRITESHEET_PATH + "sprites/player/run-shoot/run-shoot-5.png",
            Config.SPRITESHEET_PATH + "sprites/player/run-shoot/run-shoot-6.png",
            Config.SPRITESHEET_PATH + "sprites/player/run-shoot/run-shoot-7.png",
            Config.SPRITESHEET_PATH + "sprites/player/run-shoot/run-shoot-8.png",
        ]
        die_sprite_paths = [
            Config.SPRITESHEET_PATH + "sprites/player/hurt/hurt-1.png",
            Config.SPRITESHEET_PATH + "sprites/player/hurt/hurt-2.png",
            Config.SPRITESHEET_PATH + "sprites/player/hurt/hurt-3.png",
            Config.SPRITESHEET_PATH + "sprites/player/hurt/hurt-4.png",
            Config.SPRITESHEET_PATH + "sprites/player/hurt/hurt-10.png",
        ]
        hurt_sprite_paths = [
            Config.SPRITESHEET_PATH + "sprites/player/hurt/hurt-1.png",
            Config.SPRITESHEET_PATH + "sprites/player/hurt/hurt-2.png",
            Config.SPRITESHEET_PATH + "sprites/player/hurt/hurt-3.png",
            Config.SPRITESHEET_PATH + "sprites/player/hurt/hurt-4.png",
            Config.SPRITESHEET_PATH + "sprites/player/hurt/hurt-10.png",
        ]
        # Just to try different way of loading sprites
        jump_dir = os.path.join(Config.SPRITESHEET_PATH, "sprites/player/jump")
        jump_sprite_paths = [
            os.path.join(jump_dir, fname)
            for fname in sorted(os.listdir(jump_dir))
            if fname.lower().endswith(".png")
        ]
        self.idle_sprite = SpriteSheet(idle_sprite_paths)
        self.run_sprite = SpriteSheet(run_sprite_paths)
        self.attack_sprite = SpriteSheet(attack_sprite_paths)
        self.run_shoot_sprite = SpriteSheet(run_shoot_sprite_paths)
        self.jump_sprite = SpriteSheet(jump_sprite_paths)
        self.die_sprite = SpriteSheet(die_sprite_paths)
        self.hurt_sprite = SpriteSheet(hurt_sprite_paths)

        self.sprite_sheets = {
            "idle": self.idle_sprite,
            "run": self.run_sprite,
            "jump": self.jump_sprite,
            "attack": self.attack_sprite,
            "run_shoot": self.run_shoot_sprite,
            "die": self.die_sprite,
            "hurt": self.hurt_sprite,
        }
        self.animation_index = 0
        self.facing_right = face_right
        self.current_state = "idle"
        self.x = position[0]
        self.y = position[1]
        self.x_dir = 0
        self.speed = Config.HERO_SPEED
        self.vel_y = 0
        self.on_ground = False
        self._next_fire_time = 0
        self.last_hurt_time = 0
        self.hurt_cooldown = 2000
        self.knockback_dir = 0
        self.last_animation_frame = -1

    _hp = 5
    _bullets = 10

    @classmethod
    def get_hp(cls):
        return cls._hp

    @classmethod
    def change_hp(cls, hp: int):
        cls._hp += hp

    @classmethod
    def get_bullets(cls):
        return cls._bullets

    @classmethod
    def change_bullets(cls, amount: int):
        cls._bullets += amount

    def update(self, level):

        self.previous_state = self.current_state
        self.x_dir = 0

        if self.current_state not in ("die", "hurt"):
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE]:
                now_ms = pygame.time.get_ticks()
                self.try_shoot(level, now_ms)

            if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
                self.vel_y = Config.HERO_JUMP_SPEED
                self.on_ground = False
                self.current_state = "jump"
                self.sound_manager.play_sound("jump")
            elif keys[pygame.K_LEFT]:
                self.x_dir = -1
                self.facing_right = False
                if self.on_ground:
                    if keys[pygame.K_SPACE]:
                        self.current_state = "run_shoot"
                    else:
                        self.current_state = "run"
            elif keys[pygame.K_RIGHT]:
                self.x_dir = 1
                self.facing_right = True
                if self.on_ground:
                    if keys[pygame.K_SPACE]:
                        self.current_state = "run_shoot"
                    else:
                        self.current_state = "run"
            else:
                self.x_dir = 0
                if self.on_ground:
                    if keys[pygame.K_SPACE]:
                        self.current_state = "attack"
                    else:
                        self.current_state = "idle"

        if self.current_state == "idle":
            self.rect = pygame.Rect(self.x - 11, self.y - 50, 23, 50)
        elif self.current_state == "run":
            self.rect = pygame.Rect(self.x - 24, self.y - 49, 49, 49)
        elif self.current_state == "jump":
            self.rect = pygame.Rect(self.x - 17, self.y - 48, 34, 48)
        elif self.current_state == "attack":
            self.rect = pygame.Rect(self.x - 18, self.y - 53, 37, 53)
        elif self.current_state == "run_shoot":
            self.rect = pygame.Rect(self.x - 29, self.y - 48, 58, 48)
        elif self.current_state == "die":
            self.rect = pygame.Rect(self.x - 11, self.y - 50, 23, 50)
        elif self.current_state == "hurt":
            self.rect = pygame.Rect(self.x - 11, self.y - 50, 23, 50)
        if self.current_state == "hurt":
            self.x += self.knockback_dir * 10

        self.move_horizontal(level)
        self.move_vertical(level)

        if self.current_state not in ("attack", "die", "hurt"):
            if not self.on_ground:
                if self.current_state != "jump":
                    self.current_state = "jump"
                    self.animation_index = 0
            else:
                if self.current_state == "jump":
                    self.current_state = "run" if self.x_dir != 0 else "idle"
                    self.animation_index = 0

        # Reset animation
        if self.previous_state != self.current_state:
            self.animation_index = 0

        self.select_animation()

        # Update animation index
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.current_animation):
            if self.current_state == "die":
                self.animation_index = len(self.current_animation) - 1
            elif self.current_state == "hurt":
                self.animation_index = 0
                self.current_state = "idle"
                self.knockback_dir = 0
                self.last_animation_frame = -1
            elif self.current_state == "jump":
                self.animation_index = 0
            elif self.current_state == "attack":
                self.animation_index = 0
            elif self.current_state == "run_shoot":
                self.animation_index = 0
            else:
                self.animation_index = 0
                self.current_state = "idle"

        current_frame_index = int(self.animation_index)

        # Hurt logic
        if self.current_state == "hurt" and current_frame_index != self.last_animation_frame:
            self.x += self.knockback_dir * 10
            self.last_animation_frame = current_frame_index

        self.image = self.current_animation[current_frame_index]

        self.check_enemy_collision(level.flying_enemies)
        self.check_bullet_collision(level.bullets)

    def select_animation(self):
        self.animation_speed = Config.HERO_ANIMATION_SPEED_DEFFAULT
        if self.current_state == "idle":
            self.animation_speed = Config.HERO_ANIMATION_SPEED_IDLE
        elif self.current_state == "run":
            self.animation_speed = Config.HERO_ANIMATION_SPEED_RUN
        elif self.current_state == "jump":
            self.animation_speed = Config.HERO_ANIMATION_SPEED_JUMP
        elif self.current_state == "run_shoot":
            self.animation_speed = Config.HERO_ANIMATION_SPEED_RUN_SHOOT
        elif self.current_state == "die":
            self.animation_speed = Config.HERO_ANIMATION_SPEED_DIE
        elif self.current_state == "hurt":
            self.animation_speed = Config.HERO_ANIMATION_SPEED_HURT

        sprite_sheet = self.sprite_sheets[self.current_state]
        self.current_animation = sprite_sheet.get_sprites(self.facing_right)

    def move_horizontal(self, level):
        self.rect.centerx += self.x_dir * self.speed

        # Horizontal collision
        for tile in pygame.sprite.spritecollide(self, level.platform_tiles, False):
            if self.x_dir > 0:
                self.rect.right = tile.rect.left
            elif self.x_dir < 0:
                self.rect.left = tile.rect.right

        level_width = level.level_data.width * level.level_data.tilewidth
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > level_width:
            self.rect.right = level_width

        self.x = self.rect.centerx

    def move_vertical(self, level):
        self.vel_y += Config.HERO_GRAVITY
        if self.vel_y > 16:
            self.vel_y = 16

        self.on_ground = False

        self.rect.bottom += int(self.vel_y)

        for tile in pygame.sprite.spritecollide(self, level.platform_tiles, False):
            if self.vel_y > 0:
                self.rect.bottom = tile.rect.top
                self.vel_y = 0
                self.on_ground = True
            elif self.vel_y < 0:
                self.rect.top = tile.rect.bottom
                self.vel_y = 0

        # World bounds (floor/ceiling)
        if self.rect.bottom > Config.WINDOW_HEIGHT and self.current_state not in ("die", "hurt"):
            self.rect.bottom = Config.WINDOW_HEIGHT - 50
            _current_time = pygame.time.get_ticks()
            if _current_time - self.last_hurt_time > self.hurt_cooldown:
                self.die()
                self.last_hurt_time = _current_time
                Hero._hp -= 1
            self.vel_y = 0

        if self.current_state == "die" and Hero._hp > 0:
            is_animation_finished = self.animation_index >= len(self.current_animation) - 1

            if is_animation_finished:
                self.rect.bottom = 200
                self.y = 200
                self.x = 200
                self.current_state = "idle"

        if not self.on_ground and int(self.vel_y) == 0:
            probe_rect = self.rect.move(0, 1)
            for tile in level.platform_tiles:
                if probe_rect.colliderect(tile.rect):
                    self.on_ground = True
                    break

        self.y = self.rect.bottom

    def die(self):
        if self.current_state != "die":
            self.current_state = "die"
            self.animation_index = 0

    def check_bullet_collision(self, bullets):
        enemy_bullets = pygame.sprite.Group()
        for bullet in bullets:
            if bullet.bullet_type == 'enemy':
                enemy_bullets.add(bullet)

        collided_sprites = pygame.sprite.spritecollide(self, enemy_bullets, True)
        for bullet in collided_sprites:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_hurt_time > self.hurt_cooldown:
                self.current_state = "hurt"
                if bullet.move_right:
                    self.knockback_dir = 1
                else:
                    self.knockback_dir = -1
                self.last_hurt_time = current_time
                if Hero.get_hp() > 0:
                    self.sound_manager.play_sound("hitPlayer")
                Hero.change_hp(-1)
                if Hero.get_hp() <= 0:
                    self.die()

    def check_enemy_collision(self, enemies):
        current_time = pygame.time.get_ticks()
        collided_sprites = pygame.sprite.spritecollide(self, enemies, False)
        for enemy in collided_sprites:
            if self.rect.left < enemy.rect.left:
                if self.rect.right > enemy.rect.left + 16:
                    if current_time - self.last_hurt_time > self.hurt_cooldown:
                        self.current_state = "hurt"
                        self.knockback_dir = -1
                        self.last_hurt_time = current_time
                        if Hero.get_hp() > 0:
                            self.sound_manager.play_sound("hitPlayer")
                        Hero.change_hp(-1)
                        enemy.die()
                        if Hero.get_hp() <= 0:
                            self.die()
            elif self.rect.right > enemy.rect.right:
                if self.rect.left < enemy.rect.right - 16:
                    if current_time - self.last_hurt_time > self.hurt_cooldown:
                        self.current_state = "hurt"
                        self.knockback_dir = 1
                        self.last_hurt_time = current_time
                        if Hero.get_hp() > 0:
                            self.sound_manager.play_sound("hitPlayer")
                        Hero.change_hp(-1)
                        enemy.die()
                        if Hero.get_hp() <= 0:
                            self.die()

    def shoot(self, level):
        if Hero.get_bullets() > 0:
            if self.current_state == "die":
                return
            muzzle_y = self.rect.centery - 16
            muzzle_x = self.rect.right if self.facing_right else self.rect.left
            bullet = Bullet((muzzle_x, muzzle_y), move_right=self.facing_right)
            level.bullets.add(bullet)
            level.visible_sprites.add(bullet)
            Hero.change_bullets(-1)
            self.sound_manager.play_sound("shoot")

    def try_shoot(self, level, now_ms):
        if now_ms >= self._next_fire_time:
            self.shoot(level)
            self._next_fire_time = now_ms + Config.HERO_FIRE_DELAY_MS
