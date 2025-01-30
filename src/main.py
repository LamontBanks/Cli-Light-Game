from grid import Grid

grid = Grid()
display_solution = False

while True:
    print(grid)

    # Input
    print("Enter the col, row - ex: 3,5 or 3, 5:")
    print("> \'u\' to undo moves:")

    if display_solution:
       print(f"> Solution: {grid.get_solution()}")
    else:
        print("> \'solution\' to show the answer")
    print('---')

    coords_input = input('Enter coordinates: ')

    # Undo
    if coords_input == 'u':
        coords = grid.undo_last_move()
        if coords != None:
            print(f"==> Undid col: {coords[0]}, row: {coords[1]}")
        continue

    # Print the coordinates needed to turn all lights on
    elif coords_input == "solution":
        display_solution = True
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