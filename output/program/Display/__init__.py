import Colors
import os


def center_text_between_lines(text):
    line_length = len(text) + 4  # Length of the line containing dashes, accounting for padding

    # Create the line of dashes
    line = '-' * line_length

    # Construct the centered text with lines
    centered_text = f"\t\t\t{line}\n\t\t\t\t{text}\n\t\t\t{line}"

    return centered_text


# Clears the terminal
def clear_screen():
    # Check the operating system
    os.system('clear') if os.name == 'posix' else os.system('cls')


# Pauses the screen
def pause_screen():
    input(f"\t\t\tPress {Colors.red_color('any')} key to continue...")
