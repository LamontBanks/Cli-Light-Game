# Light Game

Super simple, console-based "adjacent light game" as as a fun coding exercise.

Toggle on all the lights, but each light flips the lights next to it:

         0  1  2  3  4
         -------------
    0 |  O  .  O  O  O
    1 |  .  .  O  O  O
    2 |  O  O  .  .  O
    3 |  .  O  .  .  .
    4 |  .  .  .  O  O

    Enter the col, row - ex: 3,5 or 3, 5:
    > 'u' to undo moves:
    > 'solution' to show the answer
    ---
    Enter coordinates: 2,3
    
    Entered col: 2, row: 3
        0  1  2  3  4
        -------------
    0 |  O  .  O  O  O
    1 |  .  .  O  O  O
    2 |  O  O  O  .  O
    3 |  .  .  O  O  .
    4 |  .  .  O  O  O

Print the solution with `solution`:

    Enter coordinates: solution
    
         0  1  2  3  4
         -------------
    0 |  O  .  O  O  O
    1 |  .  .  O  O  O
    2 |  O  O  O  .  O
    3 |  .  .  O  O  .
    4 |  .  .  O  O  O

    Enter the col, row - ex: 3,5 or 3, 5:
    > 'u' to undo moves:
    > Solution: [(4, 4), (0, 4), (3, 4), (1, 1), (2, 3), (2, 2)] 

Enter the coordinates in any order to solve: (shortcut: `solve`)

         0  1  2  3  4
         -------------
    0 |  O  O  O  O  O
    1 |  O  O  O  O  O
    2 |  O  O  O  O  O
    3 |  O  O  O  O  O
    4 |  O  O  O  O  O

## Usage
python3 src/main.py
