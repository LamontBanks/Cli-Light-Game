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
    
    """Perform random player on the grid"""
    def perform_player_moves(self, grid, num_moves, rand_seed):
        random.seed(rand_seed)
        num_cols, num_rows = grid.dimensions()

        for i in range(num_moves):
            random_col = random.randint(0, num_cols - 1)
            random_row = random.randint(0, num_rows - 1)
            
            grid.player_toggle_cell(random_col, random_row)

        return grid

    """Solved puzzle for test comparisons"""
    def solved_grid(self, num_cols, num_rows):
        solved_grid = Grid(num_cols, num_rows)
        solved_grid._set_all_lights_on()

        return solved_grid

    # Toggle cells tests
    def test_get_adjacent_cells(self):
        # Center cell - all cells returned
        grid3x3 = Grid(3, 3)
        actual_adj_coords = set(grid3x3._adjacent_cells_coords(1, 1))
        expected_coords = set([
                            (1, 0),
                            (0, 1),
                            (1, 2),
                            (2, 1)
                        ])
        self.assertSetEqual(actual_adj_coords, expected_coords)

        # Upper-left corner - right, bottom returned
        actual_adj_coords = set(grid3x3._adjacent_cells_coords(0, 0))
        expected_coords = set([
                            (0, 1),
                            (1, 0)
                        ])
        self.assertSetEqual(actual_adj_coords, expected_coords)

        # Upper-middle cell - left, bottom, right returned
        actual_adj_coords = set(grid3x3._adjacent_cells_coords(1, 0))
        expected_coords = set([
                            (0, 0),
                            (2, 0),
                            (1, 1)
                        ])
        self.assertSetEqual(actual_adj_coords, expected_coords)

        # Upper-left-corner cell - left, bottom returned
        actual_adj_coords = set(grid3x3._adjacent_cells_coords(2, 0))
        expected_coords = set([
                            (1, 0),
                            (2, 1)
                        ])
        self.assertSetEqual(actual_adj_coords, expected_coords)

        # left-middle cell - top, left, bottom returned
        actual_adj_coords = set(grid3x3._adjacent_cells_coords(2, 1))
        expected_coords = set([
                            (2, 0),
                            (1, 1),
                            (2, 2)
                        ])
        self.assertSetEqual(actual_adj_coords, expected_coords)

        # Lower left corner cell - top, left returned
        actual_adj_coords = set(grid3x3._adjacent_cells_coords(2, 2))
        expected_coords = set([
                            (2, 1),
                            (1, 2)
                        ])
        self.assertSetEqual(actual_adj_coords, expected_coords)

        # Lower middle cell - top, left, right returned
        actual_adj_coords = set(grid3x3._adjacent_cells_coords(1, 2))
        expected_coords = set([
                            (0, 2),
                            (1, 1),
                            (2, 2)
                        ])
        self.assertSetEqual(actual_adj_coords, expected_coords)

        # Lower right corner cell - top, right returned
        actual_adj_coords = set(grid3x3._adjacent_cells_coords(0, 2))
        expected_coords = set([
                            (0, 1),
                            (1, 2)
                        ])
        self.assertSetEqual(actual_adj_coords, expected_coords)

        # Left middle cell - top, right, bottom returned
        actual_adj_coords = set(grid3x3._adjacent_cells_coords(0, 1))
        expected_coords = set([
                            (0, 0),
                            (1, 1),
                            (0, 2)
                        ])
        self.assertSetEqual(actual_adj_coords, expected_coords)

        # 1x1 grid, nothing returned
        grid1x1 = Grid(1, 1)
        actual_adj_coords = grid1x1._adjacent_cells_coords(0, 0)
        self.assertEqual(actual_adj_coords, [])

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

    def test_player_toggle_cell(self):
        col = 5
        row = 3
        grid = Grid(col, row)

        grid._set_all_lights_on()

        # Toggle the targeted cell
        toggled_cell_col = 3
        toggled_cell_row = 1
        grid.player_toggle_cell(toggled_cell_col, toggled_cell_row)

        # Player move added to history
        self.assertEqual(grid.history(), [(toggled_cell_col, toggled_cell_row)])

        # Player move is part of the current solution
        self.assertListEqual(grid.get_curr_solution(), [(toggled_cell_col, toggled_cell_row)])

    def test_toggle_cell_group(self):
        col = 5
        row = 3
        grid = Grid(col, row)

        grid._set_all_lights_on()

        # Save state of toggled cell and adjacent cells
        toggled_cell_col = 3
        toggled_cell_row = 1

        # Assert all lights are on
        # Target cell
        self.assertEqual(grid._grid[toggled_cell_col][toggled_cell_row], grid._light_on)
        # Top
        self.assertEqual(grid._grid[toggled_cell_col][toggled_cell_row - 1], grid._light_on)
        # Bottom
        self.assertEqual(grid._grid[toggled_cell_col][toggled_cell_row + 1], grid._light_on)
        # Left
        self.assertEqual(grid._grid[toggled_cell_col - 1][toggled_cell_row], grid._light_on)
        # Right
        self.assertEqual(grid._grid[toggled_cell_col + 1][toggled_cell_row], grid._light_on)

        # Toggle the targeted cell
        grid._toggle_cell_group(toggled_cell_col, toggled_cell_row)

        # Assert expected lights are off
        # Target cell
        self.assertEqual(grid._grid[toggled_cell_col][toggled_cell_row], grid._light_off)
        # Top
        self.assertEqual(grid._grid[toggled_cell_col][toggled_cell_row - 1], grid._light_off)
        # Bottom
        self.assertEqual(grid._grid[toggled_cell_col][toggled_cell_row + 1], grid._light_off)
        # Left
        self.assertEqual(grid._grid[toggled_cell_col - 1][toggled_cell_row], grid._light_off)
        # Right
        self.assertEqual(grid._grid[toggled_cell_col + 1][toggled_cell_row], grid._light_off)

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

    def test_solve_with_no_player_input(self):
        grid = Grid(3, 5)
        grid.create_new_puzzle()
        
        grid.solve_puzzle()
        
        self.assertTrue(grid.is_solved(), f"\nGrid is not solved:\n{grid}")

    def test_solve_after_player_input(self):
        col = 5
        row = 3
        grid = Grid(col, row)
    
        grid.create_new_puzzle()
        
        player_moves = self.list_of_random_moves(col, row, num_moves=5, rand_seed=3)
        for move in player_moves:
            grid.player_toggle_cell(move[0], move[1])

        # Ensure the puzzle isn't already solved from player actions
        self.assertNotEqual(grid, self.solved_grid(col, row))

        # Solve it
        grid.solve_puzzle()
        
        self.assertTrue(grid.is_solved(), f"\nGrid is not solved:\n{grid}")

    def test_undo_last_move(self):
        rand_seed = 8

        # Two grids with the same random seed for assertions
        grid = Grid()
        grid.create_new_puzzle(rand_seed=rand_seed)

        original_grid = Grid()
        original_grid.create_new_puzzle(rand_seed=rand_seed)

        # Undo with no previous moves - no change happens 
        grid.undo_last_move()
        self.assertEqual(grid, original_grid)

        # Undo 1 player move
        self.perform_player_moves(grid, num_moves=1, rand_seed=rand_seed)
        self.assertNotEqual(grid, original_grid)
        
        # Restored
        grid.undo_last_move()
        self.assertEqual(grid, original_grid)

        # Undo 3 player moves
        self.perform_player_moves(grid, num_moves=3, rand_seed=rand_seed)

        grid.undo_last_move()
        self.assertNotEqual(grid, original_grid)

        grid.undo_last_move()
        self.assertNotEqual(grid, original_grid)

        # Restored
        grid.undo_last_move()
        self.assertEqual(grid, original_grid)

# Run single test:
# python3 src/test_grid.py TestGrid.test_undo_last_move
if __name__ == "__main__":
    unittest.main()