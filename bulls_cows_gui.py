import random
import easygui

DEFAULT_NUM_OF_DIGITS = 4


def main():
    play_on = True
    while play_on:
        number = generate_number()
        print(number)
        play_on = start_game(number)


def generate_number(num_of_digits: int = DEFAULT_NUM_OF_DIGITS) -> str:
    """
    :param num_of_digits: number size
    :return: generated number as a string
    """
    if num_of_digits <= 0:
        raise Exception("Invalid number of digits!")

    all_digits = set(range(10))
    first = random.randint(1, 9)
    remaining = random.sample(all_digits - {first}, num_of_digits-1)
    number_str = str(first) + ''.join(map(str, remaining))
    return number_str


def start_game(number: str) -> bool:
    """
    :param number: the generated number as string
    :return: whether the user would like to play another game
    """
    tries_count = 0
    guesses = []  # list of strings ["1: 1234 -> Bulls: 0, Cows: 0", ...]

    while True:
        guess = validate_guess(number)
        if guess is None:
            restart = easygui.ynbox(f"You gave up, the number was: {number}\nAnother game?")
            break

        tries_count += 1
        if guess == number:
            guess_pipe = "guess" if tries_count == 1 else "guesses"
            restart = easygui.ynbox(f"You won! The number is {number}\nIt took you {tries_count} {guess_pipe}.\nAnother game?")
            break
        else:
            bulls, cows = count_bulls_and_cows(number, guess)
            guesses.append(f"{tries_count}: {guess} -> Bulls: {bulls}, Cows: {cows}")
        easygui.msgbox('Your guesses:\n'+'\n'.join(guesses))
    return restart


def validate_guess(number) -> str or None:
    """
    :param number: the number to guess
    :return: the valid guessed number or None if user gives up
    """
    number_size = len(number)
    while True:
        guess = easygui.enterbox(f"Please guess the {number_size}-digit number: ")
        if guess is None:
            break

        if not guess.isdigit():
            err_msg = "Please enter only digits!"
        elif number_size != len(set(guess)):
            err_msg = f"Please type a {number_size}-digit number with unique digits!"
        else:
            break
        easygui.msgbox(err_msg, "Invalid input!")
    return guess


def count_bulls_and_cows(number, guessed_number) -> tuple:
    """
    :param number: the number to guess
    :param guessed_number: the guessed number
    :return: tuple containing the count of bulls and cows
    """
    bulls = 0
    cows = 0

    for x in range(len(number)):
        if guessed_number[x] == number[x]:
            bulls += 1
        elif guessed_number[x] in number:
            cows += 1
    return bulls, cows


if __name__ == '__main__':
    main()
