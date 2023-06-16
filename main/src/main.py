import os
import Colors
import Display
from Database.database_connection import Database


def clear_screen():
    # Check the operating system
    if os.name == 'posix':  # Linux and macOS
        os.system('clear')
    elif os.name == 'nt':  # Windows
        os.system('cls')


def pause_screen():
    input(f"\t\t\tPress {Colors.red_color('any')} key to continue...")


def main():
    database = Database()
    client = database.get_client()
    db = client['bms']

    while True:
        clear_screen()
        print(Display.center_text_between_lines(Colors.green_color('Banking Management System')))
        username = input(f"\t\t\tEnter {Colors.yellow_color('Username')}: ")
        password = input(f"\t\t\tEnter {Colors.yellow_color('Password')}: ").encode('utf-8')
        current_user = database.validate_user(db, username, password)

        if current_user:
            print(f"\t\t\tLogged in {Colors.green_color('Successfully')}")
            pause_screen()
        else:
            print(f"\t\t\tInvalid {Colors.red_color('Credentials')}")
            pause_screen()


main()
