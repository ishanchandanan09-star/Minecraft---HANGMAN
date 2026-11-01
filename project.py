"""
Minecraft Hangman - CS50P Final Project
A terminal Hangman game themed around Minecraft with difficulty levels,
scoring, and persistent stats.
"""

import json
import random
import string
from pathlib import Path

from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# File paths
WORDS_FILE = Path(__file__).parent / "words.txt"
STATS_FILE = Path(__file__).parent / "stats.json"

# ASCII art stages for the hangman (0 wrong -> full figure)
HANGMAN_STAGES = [
    # 0 wrong guesses
    r"""
     +---+
     |   |
         |
         |
         |
         |
    =========
    """,
    # 1
    r"""
     +---+
     |   |
     O   |
         |
         |
         |
    =========
    """,
    # 2
    r"""
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========
    """,
    # 3
    r"""
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========
    """,
    # 4
    r"""
     +---+
     |   |
     O   |
    /|\  |
         |
         |
    =========
    """,
    # 5
    r"""
     +---+
     |   |
     O   |
    /|\  |
    /    |
         |
    =========
    """,
    # 6 - game over
    r"""
     +---+
     |   |
     O   |
    /|\  |
    / \  |
         |
    =========
    """,
]


def load_words(difficulty: str = "medium") -> list[str]:
    """
    Load Minecraft words from words.txt filtered by difficulty (based on length).

    easy   -> up to 6 letters (ignoring spaces)
    medium -> 7-9 letters
    hard   -> 10+ letters

    Returns a list of lowercase words/phrases. Raises FileNotFoundError if the
    word file is missing, or ValueError if no words match the difficulty.
    """
    if not WORDS_FILE.exists():
        raise FileNotFoundError(f"Word list not found: {WORDS_FILE}")

    with open(WORDS_FILE, encoding="utf-8") as f:
        all_words = [
            line.strip().lower()
            for line in f
            if line.strip() and not line.strip().startswith("#")
        ]

    def letter_count(w: str) -> int:
        return len(w.replace(" ", ""))

    if difficulty == "easy":
        words = [w for w in all_words if letter_count(w) <= 6]
    elif difficulty == "medium":
        words = [w for w in all_words if 7 <= letter_count(w) <= 9]
    elif difficulty == "hard":
        words = [w for w in all_words if letter_count(w) >= 10]
    else:
        raise ValueError(f"Unknown difficulty: {difficulty}")

    if not words:
        raise ValueError(f"No words found for difficulty '{difficulty}'")

    return words


def check_guess(secret: str, guessed_letters: set[str], letter: str) -> tuple[bool, set[str]]:
    """
    Validate and process a single letter guess.

    Returns:
        (is_correct, updated_guessed_letters)

    - letter must be a single alphabetic character
    - already-guessed letters are rejected (returns False, original set)
    - correct letters are added to the set and return True
    - spaces in the secret are ignored for guessing (they are always shown)
    """
    letter = letter.lower().strip()

    if len(letter) != 1 or letter not in string.ascii_lowercase:
        return False, guessed_letters

    if letter in guessed_letters:
        return False, guessed_letters

    new_guessed = guessed_letters | {letter}
    # Only count as correct if the letter appears in the secret (ignoring spaces)
    is_correct = letter in secret.replace(" ", "")
    return is_correct, new_guessed


def update_score(stats: dict, won: bool) -> dict:
    """
    Update a stats dictionary after a game.

    Tracks: games, wins, losses, current_streak, best_streak, win_rate.
    Returns a new dict (does not mutate the original).
    """
    new_stats = stats.copy()
    new_stats["games"] = new_stats.get("games", 0) + 1

    if won:
        new_stats["wins"] = new_stats.get("wins", 0) + 1
        new_stats["current_streak"] = new_stats.get("current_streak", 0) + 1
        new_stats["best_streak"] = max(
            new_stats.get("best_streak", 0), new_stats["current_streak"]
        )
    else:
        new_stats["losses"] = new_stats.get("losses", 0) + 1
        new_stats["current_streak"] = 0

    total = new_stats["games"]
    wins = new_stats.get("wins", 0)
    new_stats["win_rate"] = round((wins / total) * 100, 1) if total > 0 else 0.0

    return new_stats


def load_stats() -> dict:
    """Load stats from JSON file, or return defaults if missing/corrupt."""
    defaults = {
        "games": 0,
        "wins": 0,
        "losses": 0,
        "current_streak": 0,
        "best_streak": 0,
        "win_rate": 0.0,
    }
    if not STATS_FILE.exists():
        return defaults

    try:
        with open(STATS_FILE, encoding="utf-8") as f:
            data = json.load(f)
        for key, value in defaults.items():
            data.setdefault(key, value)
        return data
    except (json.JSONDecodeError, OSError):
        return defaults


def save_stats(stats: dict) -> None:
    """Persist stats to JSON file."""
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)


