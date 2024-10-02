import sys

# Bank system data with initial accounts
bank_data = {
    "users": {
        "mdluffy": {
            "account_number": "101",
            "password": "password",
            "balance": 4850,
            "deposits": {1000: 4, 500: 1, 200: 2, 100: 0, 50: 0, 20: 7, 10: 1, 5: 9, 1: 14}
        },
        "buggy_d_clown": {
            "account_number": "102",
            "password": "12345",
            "balance": 4075,
            "deposits": {1000: 2, 500: 2, 200: 3, 100: 0, 50: 6, 20: 7, 10: 7, 5: 5, 1: 20}
        },
        "pulang.buhok": {
            "account_number": "103",
            "password": "pulang.buhok",
            "balance": 5857,
            "deposits": {1000: 5, 500: 1, 200: 1, 100: 0, 50: 5, 20: 5, 10: 2, 5: 2, 1: 7}
        },
        "balbas-ay-black": {
            "account_number": "104",
            "password": "111",
            "balance": 5703,
            "deposits": {1000: 4, 500: 1, 200: 1, 100: 0, 50: 5, 20: 7, 10: 1, 5: 6, 1: 4}
        }
    },
    "closed_accounts": set(),
    "last_account_number": 104,
    "system_balance": {1000: 15, 500: 5, 200: 7, 100: 0, 50: 16, 20: 26, 10: 11, 5: 22, 1: 45}  # total system balance
}

denominations = [1000, 500, 200, 100, 50, 20, 10, 5, 1]


def separator():
    print("\n" + "- " * 20 + "\n")


def welcome():
    while True:
        separator()
        print("WELCOME TO THE DIGITAL BANKING SYSTEM")
        print("\n1. Log in")
        print("2. Create a new account")
        print("3. Exit")
        choice = input("Please choose an option: ")

        if choice == "1":
            login()
        elif choice == "2":
            create_new_account()
        elif choice == "3":
            exit_system()
        else:
            print("Invalid choice. Please try again.")


def login():
    attempts = 0
    while attempts < 3:
        separator()
        username = input("\nEnter username: ")
        account_number = input("Enter account number: ")
        password = input("Enter password: ")

        if (username in bank_data["users"] and
                bank_data["users"][username]["account_number"] == account_number and
                bank_data["users"][username]["password"] == password):
            print(f"\nWelcome back, {username}! You are now logged in.")
            transactions(username)
            return
        else:
            attempts += 1
            print(f"Invalid login details. {3 - attempts} attempts left.")

    print("Too many failed attempts. Returning to the welcome page.")
    welcome()


def create_new_account():
    attempts = 0
    while attempts < 3:
        separator()
        username = input("\nCreate a username: ")
        if username in bank_data["users"]:
            print("Username is taken. Try another one.")
        else:
            password = input("Create a password: ")
            account_number = str(bank_data["last_account_number"] + 1)
            deposit = get_deposit()

            if deposit >= 500:
                bank_data["users"][username] = {
                    "account_number": account_number,
                    "password": password,
                    "balance": deposit,
                    "deposits": {1000: 0, 500: 0, 200: 0, 100: 0, 50: 0, 20: 0, 10: 0, 5: 0, 1: 0}
                }
                bank_data["last_account_number"] += 1
                update_system_balance(deposit)
                print(f"Account created successfully! Your account number is {account_number}.")
                login()
                return
            else:
                print("Minimum deposit is PHP 500. Please try again.")
                attempts += 1
                if attempts >= 3:
                    print("Too many failed attempts. Returning to the welcome page.")
                    welcome()
                    return


def get_deposit():
    deposit = 0
    print("\nDeposit a combination of the following denominations:")
    print(", ".join([f"PHP {den}" for den in denominations]))

    while deposit < 500:
        try:
            amount = int(input("Enter the deposit amount (PHP): "))
            if amount in denominations:
                deposit += amount
                print(f"Total deposited: PHP {deposit}")
            else:
                print("Invalid denomination. Please enter a valid denomination.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    return deposit


def transactions(username):
    while True:
        separator()
        print("\n1. Check balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Close account")
        print("5. Log out")
        choice = input("Select a transaction: ")

        if choice == "1":
            check_balance(username)
        elif choice == "2":
            deposit(username)
        elif choice == "3":
            withdraw(username)
        elif choice == "4":
            close_account(username)
        elif choice == "5":
            log_out()
            break
        else:
            print("Invalid choice. Try again.")


def check_balance(username):
    separator()
    balance = bank_data["users"][username]["balance"]
    print(f"Your current balance is PHP {balance}.")
    more_transactions(username)


def deposit(username):
    separator()
    deposit_amount = get_deposit()
    bank_data["users"][username]["balance"] += deposit_amount
    update_system_balance(deposit_amount)
    print(f"Deposit successful! Your new balance is PHP {bank_data['users'][username]['balance']}.")
    more_transactions(username)


def update_system_balance(amount):
    for denomination in denominations:
        while amount >= denomination:
            bank_data["system_balance"][denomination] += 1
            amount -= denomination


def withdraw(username):
    separator()
    try:
        amount = int(input("\nEnter the amount to withdraw (PHP): "))
        if amount > bank_data["users"][username]["balance"]:
            print("Error: Insufficient account balance.")
        elif not can_withdraw(amount):
            print("Error: Unable to dispense exact amount with available denominations.")
        else:
            dispense_cash(amount)
            bank_data["users"][username]["balance"] -= amount
            print(f"Withdrawal successful! Your new balance is PHP {bank_data['users'][username]['balance']}.")
    except ValueError:
        print("Invalid amount. Please enter a valid number.")

    more_transactions(username)


def can_withdraw(amount):
    temp_balance = bank_data["system_balance"].copy()
    for denomination in denominations:
        while amount >= denomination and temp_balance[denomination] > 0:
            amount -= denomination
            temp_balance[denomination] -= 1
    return amount == 0


def dispense_cash(amount):
    print("Dispensing:")
    for denomination in denominations:
        count = 0
        while amount >= denomination and bank_data["system_balance"][denomination] > 0:
            amount -= denomination
            bank_data["system_balance"][denomination] -= 1
            count += 1
        if count > 0:
            print(f"{count} x PHP {denomination}")


def close_account(username):
    separator()
    attempts = 0
    while attempts < 3:
        password = input("Please enter your password to close the account: ")
        if password == bank_data["users"][username]["password"]:
            withdraw(username)  # Withdraw all funds
            bank_data["closed_accounts"].add(bank_data["users"][username]["account_number"])
            del bank_data["users"][username]
            print("Account closed successfully.")
            welcome()
            return
        else:
            attempts += 1
            print(f"Incorrect password. {3 - attempts} attempts left.")
    print("Too many failed attempts. Returning to the transactions page.")
    transactions(username)


def log_out():
    print("Logging out...")


def more_transactions(username):
    choice = input("Would you like to make another transaction? (yes/no): ").strip().lower()
    if choice == 'yes':
        transactions(username)
    else:
        log_out()


def exit_system():
    separator()
    print("\nThank you for using the digital banking system. Goodbye!")
    sys.exit()


if __name__ == "__main__":
    welcome()
