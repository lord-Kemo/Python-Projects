from random import randint

lower = 1
upper = 10

randomNumber: int = randint(lower, upper)

print(f"Guess a number between {lower} and {upper}.")

while True:
    try:
        userGuess: int = int(input("Enter your guess: "))
    except ValueError as e:
        print("Invalid input. Please enter a number.")
        continue
    if userGuess != randomNumber:
        print("Incorrect guess. Try again.")
    else:
        print("Congratulations! You guessed the correct number.")
        break