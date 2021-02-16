
class Cell: 
    def __init__(self, number, level):
        self.number = number
        self.level = level
        self.sign = str(level) + str(number)


class Field:
    def __init__(self):
        self.cells = [Cell(i, 1) for i in range(1, 11)]
        self.cells += [Cell(i, 2) for i in range(1, 12)]
        self.cells += [Cell(i, 3) for i in range(1, 12)]
        self.cells += [Cell(i, 4) for i in range(1, 12)]
        self.cells += [Cell(i, 5) for i in range(1, 7)]



