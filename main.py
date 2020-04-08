import sys
from collections import namedtuple

import pygame
import pygame.freetype

from tic_tac_toe import TicTacToe

colour_data_t = namedtuple("colours", "red blue green gray black")
COLOURS = colour_data_t(
    red=(255, 127, 127),
    blue=(127, 127, 255),
    green=(127, 255, 127),
    gray=(127, 127, 127),
    black=(0, 0, 0),
)


def main():
    ttt = TicTacToe()
    while True:
        ttt.play()
        ttt.draw()

        winner = ttt.is_game_finished()
        if winner is not None:
            if winner == 0:
                print("A Tie!")
            else:
                winner = ttt.ai if ttt.turn % 2 == 0 else ttt.user
                print("{} Wins!".format(winner))
            break


def get_blocks(width, height, margin):
    blocks = []
    for i in range(3):
        for j in range(3):
            new_width = i * width + i * margin + margin
            new_height = j * height + j * margin + margin
            blocks.append(pygame.Rect(new_width, new_height, width, height))

    return blocks


def get_icons(ttt):
    icons = []
    for i in range(3):
        for j in range(3):
            icon = COLOURS.gray
            if ttt.cells[j][i] == "X":
                icon = COLOURS.green
            if ttt.cells[j][i] == "O":
                icon = COLOURS.red
            icons.append(icon)

    return icons


def get_rect_index(blocks, pos):
    needle = 0
    for index, block in enumerate(blocks, 1):
        if block.collidepoint(*pos):
            needle = index
    return needle


def draw_board(screen, ttt, blocks, mute_pos=-1):
    font = pygame.freetype.SysFont(None, 30)  # very slow to load first time
    icons = get_icons(ttt)
    for index, (block, icon) in enumerate(zip(blocks, icons), 1):

        if index == mute_pos:
            # mute the following position if passed in
            icon = (20, 20, 20)
        pygame.draw.rect(screen, icon, block)

        if icon is not COLOURS.gray:
            # render the player text
            text = "X" if icon is COLOURS.green else "O"
            x = block.x + 22
            y = block.y + 22
            font.render_to(screen, (x, y), text, COLOURS.black, size=75)


def main_pg():
    ttt = TicTacToe()

    pygame.init()
    pygame.display.set_caption("Tic Tac Toe")

    # Hack: Loads before game window as it can take a very long time on my MacOs Catalina 10.15.4
    pygame.freetype.SysFont(None, 30)

    # default background
    screen_w = 300
    screen_h = 300
    screen = pygame.display.set_mode((screen_w, screen_h))
    screen.fill((0, 0, 0))

    blocks = get_blocks(93, 93, 5)

    while ttt.is_game_finished() is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                rect_index = get_rect_index(blocks, pos)

                if ttt.play(rect_index) is False:
                    # Blink rect to indicate invalid move
                    for x in range(7):
                        # blink will either blink the square or choose a number
                        # outside of the range of blocks to blink; negating its role.
                        blink = 10 if x % 2 == 0 else 0
                        draw_board(screen, ttt, blocks, rect_index + blink)
                        pygame.display.flip()
                        pygame.event.pump()
                        pygame.time.wait(65)
                else:
                    # play as AI
                    ttt.play(-1)

            draw_board(screen, ttt, blocks)
            pygame.display.flip()

    # Ensure last state of board is drawn
    pygame.event.pump()

    # Display a winner/loser/tie screen
    winner = ttt.is_game_finished()
    if winner == 0:
        print("A Tie!")
    elif winner == 1:
        print("You Win!")
    elif winner == -1:
        print("You Lost!")
    input("press a key to end.")


if __name__ == "__main__":
    main_pg()
