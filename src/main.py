from grid import Grid

grid = Grid()
display_solution = False

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
    coords_input = input('Enter coordinates: ')

    # Undo
    if coords_input == 'u':
        coords = grid.undo_last_move()
        if coords != None:
            print(f"==> Reverted col: {coords[0]}, row: {coords[1]}")
        continue

    # Blank entry
    elif coords_input == "":
        continue

    # Print the coordinates needed to turn all lights on
    elif coords_input == "solution":
        display_solution = True
        continue

    elif coords_input == "solve":
        sol = grid.get_solution()
        if len(sol) > 0:
            for coords in sol:
                grid.toggle_cell(coords[0], coords[1])
        else:
            continue
    
    # Toggle col, row
    else:
        coords_input = coords_input.split(',')
        col = int(coords_input[0])
        row = int(coords_input[1])

        print(f"Entered col: {col}, row: {row}")

        try:
            grid.toggle_cell(col, row)
        except IndexError:
            print(f"==> Invalid col, row: {col}, {row}")