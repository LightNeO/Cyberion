import pygame


class MusicManager:
    def __init__(self, music_path="data/sounds/bg_music.mp3", initial_volume=0.5):
        pygame.mixer.init()
        self.music_path = music_path
        self.volume = initial_volume
        self.paused = False
        pygame.mixer.music.set_volume(self.volume)
        self._load_music()

    def _load_music(self):
        pygame.mixer.music.load(self.music_path)

    def play_music(self, loops=-1):
        if not pygame.mixer.music.get_busy() or self.paused:
            pygame.mixer.music.play(loops)
            self.paused = False

    def stop_music(self):
        pygame.mixer.music.stop()

    def pause_music(self):
        pygame.mixer.music.pause()
        self.paused = True

    def unpause_music(self):
        pygame.mixer.music.unpause()
        self.paused = False

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)

    def get_volume(self):
        return self.volume

    def increase_volume(self, amount=0.1):
        self.set_volume(self.volume + amount)

    def decrease_volume(self, amount=0.1):
        self.set_volume(self.volume - amount)

    def reset_and_play(self):
        self.stop_music()
        self._load_music()
        self.play_music()
        self.set_volume(self.volume)
        self.paused = False
