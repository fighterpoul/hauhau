import pathlib
import pygame


def load(audio_file: pathlib.Path):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)


def play_if_not_playing():
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()


def stop():
    pygame.mixer.music.stop()
