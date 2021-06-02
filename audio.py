import os, time
from enum import Enum
from random import randint

from electro import log

class Lang(Enum):
    RU = "ru/"
    EN = "en/"
    NONE = ""

_audio_root = "/home/pi/game/sound/"

_omx_comm = "omxplayer --no-osd --no-keys --vol 250 "

def _play_sound(file, lang: Lang):
    log(f"{_omx_comm}{_audio_root}{lang.value}{file}") 
    if os.system(f"{_omx_comm}{_audio_root}{lang.value}{file} > /dev/null 2>&1") > 0:
        os.system(f"{_omx_comm} /home/pi/game/sound/test.wav")



class Sounds:
    _final = False

    ## NO_LANG_SOUNDS
    @staticmethod
    def wellcome():
        log(f"Play - wellcome.")
        _play_sound("Beginning.wav", Lang.NONE)

    @staticmethod
    def end_game():
        log(f"Play - end_game.")
        _play_sound("GameOver.wav", Lang.NONE)
        _play_sound("GameOver2.wav", Lang.NONE)

    @staticmethod
    def water_level_down():
        log(f"Play - water_level_down.")
        _play_sound("Lower.wav", Lang.NONE)  

    @staticmethod
    def water_level_n(level):
        log(f"Play - water_level_n.")
        _play_sound(f"Siren_{level}_Layer.wav", Lang.NONE)

    @staticmethod
    def no_english():
        log(f"Play - no_english.")
        _play_sound("NoEnglish.wav", Lang.NONE)


    ## LANG_SOUNDS
    @staticmethod
    def rule(lang):
        log(f"Play - rule. Lang: {lang.name}")
        _play_sound("Rules.wav", lang)

    @staticmethod
    def error_cell(lang):
        log(f"Play - error_cell. Lang: {lang.name}")
        _play_sound("NoPlace.wav", lang)

    @staticmethod
    def no_water(lang):
        log(f"Play - no_water. Lang: {lang.name}")
        _play_sound("TooDry.wav", lang)
        
    @staticmethod
    def nothing_new(level, lang):
        log(f"Play - nothing_new. Lang: {lang.name}")
        _play_sound(f"{level}_NothingNew.wav", lang)

    @staticmethod
    def cell(number, cell_level, cur_level, lang):
        log(f"Play - Cell. Number: {number}, Cell_level: {cell_level}, Cur_level: {cur_level}, Lang: {lang.name}")
        if cur_level >= cell_level:
            if cur_level == 5: 
                if Sounds._final:
                    log(f"Play - Cell Start level 5 final.")
                    _play_sound(f"5_Final.wav", lang)
                else:
                    log(f"Play - Cell Start level 5.")
                    _play_sound(f"5_{randint(1, 3)}.wav", lang)
                    Sounds._final = True
            else:
                log(f"Play - Cell Start.")
                _play_sound(f"{cell_level}-{number}-{cur_level}.wav", lang)

