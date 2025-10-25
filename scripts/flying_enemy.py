import pygame
import config as Config
from sprite_sheet import SpriteSheet


class FlyingEnemy(pygame.sprite.Sprite):
    def __init__(self, position, patrol_distance, move_right):
        super().__init__()
        self.layer = Config.LAYER_MAIN
        sprite_paths = [
            Config.SPRITESHEET_PATH + "sprites/misc/drone/drone-1.png",
            Config.SPRITESHEET_PATH + "sprites/misc/drone/drone-2.png",
            Config.SPRITESHEET_PATH + "sprites/misc/drone/drone-3.png",
            Config.SPRITESHEET_PATH + "sprites/misc/drone/drone-4.png",
        ]
        attack_sprites_paths = [
            Config.SPRITESHEET_PATH + "sprites/misc/enemy-explosion/enemy-explosion-1.png",
            Config.SPRITESHEET_PATH + "sprites/misc/enemy-explosion/enemy-explosion-2.png",
            Config.SPRITESHEET_PATH + "sprites/misc/enemy-explosion/enemy-explosion-3.png",
            Config.SPRITESHEET_PATH + "sprites/misc/enemy-explosion/enemy-explosion-4.png",
            Config.SPRITESHEET_PATH + "sprites/misc/enemy-explosion/enemy-explosion-5.png",
            Config.SPRITESHEET_PATH + "sprites/misc/enemy-explosion/enemy-explosion-6.png",
        ]
        self.patrol_distance = patrol_distance
        self.spawn_position = position
        self.fly_sprite = SpriteSheet(sprite_paths)
        self.attack_strite = SpriteSheet(attack_sprites_paths)
        self.current_frame = 0
        self.move_right = move_right
        self.animation_index = 0
        self.current_state = "fly"
        self.select_animation()
        self.image = self.current_animation[self.current_frame]
        self.rect = self.image.get_rect(bottomleft=position)
        self.alive = True
        self.can_move = True
        self.is_dying = False

    def update(self, level):
        # Destroy
        if not self.alive:
            return
        # Moving
        if self.can_move:
            if not self.move_right:
                self.rect.x -= Config.FLYING_ENEMY_SPEED
            else:
                self.rect.x += Config.FLYING_ENEMY_SPEED

            # Change direction
            if self.rect.right < self.spawn_position[0]:
                self.move_right = True
            if self.rect.left > self.spawn_position[0] + self.patrol_distance:
                self.move_right = False

        # Attack logic
        if not self.is_dying:
            hero_rect = level.hero.sprite.rect
            hero_x = hero_rect.centerx
            if self.current_state == "fly":
                if hero_rect.top < self.rect.bottom <= hero_rect.bottom:
                    if self.move_right is True:
                        if self.rect.left < hero_x and self.rect.right > hero_x:
                            self.current_state = "attack"
                            self.animation_index = 0
                    else:
                        if self.rect.right > hero_x and self.rect.left < hero_x:
                            self.current_state = "attack"
                            self.animation_index = 0
            elif self.current_state == "attack":
                if self.move_right is True:
                    if self.rect.left >= hero_x or self.rect.right < hero_x:
                        self.current_state = "fly"
                        self.animation_index = 0
                    else:
                        if self.rect.left <= hero_x or self.rect.left > hero_x:
                            self.current_state = "fly"
                            self.animation_index = 0

        # Animation
        self.select_animation()
        
        self.animation_index += self.animation_speed
        if self.current_state == "attack":
            if self.is_dying:
                # Death animation - remove when finished
                self.can_move = False
                if self.animation_index >= len(self.current_animation):
                    self.alive = False
                    return

        else:
            if self.animation_index >= len(self.current_animation):
                self.animation_index = 0

        self.image = self.current_animation[int(self.animation_index)]

    def select_animation(self):
        self.animation_speed = Config.FLYING_ENEMY_ANIMATION_SPEED
        if self.current_state == "fly":
            self.current_animation = self.fly_sprite.get_sprites(
                flipped=not self.move_right
            )
        elif self.current_state == "attack":
            self.current_animation = self.attack_strite.get_sprites(
                flipped=not self.move_right
            )

    def die(self):
        if not self.is_dying:
            self.is_dying = True
            self.animation_index = 0
            self.current_state = "attack"
