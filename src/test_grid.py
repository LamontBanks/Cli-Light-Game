import unittest
from grid import *


class TestGrid(unittest.TestCase):
    
    def setUp(self):
        self.grid = Grid(4, 7)

    def test_get_adjacent_cells(self):
        grid1 = Grid(3, 3)

        # col, row
        actual_adj_coords = self.grid._adjacent_cells_coords(1, 1)
        expected_coords = [
                            (1, 0),
                            (0, 1),
                            (1, 2),
                            (2, 1)
                        ]

        for coord in expected_coords:
            self.assertIn(coord, actual_adj_coords)


if __name__ == "__main__":
    unittest.main()