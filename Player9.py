_author_ = "Rehan Jetha"
_date_ = "Wed, Nov 22nd, 2023"
_version_ = "5.0"
_filename_ = "Player9.py"
_description_ = "Zeus Checkers AI by Rehan Jetha"

import copy

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
        """Returns all pieces of a given colour"""
        pieces = []
        for i in range(8):
            for j in range(8):
                if (brd[i][j][0] == col):  # if piece is right colour
                    pieces.append((brd[i][j], i, j))
        return pieces   
    

    def get_pieces_amt(brd):
        """Returns # of pieces of both colours"""
        b_amt = 0
        r_amt = 0
        for i in range(8):
            for j in range(8):
                if (brd[i][j] != " ") and (brd[i][j] != "X"):
                    if (brd[i][j][0] == "B"):  # max colour
                        b_amt += 1
                    else:
                        r_amt += 1
        return b_amt, r_amt


    def get_dirs(name):
        """Outputs all raw directions of a given piece"""
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
        """Returns valid moves into empty space"""
        space_moves = []
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
        jump_moves = []

        def recursive_jump(brd, piece, jump):
            found_jump = False
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
        """Returns all valid moves abiding by rules"""
        jump_moves = get_jump_moves(brd, pieces)
        if (jump_moves):
            jump_moves = sorted(jump_moves, key=lambda x: len(x), reverse=True)  # sort by longest
            return jump_moves

        space_moves = get_space_moves(brd, pieces)
        if (space_moves):
            return space_moves
        else:
            return [["no","M00V"]]


# Minimax Dependencies

    def get_score(brd, col):
        """Returns a heuristic evaluation of board"""
        pts = 0
        for i in range(8):
            for j in range(8):
                if (brd[i][j] != " ") and (brd[i][j] != "X"):
                    piece = brd[i][j]  # selected piece

                    # Piece Weight
                    if (piece[0] == col):  # max colour
                        pts += 10
                    else:  # min colour
                        pts -= 10

                    # King Weight
                    if (piece[-1] == "K"):
                        if (piece[0] == col):  # your kings
                            pts += 10
                        else:
                            pts -= 10

                    # Promotional Weight
                    if (piece[0] == "B"):
                        prom_weight = (7-i)
                    else:
                        prom_weight = i
                    if (piece[0] == col):
                        pts += prom_weight

                    # Dynamic Center Weight
                    cent_r = 3.5
                    cent_c = 3.5
                    dist_cent = abs(i - cent_r) + abs(j - cent_c)
                    cent_weight = max(0, 3 - dist_cent)
                    if (piece[0] == col):
                        pts += cent_weight

                    # Direct Center Weight
                    if (piece[0] == col) and (3 <= i <= 4):
                        pts += 3

                    # Edge Control Weight
                    if (j == 0) or (j == 7):
                        if (piece[0] == col):
                            pts += 2
                        else:
                            pts -= 2
        return pts


    def sim_move(brd, mv):
        """Returns a board copy w/simulated move"""

        # copy items
        sim_board = copy.deepcopy(brd)
        move_copy = copy.deepcopy(mv)

        # make move easier to use
        move_idxs = []
        for idx, move in enumerate(move_copy):
            if (idx == 0):  # skip first idx
                continue
            
            i, j = map(int, move)
            move_idxs.append([i, j])

        # difference between i & js
        for i, j in move_idxs:

            # locate piece in copy board
            for x in range(8):
                for y in range(8):
                    if (sim_board[x][y] == move_copy[0]):
                        cur_i = x
                        cur_j = y
            
            # calculate diffs for idxs
            diff_i = i - cur_i
            diff_j = j - cur_j

            # Jump / Space Move
            if (abs(diff_i) > 1) and (abs(diff_j) > 1):  # jump
                # capture slot is just diff_i, diff_j, execute jump
                cap_i = cur_i + (diff_i/abs(diff_i))
                cap_j = cur_j + (diff_j/abs(diff_j))

                cap_i = int(cap_i)
                cap_j = int(cap_j)

                sim_board[cap_i][cap_j] = ' '
                sim_board[cur_i][cur_j] = ' '
                sim_board[i][j] = f'{move_copy[0]}'
            else:  # space move
                sim_board[cur_i][cur_j] = ' '
                sim_board[i][j] = f'{move_copy[0]}'

            # Special King Case
            if (i == 0) and (move_copy[0][0] == "B"):
                sim_board[i][j] = f'{move_copy[0].rstrip(move_copy[0][-1])}K'  # update copy board piece
            elif (i == 7) and (move_copy[0][0] == "R"):
                sim_board[i][j] = f'{move_copy[0].rstrip(move_copy[0][-1])}K'  # update copy board piece
        return sim_board


# Full Minimax Algorithm

    def minimax(brd, depth, max_player, col, alpha, beta):
        """Minimax AI w/Alpha Beta Pruning"""

        b_pieces, r_pieces = get_pieces_amt(brd)
        if (depth == 0) or (b_pieces == 0) or (r_pieces == 0):
            return get_score(brd, col), ["no","M00V"]
        
        if (max_player):  # is max player
            max_val = float('-inf')
            best_move = None
            valid_moves = get_valid_moves(brd, get_pieces(brd, col))
            if (valid_moves == [["no","M00V"]]):
                return [max_val, ["no","M00V"]]
                
            for move in valid_moves:
                val = minimax(sim_move(brd, move), depth-1, False, col, alpha, beta)[0]
                max_val = max(max_val, val)
                alpha = max(alpha, max_val)
                if (alpha >= beta):  # prune max values
                    break
                if (max_val == val):
                    best_move = move
            return max_val, best_move
        
        else:  # not max player
            min_val = float('inf')
            best_move = None

            opp_col = "R" if (col == "B") else "B"

            valid_moves = get_valid_moves(brd, get_pieces(brd, opp_col))
            if (valid_moves == [["no","M00V"]]):
                return [min_val, ["no","M00V"]]
            
            for move in valid_moves:
                val = minimax(sim_move(brd, move), depth-1, True, col, alpha, beta)[0]
                min_val = min(min_val, val) 
                beta = min(beta, min_val)
                if (alpha >= beta):  # prune min values
                    break
                if (min_val == val):
                    best_move = move
            return min_val, best_move

# Main Function

    og_board = [
        ['X', 'R01P', 'X', 'R03P', 'X', 'R05P', 'X', 'R07P'],
        ['R10P', 'X', 'R12P', 'X', 'R14P', 'X', 'R16P', 'X'],
        ['X', 'R21P', 'X', 'R23P', 'X', 'R25P', 'X', 'R27P'],
        [' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', 'X', ' ', 'X', ' '],
        ['B50P', 'X', 'B52P', 'X', 'B54P', 'X', 'B56P', 'X'],
        ['X', 'B61P', 'X', 'B63P', 'X', 'B65P', 'X', 'B67P'],
        ['B70P', 'X', 'B72P', 'X', 'B74P', 'X', 'B76P', 'X']
    ]

    best_val, move = minimax(board, 4, True, colour, float('-inf'), float('inf'))


    # Re-write first move to Old Faithful
    if (board == og_board):
        if (move == ['B56P', '47']):
            move = ['B52P', '43']
        elif (move == ['R27P', '36']):
            move = ['R25P', '34']

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




