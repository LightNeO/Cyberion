import pygame
import config as Config
from sprite_sheet import SpriteSheet
from bullet import Bullet


class TurretEnemy(pygame.sprite.Sprite):
    def __init__(self, position, patrol_distance, move_right, sound_manager):
        super().__init__()
        self.layer = Config.LAYER_MAIN
        self.sound_manager = sound_manager
        
        # Load sprites
        idle_sprite_paths = [
            Config.SPRITESHEET_PATH + "sprites/misc/turret/turret-1.png",
            Config.SPRITESHEET_PATH + "sprites/misc/turret/turret-2.png",
            Config.SPRITESHEET_PATH + "sprites/misc/turret/turret-3.png",
            Config.SPRITESHEET_PATH + "sprites/misc/turret/turret-4.png",
            Config.SPRITESHEET_PATH + "sprites/misc/turret/turret-5.png",
            Config.SPRITESHEET_PATH + "sprites/misc/turret/turret-6.png",
            Config.SPRITESHEET_PATH + "sprites/misc/turret/turret-7.png",
            Config.SPRITESHEET_PATH + "sprites/misc/turret/turret-8.png",
        ]
        die_sprites_paths = [
            Config.SPRITESHEET_PATH + "sprites/misc/enemy-explosion/enemy-explosion-1.png",
            Config.SPRITESHEET_PATH + "sprites/misc/enemy-explosion/enemy-explosion-2.png",
            Config.SPRITESHEET_PATH + "sprites/misc/enemy-explosion/enemy-explosion-3.png",
            Config.SPRITESHEET_PATH + "sprites/misc/enemy-explosion/enemy-explosion-4.png",
            Config.SPRITESHEET_PATH + "sprites/misc/enemy-explosion/enemy-explosion-5.png",
            Config.SPRITESHEET_PATH + "sprites/misc/enemy-explosion/enemy-explosion-6.png",
        ]

        self.spawn_position = position
        self.idle_animation = SpriteSheet(idle_sprite_paths).get_sprites(False)
        self.attack_left_image = pygame.image.load(Config.SPRITESHEET_PATH + "sprites/misc/turret/turret-1.png").convert_alpha()
        self.attack_right_image = pygame.image.load(Config.SPRITESHEET_PATH + "sprites/misc/turret/turret-5.png").convert_alpha()
        self.die_animation = SpriteSheet(die_sprites_paths).get_sprites(False)
        
        self.current_frame = 0
        self.animation_index = 0
        self.current_state = "idle"
        self.image = self.idle_animation[self.current_frame]
        self.rect = self.image.get_rect(bottomleft=position)
        self.alive = True
        self.is_dying = False
        self.last_shot_time = 0

    def update(self, level):
        if not self.is_dying:
            if level.hero.sprite.current_state != "die":
                self.detect_hero(level.hero.sprite)
                if self.current_state in ["attack_left", "attack_right"]:
                    self.shoot(level)
        
        self.select_animation()

    def detect_hero(self, hero):
        hero_pos = hero.rect.center
        turret_pos = self.rect.center
        distance = pygame.math.Vector2(hero_pos[0] - turret_pos[0], hero_pos[1] - turret_pos[1]).length()

        if distance < Config.TURRET_DETECTION_RANGE:
            if hero_pos[0] < turret_pos[0]:
                self.current_state = "attack_left"
            else:
                self.current_state = "attack_right"
        else:
            self.current_state = "idle"

    def select_animation(self):
        if self.current_state == "idle":
            self.animation_index += Config.TURRET_ANIMATION_SPEED
            if self.animation_index >= len(self.idle_animation):
                self.animation_index = 0
            self.image = self.idle_animation[int(self.animation_index)]
        elif self.current_state == "attack_left":
            self.image = self.attack_left_image
        elif self.current_state == "attack_right":
            self.image = self.attack_right_image
        elif self.current_state == "die":
            self.animation_index += Config.HERO_ANIMATION_SPEED_DIE
            if self.animation_index >= len(self.die_animation):
                self.kill()
            else:
                self.image = self.die_animation[int(self.animation_index)]

    def shoot(self, level):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > Config.TURRET_FIRE_DELAY_MS:
            move_right = self.current_state == "attack_right"
            spawn_pos = (self.rect.centerx, self.rect.centery - 17)
            bullet = Bullet(spawn_pos, move_right, bullet_type="enemy")
            level.bullets.add(bullet)
            level.visible_sprites.add(bullet)
            self.last_shot_time = current_time
            self.sound_manager.play_sound("shoot")

    def die(self):
        if not self.is_dying:
            self.is_dying = True
            self.current_state = "die"
            self.animation_index = 0
            self.sound_manager.play_sound("dieEnemy")
