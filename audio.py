import os
from enum import Enum

class Lang(Enum):
    RU = "ru/"
    EN = "en/"
    NONE = ""

_audio_root = "/home/pi/"

def _play_sound(file, lang: Lang):
    os.system("omxplayer --no-keys --vol 1000 " + _audio_root + lang.value + file)

class Sounds:
    @staticmethod
    def wellcome(lang):
        _play_sound("wellcome.mp3", lang)

    @staticmethod
    def rule(lang):
        _play_sound("rule.mp3", lang)

    @staticmethod
    def need_second_player(lang):
        _play_sound("need_second_player.mp3", lang)

    @staticmethod
    def water_level_n(level):
        _play_sound("level" + str(level) + ".mp3", Lang.NONE)

    @staticmethod
    def water_level_up():
        _play_sound("level_up.mp3", Lang.NONE)

    @staticmethod
    def water_level_down():
        _play_sound("level_down.mp3", Lang.NONE)
