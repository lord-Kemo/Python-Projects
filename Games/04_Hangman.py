from random import choice


def run_game() -> None:
    word: str = choice(["python", "java", "kotlin", "javascript"])
    
    username: str = input("Enter your name: ")
    print(f"Welcome to Hangman, {username}!")
    
    #setup
    guessed: str = ''
    tries: int = 3
    
    while tries > 0:
        blank: int = 0
        
        print('Word : ', end='')
        for char in word:
            if char in guessed:
                print(char, end='')
            else:
                print('_', end='')
                blank += 1
        print() # new line
        
        if blank == 0:
            print('Congratulations! You guessed the word.')
            break
        guess = input('Guess a letter: ')
        if guess in guessed:
            print(f'You already guessed the letter{guess}.')
            continue
        
        guessed += guess
        
        if guess not in word:
            tries -= 1
            print(f'Incorrect! You have {tries} tries left.')
            
        if tries == 0:
            print(f'Sorry, you lost. The word was {word}.')
            break
        
        
if __name__ == "__main__":
    run_game()