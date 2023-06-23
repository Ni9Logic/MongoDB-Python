import time
import Colors

def create_transaction(db: object, from_user: str, transaction_type: str, transaction_amount: float, to_user = None) -> None:

    # Lets say if the user withdraws or deposits he doesn't need a to user
    if to_user == None:
        transaction = {
                "Username": from_user,
                "Transaction Type": transaction_type,
                "To User": 'None',
                "Transaction Amount": transaction_amount,
                "Transaction At": time.strftime('%c', time.localtime())
            }
    else:
        transaction = {
                "Username": from_user,
                "Transaction Type": transaction_type,
                "To User": to_user,
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

    transactions = collection.find(query)

    if transactions:
        return transactions
    else:
        print(f"\t\t\tNo transactions found... ")
        
