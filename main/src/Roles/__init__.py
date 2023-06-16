import Colors
import Display
import bcrypt


class User:
    pass


class Admin:
    # Just a login menu
    def to_login(self, database, db):
        Display.clear_screen()
        # Dialogue Message
        print(Display.center_text_between_lines(Colors.green_color('Banking Management System')))

        # Getting username and password from the user
        user_to_login = input(f"\t\t\tEnter {Colors.yellow_color('Username')}: ")
        password = input(f"\t\t\tEnter {Colors.yellow_color('Password')}: ").encode('utf-8')

        # Validating the user
        current_user = database.validate_user(db, user_to_login, password)

        return current_user

    # Display all the users    
    def display_all_users(self, database, db):
        # View all the users
        while True:
            Display.clear_screen()
            print(Display.center_text_between_lines(f"{Colors.yellow_color('View All Users')}"))
            users = database.get_all_users(db)

            for count, user in enumerate(users):
                print(f"\t\t\t{count + 1}. {Colors.blue_color(user['Username'])}")

            break

    # Display a specific user
    def display_specific_user(self, database, db):
        while True:
            Display.clear_screen()
            print(Display.center_text_between_lines(f"{Colors.yellow_color('Find Specific User')}"))
            user_to_find = input(f"\t\t\tEnter {Colors.green_color('Username')}: ")

            user = database.find_by_username(db, user_to_find)
            if user:
                print(f"\t\t\tUsername: {Colors.blue_color(user.get('Username'))}")
                print(f"\t\t\tPassword: {Colors.blue_color(str(user.get('Password')))}")
                print(f"\t\t\tAccount Type: {Colors.blue_color(str(user.get('Account_type')))}")
                print(f"\t\t\tAdmin Status: {Colors.blue_color(str(user.get('is_Admin')))}")
                print(f"\t\t\tDate of Birth: {Colors.blue_color(str(user.get('Date-Of-Birth')))}")
                print(f"\t\t\tCreated At: {Colors.blue_color(str(user.get('Created-At')))}")
                print(f"\t\t\tCurrent Balance: {Colors.blue_color(str(user.get('Balance')))}")
            else:
                print(f"\t\t\tNo such user found... ")

            break

    # Deleting a user
    def delete_user(self, database, db):
        # Deleting a user
        while True:
            Display.clear_screen()
            print(Display.center_text_between_lines(f"{Colors.yellow_color('Delete User')}"))

            user_to_delete = input(f"\t\t\tEnter {Colors.green_color('Username')}: ")
            is_deleted = database.delete_user(db, user_to_delete)

            if is_deleted.deleted_count == 1:
                print(f"\t\t\tUser {Colors.red_color(user_to_delete)} has successfully been deleted...")
            else:
                print("\t\t\tNo such user found...")

            break

    # Creating a user
    def create_user(self, database, db):
        # Creating a user
        while True:
            Display.clear_screen()
            print(Display.center_text_between_lines(f"{Colors.yellow_color('Create User')}"))

            # Set username and password
            user_to_create_name = input(f"\t\t\tEnter {Colors.blue_color('Username')}: ")

            # Here we are going to check if the user already exists or not because we want our usernames to be unique
            is_existAlready = database.find_by_username(db, user_to_create_name)
            if is_existAlready:
                print(f"\t\t\tSorry the username {Colors.green_color(user_to_create_name)} already exists... ")
                Display.pause_screen()
                continue

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

            database.create_user(db, user_to_create_name, user_to_create_password, account_type, is_Admin,
                                 dob_to_create, starting_balance)
            break

    # Update a user
    def update_user(self, database, db):
        # Update a user
        while True:
            Display.clear_screen()
            print(Display.center_text_between_lines(f"{Colors.yellow_color('Update User')}"))

            user_to_update = input(f"\t\t\tEnter {Colors.green_color('Username')}: ")
            is_Found = database.find_by_username(db, user_to_update)

            if is_Found:
                print(f"\t\t\t1. Update {Colors.blue_color('Username')}")
                print(f"\t\t\t2. Update {Colors.blue_color('Password')}")

                choice = input(f"\t\t\tEnter {Colors.yellow_color('<1-2>')}: ")
                if choice == '1':
                    new_username = input(f"\n\t\t\tEnter {Colors.green_color('new')} {Colors.blue_color('username')}: ")

                    is_updated = database.update_user(db, 'Username', user_to_update, new_username)

                    if is_updated:
                        print(f"\t\t\tUser {Colors.green_color(user_to_update)} has successfully been updated...")
                    else:
                        print(f"\t\t\tNo such user found...")

                elif choice == '2':
                    new_password = input(
                        f"\n\t\t\tEnter {Colors.green_color('new')} {Colors.blue_color('password')}: ").encode('utf-8')
                    my_user = database.find_by_username(db, user_to_update)

                    old_password = my_user.get('Password')
                    hashed_newPass = bcrypt.hashpw(new_password, bcrypt.gensalt())

                    is_updated = database.update_user(db, 'Password', old_password, hashed_newPass)

                    if is_updated:
                        print(f"\t\t\tUser {Colors.green_color(user_to_update)} has successfully been updated...")
                    else:
                        print(f"\t\t\tNo such user found...")

                else:
                    print(f"\t\t\t{Colors.red_color('Invalid Choice...')} ")
            else:
                print("\t\t\tNo such user found... ")

            break

    # Display admin menu
    def admin_menu(self, current_user: object):
        Display.clear_screen()
        print(Display.center_text_between_lines("Welcome, " + Colors.yellow_color(f"{current_user.get('Username')}")))
        print("\t\t\t1. Create User")
        print("\t\t\t2. Delete User")
        print("\t\t\t3. Update User")
        print("\t\t\t4. View Specific User")
        print("\t\t\t5. View All Users")
        print("\t\t\t6. Log Out")
        print("\t\t\t7. Exit Program")
