import random
import logging

class Grid:
    def __init__(self, col=5, row=5):
        self._logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.CRITICAL)

        if col < 1 and row < 1:
            raise Exception(f"Both col ({col}) and row ({row}) must be >= 1")
        
        self._num_cols = col
        self._num_rows = row
        self._light_on = 'O'
        self._light_off = '.'
        self._history = []

        # Saves the coordinates used to generate the puzzle, and the current solution based on the player inputs
        # The current solution will initially contain the original coordinates used to create the puzzle
        # But, it'll also include additional, unique coordinates the player tries.
        #
        # If the player enters a coordinate that's part of the current solution, the coordinate is removed from the set.
        # This brings the game closes to completion.
        # Meaning, the player must undo all the original steps - plus any others - to solve the puzzle 
        self._original_solution = set()
        self._curr_solution = set()

        # Copy of the original grid for game reset, etc.
        self._original_grid = []
        
        # Create the grid
        self._logger.info(f"Creating grid, col: {self._num_cols}, row: {self._num_rows}...")
        self._grid = [0 for i in range(self._num_cols)]
        for c in range(col):
            self._grid[c] = [self._light_on for i in range(self._num_rows)]

    """num_moves is NOT guaranteed to create a grid requiring x moves to solve"""
    def create_new_puzzle(self, num_random_toggles=5, rand_seed=None):
        self._logger.info(f"Creating puzzle")
        
        # Initial state
        self._set_all_lights_on()

        # Toggle random lights, save solution
        if rand_seed:
            random.seed(rand_seed)

        # TODO - Too few moves and a smale grid size means it's likely for the grid to result in the original state (all lights on)
        # Implement some guard against this
        for i in range(num_random_toggles):
            random_col = random.randint(0, self._num_cols - 1)
            random_row = random.randint(0, self._num_rows - 1)

            self._toggle_cell_group(random_col, random_row)
            self._add_or_remove_coord_from_set(random_col, random_row, self._original_solution)

        # Clear history
        self._history = []
        self._curr_solution = self._original_solution.copy()
        self._original_grid = self._grid.copy()

    """Sets the puzzle to the original state"""
    def reset(self):
        self._logger.info(f"Resetting puzzle")

        self._grid = self._original_grid.copy()
        self._curr_solution = self._original_solution.copy()
        self._history = []

    def _set_all_lights_on(self):
        self._logger.debug(f"Turn all lights on...")
        for col in range(self._num_cols):
             for row in range(self._num_rows):
                self._grid[col][row] = self._light_on

    def player_toggle_cell(self, col, row):
        self._logger.info(f"Toggle cell: ({col}, {row})")
        self._toggle_cell_group(col, row)

        # Save history, update attempted solution
        self._history.append((col, row))
        self._add_or_remove_coord_from_set(col, row, self._curr_solution)

    def _toggle_cell_group(self, col, row):
        self._logger.debug(f"Toggle cell group: ({col}, {row})")
        self._toggle_single_cell(col, row)
        self._toggle_adjacent_cells(col, row)

    def _toggle_single_cell(self, col, row):
        self._logger.debug(f"Toggle single cell: ({col}, {row})")

        if (col < 0 or col > self._num_cols - 1) or (row < 0 or row > self._num_rows - 1):
            raise IndexError(f"Invalid grid range: ({col}, {row})")
        if self._grid[col][row] == self._light_on:
            self._grid[col][row] = self._light_off
        else:
            self._grid[col][row] = self._light_on

    def _toggle_adjacent_cells(self, col, row):
        self._logger.info(f"Toggle cells adjacent to: ({col}, {row})")

        adj_cells = self._adjacent_cells_coords(col, row)
        for cell in adj_cells:
            adj_col, adj_row = cell
            self._toggle_single_cell(adj_col, adj_row)

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
    
    def undo_last_move(self):
        self._logger.info(f"Undo last move")

        if len(self._history) > 0:
            col, row = self._history.pop()
            self._logger.info(f"Undo ({col}, {row})...")
            self._toggle_cell_group(col, row)
            self._add_or_remove_coord_from_set(col, row, self._curr_solution)

            return col, row
        
        return None

    def _get_solution(self):
        self._logger.debug(f"Get original solution:")
        return list(self._original_solution)
    
    def history(self):
        return self._history
    
    def get_curr_solution(self):
        self._logger.info(f"Get current solution:")
        return list(self._curr_solution)
    
    """Toggles the cells needed to turn all the lights on"""
    def solve_puzzle(self):
        self._logger.info(f"Solving puzzle using solution: {self.get_curr_solution()}")

        sol = self.get_curr_solution()
        if len(sol) > 0:
            for coords in sol:
                col, row = coords
                self._toggle_cell_group(col, row)
                self._add_or_remove_coord_from_set(col, row, self._curr_solution)
    
    """For the given coord, add to the given set if not present. Or remove from set if present"""
    def _add_or_remove_coord_from_set(self, col, row, sol_set):
        coord = (col, row)

        if coord in sol_set:
            self._logger.debug(f"Toggled cell ({col}, {row}) IS in set, removing it...")
            sol_set.remove(coord)
        else:
            self._logger.debug(f"Toggled cell ({col}, {row}) NOT in set, adding it...")
            sol_set.add(coord)

        self._logger.debug(f"Updated set: {sol_set}")

    def is_solved(self):
        # All moves must be done
        if len(self._curr_solution) > 0:
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
                if self._grid[c][r] != other._grid[c][r]:
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
