import pygame


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.master_volume = 1.0
        self.load_sounds()

    def load_sounds(self):
        sound_files = {
            "pickupCoin": "data/sounds/pickupCoin.wav",
            "jump": "data/sounds/jump.wav",
            "buyItem_shop_open": "data/sounds/buyItem_shop_open.wav",
            "hitPlayer": "data/sounds/hitPlayer.wav",
            "dieEnemy": "data/sounds/dieEnemy.wav",
            "shoot": "data/sounds/shoot_both_enemy_and_player.wav"
        }

        for name, path in sound_files.items():
            try:
                sound_obj = pygame.mixer.Sound(path)
                sound_obj.set_volume(self.master_volume)
                self.sounds[name] = sound_obj
            except pygame.error as e:
                print(f"Could not load sound {name} from {path}: {e}")

    def play_sound(self, name, volume=1.0):
        if name in self.sounds:
            sound = self.sounds[name]
            sound.set_volume(self.master_volume * volume)
            sound.play()
        else:
            print(f"Sound '{name}' not found.")

    def set_master_volume(self, volume):
        self.master_volume = max(0.0, min(1.0, volume))
        for sound_name, sound_obj in self.sounds.items():
            sound_obj.set_volume(self.master_volume)

    def set_sound_volume(self, name, volume):
        if name in self.sounds:
            self.sounds[name].set_volume(volume)
        else:
            print(f"Sound '{name}' not found.")
