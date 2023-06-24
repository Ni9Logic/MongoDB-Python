import time
import Colors
import pymongo

def create_transaction(db: object, from_user: str, transaction_type: str, transaction_amount: float, to_user = None) -> None:

    # Lets say if the user withdraws or deposits he doesn't need a to user
    transaction = {
            "Username": from_user,
            "Transaction Type": transaction_type,
            f"To User: {to_user},\n" if to_user != None else ""
            "Transaction Amount": transaction_amount,
            "Transaction At": time.strftime('%c', time.localtime())
        }
    
    

    collection = db['Transactions']
    is_added = collection.insert_one(transaction)

    if is_added:
        pass
    else:
        print(f"\t\t\tRandom {Colors.red_color('Error')} Occurred while adding a transaction...")

def show_user_transactions(db: object, current_user: str) -> object or str:
    collection = db['Transactions']
    query = {'Username': current_user.get('Username')}

    # This only gives us the last 5 results if there are and sorts them in Descending order.
    transactions = collection.find(query).sort("_id", pymongo.DESCENDING).limit(5)

    if transactions:
        return transactions
    else:
        print(f"\t\t\tNo transactions found... ")
        
