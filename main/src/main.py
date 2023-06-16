import os
import Colors
import Display
from Database.database_connection import Database


def clear_screen():
    # Check the operating system
    os.system('clear') if os.name == 'posix' else os.system('cls')


def pause_screen():
    input(f"\t\t\tPress {Colors.red_color('any')} key to continue...")


def main():
    database = Database()
    client = database.get_client()
    db = client['bms']

    while True:
        clear_screen()
        # Dialogue Message
        print(Display.center_text_between_lines(Colors.green_color('Banking Management System')))

        # Getting username and password from the user
        user_to_delete = input(f"\t\t\tEnter {Colors.yellow_color('Username')}: ")
        password = input(f"\t\t\tEnter {Colors.yellow_color('Password')}: ").encode('utf-8')

        # Validating the user
        current_user = database.validate_user(db, user_to_delete, password)
        if current_user:
            print(f"\t\t\tLogged in {Colors.green_color('Successfully')}\n")
            print(f"\t\t\tWelcome, {Colors.blue_color(current_user.get('Username'))}")

            # Pauses the screen
            pause_screen()

            # We only want to show this menu if the user currently logging in is admin or not
            if current_user.get('is_Admin'):
                while True:
                    clear_screen()
                    print(Display.center_text_between_lines("Welcome, " + Colors.yellow_color(f"{current_user.get('Username')}")))
                    print("\t\t\t1. Create User")
                    print("\t\t\t2. Delete User")
                    print("\t\t\t3. Update User")
                    print("\t\t\t4. View Users")
                    print("\t\t\t5. Log Out")
                    print("\t\t\t6. Exit Program")

                    choice = input(f"\t\t\tEnter {Colors.yellow_color('<1-6>')}: ")
                    if choice == '6':
                        # Simply exit the program
                        clear_screen()
                        exit(0)
                    elif choice == '5':
                        break
                    elif choice == '4':
                        # View all the users
                        while True: 
                            clear_screen()
                            print(Display.center_text_between_lines(f"{Colors.yellow_color('View All Users')}"))
                            users = database.get_all_users(db)

                            for count, user in enumerate(users):
                                print(f"\t\t\t{count + 1}. {Colors.blue_color(user['Username'])}")

                            break
                    elif choice == '3':
                        pass
                    elif choice == '2':
                        # Deleting a user
                        while True:
                            clear_screen()
                            print(Display.center_text_between_lines(f"{Colors.yellow_color('Delete User')}"))

                            user_to_delete = input(f"\t\t\tEnter {Colors.green_color('Username')}: ")
                            is_deleted = database.delete_user(db, user_to_delete)
                            
                            if is_deleted.deleted_count == 1:
                                print(f"\t\t\tUser {Colors.red_color(user_to_delete)} has successfully been deleted...")
                            else:
                                print("\t\t\tNo such user found...")

                            break
                    elif choice == '1':
                        # Creating a user
                        while True:
                            clear_screen()
                            print(Display.center_text_between_lines(f"{Colors.yellow_color('Create User')}"))\
                            
                            # Set username and password
                            user_to_create_name = input(f"\t\t\tEnter {Colors.blue_color('Username')}: ")
                            user_to_create_password = input(f"\t\t\tEnter {Colors.blue_color('Password')}: ")

                            # Account Type
                            print(f"\t\t\tUser {Colors.green_color('Account Type')}: ")
                            print(f"\t\t\t{Colors.red_color('1.')} Savings")
                            print(f"\t\t\t{Colors.red_color('2.')} Current")
                            account_type = input(f"\t\t\tEnter: {Colors.blue_color('<1-2>')}: ")
                            if account_type == '1':
                                account_type = True
                            else:
                                account_type = False

                            
                            # Admin account or not
                            print(f"\t\t\tUser {Colors.green_color('Admin')}: ")
                            print(f"\t\t\t{Colors.green_color('1.')} Yes")
                            print(f"\t\t\t{Colors.red_color('2.')} No")
                            is_Admin = input(f"\t\t\tEnter: {Colors.blue_color('<1-2>')}: ")
                            if is_Admin == '1':
                                is_Admin = True
                            else:
                                is_Admin = False


                            # Date of birth
                            dob_to_create = input(f"\t\t\tEnter {Colors.red_color('Date-of-birth')}: ")
                            starting_balance = input(f"\t\t\tEnter {Colors.green_color('Starting Balance')}: ")

                            database.create_user(db, user_to_create_name, user_to_create_password, account_type, is_Admin, dob_to_create, starting_balance)
                            break
                        
                    else:
                        print(f"\t\t\t{Colors.red_color('Invalid Choice')}")

                    pause_screen()

        else:
            print(f"\t\t\tInvalid {Colors.red_color('Credentials')}")
            pause_screen()



if __name__ == '__main__':
    main()
