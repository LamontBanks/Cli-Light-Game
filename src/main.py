import re

from grid import Grid

# Create grid
grid = Grid(5, 5)
grid.create_new_puzzle(num_moves=10)

# Commands
cmd_undo = ['u', 'undo']
cmd_solution = ['solution']
cmd_solve = ['solve']
cmd_reset = ['reset']
cmd_new = ['n', 'new']
cmd_history = ['h', 'history']

# Game loop flags
display_solution = False
display_history = False

while True:
    # Instructions
    print('\n')
    print(grid)
    print("Instructions - turn on all the lights")
    print("> Enter the col, row - format: 3, 5")
    print("Commands:")
    print(f"> Undo: {cmd_undo}")
    print(f"> Solution: {cmd_solution}")
    print(f"> Solve: {cmd_solve}")
    print(f"> New Puzzle: {cmd_new}")

    # Persistently show solution, history after asked for
    if display_history:
       print(f"> History: {grid.history}")
    else:
        print(f"> History: {cmd_history}")

    if display_solution:
       print(f"> Solution: {grid.get_curr_solution()}")
    else:
        print(f"> Solution: {cmd_solution}")

    print('---')

    # Read command
    command = input('Enter coordinates or command: ')

    # Toggle cell
    # TODO: Couldn't do re.match in case statements?
    if (re.match(r"\s*\d+\s*,\s*\d+\s*", command)):
        coords_input = command.split(',')
        col = int(coords_input[0])
        row = int(coords_input[1])

        print(f"Entered col: {col}, row: {row}")

        try:
            grid.player_toggle_cell(col, row)
        except IndexError:
            print(f"==> Invalid col: {col}, row: {row}")

    elif command in cmd_undo:
        last_coords = grid.undo_last_move()
        if last_coords != None:
            print(f"==> Reverted col: {last_coords[0]}, row: {last_coords[1]}")
            last_coords = None

    elif command in cmd_solution:
        display_solution = True

    elif command in cmd_solve:
        sol = grid.get_curr_solution()
        if len(sol) > 0:
            for coords in sol:
                grid.toggle_cell(coords[0], coords[1])

    elif command in cmd_reset:
        grid.reset()
        display_solution = False

    elif command in cmd_history:
        display_history = True

    elif command in cmd_new:
        grid.create_new_puzzle()
        display_solution = False

    else:
        continue