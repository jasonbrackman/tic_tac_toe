import random


class TicTacToe:

    def __init__(self):
        self.user = 'X'
        self.ai = 'O'

        self.cells = [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' '],
        ]

        self.turn = 0

    # __ Validators
    def is_position_valid(self, pos):
        # must be a digit
        if str(pos).isdigit() is False:
            return False

        # must be in range and not a position already filled
        row, col = self.convert_input_to_pos(pos)
        if row < 0 or row > 2 or col < 0 or col > 2:
            return False

        elif self.cells[row][col] in (self.user, self.ai):
            return False

        # checks passed, so must be good
        return True

    def is_game_finished(self):
        result = {
            self.user: 1,
            self.ai: -1,
        }

        # COLS
        for row in self.cells:
            if len(set(row)) == 1 and row[0] in result:
                return result[row[0]]

        # ROWS
        for index in range(3):
            col_swizzle = [row[index] for row in self.cells]
            if len(set(col_swizzle)) == 1 and col_swizzle[0] in result:
                return result[col_swizzle[0]]

        # DIAGS
        diag1 = [self.cells[i][i] for i in range(3)]
        diag2 = [self.cells[i][j] for i, j in enumerate(reversed(range(3)))]
        if len(set(diag1)) == 1 and diag1[0] in result:
            return result[diag1[0]]
        if len(set(diag2)) == 1 and diag2[0] in result:
            return result[diag2[0]]

        # TIE
        if not self.available_positions():
            return 0

        return None

    def available_positions(self):
        """Returns a list of row, col tuples for each pos available."""

        options = list()
        for row in range(3):
            for col in range(3):
                if self.cells[row][col] not in (self.user, self.ai):
                    options.append((row, col))

        return options

    # __ AI
    def ai_random(self, options):
        row, col = random.choice(options)
        self.cells[row][col] = self.ai
        self.turn += 1

    def ai_minimax(self, options):
        best_score = float("inf")
        move = None
        for (row, col) in options:
            self.cells[row][col] = self.ai
            score = self.minimax(0, True)
            self.cells[row][col] = ' '
            if score < best_score:
                best_score = score
                move = (row, col)
        row, col = move
        self.cells[row][col] = self.ai
        self.turn += 1

    def minimax(self, depth, is_maximizing):
        result = self.is_game_finished()

        # if someone won -- return the score
        if result is not None:
            return result

        # setup vars based on maximizing or minimizing
        # - if not the maximizer you want to find the min score for the opponent
        best_score = float("-inf") if is_maximizing else float("inf")
        board_icon = self.user if is_maximizing else self.ai
        min_or_max = max if is_maximizing else min

        for (row, col) in self.available_positions():
            self.cells[row][col] = board_icon
            score = self.minimax(depth + 1, not is_maximizing)
            self.cells[row][col] = ' '

            best_score = min_or_max(best_score, score)

        return best_score

    @staticmethod
    def convert_input_to_pos(response):
        index = int(response) - 1
        col = index // 3
        row = index % 3
        return row, col

    # __ Work
    def play(self, response=None):
        played = True

        if self.turn % 2 == 0:
            if response is None:
                response = input("Select a number from 1 to 9: ")

            if self.is_position_valid(response):
                row, col = self.convert_input_to_pos(response)

                self.cells[row][col] = self.user
                self.turn += 1
            else:
                played = False
            #
            # print("Unexpected input or space already occupied for >> {}".format(response))
            # self.play()

        else:
            options = self.available_positions()
            if options:
                self.ai_minimax(options)
                # self.ai_random(options)

        return played

    def draw(self):
        """
        X : X : O
        - : - : -
        X : O : O
        - : - : -
        O : X : X

        :return:
        """
        for row in range(3):
            for col in range(3):
                print(self.cells[row][col], end='')
                print(' ' if col == 2 else ' : ', end='')

            print('\n' if row == 2 else "\n- : - : - ")