import random
from app.services.rps import play

class DummyRng:
    def __init__(self, seq):
        self.seq = seq
        self.i = 0
    def choice(self, options):
        val = self.seq[self.i % len(self.seq)]
        self.i += 1
        return val

def test_rps_draw():
    rng = DummyRng(["rock"])
    bot, outcome = play("rock", rng=rng)
    assert bot == "rock"
    assert outcome == "draw"

def test_rps_win():
    rng = DummyRng(["scissors"])
    bot, outcome = play("rock", rng=rng)
    assert bot == "scissors"
    assert outcome == "win"

def test_rps_lose():
    rng = DummyRng(["paper"])
    bot, outcome = play("rock", rng=rng)
    assert bot == "paper"
    assert outcome == "lose"
