import re

from grid import Grid

# Create grid
grid = Grid()
grid.create_new_puzzle(num_random_toggles=4)

# Commands
cmd_undo = ['undo', 'u']
cmd_solution = ['solution']
cmd_solve = ['solve']
cmd_reset = ['reset']
cmd_new = ['new', 'n']
cmd_quit = ['quit', 'exit']
cmd_history = ['history', 'h']
cmd_hint = ['hint']

# Game loop flags
display_solution = False
curr_solution = ""
display_history = False
display_coord_hint = False

while True:
    # Instructions
    print('\n')
    print(grid)
    print(f">>> Turn on all the lights! <<<")
    print("Adjacent lights (up, down, left, right) will flip on/off at the same time.")
    print("Enter the col, row, ex: 3, 5\n")

    # Commands
    print(f"\t\t\tCommands:")

    ## Undo
    print(f"Undo: {cmd_undo}\tReset: {cmd_reset}\tNew Puzzle: {cmd_new}")

    ## History
    if display_history:
        print(f"History: {grid.history()}")
    else:
        print(f"History: {cmd_history}")

    ## Solve
    print(f"Solve: {cmd_solve}")

    ## Quit
    print(f"Quit: {cmd_quit}")

    ## Hint
    # Always show the number of moves remaining
    # Only show next coordinate if requested
    hint = grid.hint()
    hint_coord, num_moves_left = hint
    hint_num_moves_left = f"Lights remaining: {str(num_moves_left)}"

    if display_coord_hint:
       print(f"> {hint_num_moves_left}, next light: {hint_coord}")
    else:
        print(f"> {hint_num_moves_left}, {cmd_hint} to show next light")

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

            # Disable the coordinate hint if entered
            if hint_coord:
                if col == hint_coord[0] and row == hint_coord[1]:
                    display_coord_hint = False
            
            # End the game if the grid is solved
            if grid.is_solved():
                print(grid)
                print("Grid solved")
                break

        except IndexError:
            print(f"==> Invalid col: {col}, row: {row}")

    elif command in cmd_undo:
        last_coords = grid.undo_last_move()
        if last_coords != None:
            print(f"==> Reverted col: {last_coords[0]}, row: {last_coords[1]}")
            last_coords = None

    elif command in cmd_solution:
        display_solution = True

    # Shows next light location
    elif command in cmd_hint:
        display_coord_hint = True

    elif command in cmd_solve:
        sol = grid.get_curr_solution()
        if len(sol) > 0:
            for coords in sol:
                grid.player_toggle_cell(coords[0], coords[1])

    elif command in cmd_reset:
        grid.reset()

        display_solution = False
        display_hint = False
        display_history = False

        curr_hint = ""
        curr_solution = ""

    elif command in cmd_history:
        display_history = True

    elif command in cmd_new:
        grid.create_new_puzzle()

        display_solution = False
        display_hint = False
        display_history = False

        curr_hint = ""
        curr_solution = ""

    elif command in cmd_quit:
        break

    else:
        continue