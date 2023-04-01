import math
import time

rolls = ['-', '\\', '|', '/']


def progress_bar(duration):
    print()

    bar_length = 32
    tot_ticks = 128

    # Loop for the duration of the progress bar
    for tick in range(tot_ticks):
        progress = tick / (tot_ticks - 1)
        filled_length = max(math.ceil(progress * bar_length), 1)
        roll = rolls[tick % 4]
        if progress == 1:
            roll = "#"

        print(f"\033[1AProgress: [{'#' * (filled_length - 1)}{roll}{'-' * (bar_length - filled_length)}] {progress * 100:.0f}% ")

        time.sleep(duration / tot_ticks)


def calculator():
    load_time = 3
    quit_time = 1
    calculate_time = 0.5

    print("Loading calculator...")
    progress_bar(load_time)
    print()

    # Loop to allow for multiple calculations
    while True:
        operator = input("Enter operator or 'q' to quit: ").lower()

        if operator not in ('+', '-', '*', '/', 'q'):
            print("Invalid operator. Please enter a valid operator (+, -, *, /).")
            print()
            continue

        # Quit if the user enters 'q'
        if operator == 'q':
            print("Exiting calculator...")
            progress_bar(quit_time)
            break

        # Get user input for the operands
        try:
            num1 = float(input("Enter first number:            "))
            num2 = float(input("Enter second number:           "))
        except ValueError:
            print("Invalid input. Please enter numbers only.")
            print()
            continue

        # Perform the calculation
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0:
                print("Error: division by zero")
                print()
                continue
            else:
                result = num1 / num2

        # Display the result with a progress bar
        print("Calculating...")
        progress_bar(calculate_time)
        print()
        print(f"Result: {result}")
        print()


calculator()
