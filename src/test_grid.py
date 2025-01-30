import unittest
from grid import *


class TestGrid(unittest.TestCase):
    
    def setUp(self):
        pass

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
            grid1.toggle_cell(-1, 0)

        with self.assertRaises(IndexError):
            grid1.toggle_cell(0, -1)

        with self.assertRaises(IndexError):
            grid1.toggle_cell(4, 0)

        with self.assertRaises(IndexError):
            grid1.toggle_cell(0, 4)

        with self.assertRaises(IndexError):
            grid1.toggle_cell(-1, 4)

    def test_solution_solves_grid(self):
        grid = Grid(2, 2)
        grid.create_new_puzzle()
        
        grid.solve_puzzle()
        
        self.assertTrue(grid.is_solved(), f"\nGrid is not solved:\n{grid}")

# Run single test:
# $ python3 src/test_grid.py TestGrid.test_solution_solves_grid
if __name__ == "__main__":
    unittest.main()