import time
from gameclass import Game

class TimedGameProxy:
    def __init__(self, timed=False):
        self.game = Game()
        self.timed = timed
        self.start_time = None

    def start(self):
        if self.timed:
            self.start_time = time.time()
        self.game.start()

    def roll(self):
        if self.timed and time.time() - self.start_time >= 60:
            print("One minute has elapsed. Game over.")
            return
        self.game.roll()

    def hold(self):
        if self.timed and time.time() - self.start_time >= 60:
            print("One minute has elapsed. Game over.")
            return
        self.game.hold()

    def get_scores(self):
        return self.game.get_scores()

