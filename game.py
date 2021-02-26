import numpy
from audio import Lang, Sounds
from electro import Electro, ELECTRO
from field import Cell

class Player:
    def __init__(self):
        self.reset()

    def reset(self):
        self.score = 0
        self.known_cells = set()
        self.lang = Lang.RU

    def switchLang(self):
        if self.lang == Lang.RU:
            self.lang = Lang.EN
        else:
            self.lang = Lang.RU

    def changeLang(self, lang: Lang):
        self.lang = lang

    def visitCell(self, cell: Cell):
        self.known_cells.add(cell)

    def isVisitCell(self, cell: Cell):
        return cell in self.known_cells


class Game:
    _fin_level = 5
    _fin_turn = 5

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.new_game()

    def new_game(self):
        self.turn = 1
        self.level = 1
        self.player1.reset()
        self.player2.reset()

    def start(self):
        if self.player1.lang == self.player2.lang:
            Sounds.wellcome(self.player1.lang)
        else:
            Sounds.wellcome(Lang.RU)
            Sounds.wellcome(Lang.EN)

    def _change_level(self):
        while True:
            new_level = self.level + numpy.random.choice(numpy.arange(-2, 3), p = [1/6, 1/6, 0, 1/3, 1/3])
            if new_level < 1:
                continue
            if new_level > self._fin_level:
                new_level = self._fin_level

            if self.turn < self._fin_turn and new_level == self._fin_level:
                continue
            if self.level == new_level:
                continue
            
            ELECTRO.change_level(new_level)
            Sounds.water_level_n(new_level)
            if new_level > self.level:
                Sounds.water_level_up
            else:
                Sounds.water_level_down

            self.level = new_level
            break    

    def next_turn(self):
        self.turn += 1
        self._change_level()

