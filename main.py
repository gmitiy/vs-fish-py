
from game import Player, Game
from field import FIELD
from audio import Sounds

from electro import ELECTRO, log
from signal import pause
import time

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


    prev_cell1 = FIELD.getCell("AB")
    prev_cell2 = FIELD.getCell("BA")

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
        player1.printMsg("GAME OVER")
        player2.printMsg("GAME OVER")
        time.sleep(2)
        player1.printMsg("PRESS RESET")
        player2.printMsg("PRESS RESET")
        time.sleep(2)


if __name__ == "__main__":
    main()
