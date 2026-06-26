import Player9
import PlayerRandom
import copy
import time

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
test_colour = ["R", "B"]
board_pass = copy.deepcopy(test_board)

Player1 = Player9
Player2 = PlayerRandom

# Settings
games = 100

# Counters
p1_w = 0
p2_w = 0
moves = 0
draws = 0


def sim_move(brd, mv):
    """Return a board copy w/simulated move"""

    # copy items
    move_copy = copy.deepcopy(mv)

    # make move easier to use
    move_idxs = []
    if (move_copy == None):
        return brd
    for idx, move in enumerate(move_copy):
        if (idx == 0):  # skip first idx
            continue
        elif (move_copy == ["no","M00V"]):
            return brd
        
        i, j = map(int, move)
        move_idxs.append([i, j])

    # difference between i & js
    for i, j in move_idxs:

        # locate piece in copy board
        for x in range(8):
            for y in range(8):
                if (brd[x][y] == move_copy[0]):
                    cur_i = x
                    cur_j = y
        
        # calculate diffs for idxs
        diff_i = i - cur_i
        diff_j = j - cur_j

        # Jump / Space Move
        if (abs(diff_i) == 2) and (abs(diff_j) == 2):  # jump
            cap_i = cur_i + (diff_i/abs(diff_i))
            cap_j = cur_j + (diff_j/abs(diff_j))
            cap_i = int(cap_i)
            cap_j = int(cap_j)
            brd[cap_i][cap_j] = ' '
            brd[cur_i][cur_j] = ' '
            brd[i][j] = f'{move_copy[0]}'
        else:  # space move
            brd[cur_i][cur_j] = ' '
            brd[i][j] = f'{move_copy[0]}'

        # Special King Case
        if (i == 0) and (move_copy[0][0] == "B"):
            brd[i][j] = f'{move_copy[0].rstrip(move_copy[0][-1])}K'  # update copy board piece
        elif (i == 7) and (move_copy[0][0] == "R"):
            brd[i][j] = f'{move_copy[0].rstrip(move_copy[0][-1])}K'  # update copy board piece
    return brd

gm_count = 0
start_time = time.time()
for game_num in range(games):


    game_done = False
    moves = 0
    board_pass = copy.deepcopy(test_board)

    while not game_done:
        player9_move = Player1.main(board_pass, test_colour[0])
        if (player9_move == ["no","M00V"]):
            p2_w += 1
            game_done = True
            gm_count += 1
            print(f"\nGame {gm_count} done.\nP1W: {p1_w}\nP2W: {p2_w}\nDraws: {draws}\n")
            continue
        else:
            sim_move(board_pass, player9_move)
            moves += 1


        random_move = Player2.main(board_pass, test_colour[1])
        if (random_move == ["no","M00V"]):
            p1_w += 1
            game_done = True
            gm_count += 1
            print(f"\nGame {gm_count} done.\nP1W: {p1_w}\nP2W: {p2_w}\nDraws: {draws}\n")
            continue
        else:
            sim_move(board_pass, random_move)
            moves += 1

        if (moves >= 400):
            draws += 1
            game_done = True
            gm_count += 1
            print(f"\nGame {gm_count} done.\nP1W: {p1_w}\nP2W: {p2_w}\nDraws: {draws}\n")
            continue

end_time = time.time()
elap_time = start_time - end_time

print('Player 1 Wins: ', p1_w)
print('Player 2 Wins: ', p2_w)
print('Draws: ', draws)
print(f"Elapsed Time: {elap_time:.6f} seconds")

      


