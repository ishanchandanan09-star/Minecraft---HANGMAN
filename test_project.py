"""
Tests for Minecraft Hangman project.py
Run with: pytest test_project.py
"""

import pytest

from project import (
    check_guess,
    load_words,
    update_score,
    display_word,
)


def test_load_words():
    """load_words returns non-empty lists of correct length for each difficulty."""
    easy = load_words("easy")
    medium = load_words("medium")
    hard = load_words("hard")

    assert len(easy) > 0
    assert len(medium) > 0
    assert len(hard) > 0

    def letter_count(w: str) -> int:
        return len(w.replace(" ", ""))

    assert all(letter_count(w) <= 6 for w in easy)
    assert all(7 <= letter_count(w) <= 9 for w in medium)
    assert all(letter_count(w) >= 10 for w in hard)

    # All lowercase
    assert all(w.islower() for w in easy + medium + hard)

    with pytest.raises(ValueError):
        load_words("impossible")


def test_check_guess():
    """check_guess correctly validates and processes letters."""
    secret = "creeper"
    guessed = set()

    # Correct guess
    is_correct, new_guessed = check_guess(secret, guessed, "c")
    assert is_correct is True
    assert "c" in new_guessed
    assert len(new_guessed) == 1

    # Wrong guess
    is_correct, new_guessed = check_guess(secret, new_guessed, "z")
    assert is_correct is False
    assert "z" in new_guessed

    # Already guessed
    is_correct, same = check_guess(secret, new_guessed, "c")
    assert is_correct is False
    assert same == new_guessed

    # Invalid input (not a single letter)
    is_correct, same = check_guess(secret, new_guessed, "ab")
    assert is_correct is False
    assert same == new_guessed

    is_correct, same = check_guess(secret, new_guessed, "1")
    assert is_correct is False
    assert same == new_guessed

    is_correct, same = check_guess(secret, new_guessed, "")
    assert is_correct is False
    assert same == new_guessed

    # Case insensitive
    is_correct, new_guessed2 = check_guess(secret, set(), "C")
    assert is_correct is True
    assert "c" in new_guessed2

    # Phrase with space
    secret2 = "ender dragon"
    is_correct, g = check_guess(secret2, set(), "e")
    assert is_correct is True
    assert "e" in g


def test_update_score():
    """update_score correctly tracks wins, losses, streaks and win rate."""
    stats = {
        "games": 0,
        "wins": 0,
        "losses": 0,
        "current_streak": 0,
        "best_streak": 0,
        "win_rate": 0.0,
    }

    # Win
    stats = update_score(stats, won=True)
    assert stats["games"] == 1
    assert stats["wins"] == 1
    assert stats["losses"] == 0
    assert stats["current_streak"] == 1
    assert stats["best_streak"] == 1
    assert stats["win_rate"] == 100.0

    # Another win
    stats = update_score(stats, won=True)
    assert stats["games"] == 2
    assert stats["wins"] == 2
    assert stats["current_streak"] == 2
    assert stats["best_streak"] == 2
    assert stats["win_rate"] == 100.0

    # Loss resets streak
    stats = update_score(stats, won=False)
    assert stats["games"] == 3
    assert stats["wins"] == 2
    assert stats["losses"] == 1
    assert stats["current_streak"] == 0
    assert stats["best_streak"] == 2
    assert abs(stats["win_rate"] - 66.7) < 0.1

    # Does not mutate original
    original = {
        "games": 5,
        "wins": 3,
        "losses": 2,
        "current_streak": 1,
        "best_streak": 3,
        "win_rate": 60.0,
    }
    copy = original.copy()
    update_score(original, won=True)
    assert original == copy


def test_display_word():
    """display_word shows known letters, underscores, and preserves spaces."""
    assert display_word("cat", set()) == "_ _ _"
    assert display_word("cat", {"c"}) == "c _ _"
    assert display_word("cat", {"c", "a", "t"}) == "c a t"
    assert display_word("hello", {"l"}) == "_ _ l l _"

    # Phrases with spaces
    assert display_word("ender dragon", set()) == "_ _ _ _ _   _ _ _ _ _ _"
    assert display_word("ender dragon", {"e", "d"}) == "e _ d e _   d _ _ _ _ _"
    assert display_word("axe", {"a", "x", "e"}) == "a x e"
