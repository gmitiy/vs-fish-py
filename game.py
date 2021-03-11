import numpy
from audio import Lang, Sounds
from electro import Electro, ELECTRO, Controller
from field import Cell, FIELD
from gpiozero import Button, LED


class Player:
    def __init__(self, controller: Controller, sw_lang_btn: Button, led: LED):
        self.lang = Lang.RU
        self.controller = controller
        self.sw_lang_btn = sw_lang_btn
        self.sw_lang_btn.when_pressed = self.switchLang
        self.led = led

        self.score = 0
        self.known_cells = set()
        self.printMsg("")        

    def activate(self, state = None):
         self.led.value = not self.led.value if state is None else state

    def switchLang(self):
        if self.lang == Lang.RU:
            self.lang = Lang.EN
        else:
            self.lang = Lang.RU
        self.printMsg(self.cur_msg)

    def visitCell(self, cell, level):
        self.known_cells.add((cell, level))

    def isVisitCell(self, cell, level):
        return (cell, level) in self.known_cells

    def printMsg(self, msg):
        self.cur_msg = msg
        return self.controller.sendText(msg + self._getPlayerText())
    
    def turn(self, cur_level, prev_cell):
        self.printMsg("")
        while True:
            tmp = self.readChar()
            cell_str = tmp
            cell_str_p = '^' + tmp
            self.printMsg(cell_str_p)

            tmp = self.readChar()
            cell_str += tmp
            cell_str_p += '^' + tmp
            self.printMsg(cell_str_p)

            cell = FIELD.getCell(cell_str)

            if cell is None:
                self.printMsg("")
                Sounds.error_cell(self.lang)
                continue  

            if cell.get_level() < cur_level:
                self.printMsg("")
                Sounds.no_water(self.lang)
                continue


            if self.isVisitCell(cell, cur_level):
                if prev_cell.get_level() < cur_level:
                    self.score -= prev_cell.get_level()
                else:
                    self.score += 1
                self.printMsg("")
                Sounds.nothing_new(cur_level, self.lang)
                return cell
                
            
            if prev_cell.get_level() < cur_level:
                self.score -= prev_cell.get_level()
            else:
                self.score += cell.get_level()
            self.printMsg("")
            cell.play_sound(cur_level, self.lang)
            self.visitCell(cell, cur_level)
            return cell


            

    
    
    def readChar(self):
        ch = self.controller.readMsg()
        if ch == '?':
            Sounds.rule(self.lang)
            ch = self.controller.readMsg()
        return ch

    def _getPlayerText(self):
        sc = "SCORE: " if self.lang == Lang.EN else "C^YET: "
        sc += str(self.score)
        ln = "EN" if self.lang == Lang.EN else "RU"
        return "#" + sc.ljust(14) + ln



class Game:
    _fin_level = 5
    _fin_turn = 5

    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        ELECTRO.langB1.when_pressed = player1.switchLang
        self.player1.activate(True)

        self.player2 = player2
        ELECTRO.langB2.when_pressed = player2.switchLang
        self.player2.activate(False)

        self.turn = 1
        self.level = 1
        ELECTRO.change_level(1)

        Sounds.wellcome(Lang.RU)
        Sounds.wellcome(Lang.EN)


    def changePlayer(self):
        self.player1.activate()
        self.player2.activate()
            

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
                Sounds.water_level_up()
            else:
                Sounds.water_level_down()

            self.level = new_level
            break    

    def next_turn(self):
        self.turn += 1
        self._change_level()

