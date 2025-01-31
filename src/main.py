import re

from grid import Grid

# Create grid
grid = Grid(5, 5)
grid.create_new_puzzle(num_random_toggles=10)

# Commands
cmd_undo = ['u', 'undo']
cmd_solution = ['solution']
cmd_solve = ['solve']
cmd_reset = ['reset']
cmd_new = ['new']
cmd_quit = ['quit', 'exit']
cmd_history = ['h', 'history']
cmd_hint = ['hint']

# Game loop flags
display_solution = False
display_history = False
display_hint = False
curr_hint = []

def toggle_flag(flag):
    if flag == True:
        flag == False
    else:
        flag = True

while True:
    # Instructions
    print('\n')
    print(grid)
    print(f">>> Turn on all the lights! <<<")
    print("Adjacent lights (up, down, left, right) will flip on/off")
    print("Enter the col, row, ex: 3, 5\n")
    print(f"\t\t\tCommands:")
    print(f"Undo: {cmd_undo}\tReset: {cmd_reset}\tNew Puzzle: {cmd_new}")

    if display_hint:
        print(f"Hint: {curr_hint}")
    else:
        print(f"Hint: {cmd_hint}")

    if display_history:
        print(f"History: {grid.history()}")
    else:
        print(f"History: {cmd_history}")

    # if display_solution:
    #    print(f"Solution: {grid.get_curr_solution()}")
    # else:
    #     print(f"Solution: {cmd_solution}")

    print(f"Solve: {cmd_solve}")
    print(f"Quit: {cmd_quit}")
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

    # Shows 1 random move in the solution + number of moves remaining
    elif command in cmd_hint:
        display_hint = True

        hint = grid.hint()
        hint_coord, hint_num_moves_left = hint
        if hint_coord:
            curr_hint = f"f{hint_coord}, Moves Left: {str(hint_num_moves_left)}"
        else:
            curr_hint = "No hint available"

    elif command in cmd_solve:
        sol = grid.get_curr_solution()
        if len(sol) > 0:
            for coords in sol:
                grid.player_toggle_cell(coords[0], coords[1])

    elif command in cmd_reset:
        grid.reset()
        display_solution = False

    elif command in cmd_history:
        display_history = True

    elif command in cmd_new:
        grid.create_new_puzzle()
        display_solution = False

    elif command in cmd_quit:
        break

    else:
        continue