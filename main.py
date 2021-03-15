
import time
from signal import pause

from field import FIELD
from audio import Sounds
from game import Player, Game
from electro import ELECTRO, log

def main():
    log("Run script")

    log("Create Player1")
    player1 = Player("Player1", ELECTRO.controller1, ELECTRO.langB1, ELECTRO.led1)
    log("Create Player1 - DONE")

    log("Create Player2")
    player2 = Player("Player2", ELECTRO.controller2, ELECTRO.langB2, ELECTRO.led2)
    log("Create Player1 - DONE")  

    log("Create Game")
    game = Game(player1, player2)
    log("Create Game - DONE")


    prev_cell1 = FIELD.getCell("BB")  
    prev_cell2 = FIELD.getCell("AD")  

    log("Start game")
    while True:
        log("Next turn")
        game.next_turn()

        log(f"Current level = {game.level}")
        cur_level = game.level
        
        log("Player1 turn")
        prev_cell1 = player1.turn(cur_level, prev_cell1)
        log(f"Player1 turn - DONE. Current cell: {prev_cell1}")
        game.changePlayer()

        log("Player2 turn")
        prev_cell2 = player2.turn(cur_level, prev_cell2)
        log(f"Player2 turn - DONE. Current cell: {prev_cell1}")
        game.changePlayer()

        log("Test end-game")
        if game.testEnd():
            log("Game over")
            break

    log("Game suspend")
    while True:
        
        player1.printMsg(" ^A ^B ^C ^D ^E ^F ^G#   GAME OVER")
        player2.printMsg(" ^A ^B ^C ^D ^E ^F ^G#   GAME OVER")
        time.sleep(1)
        player1.printMsg("   GAME OVER# ^A ^B ^C ^D ^E ^F ^G")
        player2.printMsg("   GAME OVER# ^A ^B ^C ^D ^E ^F ^G")
        time.sleep(1)


if __name__ == "__main__":
    main()
