_author_ = "Rehan Jetha"
_date_ = "Wed, Nov 22nd, 2023"
_version_ = "1.0"
_filename_ = "PlayerRandom.py"
_description_ = "Random Checkers AI"

import copy
import random

def main(board, colour):
    """Zeus AI Function"""


# Utility Functions

    def make_king(piece):
        """Returns a crowned version of a piece"""
        king_piece = copy.deepcopy(piece)
        king_piece = (king_piece[0].replace("P", "K"), king_piece[1], king_piece[2])
        return king_piece


# Board/Piece Info Functions

    def get_pieces(brd, col) -> list[tuple[str, int, int]]:
        """Returns the positions of all owned pieces"""
        pieces = []
        for i in range(8):
            for j in range(8):
                if (brd[i][j][0] == col):  # if piece is right colour
                    pieces.append((brd[i][j], i, j))
        return pieces   


    def get_dirs(name):
        """Output all possible raw directions of a piece"""
        dirs = []
        if name[-1] == 'K':  # piece is king
            dirs = [[-1, -1], [-1, 1], [1, -1], [1, 1]]
        elif name[0] == 'B':  # piece is black
            dirs = [[-1, -1], [-1, 1]]
        else:  # piece is red
            dirs = [[1, -1], [1, 1]]
        return dirs


# Valid Moves Functions

    def get_space_moves(brd, pieces):
        """Returns valid space moves"""
        space_moves = []  # all moves into empty space
        for piece in pieces:
            dirs = get_dirs(piece[0])
            for dir_i, dir_j in dirs:
                new_i = piece[1] + dir_i
                new_j = piece[2] + dir_j
                if (0 <= new_i <= 7) and (0 <= new_j <= 7) and (brd[new_i][new_j] == " "):  # within domain
                    space_moves.append([piece[0], f"{new_i}{new_j}"])  # moves in right format
        return space_moves


    def get_jump_moves(brd, pieces):
        """Returns valid jump moves"""
        jump_moves = []  # all jump moves

        def recursive_jump(brd, piece, jump):
            found_jump = False  # jump found flag
            for dir_i, dir_j in get_dirs(piece[0]):  # iterate through all possible dirs for piece

                # make deep copies of new values
                brd_copy = copy.deepcopy(brd)
                new_jump = copy.deepcopy(jump)

                # locate piece in copy board
                for i in range(8):
                    for j in range(8):
                        if (brd_copy[i][j] == piece[0]):
                            i_cur = i
                            j_cur = j

                # calculate slots before jumps
                pre_i = i_cur + dir_i
                pre_j = j_cur + dir_j

                # calculate jump slots
                new_i = pre_i + dir_i
                new_j = pre_j + dir_j

                # check valid jump conditions
                if (0 <= pre_i <= 7) and (0 <= pre_j <= 7) and (0 <= new_i <= 7) and (0 <= new_j <= 7) \
                and (brd_copy[pre_i][pre_j][0] != piece[0][0]) \
                and (brd_copy[pre_i][pre_j] != ' ') \
                and (brd_copy[new_i][new_j] == ' '):
                    
                    # execute jump on board copy
                    brd_copy[i_cur][j_cur] = ' '
                    brd_copy[pre_i][pre_j] = ' '
                    brd_copy[new_i][new_j] = f'{piece[0]}'

                    new_jump.append(f"{new_i}{new_j}")  # record the jump
                    found_jump = True  # jump was found on this iteration

                    # Special King Case:
                    if (new_i == 0) and (piece[0][0] == "B"):
                        king_piece = make_king(piece)
                        brd_copy[new_i][new_j] = f'{king_piece[0]}'  # update copy board piece
                        recursive_jump(brd_copy, king_piece, new_jump)
                    elif (new_i == 7) and (piece[0][0] == "R"):
                        king_piece = make_king(piece)
                        brd_copy[new_i][new_j] = f'{king_piece[0]}'  # update copy board piece
                        recursive_jump(brd_copy, king_piece, new_jump)
                    else:
                        recursive_jump(brd_copy, piece, new_jump)  # call function normally
            # End of Tree
            if not (found_jump) and (len(new_jump) > 1):
                jump_moves.append(new_jump)  # add jump

        # First Call(s) to recursive function
        for piece in pieces:
            recursive_jump(brd, piece, jump=[piece[0]])
        return jump_moves


    def get_valid_moves(brd, pieces):
        """Returns a 2D list of valid moves"""
        jump_moves = get_jump_moves(brd, pieces)
        if (jump_moves):
            return jump_moves

        space_moves = get_space_moves(brd, pieces)
        if (space_moves):
            return space_moves
        else:
            return [["no","M00V"]]


# Main Function
    valid_moves = get_valid_moves(board, get_pieces(board, colour))

    max_rand = len(valid_moves) - 1
    move = valid_moves[random.randint(0, max_rand)]

    return move  # return the best possible computed move


"""
test_board = [
    ['X', 'R01P', 'X', 'R03P', 'X', 'R05P', 'X', 'R07P'],
    ['R10P', 'X', 'R12P', 'X', 'R14P', 'X', 'R16P', 'X'],
    ['X', 'R21P', 'X', 'R23P', 'X', 'R25P', 'X', 'R27P'],
    [' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X'],
    ['X', ' ', 'X', ' ', 'X', ' ', 'X', ' '],
    ['B50P', 'X', 'B52P', 'X', 'B54P', 'X', 'B56P', 'X'],
    ['X', 'B61P', 'X', 'B63P', 'X', 'B65P', 'X', 'B67P'],
    ['B70P', 'X', 'B72P', 'X', 'B74P', 'X', 'B76P', 'X']
]

test_colour = "B"

print(main(test_board, test_colour))
"""




