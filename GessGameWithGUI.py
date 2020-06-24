import os
import sys
import pygame
from pygame.locals import *


class GessGame:
    """
    Represents a Gess Game.
    Each game is initialized with the same board, (in state unfinished), and starts with current player = black.
    """

    def __init__(self):
        """Initializes members of class GessGame"""
        self._game_state = 'UNFINISHED'             # 'UNFINISHED', 'BLACK_WON' or 'WHITE_WON'
        self._current_player = 'BLACK'              # 'BLACK' or 'WHITE' (black goes first)
        self._black_rings = 0                       # number of rings player has (should never be called without first calling check_for_rings)
        self._white_rings = 0
        self._temp_board = []                       # temporary board used for testing move legality
        self._move_direction = ''                   # player's current move direction (only if valid)
        self._board = [ # A    B    C    D    E    F    G    H    I    J    K    L    M    N    O    P    Q    R    S    T
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], #1
                        [' ', ' ', 'B', ' ', 'B', ' ', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', ' ', 'B', ' ', 'B', ' ', ' '], #2
                        [' ', 'B', 'B', 'B', ' ', 'B', ' ', 'B', 'B', 'B', 'B', ' ', 'B', ' ', 'B', ' ', 'B', 'B', 'B', ' '], #3
                        [' ', ' ', 'B', ' ', 'B', ' ', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', ' ', 'B', ' ', 'B', ' ', ' '], #4
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], #5
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], #6
                        [' ', ' ', 'B', ' ', ' ', 'B', ' ', ' ', 'B', ' ', ' ', 'B', ' ', ' ', 'B', ' ', ' ', 'B', ' ', ' '], #7
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], #8
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], #9
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], #10
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], #11
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], #12
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], #13
                        [' ', ' ', 'W', ' ', ' ', 'W', ' ', ' ', 'W', ' ', ' ', 'W', ' ', ' ', 'W', ' ', ' ', 'W', ' ', ' '], #14
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], #15
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], #16
                        [' ', ' ', 'W', ' ', 'W', ' ', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', ' ', 'W', ' ', 'W', ' ', ' '], #17
                        [' ', 'W', 'W', 'W', ' ', 'W', ' ', 'W', 'W', 'W', 'W', ' ', 'W', ' ', 'W', ' ', 'W', 'W', 'W', ' '], #18
                        [' ', ' ', 'W', ' ', 'W', ' ', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', ' ', 'W', ' ', 'W', ' ', ' '], #19
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], #20
                        ]

    def get_board(self):
        """Prints board"""
        print("  A    B    C    D    E    F    G    H    I    J    K    L    M    N    O    P    Q    R    S    T")
        for row in self._board:
            print(row)

    def get_game_state(self):
        """Returns the state of the game"""
        return self._game_state

    def resign_game(self):
        """Lets the current player concede the game, giving the other player the win. Updates game_state accordingly."""
        if self._current_player == 'BLACK':
            self._game_state = 'WHITE_WON'
        else:
            self._game_state = 'BLACK_WON'

    def make_move(self, center_from, center_to):
        """
        Takes two strings that represent the center square of the piece being moved and the desired new location of
        the center square. Checks if move is illegal and if game has already been won -- if so, returns False. Else,
        makes the move, removes any captured stones, updates game state if necessary, updates whose turn it is, removes
        stones in the gutters, and returns True.
        """
        center_from = self.convert_center(center_from)                      # convert beginning and ending centers to the list axes of the board (column, row)
        center_to = self.convert_center(center_to)
        if self.get_game_state() == 'UNFINISHED':                           # if the game is not over
            if self.is_valid_piece(center_from) is True:                    # and the piece is valid
                if self.is_valid_move(center_from, center_to) is True:      # and the move is valid
                    self.move_piece(self._board, center_from, center_to)    # make the move
                    self.clean_gutters(self._board)                         # clean the gutters
                    self.check_for_rings(self._board)                       # check for rings
                    self.check_for_winners()                                # check for winners
                    self.change_current_player()                            # change current player
                    return True
                else:                                                       # move is invalid
                    return False
            else:                                                           # piece is invalid
                return False
        else:                                                               # game is already over
            return False

    def convert_center(self, beg_center):
        """Takes user inputted centers and converts to same axes as board"""
        column_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11,
                       'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19}
        # convert from letter supplied to corresponding list column
        converted_column = column_dict[beg_center[0]]
        # convert from number supplied to corresponding list row
        converted_row = int(beg_center[1:]) - 1
        return converted_column, converted_row

    def get_center(self, board, center):
        """Returns the value at the center provided"""
        return board[center[1]][center[0]]

    def get_north(self, board, center):
        """Returns the value at the space north of the center provided"""
        return board[center[1] - 1][center[0]]

    def get_south(self, board, center):
        """Returns the value at the space south of the center provided"""
        return board[center[1] + 1][center[0]]

    def get_northwest(self, board, center):
        """Returns the value at the space northwest of the center provided"""
        return board[center[1] - 1][center[0] - 1]

    def get_northeast(self, board, center):
        """Returns the value at the space northeast of the center provided"""
        return board[center[1] - 1][center[0] + 1]

    def get_southwest(self, board, center):
        """Returns the value at the space southwest of the center provided"""
        return board[center[1] + 1][center[0] - 1]

    def get_southeast(self, board, center):
        """Returns the value at the space southeast of the center provided"""
        return board[center[1] + 1][center[0] + 1]

    def get_east(self, board, center):
        """Returns the value at the space east of the center provided"""
        return board[center[1]][center[0] + 1]

    def get_west(self, board, center):
        """Returns the value at the space west of the center provided"""
        return board[center[1]][center[0] - 1]

    def get_center_location(self, center):
        """Returns the location of the center provided"""
        return center[0], center[1]

    def get_north_location(self, center):
        """Returns the location of the space north of the center provided"""
        return center[0], center[1] - 1

    def get_south_location(self, center):
        """Returns the location of the space south of the center provided"""
        return center[0], center[1] + 1

    def get_east_location(self, center):
        """Returns the location of the space east of the center provided"""
        return center[0] + 1, center[1]

    def get_west_location(self, center):
        """Returns the location of the space west of the center provided"""
        return center[0] - 1, center[1]

    def get_northwest_location(self, center):
        """Returns the location of the space northwest of the center provided"""
        return center[0] - 1, center[1] - 1

    def get_northeast_location(self, center):
        """Returns the location of the space northeast of the center provided"""
        return center[0] + 1, center[1] - 1

    def get_southwest_location(self, center):
        """Returns the location of the space southwest of the center provided"""
        return center[0] - 1, center[1] + 1

    def get_southeast_location(self, center):
        """Returns the location of the space southeast of the center provided"""
        return center[0] + 1, center[1] + 1

    def get_piece(self, board, center):
        """Returns the values of the piece using the center provided"""
        return [self.get_center(board, center),
                self.get_north(board, center),
                self.get_south(board, center),
                self.get_northeast(board, center),
                self.get_northwest(board, center),
                self.get_southeast(board, center),
                self.get_southwest(board, center),
                self.get_east(board, center),
                self.get_west(board, center)]

    def get_north_row(self, board, center):
        """Returns the values of the piece's north row using the center provided"""
        return [self.get_north(board, center),
                self.get_northeast(board, center),
                self.get_northwest(board, center)]

    def get_south_row(self, board, center):
        """Returns the values of the piece's south row using the center provided"""
        return [self.get_south(board, center),
                self.get_southeast(board, center),
                self.get_southwest(board, center)]

    def get_east_row(self, board, center):
        """Returns the values of the piece's east row using the center provided"""
        return [self.get_northeast(board, center),
                self.get_southeast(board, center),
                self.get_east(board, center)]

    def get_west_row(self, board, center):
        """Returns the values of the piece's west row using the center provided"""
        return [self.get_northwest(board, center),
                self.get_southwest(board, center),
                self.get_west(board, center)]

    def get_current_player_initial(self):
        """Gets initial of current player"""
        return self._current_player[0]

    def is_valid_piece(self, center_from):
        """Checks whether piece is valid"""
        # is the center off the board?
        if self.center_in_gutter(center_from) is True:
            print("This piece is invalid because its center is on the board's outermost row or column")
            return False
        # do all of the squares surrounding the center contain either the current player's stones or blank squares?
        else:
            piece = self.get_piece(self._board, center_from)
            valid_piece = True
            elem = self.get_current_player_initial()
            for e in piece:
                if e != elem and e != ' ':
                    valid_piece = False
                    break
            if valid_piece is False:
                print("This piece is invalid because it contains the other player's stones.")
            return valid_piece

    def move_piece(self, board, center_from, center_to):
        """Once a move has been approved, this function is called to clear the existing piece and repopulate it at its destination"""
        temp_center = board[center_from[1]][center_from[0]]
        temp_north = board[center_from[1] - 1][center_from[0]]
        temp_south = board[center_from[1] + 1][center_from[0]]
        temp_northeast = board[center_from[1] - 1][center_from[0] - 1]
        temp_northwest = board[center_from[1] - 1][center_from[0] + 1]
        temp_southeast = board[center_from[1] + 1][center_from[0] - 1]
        temp_southwest = board[center_from[1] + 1][center_from[0] + 1]
        temp_east = board[center_from[1]][center_from[0] + 1]
        temp_west = board[center_from[1]][center_from[0] - 1]
        # clear old
        board[center_from[1]][center_from[0]] = ' '
        board[center_from[1] - 1][center_from[0]] = ' '
        board[center_from[1] + 1][center_from[0]] = ' '
        board[center_from[1] - 1][center_from[0] - 1] = ' '
        board[center_from[1] - 1][center_from[0] + 1] = ' '
        board[center_from[1] + 1][center_from[0] - 1] = ' '
        board[center_from[1] + 1][center_from[0] + 1] = ' '
        board[center_from[1]][center_from[0] + 1] = ' '
        board[center_from[1]][center_from[0] - 1] = ' '
        # populate new
        board[center_to[1]][center_to[0]] = temp_center
        board[center_to[1] - 1][center_to[0]] = temp_north
        board[center_to[1] + 1][center_to[0]] = temp_south
        board[center_to[1] - 1][center_to[0] - 1] = temp_northeast
        board[center_to[1] - 1][center_to[0] + 1] = temp_northwest
        board[center_to[1] + 1][center_to[0] - 1] = temp_southeast
        board[center_to[1] + 1][center_to[0] + 1] = temp_southwest
        board[center_to[1]][center_to[0] + 1] = temp_east
        board[center_to[1]][center_to[0] - 1] = temp_west

    def clean_gutters(self, board):
        """At the end of a successful move, eliminates the stones that have landed in the board's outside rows"""
        board[0] = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        board[19] = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        for i in range(1, 18):
            board[i][0] = ' '
            board[i][19] = ' '

    def check_for_rings(self, board):
        """
        Checks whether a player has any rings, returns True or False accordingly.
        For use in checking for winners and checking whether a move is valid.
        """
        self._black_rings = 0                                   # resetting/initializing ring counts
        self._white_rings = 0
        for row in range(1, 19):                                # for every center between row 1 & 19 and column 1 & 19
            for column in range(1, 19):
                center = row, column
                if self.get_center(board, center) == ' ':       # a ring is only a ring if it has no center
                    ring = self.get_piece(board, center)[1:]    # get a list of the elements in the ring surrounding the center (excluding center)
                    ring_found = True
                    elem = ring[0]
                    for e in ring:
                        if e != elem or e == ' ':               # if an element in the ring is different from the first or blank, set ring_found to False
                            ring_found = False
                            break
                    if ring_found is True:                      # if there is a ring, increment the appropriate player's ring count
                        if elem == "B":
                            self._black_rings += 1
                        if elem == "W":
                            self._white_rings += 1

    def check_for_winners(self):
        """
        Checks whether anyone has won -- if so, updates self._game_state.
        This should only be called immediately after check_for_rings.
        """
        if self._black_rings == 0:
            self._game_state = 'WHITE_WON'
        if self._white_rings == 0:
            self._game_state = 'BLACK_WON'

    def check_for_eliminating_own_ring(self, center_from, center_to):
        """Checks whether the player's move eliminates their last ring"""
        self._temp_board = []                                           # initialize a temporary board for testing the move
        for i in self._board:
            self._temp_board.append(list(i))
        self.move_piece(self._temp_board, center_from, center_to)       # make the move on the temporary board
        self.check_for_rings(self._temp_board)                          # check how the move impacts rings
        if self._black_rings == 0 and self._current_player == 'BLACK':  # check whether the current player is eliminating all of their own rings
            return True
        elif self._white_rings == 0 and self._current_player == 'WHITE':
            return True
        else:
            return False

    def change_current_player(self):
        """Updates the current player (to be called at the end of a valid move)"""
        if self._current_player == 'BLACK':
            self._current_player = 'WHITE'
        else:
            self._current_player = 'BLACK'

    def unlimited_distance(self, center_from):
        """Checks whether a piece has a center, and is thus able to move an unlimited distance if unobstructed"""
        if self.get_center(self._board, center_from) == self.get_current_player_initial():  # has center
            return True
        else:                                                                               # has no center
            return False

    def violating_distance(self, center_from, center_to):
        """Checks whether the proposed move is further than it is allowed to move"""
        # If there is a stone in the center, the piece can move any unobstructed distance.
        if self.unlimited_distance(center_from) is True:                # distance cannot be violated
            return False
        # If the center is empty, the piece can move up to three squares.
        else:
            vertical_movement = abs(center_to[1] - center_from[1])
            horizontal_movement = abs(center_to[0] - center_from[0])
            if vertical_movement > 3 or horizontal_movement > 3:        # distance is violated
                return True
            else:                                                       # piece has limited distance, but it is not violated
                return False

    def violating_direction(self, center_from, center_to):
        """Checks whether the proposed move is in a direction it is allowed to move"""
        board = self._board
        populated_direction = self.get_current_player_initial()
        proposed_row_change = center_to[1] - center_from[1]
        proposed_column_change = center_to[0] - center_from[0]
        forty_five_degrees = False                              # validate that any angled move has a slope of 1
        if proposed_column_change != 0:                         # to avoid zero division error
            forty_five_degrees = abs(proposed_row_change / proposed_column_change) == 1
        if proposed_row_change < 0 and proposed_column_change == 0 and self.get_north(board, center_from) == populated_direction:
            self._move_direction = 'north'
            return False
        elif proposed_row_change > 0 and proposed_column_change == 0 and self.get_south(board, center_from) == populated_direction:
            self._move_direction = 'south'
            return False
        elif proposed_column_change < 0 and proposed_row_change == 0 and self.get_west(board, center_from) == populated_direction:
            self._move_direction = 'west'
            return False
        elif proposed_column_change > 0 and proposed_row_change == 0 and self.get_east(board, center_from) == populated_direction:
            self._move_direction = 'east'
            return False
        elif proposed_row_change < 0 and proposed_column_change < 0 and forty_five_degrees and self.get_northwest(board, center_from) == populated_direction:
            self._move_direction = 'northwest'
            return False
        elif proposed_row_change < 0 and proposed_column_change > 0 and forty_five_degrees and self.get_northeast(board, center_from) == populated_direction:
            self._move_direction = 'northeast'
            return False
        elif proposed_row_change > 0 and proposed_column_change < 0 and forty_five_degrees and self.get_southwest(board, center_from) == populated_direction:
            self._move_direction = 'southwest'
            return False
        elif proposed_row_change > 0 and proposed_column_change > 0 and forty_five_degrees and self.get_southeast(board, center_from) == populated_direction:
            self._move_direction = 'southeast'
            return False
        else:                                                   # the move is in an disallowed direction
            return True

    def center_in_gutter(self, center):
        """Checks whether the proposed center is in an disallowed location"""
        if center[1] == 0 or center[1] == 19 or center[0] == 0 or center[0] == 19:
            return True
        else:
            return False

    def is_blocked(self, center_from, center_to):
        """Checks whether move is blocked by stones, returns True or False accordingly"""
        # find the number of rows and columns the piece is expected to move
        proposed_row_change = center_to[1] - center_from[1]
        proposed_column_change = center_to[0] - center_from[0]

        if self._move_direction == 'south':
            center = center_from                            # while we still have rows to check, start with original center
            while proposed_row_change > 1:
                potential_blockages = self.get_south_row(self._board, self.get_south_location(center))
                center = self.get_south_location(center)    # set the center one row further south
                proposed_row_change -= 1                    # decrement the rows to check
                for element in potential_blockages:         # if the row south of the current south square of the piece is not blank, return True
                    if element != ' ':
                        return True
            else:                                           # if we made it down to only 1 remaining row/col of movement, the piece was not blocked
                return False

        elif self._move_direction == 'north':
            proposed_row_change = proposed_row_change * - 1
            center = center_from
            while proposed_row_change > 1:
                potential_blockages = self.get_north_row(self._board, self.get_north_location(center))
                center = self.get_north_location(center)
                proposed_row_change -= 1
                for element in potential_blockages:
                    if element != ' ':
                        return True
            else:
                return False

        elif self._move_direction == 'east':
            center = center_from
            while proposed_column_change > 1:
                potential_blockages = self.get_east_row(self._board, self.get_east_location(center))
                center = self.get_east_location(center)
                proposed_column_change -= 1
                for element in potential_blockages:
                    if element != ' ':
                        return True
            else:
                return False

        elif self._move_direction == 'west':
            proposed_column_change = proposed_column_change * - 1
            center = center_from
            while proposed_column_change > 1:
                potential_blockages = self.get_west_row(self._board, self.get_west_location(center))
                center = self.get_west_location(center)
                proposed_column_change -= 1
                for element in potential_blockages:
                    if element != ' ':
                        return True
            else:
                return False

        elif self._move_direction == 'northwest':
            # north function + west function but replaced direction we're traveling with northwest
            proposed_row_change = proposed_row_change * - 1
            center = center_from
            while proposed_row_change > 1:
                potential_blockages = self.get_north_row(self._board, self.get_north_location(center))
                center = self.get_northwest_location(center)
                proposed_row_change -= 1
                for element in potential_blockages:
                    if element != ' ':
                        return True
            proposed_column_change = proposed_column_change * - 1
            center = center_from
            while proposed_column_change > 1:
                potential_blockages = self.get_west_row(self._board, self.get_west_location(center))
                center = self.get_northwest_location(center)
                proposed_column_change -= 1
                for element in potential_blockages:
                    if element != ' ':
                        return True
            else:
                return False

        elif self._move_direction == 'northeast':
            # north function + east function but replaced direction we're traveling with northeast
            proposed_row_change = proposed_row_change * - 1
            center = center_from
            while proposed_row_change > 1:
                potential_blockages = self.get_north_row(self._board, self.get_north_location(center))
                center = self.get_northeast_location(center)
                proposed_row_change -= 1
                for element in potential_blockages:
                    if element != ' ':
                        return True
            center = center_from
            while proposed_column_change > 1:
                potential_blockages = self.get_east_row(self._board, self.get_east_location(center))
                center = self.get_northeast_location(center)
                proposed_column_change -= 1
                for element in potential_blockages:
                    if element != ' ':
                        return True
            else:
                return False

        elif self._move_direction == 'southwest':
            # south function + west function but replaced direction we're traveling with southwest
            center = center_from
            while proposed_row_change > 1:
                potential_blockages = self.get_south_row(self._board, self.get_south_location(center))
                center = self.get_southwest_location(center)
                proposed_row_change -= 1
                for element in potential_blockages:
                    if element != ' ':
                        return True
            proposed_column_change = proposed_column_change * - 1
            center = center_from
            while proposed_column_change > 1:
                potential_blockages = self.get_west_row(self._board, self.get_west_location(center))
                center = self.get_southwest_location(center)
                proposed_column_change -= 1
                for element in potential_blockages:
                    if element != ' ':
                        return True
            else:
                return False

        elif self._move_direction == 'southeast':
            # south function + east function but replaced direction we're traveling with southeast
            center = center_from
            while proposed_row_change > 1:
                potential_blockages = self.get_south_row(self._board, self.get_south_location(center))
                center = self.get_southeast_location(center)
                proposed_row_change -= 1
                for element in potential_blockages:
                    if element != ' ':
                        return True
            center = center_from
            while proposed_column_change > 1:
                potential_blockages = self.get_east_row(self._board, self.get_east_location(center))
                center = self.get_southeast_location(center)
                proposed_column_change -= 1
                for element in potential_blockages:
                    if element != ' ':
                        return True
            else:
                return False

    def is_valid_move(self, center_from, center_to):
        """Checks whether move is valid, returns True or False accordingly"""

        if self.center_in_gutter(center_to) is False:                                           # move does not move the center off the board
            if self.violating_direction(center_from, center_to) is False:                       # direction limit is not violated
                if self.violating_distance(center_from, center_to) is False:                    # distance limit is not violated
                    if self.is_blocked(center_from, center_to) is False:                        # there are no stones in the way
                        if self.check_for_eliminating_own_ring(center_from, center_to) is True:
                            print("This move is invalid because it eliminates the current player's last ring")
                            return False
                        else:                                                                   # move does not eliminate player's own last ring
                            return True
                    else:
                        print("This move is invalid because there are stones in the way.")
                        return False
                else:                                                                           # distance is violated
                    print("This move is invalid because it is further than the current piece is permitted to move")
                    return False
            else:                                                                               # direction is violated
                print("This move is invalid because it is in a direction that is not allowed for the chosen piece.")
                return False
        else:                                                                                   # proposed center is in the gutter
            print("This move is invalid because the proposed center is in the board's outermost row or column.")
            return False

    def draw_board(self):
        """Creates a representation of the board for the player"""
        square_size = 25
        radius = 12.5
        indent = square_size * 2
        font = pygame.font.Font(None, 24)
        for column in range(20):
            for row in range(20):
                # initial grid
                pygame.draw.rect(screen, (50, 50, 50), (column * square_size + indent, row * square_size + indent, square_size, square_size), 1)
                # populate stones
                if self._board[row][column] == 'B':
                    pygame.draw.circle(screen, (50, 50, 50), (int(column * square_size + indent + square_size / 2), int(row * square_size + 2 * square_size + square_size / 2)), radius)
                if self._board[row][column] == 'W':
                    pygame.draw.circle(screen, (250, 250, 250), (int(column * square_size + indent + square_size / 2), int(row * square_size + 2 * square_size + square_size / 2)), radius)
                    # borders for the white stones because otherwise they are garish
                    pygame.draw.circle(screen, (50, 50, 50), (int(column * square_size + indent + square_size / 2), int(row * square_size + 2 * square_size + square_size / 2)), radius, 1)
        # outside border
        pygame.draw.rect(screen, (50, 50, 50), (indent, indent, 500, 500), 2)
        # axes
        column_text = font.render("A   B   C    D   E    F   G   H    I     J    K   L    M   N   O    P   Q   R    S   T", 1, (50, 50, 50))
        screen.blit(column_text, (57, 35))
        row_1 = font.render("1", 1, (50, 50, 50))
        row_2 = font.render("2", 1, (50, 50, 50))
        row_3 = font.render("3", 1, (50, 50, 50))
        row_4 = font.render("4", 1, (50, 50, 50))
        row_5 = font.render("5", 1, (50, 50, 50))
        row_6 = font.render("6", 1, (50, 50, 50))
        row_7 = font.render("7", 1, (50, 50, 50))
        row_8 = font.render("8", 1, (50, 50, 50))
        row_9 = font.render("9", 1, (50, 50, 50))
        row_10 = font.render("10", 1, (50, 50, 50))
        row_11 = font.render("11", 1, (50, 50, 50))
        row_12 = font.render("12", 1, (50, 50, 50))
        row_13 = font.render("13", 1, (50, 50, 50))
        row_14 = font.render("14", 1, (50, 50, 50))
        row_15 = font.render("15", 1, (50, 50, 50))
        row_16 = font.render("16", 1, (50, 50, 50))
        row_17 = font.render("17", 1, (50, 50, 50))
        row_18 = font.render("18", 1, (50, 50, 50))
        row_19 = font.render("19", 1, (50, 50, 50))
        row_20 = font.render("20", 1, (50, 50, 50))
        screen.blit(row_1, (35, 57 + 25 * 0))
        screen.blit(row_2, (35, 57 + 25 * 1))
        screen.blit(row_3, (35, 57 + 25 * 2))
        screen.blit(row_4, (35, 57 + 25 * 3))
        screen.blit(row_5, (35, 57 + 25 * 4))
        screen.blit(row_6, (35, 57 + 25 * 5))
        screen.blit(row_7, (35, 57 + 25 * 6))
        screen.blit(row_8, (35, 57 + 25 * 7))
        screen.blit(row_9, (35, 57 + 25 * 8))
        screen.blit(row_10, (27, 57 + 25 * 9))
        screen.blit(row_11, (27, 57 + 25 * 10))
        screen.blit(row_12, (27, 57 + 25 * 11))
        screen.blit(row_13, (27, 57 + 25 * 12))
        screen.blit(row_14, (27, 57 + 25 * 13))
        screen.blit(row_15, (27, 57 + 25 * 14))
        screen.blit(row_16, (27, 57 + 25 * 15))
        screen.blit(row_17, (27, 57 + 25 * 16))
        screen.blit(row_18, (27, 57 + 25 * 17))
        screen.blit(row_19, (27, 57 + 25 * 18))
        screen.blit(row_20, (27, 57 + 25 * 19))

        # display player whose turn it is
        current_player_text = font.render("Turn:", 1, (50, 50, 50))
        screen.blit(current_player_text, (10, 570))
        if self._current_player == 'BLACK':
            pygame.draw.circle(screen, (50, 50, 50), (70, 578), radius)
        if self._current_player == 'WHITE':
            pygame.draw.circle(screen, (250, 250, 250), (70, 578), radius)
            pygame.draw.circle(screen, (50, 50, 50), (70, 578), radius, 1)
        pygame.display.update()


# create new game
game = GessGame()
# initialize pygame -- set screen size, window name, background image,
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Gess!")
background = pygame.image.load("background.png")
screen.blit(background, (0, 0))
# draw the board -- grid lines, pieces, etc & update display
game.draw_board()

pygame.display.update()


while game.get_game_state() == 'UNFINISHED':
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            print('hi!')

print(game.get_game_state())