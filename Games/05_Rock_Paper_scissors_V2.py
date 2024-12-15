import random
import sys

class RPS:
    def __init__(self):
        print("Welcome to Rock, Paper, Scissors!")
        self.moves : dict = {'rock' : '🪨', 'paper' : '📜', 'scissors' : '✂️'}
        self.valid_moves : list[str] = list(self.moves.keys())
        
    def run_game(self) -> None:
        user_moves : str = input("Enter your move: ").lower()
        if user_moves == 'exit':
            print("Goodbye!")
            sys.exit()
        if user_moves not in self.valid_moves:
            print("Please enter a valid move.")
            return self.run_game()
        
        ai_moves : str = random.choice(self.valid_moves)
        
        self.display_moves(user_moves, ai_moves)
        self.check_winner(user_moves, ai_moves)
        
        
    def display_moves(self, user_moves: str, ai_moves: str) -> None:
        print('----')
        print(f'You: {self.moves[user_moves]}')
        print(f'Computer: {self.moves[ai_moves]}')
        print('----')
        
    def check_winner(self, user_moves: str, ai_moves: str) -> None:
        if user_moves == ai_moves:
            print("It's a draw!")
        elif (user_moves == 'rock' and ai_moves == 'scissors') or (user_moves == 'scissors' and ai_moves == 'paper') or (user_moves == 'paper' and ai_moves == 'rock'):
            print("You win!")
        else:
            print("You lose!")
            
            
if __name__ == "__main__":
    rps = RPS()
    while True:
        rps.run_game()