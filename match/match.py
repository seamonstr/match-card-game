from enum import Enum, auto
import random
from collections.abc import Callable

CARDS_IN_PACK = 52


class Suite(Enum):
    SPADES = auto()
    CLUBS = auto()
    HEARTS = auto()
    DIAMONDS = auto()


class Value(Enum):
    ONE = auto()
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    TEN = auto()
    JACK = auto()
    QUEEN = auto()
    KING = auto()


class Card:
    def __init__(self, suite, value):
        self.suite = suite
        self.value = value

    def __eq__(self, other):
        return self.suite == other.suite and self.value == other.value

    def __hash__(self):
        return hash((self.suite, self.value))


class Deck:
    """
    Represents a deck of cards comprising num_packs_ packs.
    """

    def __init__(self, num_packs: int):
        """
        Cards will be initially sorted by suite and value.
        """
        self.cards: list[Card] = []
        inx = 0
        for i in range(num_packs):
            for suite in Suite:
                for card_val in Value:
                    inx += 1
                    self.cards[
                        i * CARDS_IN_PACK
                        + ((card_val.value - 1) * len(Suite))
                        + suite.value
                        - 1
                    ] = Card(suite, card_val)

    def shuffle(self):
        random.shuffle(self.cards)

    def __iter__(self):
        def deck_iterator(deck_):
            for card in deck_.cards:
                yield card

        return deck_iterator(self)


###########################################
# Set of matching strategies - either match just by value, just by suite, or both
class MatchFunction(Enum):
    SUITE = auto()
    VALUE = auto()
    EXACT = auto()


MatcherType = Callable[[Card, Card], bool]


def matchExact(card_a: Card, card_b: Card) -> bool:
    return card_a == card_b


def matchSuite(card_a: Card, card_b: Card) -> bool:
    return card_a.suite == card_b.suite


def matchValue(card_a: Card, card_b: Card) -> bool:
    return card_a.value == card_b.value


def matcher_for_string(match_name: str) -> MatcherType:
    try:
        return {
            MatchFunction.SUITE: matchSuite,
            MatchFunction.VALUE: matchValue,
            MatchFunction.EXACT: matchExact,
        }[MatchFunction[match_name.upper()]]
    except (KeyError):
        raise ValueError("No such match-type")


#########################################
# Play a game of cards with the specified deck and matching strategy.
def play_cards(deck_: Deck, matcher_: MatcherType) -> list[int]:
    player_scores = [0, 0]
    curr_card = None
    cards_in_play = 0
    for card in deck_:
        cards_in_play += 1
        if not curr_card:
            # IF this is the first iteration (or we're starting a new round) then
            # there's nothing to match against
            curr_card = card
            continue

        if matcher_(curr_card, card):
            # As per the rules, randomise which player wins this round.
            player_scores[random.randint(0, 1)] += cards_in_play
            cards_in_play = 0
            curr_card = None
            continue

        curr_card = card

    return player_scores
