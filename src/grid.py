import random
import logging

class Grid:
    def __init__(self, col=5, row=5):
        self._logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG)

        if col < 1 and row < 1:
            raise Exception(f"Both col ({col}) and row ({row}) must be >= 1")
        
        self._num_cols = col
        self._num_rows = row

        self._light_on = 'O'
        self._light_off = '.'

        self.history = []

        # Saves the moves needed to solve the puzzle
        self._original_solution = set()
        
        # Create the grid
        self._logger.info(f"---\nCreating grid, col: {self._num_cols}, row: {self._num_rows}...")
        self._grid = [0 for i in range(self._num_cols)]
        for c in range(col):
            self._grid[c] = [self._light_on for i in range(self._num_rows)]

    def create_new_puzzle(self, num_moves=5):
        self._logger.info(f"Creating puzzle")

        self._set_all_lights_on()
        self.toggle_random_lights(num_moves)
        self.history = []

    def toggle_random_lights(self, num_moves):
        self._logger.debug(f"Toggle random lights")
        for i in range(num_moves):
            random_col = random.randint(0, self._num_cols - 1)
            random_row = random.randint(0, self._num_rows - 1)

            self.toggle_cell(random_col, random_row)

    def _set_all_lights_on(self):
        self._logger.debug(f"Turn all lights on...")
        for col in range(self._num_cols):
             for row in range(self._num_rows):
                self._grid[col][row] = self._light_on

    """Return a list of tuples containing the adjacent cells col, row coordinates.
        Format: [(col, row), (col, row), etc.]
    """
    def _adjacent_cells_coords(self, col, row):
        cells = []

        # left
        if 0 <= col - 1:
            cells.append((col - 1, row))
        # right
        if col + 1 <= self._num_cols - 1:
            cells.append((col + 1, row))
        # top
        if row - 1 >= 0:
            cells.append((col, row - 1))
        # bottom
        if row + 1 <= self._num_rows - 1:
            cells.append((col, row + 1))

        return cells

    def toggle_cell(self, col, row):
        self._logger.info(f"Toggle ({col}, {row})")

        self._toggle_single_cell(col, row)

        # Save history, update solution
        self._logger.debug(f"Save ({col}, {row}) to history")
        self.history.append((col, row))
        self._add_or_remove_coord_from_solution(col, row)

        # Toggle adjacent cells
        adj_cells = self._adjacent_cells_coords(col, row)
        for cell in adj_cells:
            adj_col, adj_row = cell
            self._toggle_single_cell(adj_col, adj_row)

    def _toggle_single_cell(self, col, row):
        if (col < 0 or col > self._num_cols - 1) or (row < 0 or row > self._num_rows - 1):
            raise IndexError(f"Invalid grid range: ({col}, {row})")

        if self._grid[col][row] == self._light_on:
            self._grid[col][row] = self._light_off
        else:
            self._grid[col][row] = self._light_on
    
    def undo_last_move(self):
        self._logger.info(f"Undo last move...")

        if len(self.history) > 0:
            col, row = self.history.pop()
            self._logger.info(f"Undo ({col}, {row})...")
            self.toggle_cell(col, row)

            # TODO - Handle this better
            # toggle() adds the col, row back to history
            # So, remove it a second time
            self.history.pop()

            return col, row
        
        self._logger.info(f"...nothing to undo")
        return None

    def get_solution(self):
        return list(self._original_solution)
    
    """Toggles the cells needed to turn all the lights on"""
    def solve_puzzle(self):
        self._logger.info(f"Solution: {self.get_solution()}")

        sol = self.get_solution()
        if len(sol) > 0:
            for coords in sol:
                self.toggle_cell(coords[0], coords[1])
    
    """Save or remove given coords from the solution"""
    def _add_or_remove_coord_from_solution(self, col, row):
        coord = (col, row)

        if coord in self._original_solution:
            self._logger.debug(f"({col}, {row}) IS in solution, removing it...")
            self._original_solution.remove(coord)
        else:
            self._logger.debug(f"({col}, {row}) NOT in solution, adding it...")
            self._original_solution.add(coord)

        self._logger.debug(f"Updated solution: {self.get_solution()}")

    def is_solved(self):
        # All moves must be done
        if len(self._original_solution) > 0:
            return False
        
        # All lights on
        for c in range(self._num_cols):
            for r in range(self._num_rows):
                if self._grid[c][r] != self._light_on:
                    return False
        
        # Otherwise, puzzle is solved
        return True

    """Grids are equal if:
    - Same dimensions
    - Same lights on off
    """
    def __eq__(self, other):
        if not isinstance(other, Grid):
            return False
        
        if (self._num_cols != other._num_cols) or (self._num_rows != other._num_rows):
            return False

        for c in range(self._num_cols):
            for r in range(self._num_rows):
                if self._grid[c][r] != other[c][r]:
                    return False
        
        return True


    # Print the grid with some formatting
    def __repr__(self):
        repr_str = ""
        col_labels = "   "
        
        # Top column labels, with underline
        for i in range(self._num_cols):
            col_labels += "  " + str(i)
        col_labels += "\n     "
        # "underline"
        for i in range(self._num_cols):
            col_labels += "---"
        # Remove trailing underlines
        col_labels = col_labels[:-2] + "\n"

        repr_str += col_labels

        # Row labels and values
        row = ""
        for r in range(self._num_rows):
            row += f"{str(r)} |"
            for c in range(self._num_cols):
                row += "  " + self._grid[c][r]
            repr_str += row + "\n"
            row = ""

        return repr_str
