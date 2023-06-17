import pymongo
import bcrypt
import datetime
import os
from dotenv import load_dotenv


class Database:
    def __init__(self):
        # Loading data from the .env files
        load_dotenv()
        self.connectionString = os.environ.get('DB_CONNECTION_STRING')

    def delete_user(self, db, username):
        collection = db['Users']

        is_deleted = collection.delete_one({"Username": username})

        return is_deleted

    def get_all_users(self, db):
        collection = db['Users']
        users = collection.find()

        return users

    def validate_user(self, db, username, password) -> object or bool:
        collection = db['Users']
        query = {"Username": username}
        user = collection.find_one(query)

        if user:
            account_password = user.get('Password')
            if account_password and bcrypt.checkpw(password, account_password):
                return user
        else:
            return False

    def create_user(self, db, username: str, password: str, account_type: bool, is_admin: bool, dob: str,
                    bank_bal: str) -> None:
        # Loading collection of users from users table
        collection = db['Users']

        # Hashing password
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # Formatting createdAt in the right format
        created_at = datetime.datetime.now()
        formatted_created_at = created_at.strftime("%Y-%m-%d %H:%M:%S")

        # Creating a dictionary of an object and this will be inserted inside the collection of table users
        user_data = {
            "Username": username,
            "Password": hashed_password,
            "Account_type": account_type,
            "is_Admin": is_admin,
            "Date-Of-Birth": dob,
            "Created-At": formatted_created_at,
            "Balance": bank_bal
        }

        # Inserting the user inside database and table users
        is_created = collection.insert_one(user_data)

        # Print the inserted document ID
        print(f"\t\t\tUser created with ID: {is_created.inserted_id}")

    def update_user(self, db, field_name, old_data, new_data):
        collection = db['Users']
        is_find = {f'{field_name}': old_data}
        is_update = {'$set': {f'{field_name}': new_data}}

        is_updated = collection.update_one(is_find, is_update)

        return is_updated

    def find_by_username(self, db, username) -> object:
        collection = db['Users']
        query = {"Username": username}
        isFound = collection.find_one(query)

        return isFound

    def is_connected(self) -> bool:
        try:
            # Establish a connection to the MongoDB database
            client = pymongo.MongoClient(self.connectionString)

            # Check if the connection is successful
            if client.server_info():
                return True
            else:
                return False

        except pymongo.mongo_client.ConnectionFailure as e:
            print(f"Error connecting to MongoDB: {e}")

    def get_client(self):
        try:
            client = pymongo.MongoClient(self.connectionString)
            if client.server_info():
                return client

        except pymongo.mongo_client.ConnectionFailure as e:
            print(f"Error connecting to MongoDB: {e}")
