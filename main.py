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


def draw_error(screen, ttt, width, height, margin, pos):
    i, j = pos
    new_width = i * width + i * margin + margin
    new_height = j * height + j * margin + margin
    block = pygame.Rect(new_width, new_height, width, height)
    icon = (20, 20, 20)
    pygame.draw.rect(screen, icon, block)


def draw_board(screen, ttt, width, height, margin):

    for i in range(3):
        for j in range(3):
            new_width = i * width + i * margin + margin
            new_height = j * height + j * margin + margin
            block = pygame.Rect(new_width, new_height, width, height)
            icon = (127, 127, 127)
            if ttt.cells[j][i] == 'X':
                icon = (127, 255, 127)
            if ttt.cells[j][i] == 'O':
                icon = (255, 127, 127)
            pygame.draw.rect(screen, icon, block)


def main_pg():
    ttt = TicTacToe()
    pygame.init()

    # default background
    screen_w = 300
    screen_h = 300
    screen = pygame.display.set_mode((screen_w, screen_h))
    screen.fill((0, 0, 0))

    draw_board(screen, ttt, 93, 93, 5)
    pygame.display.flip()

    user_turn = True

    while True:
        if user_turn is False:
            ttt.play(1)
            draw_board(screen, ttt, 93, 93, 5)
            pygame.display.flip()
            user_turn = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                w, h = pygame.mouse.get_pos()
                total_w = ((w // 10) // 10) + 1
                total_h = (((h // 10) // 10) * 3)

                result = total_w + total_h
                if result in range(1, 10):
                    result = ttt.play(result)
                    if result:
                        draw_board(screen, ttt, 93, 93, 5)
                        pygame.display.flip()
                        user_turn = False
                    else:
                        current = 0
                        for x in range(10):
                            draw_error(screen, ttt, 93, 93, 5, (total_w - 1, total_h // 3))
                            pygame.event.pump()
                            pygame.display.flip()

                            current += pygame.time.get_ticks()
                            while current > 7000:

                                draw_board(screen, ttt, 93, 93, 5)
                                pygame.event.pump()
                                pygame.display.update()

                                current = 0

                    draw_board(screen, ttt, 93, 93, 5)
                    pygame.display.flip()

        # Display a winner/loser/tie screen
        is_winner = ttt.check_winner()
        if is_winner is not None:
            if is_winner == 0:
                print("A Tie!")
            elif is_winner == 1:
                print("You Win!")
            elif is_winner == -1:
                print("You Lost!")
            break


if __name__ == "__main__":
    main_pg()
