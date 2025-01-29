class Grid:

    def __init__(self, col=5, row=8):
        if col < 1 and row < 1:
            raise Exception(f"Both col ({col}) and row ({row}) must be >= 1")
        
        self._num_cols = col
        self._num_rows = row
        
        # Create the grid
        self._grid = [0 for i in range(self._num_cols)]
        for c in range(col):
            self._grid[c] = [0 for i in range(self._num_rows)]

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
    
    """Set all cells to 0"""
    def _reset_grid(self):
        for col in range(self._num_cols):
             for row in range(self._num_rows):
                self.grid[col][row] = 0

    """Flips given cell and its adjacent cells from 1 to 0, or 0 to 1"""
    def toggle_cell(self, col, row):
        if (col < 0 or col > self._num_cols - 1) or (row < 0 or row > self._num_rows - 1):
            raise IndexError(f"Invalid grid range: col: {col}, row: {row}")
        

    
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
                row += "  " + str(self._grid[c][r])
            repr_str += row + "\n"
            row = ""

        return repr_str
