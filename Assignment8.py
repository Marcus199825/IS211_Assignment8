import time
from gameclass import Game, HumanPlayer, ComputerPlayer

class TimedPlayerFactory:
    def __init__(self, player_type):
        self.player_type = player_type
        self.player = None

    def create_player(self):
        if self.player_type == "human":
            self.player = HumanPlayer()
        elif self.player_type == "computer":
            self.player = ComputerPlayer()
        return self.player

class TimedGameProxy:
    def __init__(self, player1, player2, timed=False):
        self.player_factory1 = TimedPlayerFactory(player1)
        self.player_factory2 = TimedPlayerFactory(player2)
        self.game = Game(self.player_factory1.create_player(), self.player_factory2.create_player())
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

    def is_game_over(self):
        if self.timed and time.time() - self.start_time >= 60:
            return True
        return self.game.is_game_over()

    def get_winner(self):
        if self.timed and time.time() - self.start_time >= 60:
            return "Time's up!"
        return self.game.get_winner()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="TimedGameProxy for Pig game")
    parser.add_argument("--timed", action="store_true", help="Activate timed mode")
    parser.add_argument("--player1", choices=["human", "computer"], default="human", help="Specify player 1 type")
    parser.add_argument("--player2", choices=["human", "computer"], default="human", help="Specify player 2 type")
    args = parser.parse_args()

    game_proxy = TimedGameProxy(player1=args.player1, player2=args.player2, timed=args.timed)
    game_proxy.start()

    while not game_proxy.is_game_over():
        print("Current scores:", game_proxy.get_scores())
        action = input("Enter 'r' to roll or 'h' to hold: ").strip().lower()
        if action == "r":
            game_proxy.roll()
        elif action == "h":
            game_proxy.hold()
        else:
            print("Invalid input. Please enter 'r' or 'h'.")

    print("Game over.")
    print("Winner:", game_proxy.get_winner())
