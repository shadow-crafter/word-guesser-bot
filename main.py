from src.word_guesser import WordGuesser

guesser = WordGuesser()
target = "teacher"
guesses = ["apple", "school", "person"]

while True:
    guess, confidence = guesser.guess_next_word(guesses)
    if guess:
        guesses.append(guess)
        print(f"Guessed word: {guess} (confidence: {confidence:.2f})")
        if guess == target:
            break
