from argparse import ArgumentParser
from match.match import (
    matcher_for_string,
    MatchFunction,
    Deck,
    play_cards,
    Card,
    MatcherType,
)
from collections.abc import Callable
import sys


def get_user_setup(argv_: list[str]) -> tuple[int, MatcherType]:
    parser = ArgumentParser("Play a snap-like game of cards")
    parser.add_argument("packs", type=int, help="Number of packs to play with")
    parser.add_argument(
        "--match-type",
        "-m",
        type=matcher_for_string,
        choices=[matcher_for_string(n.name.lower()) for n in MatchFunction],
        help="Type of match that constitutes a win",
        default=matcher_for_string("exact"),
    )

    args = parser.parse_args(argv_)

    return args.packs, args.match_type


if __name__ == "__main__":
    packs, match_function = get_user_setup(None)

    deck = Deck(packs)
    deck.shuffle()

    score1, score2 = play_cards(deck, match_function)
    if score1 == score2:
        print(f"It was a draw, with both players scoring {score1}.")
    elif score1 > score2:
        print(f"Player 1 won with a score of {score1} to {score2}")
    else:
        print(f"Player 2 won with a score of {score2} to {score1}")
