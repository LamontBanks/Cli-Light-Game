# Light Game

Super simple, console-based "adjacent light game" as as a fun coding exercise.

Toggle on all the lights, but each light flips the lights next to it:

1. Start Game

            0  1  2  3  4
            -------------
        0 |  O  O  .  O  O
        1 |  O  .  O  .  O
        2 |  O  .  O  O  O
        3 |  .  O  O  .  .
        4 |  .  .  O  .  O

        Instructions - turn on all the lights
        > Enter the col, row - format: 3,5 or 3, 5 or 3 , 5
        Commands:
        > Undo: ['u']
        > Solution: ['solution']
        > Solve: ['solve']
        > New Puzzle: ['new']
        > Solution: ['solution']
        ---
        Enter coordinates or command: 

1. Toggle a light: `1, 3`

            0  1  2  3  4
            -------------
        0 |  O  O  .  O  O
        1 |  O  .  O  .  O
        2 |  O  O  O  O  O
        3 |  O  .  .  .  .
        4 |  .  O  O  .  O

1. Toggle another light: `3, 3`, etc.

            0  1  2  3  4
            -------------
        0 |  O  O  .  O  O
        1 |  O  .  O  .  O
        2 |  O  O  O  .  O
        3 |  O  .  O  O  O
        4 |  .  O  O  O  O

## Commands
Show the current solution with `solution`:

    Enter coordinates or command: solution

    
        0  1  2  3  4
        -------------
    0 |  O  O  .  O  O
    1 |  O  .  O  .  O
    2 |  O  O  O  .  O
    3 |  O  .  O  O  O
    4 |  .  O  O  O  O

    Instructions - turn on all the lights
    > Enter the col, row - format: 3,5 or 3, 5 or 3 , 5
    Commands:
    > Undo: ['u']
    > Solution: ['solution']
    > Solve: ['solve']
    > New Puzzle: ['new']
    > Solution: [(0, 4), (2, 1), (2, 2), (1, 3)]

Enter each coordinate to solve one at a time (order doesn't matter).

         0  1  2  3  4
         -------------
    0 |  O  O  O  O  O
    1 |  O  O  O  O  O
    2 |  O  O  O  O  O
    3 |  O  O  O  O  O
    4 |  O  O  O  O  O

## Usage
`$ python3 src/main.py`

## Future Enhancements
- Display most recent move
- Detect solved puzzle
- UI + click to toggle
- Reset to initial state
- Custom dimensions
- Cleanr display - only show instuctions on demand
- More unit tests
- Higher-level Interaction tests