import sys

import pygame

from tic_tac_toe import TicTacToe


def main():
    ttt = TicTacToe()
    while True:
        ttt.play()
        ttt.draw()

        winner = ttt.check_winner()
        if winner is not None:
            if winner == 0:
                print("A Tie!")
            else:
                winner = ttt.ai if ttt.turn % 2 == 0 else ttt.user
                print("{} Wins!".format(winner))
            break


def main_pg():
    ttt = TicTacToe()
    pygame.init()

    # default background
    screen = pygame.display.set_mode((300, 300))
    screen.fill((0, 0, 0))

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        ttt.play()

        blocks = get_blocks(screen, ttt)
        # pygame.display.update(blocks)
        pygame.display.flip()


def get_blocks(screen, ttt):
    blocks = list()
    dist = 100

    for row in range(len(ttt.cells)):
        for col in range(len(ttt.cells[row])):
            block = pygame.Rect(col*dist, row*dist, dist, dist)

            if ttt.cells[row][col] == ttt.user:
                pygame.draw.rect(screen, (127, 0, 0), block)
            elif ttt.cells[row][col] == ttt.ai:
                pygame.draw.rect(screen, (0, 127, 0), block)
            else:
                pygame.draw.rect(screen, (127, 127, 127), block)
            blocks.append(blocks)

    return blocks


if __name__ == "__main__":
    main_pg()
