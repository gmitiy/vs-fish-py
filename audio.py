import os, time
from random import randint
from enum import Enum
from electro import log

class Lang(Enum):
    RU = "ru/"
    EN = "en/"
    NONE = ""

_audio_root = "/home/pi/game/sound/"

def _play_sound(file, lang: Lang):
    log(f"omxplayer --no-keys --vol 900 {_audio_root}{lang.value}{file}") 
    if os.system(f"omxplayer --no-keys --vol 900 {_audio_root}{lang.value}{file}") > 0:
        os.system("omxplayer --no-keys --vol 300 /home/pi/game/sound/all_fail.m4a")

class Sounds:
    @staticmethod
    def wellcome(lang):
        log(f"Play - wellcome. Lang: {lang.name}")
        _play_sound("wellcome.mp3", lang)

    @staticmethod
    def rule(lang):
        log(f"Play - rule. Lang: {lang.name}")
        _play_sound("rule.mp3", lang)

    @staticmethod
    def end_game(lang):
        log(f"Play - end_game. Lang: {lang.name}")
        _play_sound("end_game.mp3", lang)        

    @staticmethod
    def water_level_up():
        log(f"Play - water_level_up.")
        _play_sound("level_up.mp3", Lang.NONE)

    @staticmethod
    def water_level_down():
        log(f"Play - water_level_down.")
        _play_sound("level_down.mp3", Lang.NONE)

    @staticmethod
    def error_cell(lang):
        log(f"Play - error_cell. Lang: {lang.name}")
        _play_sound("error.mp3", lang)

    @staticmethod
    def no_water(lang):
        log(f"Play - no_water. Lang: {lang.name}")
        _play_sound("no_water.mp3", lang)
        

    @staticmethod
    def water_level_n(level):
        log(f"Play - water_level_n.")
        _play_sound(f"Siren_{level}_Layer.wav", Lang.NONE)

    @staticmethod
    def nothing_new(level, lang):
        log(f"Play - nothing_new. Lang: {lang.name}")
        _play_sound(f"{level}_NothingNew.wav", lang)

    @staticmethod
    def cell(number, cell_level, cur_level, lang):
        log(f"Play - Cell. Number: {number}, Cell_level: {cell_level}, Cur_level: {cur_level}, Lang: {lang.name}")
        if cur_level >= cell_level:
            if cur_level == 5:
                log(f"Play - Cell Start level 5.")
                _play_sound(f"5_{randint(1, 3)}.wav", lang)
            else:
                log(f"Play - Cell Start.")
                _play_sound(f"{cell_level}-{number}-{cur_level}.wav", lang)

