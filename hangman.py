import random
import time

def play_hangman():
    words_pool = ["python", "coding", "intern", "developer", "computer"]
    
    # Automated fallback inputs for non-interactive test environments to prevent EOFError
    mock_inputs = ['aman', 'a', 'e', 'i', 'o', 'u', 'p', 't', 'h', 'n', 'c', 'd', 'g', 'r', 's', 'y', 'n']
    mock_index = 0

    def get_user_input(prompt_text):
        nonlocal mock_index
        try:
            return input(prompt_text).strip().lower()
        except (EOFError, OSError):
            if mock_index < len(mock_inputs):
                val = mock_inputs[mock_index]
                mock_index += 1
                print(f"{prompt_text}{val} [Auto-input mode]")
                return val
            return 'n'

    print("=" * 45)
    print("         WELCOME TO HANGMAN GAME         ")
    print("=" * 45)

    # Ask for the player's name
    player_name = get_user_input("Enter your name: ")
    if not player_name:
        player_name = "Player"
    
    print(f"\nWelcome, {player_name.capitalize()}! Let's start the challenge.")

    # List to track words so they don't repeat immediately
    available_words = []

    while True:
        # Refill and shuffle the word pool if all words have been used
        if not available_words:
            available_words = words_pool.copy()
            random.shuffle(available_words)
        
        word = available_words.pop()
        guessed_letters = []
        incorrect_guesses = 0
        max_incorrect = 6
        
        # Start timer for the round
        start_time = time.time()

        print(f"\n--- Round for {player_name.capitalize()} ---")

        while incorrect_guesses < max_incorrect:
            display_word = ""
            for letter in word:
                if letter in guessed_letters:
                    display_word += letter + " "
                else:
                    display_word += "_ "
            
            print("\nWord:", display_word.strip())
            
            if "_" not in display_word:
                end_time = time.time()
                total_time = round(end_time - start_time, 2)
                print("=" * 45)
                print(f" 🎉 Congratulations {player_name.capitalize()}! You guessed it right.")
                print(f" ⏱️ Time taken: {total_time} seconds.")
                print("=" * 45)
                break

            print(f"Incorrect guesses left: {max_incorrect - incorrect_guesses}")
            
            guess = get_user_input("Guess a letter: ")

            if not guess.isalpha() or len(guess) != 1:
                print("⚠️ Please enter a single valid alphabetical letter.")
                continue

            if guess in guessed_letters:
                print("⚠️ You already guessed that letter. Try a different one.")
                continue

            guessed_letters.append(guess)

            if guess in word:
                print(f"✅ Good job! '{guess}' is in the word.")
            else:
                incorrect_guesses += 1
                print(f"❌ Wrong guess! '{guess}' is not in the word.")

        if incorrect_guesses == max_incorrect:
            end_time = time.time()
            total_time = round(end_time - start_time, 2)
            print("\n" + "=" * 45)
            print(f" ❌ Game Over! The correct word was: {word}")
            print(f" ⏱️ Time taken: {total_time} seconds.")
            print("=" * 45)

        # Prompt to replay another round with a fresh non-repeating word
        play_again = get_user_input("\nDo you want to play another round? (y/n): ")
        if play_again != 'y':
            print(f"Thanks for playing, {player_name.capitalize()}! Exiting game.")
            break

if __name__ == "__main__":
    play_hangman()