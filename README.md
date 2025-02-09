# Light Game

Super simple, console-based "adjacent light game" as as a fun coding/small projec exercise.

Toggle on all the lights, but each light flips the lights next to it, ex:

When all lights are off, toggle column `1`, row `1`...

         0 ›1  2  
         -------
     0 | ·  ·  ·
    ›1 | · ›·  ·        
     2 | ·  ·  ·

...lights on:

         0  1  2  
         -------
     0 | ·  O  ·
     1 | O  O  O        
     2 | ·  O  ·

Toggling column `2`, row `0`...:

         0  1 ›2  
         -------
    ›0 | ·  O ›·
     1 | O  O  O        
     2 | ·  O  ·

...lights on or off, depending on their previous state:

         0  1  2  
         -------
     0 | ·  ·  O
     1 | O  O  ·        
     2 | ·  O  ·

## Usage
`$ python3 src/main.py`

        0  1  2  3  4
        -------------
    0 |  ·  ·  O  ·  ·
    1 |  ·  ·  O  O  ·
    2 |  O  O  O  ·  ·
    3 |  O  O  O  ·  ·
    4 |  ·  O  ·  O  ·

    >>> Turn on all the lights! <<<
    Adjacent lights (up, down, left, right) will flip on/off at the same time.
    Enter the col, row, ex: 3, 5

                            Commands:
    Undo: ['undo', 'u']     Reset: ['reset']        New Puzzle: ['new', 'n']
    History: ['history', 'h']
    Solve: ['solve']
    Quit: ['quit', 'exit']
    Moves required: 2, ['hint'] to show next light
    ---
    Enter coordinates or command: 

1. Toggle a light, ex: `1, 2`, etc:

             0 ›1  2  3  4           0  1  2  3  4
            --------------           -------------
        0 |  ·  ·  O  ·  ·       0 |  ·  ·  O  ·  ·
        1 |  ·  ·  O  O  ·       1 |  ·  O  O  O  ·
       ›2 |  O ›O  O  ·  ·  ==>  2 |  ·  ·  ·  ·  ·
        3 |  O  O  O  ·  ·       3 |  O  ·  O  ·  ·       
        4 |  ·  O  ·  O  ·       4 |  ·  O  ·  O  ·

1. The `Moves required` count is key to solving the puzzle!

## Commands
Use the displayed commands as needed:

                            Commands:
    Undo: ['undo', 'u']     Reset: ['reset']        New Puzzle: ['new', 'n']
    History: ['history', 'h']
    Solve: ['solve']
    Quit: ['quit', 'exit']
    Moves required: 2, ['hint'] to show next light

Show the solution steps with `solve`, ex:

    - Step: (3, 1)

        0  1  2 ›3            0  1  2  3
        ----------            ----------
    0 | O  ·  ·  ·       0 |  O  ·  ·  O
    1›| ·  O  ·  X       1 |  ·  O  O  O
    2 | ·  O  O  ·  -->  2 |  ·  O  O  O
    3 | O  O  O  O       3 |  O  O  O  O

    - Step: (1, 0)

        0 ›1  2  3            0  1  2  3
        ----------            ----------
    0›| O  X  ·  O       0 |  ·  O  O  O
    1 | ·  O  O  O       1 |  ·  ·  O  O
    2 | ·  O  O  O  -->  2 |  ·  O  O  O
    3 | O  O  O  O       3 |  O  O  O  O

    - Step: (0, 1)

        ›0  1  2  3           0  1  2  3
        ----------            ----------
    0 | ·  O  O  O       0 |  O  O  O  O
    1›| X  ·  O  O       1 |  O  O  O  O
    2 | ·  O  O  O  -->  2 |  O  O  O  O
    3 | O  O  O  O       3 |  O  O  O  O

## Tests
- Unit: `$ ./test.sh`
- Coverage: `https://coverage.readthedocs.io/en/7.6.10/`

## Future Enhancements
- Use [`cmd`](https://docs.python.org/3.12/library/cmd.html) to handle commands
- Display most recent move
- Show step-by-step when displaying the solution
- TKinter UI + click to toggle
- Set Custom dimensions
- Minimize commands
- More unit tests
- Higher-level Interaction tests