
from game import Player, Game
from field import FIELD
from audio import Sounds

from electro import ELECTRO

import time

def main():
    player1 = Player(ELECTRO.controller1, ELECTRO.langB1, ELECTRO.led1)
    player2 = Player(ELECTRO.controller2, ELECTRO.langB2, ELECTRO.led2)
    game = Game(player1, player2)

    prev_cell1 = FIELD.getCell("AB")
    prev_cell2 = FIELD.getCell("BA")

    while True:
       game.next_turn()
       cur_level = game.level

       prev_cell1 = player1.turn(cur_level, prev_cell1)
       game.changePlayer()

       prev_cell2 = player1.turn(cur_level, prev_cell2)
       game.changePlayer()



    
    
    


if __name__ == "__main__":
    main()
