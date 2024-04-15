import time
import random
import argparse

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
    
    def play_turn(self):
        pass

class HumanPlayer(Player):
    def play_turn(self):
        print(f"{self.name}'s turn:")
        choice = input("Roll (r) or Hold (h): ").lower()
        return choice == 'r'

class ComputerPlayer(Player):
    def play_turn(self):
        threshold = min(25, 100 - self.score)
        return self.score < threshold

class PlayerFactory:
    @staticmethod
    def create_player(player_type, name):
        if player_type == 'human':
            return HumanPlayer(name)
        elif player_type == 'computer':
            return ComputerPlayer(name)
        else:
            raise ValueError("Invalid player type")

class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.current_player = random.choice(self.players)
        self.scores = {player1.name: 0, player2.name: 0}
        self.start_time = time.time()

    def play(self):
        while max(self.scores.values()) < 100 and time.time() - self.start_time < 60:
            print(f"\n{self.current_player.name}'s turn:")
            choice = self.current_player.play_turn()
            if choice:
                roll = random.randint(1, 6)
                if roll == 1:
                    print("You rolled a 1! Turn ends with no points.")
                    self.scores[self.current_player.name] = 0
                    self.switch_turn()
                    continue
                else:
                    print(f"You rolled a {roll}.")
                    self.scores[self.current_player.name] += roll
                    print(f"Current score: {self.scores[self.current_player.name]}")
            else:
                print(f"{self.current_player.name} holds.")
                self.switch_turn()

        winner = max(self.scores, key=self.scores.get)
        print(f"\nGame over! {winner} wins with {self.scores[winner]} points.")

    def switch_turn(self):
        self.current_player = [player for player in self.players if player != self.current_player][0]

class TimedGameProxy(Game):
    def __init__(self, player1, player2):
        super().__init__(player1, player2)
        self.timed = True

    def play(self):
        while max(self.scores.values()) < 100 and time.time() - self.start_time < 60:
            super().play()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play Pig game with timed version and computer player.")
    parser.add_argument("--player1", choices=['human', 'computer'], default='human', help="Type of player 1")
    parser.add_argument("--player2", choices=['human', 'computer'], default='human', help="Type of player 2")
    parser.add_argument("--timed", action='store_true', help="Play timed version of the game")
    args = parser.parse_args()

    player1 = PlayerFactory.create_player(args.player1, "Player 1")
    player2 = PlayerFactory.create_player(args.player2, "Player 2")

    if args.timed:
        game = TimedGameProxy(player1, player2)
    else:
        game = Game(player1, player2)

    game.play()

