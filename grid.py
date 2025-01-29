class Grid:

    def __init__(self, col=5, row=8):
        if col <= 1 and row <= 1:
            raise Exception(f"Both col ({col}) and row ({row}) must be >= 1")
        
        self._num_cols = col
        self._num_rows = row
        
        # Create the grid
        self._grid = [0 for i in range(self._num_cols)]
        for c in range(col):
            self._grid[c] = [0 for i in range(self._num_rows)]

    
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
