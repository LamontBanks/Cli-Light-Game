import random

class Grid:
    def __init__(self, col=3, row=5):
        if col < 1 and row < 1:
            raise Exception(f"Both col ({col}) and row ({row}) must be >= 1")
        
        self._num_cols = col
        self._num_rows = row

        self._light_on = 'O'
        self._light_off = '.'

        self.toggle_history = []
        self._full_solution = set()
        
        # Create the grid
        self._grid = [0 for i in range(self._num_cols)]
        for c in range(col):
            self._grid[c] = [self._light_on for i in range(self._num_rows)]

        # Generate the puzzle
        self._set_all_lights_on()
        self.toggle_random_lights()

        # Clear history after setting the grid
        self.toggle_history = []

    def toggle_random_lights(self, num_moves=3):
        for i in range(num_moves):
            random_col = random.randint(0, self._num_cols - 1)
            random_row = random.randint(0, self._num_rows - 1)

            self.toggle_cell(random_col, random_row)

            self._full_solution.add((random_col, random_row))

    """Return a list of tuples containing the adjacent cells col, row coordinates.
        Format: [(col, row), (col, row), etc.]
    Don't rely on the cells being listed in a particular order (i.e., top, bottom, ..., etc.)"""
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
    
    def _set_all_lights_on(self):
        for col in range(self._num_cols):
             for row in range(self._num_rows):
                self._grid[col][row] = self._light_on

    def toggle_cell(self, col, row):
        self._toggle_single_cell(col, row)

        self.toggle_history.append((col, row))

        adj_cells = self._adjacent_cells_coords(col, row)
        for cell in adj_cells:
            adj_col, adj_row = cell
            self._toggle_single_cell(adj_col, adj_row)

    def _toggle_single_cell(self, col, row):
        if (col < 0 or col > self._num_cols - 1) or (row < 0 or row > self._num_rows - 1):
            raise IndexError(f"Invalid grid range: col: {col}, row: {row}")

        if self._grid[col][row] == self._light_on:
            self._grid[col][row] = self._light_off
        else:
            self._grid[col][row] = self._light_on
    
    def undo_last_move(self):
        if len(self.toggle_history) > 0:
            col, row = self.toggle_history.pop()
            self.toggle_cell(col, row)

            return col, row
        return None

    def get_solution(self):
        return list(self._full_solution)

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
