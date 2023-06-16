import Colors
import Display
from Roles import Admin
from Database.database_connection import Database


# Main Function
def main():
    # Database Object
    database = Database()

    # Mongo db client
    client = database.get_client()

    # Selecting current database
    db = client['bms']

    # Admin Object Re
    admin = Admin()

    while True:
        current_user = admin.to_login(database, db)
        if current_user:
            print(f"\t\t\tLogged in {Colors.green_color('Successfully')}\n")
            print(f"\t\t\tWelcome, {Colors.blue_color(current_user.get('Username'))}")

            # Pauses the screen
            Display.pause_screen()

            # We only want to show this menu if the user currently logging in is admin or not
            if current_user.get('is_Admin'):
                while True:
                    admin.admin_menu(current_user)

                    choice = input(f"\t\t\tEnter {Colors.yellow_color('<1-7>')}: ")
                    if choice == '7':
                        # Simply exit the program
                        Display.clear_screen()
                        exit(0)
                    elif choice == '6':
                        break
                    elif choice == '5':
                        admin.display_all_users(database, db)
                    elif choice == '4':
                        admin.display_specific_user(database, db)
                    elif choice == '3':
                        admin.update_user(database, db)
                    elif choice == '2':
                        admin.delete_user(database, db)
                    elif choice == '1':
                        admin.create_user(database, db)

                    else:
                        print(f"\t\t\t{Colors.red_color('Invalid Choice')}")

                    Display.pause_screen()

        else:
            print(f"\t\t\tInvalid {Colors.red_color('Credentials')}")
            Display.pause_screen()


if __name__ == '__main__':
    main()
