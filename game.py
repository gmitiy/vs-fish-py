import numpy
from gpiozero import Button, LED

from field import Cell, FIELD
from audio import Lang, Sounds
from electro import Electro, ELECTRO, Controller, log


class Player:
    def __init__(self, name, controller: Controller, sw_lang_btn: Button, led: LED):
        self.name = name
        self.lang = Lang.RU
        self.controller = controller
        self.sw_lang_btn = sw_lang_btn
        self.sw_lang_btn.when_pressed = self.no_lang
        self.led = led

        self.score = 0
        self.known_cells = set()
        self.printMsg("----------------")      
        self.printMsg("----------------")  
        self.printMsg("----------------")   

    def activate(self, state = None):
         self.led.value = not self.led.value if state is None else state
         log(f"{self.name} - Led {'activate' if self.led.value else 'deactivate'}")


    def switchLang(self):
        if self.lang == Lang.RU:
            self.lang = Lang.EN
        else:
            self.lang = Lang.RU
        log(f"{self.name} - Switch lang to {self.lang.name}")
        self.printMsg()

    def no_lang(self):
        log(f"{self.name} - Press lang button - NO-LANG")
        Sounds.no_english()

    def printMsg(self, message = None):
        if message is not None:
            self.cur_msg = message
        return self.controller.writeMsg(self.cur_msg + self._getPlayerText())

    def printMsgAll(self, msg):
        return self.controller.writeMsg(msg)

    def visitCell(self, cell, level):
        self.known_cells.add((cell, level))

    def isVisitCell(self, cell, level):
        return (cell, level) in self.known_cells

    def turn(self, cur_level, prev_cell):
        self.printMsg(">")
        while True:
            tmp = self.readChar()
            log(f"{self.name} - Read char {tmp}")
            cell_str = tmp
            cell_str_p = '^' + tmp
            self.printMsg("> " + cell_str_p)

            tmp = self.readChar()
            log(f"{self.name} - Read second char {tmp}")
            cell_str += tmp
            cell_str_p += '^' + tmp
            self.printMsg("> " + cell_str_p)

            cell = FIELD.getCell(cell_str)
            
            if cell is None:
                log(f"{self.name} - Select error cell")
                Sounds.error_cell(self.lang)
                self.printMsg(">")
                continue  

            if cell.get_level() > cur_level:
                log(f"{self.name} - Select no water")
                Sounds.no_water(self.lang)
                self.printMsg(">")
                continue

            log(f"{self.name} - Go to cell: {str(cell)}")

            if self.isVisitCell(cell, cur_level):
                
                if prev_cell.get_level() > cur_level:
                    log(f"{self.name} - Go to visited cell from no water")
                    self.score -= prev_cell.get_level()
                else:
                    log(f"{self.name} - Go to visited cell")
                    self.score += 1
                self.printMsg()   
                Sounds.nothing_new(cur_level, self.lang)
                self.printMsg("----------------")
                log(f"{self.name} - Score: {self.score}")
                return cell
                
            
            if prev_cell.get_level() > cur_level:
                log(f"{self.name} - Go to new cell from no water")
                self.score -= prev_cell.get_level()
            else:
                log(f"{self.name} - Go to new cell")
                self.score += cell.get_level()
            self.visitCell(cell, cur_level)
            self.printMsg() 
            cell.play_sound(cur_level, self.lang)
            self.printMsg("----------------")
            log(f"{self.name} - Score: {self.score}")
            return cell

    def readChar(self):
        while True:
            try:
                ch = self.controller.readMsg()
                if ch == '?':
                    Sounds.rule(self.lang)
                    ch = self.controller.readMsg()
                if ch is None:
                    log(f"{self.name} - readChar None")
                    continue
                return ch
            except:
                log(f"{self.name} - readChar ERROR")

    def _getPlayerText(self):
        sc =  f"{'SCORE:' if self.lang == Lang.EN else 'C^YET:'} {str(self.score)}"  
        return "#" + sc.ljust(14) + self.lang.name


class Game:
    _fin_level = 5
    _fin_turn = 5

    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        ELECTRO.langB1.when_pressed = player1.switchLang
        self.player1.activate(True)
        log("Game - Player1 init")

        self.player2 = player2
        ELECTRO.langB2.when_pressed = player2.switchLang
        self.player2.activate(False)
        log("Game - Player2 init")

        self.turn = 0
        self.level = 1
        ELECTRO.change_level(1)


    def changePlayer(self):
        self.player1.activate()
        self.player2.activate()

    def testEnd(self):
        if self.level == self._fin_level:
            log("Game - End by fin level")
            Sounds.end_game()
            return True

        if self.player1.score > 16 or self.player2.score > 16:
            log("Game - End by score")
            Sounds.end_game()
            return True

        return False
            

    def _change_level(self):
        log(f"Game - Current level: {self.level}")
        while True:
            if self.turn == 1:
                new_level = 2
            else:
                new_level = self.level + numpy.random.choice(numpy.arange(-2, 3), p = [1/6, 1/6, 0, 1/3, 1/3])
            
            if new_level < 1:
                log(f"Game - Select level skip by negative value. Candidat: {new_level}")
                continue

            if new_level > self._fin_level:
                new_level = self._fin_level

            if self.turn < self._fin_turn and new_level == self._fin_level:
                log(f"Game - Select level skip by not final turn. Candidat: {new_level}")
                continue

            if self.level == new_level:
                log(f"Game - Select level skip by no change. Candidat: {new_level}")
                continue

            log(f"Game - Select new level: {new_level}")
            Sounds.water_level_n(new_level)
            ELECTRO.change_level(new_level)
            if new_level < self.level:
                Sounds.water_level_down()

            self.level = new_level
            break    

    def next_turn(self):
        self.turn += 1
        log(f"Game - Turn number: {self.turn}")
        self._change_level()
        

