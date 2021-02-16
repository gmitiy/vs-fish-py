import numpy
from audio import Lang, Sounds

class Player:
    def __init__(self):
        self.reset()

    def reset(self):
        self.score = 0
        self.lang = Lang.RU


class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.new_game()

    def new_game(self):
        self.turn = 1
        self.level = 1
        self.player1.reset()
        self.player2.reset()

    def change_level(self):
        while True:
            new_level = self.level + numpy.random.choice(numpy.arange(-2, 3), p = [1/6, 1/6, 0, 1/3, 1/3])
            if new_level < 1:
                continue
            if new_level > 6:
                new_level = 6

            if self.turn < 6 and new_level == 6:
                continue
            if self.level == new_level:
                continue
            
            Sounds.water_level_n(new_level)
            if new_level > self.level:
                Sounds.water_level_up
            else:
                Sounds.water_level_down

            self.level = new_level
            break    

