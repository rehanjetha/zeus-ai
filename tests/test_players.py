import copy
import unittest
from unittest.mock import patch

import Player9
import PlayerRandom


def empty_board():
    return [["X" if (row + col) % 2 == 0 else " " for col in range(8)] for row in range(8)]


class PlayerTests(unittest.TestCase):
    def test_zeus_takes_forced_jump(self):
        board = empty_board()
        board[5][4] = "B54P"
        board[4][3] = "R43P"

        self.assertEqual(Player9.main(copy.deepcopy(board), "B"), ["B54P", "32"])

    def test_zeus_does_not_mutate_input_board(self):
        board = empty_board()
        board[5][4] = "B54P"
        board[4][3] = "R43P"
        original = copy.deepcopy(board)

        Player9.main(board, "B")

        self.assertEqual(board, original)

    def test_zeus_reports_when_no_move_exists(self):
        board = empty_board()
        board[0][1] = "B01P"
        board[7][0] = "R70P"

        self.assertEqual(Player9.main(board, "B"), ["no", "M00V"])

    def test_random_player_can_return_deterministic_space_move(self):
        board = empty_board()
        board[5][4] = "B54P"

        with patch("PlayerRandom.random.randint", return_value=0):
            self.assertEqual(PlayerRandom.main(board, "B"), ["B54P", "43"])


if __name__ == "__main__":
    unittest.main()
