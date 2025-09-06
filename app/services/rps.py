import random
from typing import Literal, Tuple

Move = Literal["rock", "paper", "scissors"]

RULES = {
    ("rock", "scissors"): "win",
    ("rock", "paper"): "lose",
    ("paper", "rock"): "win",
    ("paper", "scissors"): "lose",
    ("scissors", "paper"): "win",
    ("scissors", "rock"): "lose",
}

def play(user: Move, rng=random) -> Tuple[Move, str]:
    bot: Move = rng.choice(["rock", "paper", "scissors"])
    if bot == user:
        return bot, "draw"
    outcome = RULES.get((user, bot), "lose")
    return bot, outcome