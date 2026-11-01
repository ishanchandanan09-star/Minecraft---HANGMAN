# Minecraft Hangman – CS50P Final Project
#### Video Demo: https://youtu.be/plEsxFk_b-4
#### Description:
A terminal-based Hangman game themed entirely around **Minecraft**.
Guess letters to reveal Minecraft items, blocks, mobs and features before the hangman is fully drawn.

The project includes three difficulty levels based on word length, persistent player statistics, colored terminal output, and a clean menu system.

---

## Features

- **Minecraft-themed word list**  
  Words taken from classic Minecraft items, blocks, mobs and structures (axe, creeper, ender dragon, crafting table, etc.).

- **Three difficulty levels**  
  - **Easy** – up to 6 letters (axe, bed, blaze, zombie…)  
  - **Medium** – 7–9 letters (creeper, diamond, enderman, redstone…)  
  - **Hard** – 10+ letters / short phrases (ender dragon, crafting table, nether portal…)

- **Persistent statistics** – Wins, losses, current streak, best streak and win rate are saved to `stats.json` so your progress survives across sessions.

- **Input validation** – Rejects non-letters, repeated guesses and empty input with clear feedback.

- **Colored terminal UI** – Uses the `colorama` library for cross-platform colored text and classic ASCII-art hangman stages that update after every wrong guess.

- **Clean menu** – Play Easy / Medium / Hard, view stats, or quit.

- **Phrase support** – Hard mode includes multi-word phrases. Spaces are automatically shown and do not need to be guessed.

---

## Project Structure

```
hangman/
├── project.py          # Main game logic and entry point
├── test_project.py     # pytest unit tests
├── words.txt           # Minecraft word list (one word/phrase per line)
├── requirements.txt    # Dependencies
├── stats.json          # Created automatically on first game
└── README.md           # This file
```

---

## Installation & Running

1. Clone the repository (or download the files).

2. Create a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate        # Linux / macOS
   venv\Scripts\activate           # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the game:

   ```bash
   python project.py
   ```

5. Run the tests:

   ```bash
   pytest test_project.py -v
   ```

---

## Design Choices

### Pure, testable functions
The three required top-level functions (`load_words`, `check_guess`, `update_score`) contain no `input()` or `print()` calls.  
They receive data and return results, which makes them easy to unit-test with `pytest`.  
All interactive logic lives inside `play_game()` and `main()`.

### Minecraft word list
A single `words.txt` file holds every word, grouped by comments.  
`load_words()` filters at runtime by letter count (spaces are ignored when measuring length).  
This keeps the list easy to expand and avoids maintaining three separate files.

### Difficulty by length
Matching the source list:
- Easy ≤ 6 letters  
- Medium 7–9 letters  
- Hard ≥ 10 letters (includes short phrases)

### Phrase handling
Hard-mode entries such as “ender dragon” and “crafting table” contain spaces.  
Spaces are always displayed and never need to be guessed.  
`display_word()` and the win-condition check both treat spaces as already known.

### Statistics
Stats are stored as a plain JSON file.  
`update_score` returns a *new* dictionary rather than mutating the old one; this keeps the function pure and easier to reason about.  
Win rate is calculated as a percentage rounded to one decimal place.

### Visual feedback
The six classic hangman stages are stored as multi-line raw strings.  
After every wrong guess the appropriate stage is printed so the player always knows how close they are to losing.

### Colorama
`colorama` was chosen because it works on Windows, macOS and Linux without extra configuration.  
Colors are used sparingly: cyan/green for titles and prompts, red for errors, yellow for the hangman figure.

---

## Functions Overview

| Function          | Purpose |
|-------------------|---------|
| `load_words(difficulty)` | Reads `words.txt` and returns words matching the chosen difficulty. |
| `check_guess(secret, guessed_letters, letter)` | Validates a letter and returns whether it was correct together with the updated set of guessed letters. |
| `update_score(stats, won)` | Updates games / wins / losses / streaks / win-rate and returns a new stats dict. |
| `display_word(secret, guessed_letters)` | Builds the `_ _ a _` style string (spaces always shown). |
| `play_game(difficulty)` | Runs a single round of Hangman and returns `True`/`False` for win/loss. |
| `main()` | Displays the menu and drives the overall program loop. |

---

## Testing

The test suite covers the three required functions plus the display helper:

- `test_load_words` – checks length filtering and error handling  
- `test_check_guess` – correct / incorrect / repeated / invalid input + phrases  
- `test_update_score` – wins, losses, streak reset, immutability  
- `test_display_word` – progressive letter revelation and space handling  

Run them with:

```bash
pytest test_project.py -v
```

All tests are independent of the terminal and of the random word selection, so they are deterministic and fast.

---

## Word List Source

The words come from a public Minecraft Hangman word list (items, blocks, mobs and structures).  
Easy, Medium and Hard groupings follow the original length categories.

---

## Future Improvements (optional)

- Computer-guesser mode that uses letter-frequency analysis.
- Categories (tools, mobs, blocks, biomes) in addition to pure length-based difficulty.
- A simple leaderboard that stores high scores across multiple players.
- Richer TUI using the `rich` library or Minecraft-style ASCII art.

---

## Credits

- Word list adapted from public Minecraft Hangman resources.  
- Hangman ASCII art is a classic public-domain design.  
- Built as the final project for CS50’s Introduction to Programming with Python.

---

Enjoy the game, and good luck in the Overworld!
