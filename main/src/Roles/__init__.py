import Display
import Colors
import bcrypt

class User:

    def user_menu(self, current_user: object) -> None:
        Display.clear_screen()
        print(Display.center_text_between_lines("Welcome, " + Colors.yellow_color(f"{current_user.get('Username')}")))
        print("\t\t\t1. Withdraw Amount")
        print("\t\t\t2. Deposit Amount")
        print("\t\t\t3. Transfer Amount")
        print("\t\t\t4. View Profile")
        print("\t\t\t5. View Last 5 Transactions")
        print("\t\t\t6. Log Out")
        print("\t\t\t7. Exit Program")

    def deposit(self, db, current_user: object) -> None:
        Display.clear_screen()
        print(Display.center_text_between_lines(f"{Colors.yellow_color('Deposit Amount')}"))

        print(f"\t\t\tYour current balance is {Colors.green_color(current_user.get('Balance'))}")
        
        # This is to avoid if someone enters a string where he's expected to enter a number
        try:
            # Amount to deposit
            amount_to_deposit = float(input("\t\t\tEnter the amount you want to deposit: "))
            current_balance = float(current_user.get('Balance'))

            # Getting the new balance
            new_balance = amount_to_deposit + current_balance

            # Updating the balance
            from_update = {'Balance': current_user.get('Balance')}
            to_update = {'$set': {'Balance': str(new_balance)}}

            # Committing into the database
            collection = db['Users']
            is_updated = collection.update_one(from_update, to_update)

            # Checking
            if is_updated:
                print(f"\t\t\tYou have successfully withdrawn {Colors.green_color(str(amount_to_deposit))} rs /-")
                print(f"\t\t\tYour new balance is: {Colors.blue_color(str(new_balance))} rs /-")
            else:
                print(f"\t\t\tSome random {Colors.red_color('Error')} has occurred...")

        
        except ValueError:
            print("\t\t\tKindly enter a correct value...")

    def withdraw(self, db, current_user: object) -> None:
        while True:
            Display.clear_screen()
            print(Display.center_text_between_lines(f"{Colors.yellow_color('Withdraw Amount')}"))

            
            print(f"\t\t\tYour current balance is {Colors.green_color(current_user.get('Balance'))}")

            # This is to avoid if someone enters a string where he's expected to enter a number
            try:
                # Amount to withdraw
                amount_to_withdraw = float(input("\t\t\tEnter the amount you want to withdraw: "))

                if amount_to_withdraw > float(current_user.get('Balance')):
                    print(f"\t\t\tThe amount you are trying to {Colors.green_color('Withdraw')} is greater than "
                          f"{Colors.green_color('Current Balance')}...")
                else:
                    # Updating balance
                    from_update = {'Balance': current_user.get('Balance')}
                    to_update = {'$set': {'Balance': str(float(current_user.get('Balance')) - amount_to_withdraw)}}

                    # Committing the changes in the database
                    collection = db['Users']
                    is_updated = collection.update_one(from_update, to_update)

                    # Checking
                    if is_updated:
                        print(f"\t\t\tYou have successfully withdrawn {Colors.green_color(str(amount_to_withdraw))} rs /-")
                        print(f"\t\t\tYour new balance is: {Colors.blue_color(str(float(current_user.get('Balance')) - amount_to_withdraw))} rs /-")

                    else:
                        print(f"\t\t\tSome random {Colors.red_color('Error')} has occurred...")

            except ValueError:
                print("\t\t\tKindly Enter a correct value... ")

            break
    
    def view_profile(self, current_user: object) -> None:
        while True:
            Display.clear_screen()
            print(Display.center_text_between_lines(f"{Colors.yellow_color('View Profile')}"))

            print(f"\t\t\tUsername: {Colors.blue_color(current_user.get('Username'))}")
            print(f"\t\t\tPassword: {Colors.blue_color(str(current_user.get('Password')))}")
            print(f"\t\t\tAccount Type: {Colors.blue_color(str(current_user.get('Account_type')))}")
            print(f"\t\t\tDate of Birth: {Colors.blue_color(str(current_user.get('Date-Of-Birth')))}")
            print(f"\t\t\tCreated At: {Colors.blue_color(str(current_user.get('Created-At')))}")
            print(f"\t\t\tCurrent Balance: {Colors.blue_color(str(current_user.get('Balance')))}")
            
            break

    def transfer_balance(self, database: object, db, current_user: object) -> None:
        while True:
            Display.clear_screen()
            print(Display.center_text_between_lines(f"{Colors.yellow_color('Transfer Amount')}"))
            
            # Amount he wants to transfer
            try:
                amount_to_transfer = float(input(f"\t\t\tEnter the amount to {Colors.green_color('Transfer')}: "))

                # Checking if the amount user wants to send is available in his asset
                if amount_to_transfer > float(current_user.get('Balance')):
                    print(f"\t\t\tThe amount you wish to {Colors.green_color('transfer')} is {Colors.red_color('greater')} than {Colors.blue_color('available balance')}")
                else:
                    # Name of the user to whom the amount shall be sent
                    to_username = input(f"\t\t\tEnter {Colors.green_color('their')} username: ")

                    # Lets check if the user didn't entered their own username
                    if to_username == current_user.get('Username'):
                        print(f"\t\t\tYou {Colors.red_color('cannot')} enter your own username...")
                    else:
                        # Findind the user inside database
                        to_user_exist = database.find_by_username(db, to_username)
                        
                        # Checking if the user exists or not
                        if to_user_exist:
                            # If the user exists we want to deposit the amount in his account and withdraw amount from in session user
                            
                            # Firstly wihdrawing from current user
                            from_update = {'Balance': current_user.get('Balance')}
                            to_update = {'$set': {'Balance': str(float(current_user.get('Balance')) - amount_to_transfer)}}

                            # Commiting the withdraw
                            collection = db['Users']
                            collection.update_one(from_update, to_update)

                            # Now depositing the amount in the to_username
                            from_update = {'Balance': to_user_exist.get('Balance')}
                            to_update = {'$set': {'Balance': str(float(to_user_exist.get('Balance')) + amount_to_transfer)}}

                            # Commiting the deposit
                            collection = db['Users']
                            collection.update_one(from_update, to_update)

                            # Success message
                            print(f"\t\t\tAmount has {Colors.green_color('successfully')} transferred...")
                        
                        else:
                            print(f"\t\t\tNo such user exists...")
                                    
            except ValueError:
                print(f"\t\t\tKindly enter {Colors.green_color('correct')} value...")

            break

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
