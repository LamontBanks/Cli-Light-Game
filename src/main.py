import re

from grid import Grid

grid = Grid()
display_solution = False
grid.create_new_puzzle(num_moves=10)

while True:
    print('\n')
    print(grid)
    print("Enter the col, row - ex: 3,5 or 3, 5:")
    print("> \'u\' to undo moves:")

    if display_solution:
       print(f"> Solution: {grid.get_solution()}")
    else:
        print("> \'solution\' to show the answer")
    print('---')

    # Input
    command = input('Enter coordinates: ')

    # Toggle cell
    # TODO: Couldn't do re.match in case statements?
    if (re.match(r"\s*\d+\s*,\s*\d+\s*", command)):
        coords_input = command.split(',')
        col = int(coords_input[0])
        row = int(coords_input[1])

        print(f"Entered col: {col}, row: {row}")

        try:
            grid.toggle_cell(col, row)
        except IndexError:
            print(f"==> Invalid col: {col}, row: {row}")

        continue

    match command:
        # Undo
        case 'u':
            last_coords = grid.undo_last_move()
            if last_coords != None:
                print(f"==> Reverted col: {last_coords[0]}, row: {last_coords[1]}")
                last_coords = None
        # Solution
        case "solution":
            display_solution = True
        # Blank entry
        case "":
            continue
        # Reset
        case "reset":
            grid.create_new_puzzle()
            display_solution = False
        # Solve
        case "solve":
            sol = grid.get_solution()
            if len(sol) > 0:
                for coords in sol:
                    grid.toggle_cell(coords[0], coords[1])
        case _:
            continue