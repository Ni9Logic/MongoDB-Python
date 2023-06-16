import pymongo
import bcrypt
from dotenv import dotenv_values


class Database:
    def __init__(self):
        # Loading data from the .env files
        self.env_vars = dotenv_values()
        self.connectionString = self.env_vars['DB_CONNECTION_STRING']

    def validate_user(self, db, username, password):
        collection = db['Users']
        query = {"Username": username}
        user = collection.find_one(query)

        if user:
            account_password = user.get('Password')
            print((account_password), (password), (bcrypt.hashpw(password, bcrypt.gensalt())))
            if account_password and bcrypt.checkpw(password, account_password):
                return user
        else:
            return False

    def create_user(self, db, username: str, password: str, account_type: bool, is_admin: bool, dob: str,
                    created_at: str,
                    bank_bal: float):
        # Loading collection of users from users table
        collection = db['Users']

        # Hashing password
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        # Creating a dictionary of an object and this will be inserted inside the collection of table users
        user_data = {
            "Username": username,
            "Password": hashed_password,
            "Account_type": account_type,
            "is_Admin": is_admin,
            "Date-Of-Birth": dob,
            "Created-At": created_at,
            "Balance": bank_bal
        }

        # Inserting the user inside database and table users
        is_created = collection.insert_one(user_data)

        # Print the inserted document ID
        print(f"User created with ID: {is_created.inserted_id}")

    def find_by_username(self, db, username):
        collection = db['Users']
        query = {"Username": username}
        result = collection.find(query)

        return result

    def is_connected(self):
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
