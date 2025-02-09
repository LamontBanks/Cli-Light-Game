import random
import logging

class Grid:
    def __init__(self, col=3, row=4):
        self._logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.CRITICAL)

        if col < 1 and row < 1:
            raise Exception(f"Both col ({col}) and row ({row}) must be >= 1")
        
        self._num_cols = col
        self._num_rows = row
        self._light_on = 'O'
        self._light_off = '·'   # Mac: Shift+Option+9
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

    def create_new_puzzle(self, num_random_toggles=None, rand_seed=None):
        self._logger.info(f"Creating puzzle")

        if not num_random_toggles:
            num_random_toggles = (self._num_cols * self._num_rows) // 4
        
        # Initial state
        self._set_all_lights_on()
        self._original_solution = set()

        # Toggle random lights, save solution
        random.seed(rand_seed)

        # .pop() random coordinates from col and row sets
        col_values = [x for x in range(self._num_cols)]
        row_values = [x for x in range(self._num_rows)]

        for i in range(num_random_toggles):
            # Reset values if needed
            if len(col_values) == 0:
                col_values = [x for x in range(self._num_cols)]
            if len(row_values) == 0:
                row_values = [x for x in range(self._num_rows)]

            random_col = col_values.pop(random.randrange(0, len(col_values)))
            random_row = row_values.pop(random.randrange(0, len(row_values)))

            self._toggle_cell_group(random_col, random_row)
            self._add_or_remove_coord_from_set(random_col, random_row, self._original_solution)

        # Clear history and solution
        self._history = []
        self._curr_solution = self._original_solution.copy()

        # Save a copy of the created grid
        self._original_grid = []
        for column in self._grid:
            self._original_grid.append(column.copy())

    """Sets the puzzle to the original state"""
    def reset(self):
        self._logger.info(f"Resetting puzzle")

        self._grid = []
        for column in self._original_grid:
            self._grid.append(column.copy())

        self._curr_solution = self._original_solution.copy()
        self._history = []

    def _set_all_lights_on(self):
        self._logger.debug(f"Turn all lights on...")
        for col in range(self._num_cols):
             for row in range(self._num_rows):
                self._grid[col][row] = self._light_on

    """Used by the player - toggles the cell, but also updates the current solution and history"""
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
    
    """Returns the step-by-step string of the solution. Solves the puzzle"""
    def solution_steps_str(self):
        steps = ""
        solution = self.get_curr_solution()

        if len(solution) == 0:
            return self.__repr__()
    
        for coords in solution:
            col, row = coords

            # Save initial state
            original_grid_state = []
            for column in self._grid:
                original_grid_state.append(column.copy())

            # Toggle the cell
            self._toggle_cell_group(col, row)
            self._add_or_remove_coord_from_set(col, row, self._curr_solution)
            
            # Save next state
            next_grid_state = []
            for column in self._grid:
                next_grid_state.append(column.copy())

            # Get transtion, add to result string
            steps += self._grid_transtion_repr(original_grid_state, next_grid_state, label=f"Step: {coords[0], coords[1]}", highlight_first_grid_cell_coord=coords)
            steps += "\n"

        return steps
    
    def history(self):
        return self._history
    
    def get_curr_solution(self):
        self._logger.info(f"Get current solution:")
        return list(self._curr_solution)
    
    """Returns a random coordinate tuple from the current solution, and the number of moves remaining (including the displayed hint)
    Ex: ((3, 5), 2)
    Ex: (None, 0)
    """
    def hint(self):
        try:
            num_moves_left = len(self._curr_solution)
            rand_coord = self._curr_solution.pop()
            
            hint = (rand_coord, num_moves_left)

            # set.pop() removes item; put the coordinate back
            self._curr_solution.add(rand_coord)
            
            return hint
        except KeyError:
            return (None, 0)
    
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
    
    """Num columns, num rows"""
    def dimensions(self):
        return self._num_cols, self._num_rows

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
        col_labels = "\n   "
        
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
    
    """Prints this grid (__repr__) followed by a second grid.
    Can provide an optional label (ex: coordinates) to display between the grids
    Inputs: 
    grid1 - The underlying grid (ex, self._grid)
    grid2 - The underlying grid, usually taken after a cell has been toggled
    label (optional) - str to display between grids, usually indicating the action taken
    highlight_first_grid_cell_coord (optional) - (int, int) col, row tuple in the first grid to "highlight" with a different symbol, ex: X

    Ex:

    (1, 2)
        0 ›1  2  3            0  1  2  3
        ----------            ----------
    0 | ·  ·  ·  O       0 |  ·  ·  ·  O
    1 | ·  O  ·  ·       1 |  ·  ·  ·  ·
    2›| ·  X  O  ·  -->  2 |  O  O  ·  ·
    3 | O  ·  ·  ·       3 |  O  O  ·  ·
    """
    def _grid_transtion_repr(self, grid1, grid2, label="", highlight_first_grid_cell_coord=None):
        repr_str = ""
        grid_space_sep = " "

        grid1_num_cols = len(grid1)
        grid1_num_rows = len(grid1[0])

        grid2_num_cols = len(grid2)
        grid2_num_rows = len(grid2[0])

        grid_space_sep = "       "
        grid_transition_arrow = "  -->  "

        # Label as the first line, if provided
        col_labels = ""
        if label != "":
            col_labels += "- " + label + "\n"
        
        ### First grid column labels
        col_label_indent = "   "
        col_labels += "\n" + col_label_indent
        for i in range(grid1_num_cols):
            if highlight_first_grid_cell_coord != None:
                if i == highlight_first_grid_cell_coord[0]:
                    col_labels += " ›" + str(i)
                else:
                    col_labels += "  " + str(i)
            else:
                col_labels += "  " + str(i)

        # Second grid column labels
        col_labels += grid_space_sep + col_label_indent
        for i in range(grid2_num_cols):
            col_labels += "  " + str(i)

        ### Column underline for first grid...
        col_underline_indent = "     "
        col_labels += "\n" + col_underline_indent
        for i in range(grid1_num_cols):
            col_labels += "---"
        # Remove trailing underlines
        col_labels = col_labels[:-2]
        
        # Column underline for the second grid...
        col_labels += grid_space_sep + col_underline_indent
        for i in range(grid2_num_cols):
            col_labels += "---"
        # Remove trailing underlines
        col_labels = col_labels[:-2] + "\n"

        repr_str += col_labels

        ### Rows
        # Determine max number of rows to draw
        # For the grid with fewer rows, insert spaces to preserve formatting
        max_num_rows = max(grid1_num_rows, grid2_num_rows)

        # Insert arrow on middle row of the grid with fewer rows
        arrow_row_index = None
        min_row_count = min(grid1_num_rows, grid2_num_rows)
        arrow_row_index = (min_row_count // 2)
        
        row = ""
        for r in range(max_num_rows):
            ### First grid row labels and values
            if r < grid1_num_rows:
                # Label
                if highlight_first_grid_cell_coord != None:
                    if r == highlight_first_grid_cell_coord[1]:
                        row += f"{str(r)}›|"
                    else:
                        row += f"{str(r)} |"
                else:
                    row += f"{str(r)} |"
                # Values
                for c in range(grid1_num_cols):
                    # Draw special symbol, or original value
                    if highlight_first_grid_cell_coord != None:
                        if c == highlight_first_grid_cell_coord[0] and r == highlight_first_grid_cell_coord[1]:
                            row += "  " + "X"
                        else:
                            row += "  " + grid1[c][r]
                    else:
                        row += "  " + grid1[c][r]
            # Or, whitespace
            else:
                row += col_label_indent
                for c in range(grid1_num_cols + 1):
                    row += "   "
                # Remove trailing whitespace
                row = row[:-3]

            ### Add arrow or whitespace after grid rows
            if r == arrow_row_index:
                row += grid_transition_arrow
            else:
                row += grid_space_sep

            ### Second grid labels and values
            if i < grid2_num_rows:
                # Label
                row += f"{str(r)} |"
                # Values
                for c in range(grid1_num_cols):
                    row += "  " + grid2[c][r]

            repr_str += row + "\n"
            # Clear row for the next values
            row = ""

        return repr_str

grid = Grid()
grid.create_new_puzzle()

print(grid.solution_steps_str())
