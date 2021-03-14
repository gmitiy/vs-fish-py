from audio import Sounds


class Cell: 
    def __init__(self, level, number, symbol1, symbol2):
        self._level = level
        self._number = number
        self.symbol1 = symbol1
        self.symbol2 = symbol2
    
    def play_sound(self, cur_level, lang):
        Sounds.cell(self._number, self._level, cur_level, lang)

    def testSymbol(self, symbol):
        return symbol == str(self.symbol1) + str(self.symbol2)

    def get_level(self):
        return self._level

    def __eq__(self, other):
        if isinstance(other, Cell):
            return (self._number, self._level) == (other._number, other._level)
        return NotImplemented

    def __hash__(self):
        return hash((self._level, self._number))

    def __str__(self):
        return f"Cell[level={self._level}, number={self._number}, symbol={str(self.symbol1) + str(self.symbol2)}]"


class Field:
    def __init__(self):
        self.cells = [Cell(1, 1, 'A', 'B')] 
        self.cells += [Cell(1, 2, 'D', 'A')] 
        self.cells += [Cell(1, 3, 'A', 'D')] 
        self.cells += [Cell(1, 4, 'B', 'A')] 
        self.cells += [Cell(1, 5, 'A', 'C')] 
        self.cells += [Cell(1, 6, 'B', 'D')] 
        self.cells += [Cell(1, 7, 'H', 'G')] 
        self.cells += [Cell(1, 8, 'H', 'O')] 
        self.cells += [Cell(1, 9, 'B', 'B')] 
        self.cells += [Cell(2, 10, 'E', 'H')] 
        self.cells += [Cell(2, 11, 'E', 'C')] 
        self.cells += [Cell(2, 12, 'G', 'L')] 
        self.cells += [Cell(2, 13, 'C', 'B')] 
        self.cells += [Cell(2, 14, 'C', 'L')] 
        self.cells += [Cell(2, 15, 'G', 'F')] 
        self.cells += [Cell(2, 16, 'W', 'D')] 
        self.cells += [Cell(2, 17, 'D', 'B')] 
        self.cells += [Cell(2, 18, 'G', 'O')] 
        self.cells += [Cell(2, 19, 'F', 'E')] 
        self.cells += [Cell(3, 20, 'O', 'W')] 
        self.cells += [Cell(3, 21, 'O', 'H')] 
        self.cells += [Cell(3, 22, 'C', 'E')] 
        self.cells += [Cell(3, 23, 'F', 'O')] 
        self.cells += [Cell(3, 24, 'W', 'L')] 
        self.cells += [Cell(3, 25, 'W', 'B')] 
        self.cells += [Cell(3, 26, 'G', 'C')] 
        self.cells += [Cell(3, 27, 'F', 'G')] 
        self.cells += [Cell(3, 28, 'L', 'H')] 
        self.cells += [Cell(3, 29, 'W', 'O')] 
        self.cells += [Cell(4, 30, 'H', 'F')] 
        self.cells += [Cell(3, 31, 'D', 'G')] 
        self.cells += [Cell(4, 32, 'C', 'H')] 
        self.cells += [Cell(3, 33, 'W', 'G')] 
        self.cells += [Cell(3, 34, 'W', 'E')] 
        self.cells += [Cell(4, 35, 'D', 'E')] 
        self.cells += [Cell(4, 36, 'L', 'G')] 
        self.cells += [Cell(4, 37, 'E', 'O')] 
        self.cells += [Cell(4, 38, 'A', 'W')]

    def getCell(self, symbol):
        for cell in self.cells:
            if cell.testSymbol(symbol):
                return cell
        return None

FIELD = Field()


