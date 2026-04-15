import os
import pygame


class Player:
    SUPPORTED = (".mp3", ".wav", ".ogg")

    def __init__(self, music_dir):
        self.music_dir = music_dir
        self.tracks = self._load_tracks()
        self.current = 0
        self.status = "Stopped"

    def _load_tracks(self):
        if not os.path.isdir(self.music_dir):
            return []
        files = sorted(os.listdir(self.music_dir))
        return [os.path.join(self.music_dir, f) for f in files
                if f.lower().endswith(self.SUPPORTED)]

    def has_tracks(self):
        return len(self.tracks) > 0

    def play(self):
        if not self.has_tracks():
            return
        pygame.mixer.music.load(self.tracks[self.current])
        pygame.mixer.music.play()
        self.status = "Playing"

    def stop(self):
        pygame.mixer.music.stop()
        self.status = "Stopped"

    def next(self):
        if not self.has_tracks():
            return
        self.current = (self.current + 1) % len(self.tracks)
        self.play()

    def back(self):
        if not self.has_tracks():
            return
        self.current = (self.current - 1) % len(self.tracks)
        self.play()

    def current_name(self):
        if not self.has_tracks():
            return "(no tracks)"
        return os.path.basename(self.tracks[self.current])