def display_word(secret: str, guessed_letters: set[str]) -> str:
    """
    Return the current display of the word/phrase.
    Spaces are always shown; letters are revealed only if guessed.
    """
    result = []
    for char in secret:
        if char == " ":
            result.append(" ")
        elif char in guessed_letters:
            result.append(char)
        else:
            result.append("_")
    return " ".join(result)


def play_game(difficulty: str = "medium", max_wrong: int = 6) -> bool:
    """
    Run a single game of Minecraft Hangman.
    Returns True if the player won, False otherwise.
    """
    words = load_words(difficulty)
    secret = random.choice(words)
    guessed_letters: set[str] = set()
    wrong_guesses = 0

    print(Fore.CYAN + Style.BRIGHT + "\n=== MINECRAFT HANGMAN ===")
    print(f"Difficulty: {difficulty.upper()}")
    letter_len = len(secret.replace(" ", ""))
    print(f"Letters to guess: {letter_len}\n")

    while wrong_guesses < max_wrong:
        print(Fore.YELLOW + HANGMAN_STAGES[wrong_guesses])
        print(Fore.WHITE + Style.BRIGHT + "Word: " + display_word(secret, guessed_letters))
        print(f"Guessed: {', '.join(sorted(guessed_letters)) or '(none)'}")
        print(f"Wrong guesses left: {max_wrong - wrong_guesses}")

        user_input = input(Fore.GREEN + "\nGuess a letter: ").strip().lower()

        if len(user_input) != 1 or user_input not in string.ascii_lowercase:
            print(Fore.RED + "Please enter a single letter (a-z).")
            continue

        if user_input in guessed_letters:
            print(Fore.RED + f"You already guessed '{user_input}'.")
            continue

        is_correct, guessed_letters = check_guess(secret, guessed_letters, user_input)

        if is_correct:
            print(Fore.GREEN + f"Good! '{user_input}' is in the word.")
        else:
            wrong_guesses += 1
            print(Fore.RED + f"Sorry, '{user_input}' is not in the word.")

        # Win check (ignore spaces)
        if all(c in guessed_letters or c == " " for c in secret):
            print(Fore.YELLOW + HANGMAN_STAGES[wrong_guesses])
            print(Fore.GREEN + Style.BRIGHT + f"\nYou won! The word was: {secret.upper()}")
            return True

    # Lost
    print(Fore.YELLOW + HANGMAN_STAGES[wrong_guesses])
    print(Fore.RED + Style.BRIGHT + f"\nGame over! The word was: {secret.upper()}")
    return False


def show_stats(stats: dict) -> None:
    """Pretty-print the current statistics."""
    print(Fore.CYAN + Style.BRIGHT + "\n--- Your Stats ---")
    print(f"Games played  : {stats.get('games', 0)}")
    print(f"Wins          : {stats.get('wins', 0)}")
    print(f"Losses        : {stats.get('losses', 0)}")
    print(f"Win rate      : {stats.get('win_rate', 0.0)}%")
    print(f"Current streak: {stats.get('current_streak', 0)}")
    print(f"Best streak   : {stats.get('best_streak', 0)}")
    print("------------------\n")


def main() -> None:
    """Main entry point: menu loop."""
    stats = load_stats()

    print(Fore.GREEN + Style.BRIGHT + r"""
 __  __ _                           __ _     _   _                                  
|  \/  (_)_ __   ___  ___ _ __ __ _/ _| |_  | | | | __ _ _ __   __ _ _ __ ___   __ _ 
| |\/| | | '_ \ / _ \/ __| '__/ _` | |_| __| | |_| |/ _` | '_ \ / _` | '_ ` _ \ / _` |
| |  | | | | | |  __/ (__| | | (_| |  _| |_  |  _  | (_| | | | | (_| | | | | | | (_| |
|_|  |_|_|_| |_|\___|\___|_|  \__,_|_|  \__| |_| |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|
                                                                |___/                
    """)
    print(Fore.WHITE + "Welcome to Minecraft Hangman!")
    print(Fore.YELLOW + "Guess Minecraft items, blocks, mobs and more.\n")

    while True:
        print(Fore.YELLOW + "Menu:")
        print("  1. Play (Easy)   - short words (axe, bed, creeper...)")
        print("  2. Play (Medium) - longer words (diamond, enderman...)")
        print("  3. Play (Hard)   - phrases (ender dragon, crafting table...)")
        print("  4. View Stats")
        print("  5. Quit")
        choice = input(Fore.GREEN + "\nChoose an option (1-5): ").strip()

        if choice == "1":
            won = play_game("easy")
            stats = update_score(stats, won)
            save_stats(stats)
            show_stats(stats)
        elif choice == "2":
            won = play_game("medium")
            stats = update_score(stats, won)
            save_stats(stats)
            show_stats(stats)
        elif choice == "3":
            won = play_game("hard")
            stats = update_score(stats, won)
            save_stats(stats)
            show_stats(stats)
        elif choice == "4":
            show_stats(stats)
        elif choice == "5":
            print(Fore.CYAN + "Thanks for playing! See you in the Overworld.")
            break
        else:
            print(Fore.RED + "Invalid choice. Please enter 1-5.")


if __name__ == "__main__":
    main()
