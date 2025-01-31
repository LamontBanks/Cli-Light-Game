import random
import unittest

from grid import *


class TestGrid(unittest.TestCase):
    
    def setUp(self):
        pass

    """List of coordinate tuples simulating player toggles (within range)"""
    def list_of_random_moves(self, num_cols, num_rows, num_moves, rand_seed):
        moves = []

        for i in range(num_moves):
            random.seed(rand_seed)
            random_col = random.randint(0, num_cols - 1)
            random_row = random.randint(0, num_rows - 1)

            moves.append(
                (random_col, random_row)
            )

        return moves

    """Solved puzzle for test comparisons"""
    def solved_grid(self, num_cols, num_rows):
        solved_grid = Grid(num_cols, num_rows)
        solved_grid._set_all_lights_on()

        return solved_grid

    # Toggle cells tests
    def test_get_adjacent_cells(self):
        # col, row
        grid1 = Grid(3, 3)
        actual_adj_coords = grid1._adjacent_cells_coords(1, 1)
        expected_coords = [
                            (1, 0),
                            (0, 1),
                            (1, 2),
                            (2, 1)
                        ]

        for coord in expected_coords:
            self.assertIn(coord, actual_adj_coords)

        # col, row
        grid2 = Grid(1, 5)
        actual_adj_coords = grid2._adjacent_cells_coords(0, 2)
        expected_coords = [
                            (0, 1),
                            (0, 3),
                        ]

        for coord in expected_coords:
            self.assertIn(coord, actual_adj_coords)

        # col, row
        grid3 = Grid(1, 1)
        actual_adj_coords = grid3._adjacent_cells_coords(0, 0)
        expected_coords = []

        for coord in expected_coords:
            self.assertListEqual(expected_coords, actual_adj_coords)

    def test_toggle_cell_index_error(self):
        grid1 = Grid(3, 3)

        with self.assertRaises(IndexError):
            grid1._toggle_single_cell(-1, 0)

        with self.assertRaises(IndexError):
            grid1._toggle_single_cell(0, -1)

        with self.assertRaises(IndexError):
            grid1._toggle_single_cell(4, 0)

        with self.assertRaises(IndexError):
            grid1._toggle_single_cell(0, 4)

        with self.assertRaises(IndexError):
            grid1._toggle_single_cell(-1, 4)

    # Grid creation and reset
    def test_create_new_puzzle(self):
        col = 3
        row = 5
        grid = Grid(col, row)

        grid.create_new_puzzle(rand_seed=7)

        # Not already solved (ultimately depends on random seed)
        self.assertNotEqual(grid, self.solved_grid(col, row))

        # Empty player move history
        self.assertEqual(grid.history(), [])

        # At least 1 move required to solve
        self.assertGreaterEqual(len(grid._original_solution), 1)

        # Current solution set equal to the original solution
        self.assertEqual(grid._original_solution, grid._curr_solution)

    def test_reset(self):
        col = 3
        row = 5
        grid = Grid(col, row)
        grid.create_new_puzzle(rand_seed=7)

        # Save grid state
        saved_original_grid = grid._grid

        # Player does some moves
        player_moves = self.list_of_random_moves(
            col, row, 5, rand_seed=11
        )
        for move in player_moves:
            c, r = move
            grid.player_toggle_cell(c, r)

        # Reset grid
        grid.reset()

        # Current grid re-initailized to original
        self.assertEqual(grid._grid, saved_original_grid)
        # Clear history  
        self.assertEqual(grid.history(), [])
        # Current solution re-initialized
        self.assertEqual(grid._curr_solution, grid._original_solution)

    def test_solve(self):
        grid = Grid(2, 2)
        grid.create_new_puzzle()
        
        grid.solve_puzzle()
        
        self.assertTrue(grid.is_solved(), f"\nGrid is not solved:\n{grid}")

# Run single test:
# $ python3 src/test_grid.py TestGrid.test_reset
if __name__ == "__main__":
    unittest.main()