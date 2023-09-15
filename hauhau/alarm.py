import pathlib
import pygame
import time

AUDIO_FILES_DIR = pathlib.Path(__file__).parent.parent.joinpath('assets').resolve()
_ON_SOUND = AUDIO_FILES_DIR.joinpath('on.mp3')
_OFF_SOUND = AUDIO_FILES_DIR.joinpath('off.mp3')

def init(alarm_audio_file: pathlib.Path):
    pygame.mixer.init()

    pygame.mixer.music.load(_ON_SOUND)
    pygame.mixer.music.play()
    time.sleep(3)

    pygame.mixer.music.load(alarm_audio_file)


def play_if_not_playing():
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()


def stop():
    pygame.mixer.music.stop()


def release():
    pygame.mixer.music.load(_OFF_SOUND)
    pygame.mixer.music.play()