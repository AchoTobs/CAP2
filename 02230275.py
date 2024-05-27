# Your_Name:TOBDEN THAPA
# Your_Section:ME
# Your_Student ID Number:02230275
################################
# REFERENCES
#https://youtu.be/rfscVS0vtbw
#https://youtu.be/QXeEoD0pB3E?list=PLsyeobzWxl7poL9JTVyndKe62ieoN-MZ3
#https://youtu.be/hEgO047GxaQ?list=PLsyeobzWxl7poL9JTVyndKe62ieoN-MZ3
#https://youtu.be/CScxy0294SE?list=PLsyeobzWxl7poL9JTVyndKe62ieoN-MZ3
###############################


import os
import random
import hashlib
import uuid

# Base class for all accounts
class Account:
    def __init__(self, account_id, password, account_type, balance=0, interest_rate=0):
        self.account_id = account_id
        self.password = self.hash_password(password)
        self.account_type = account_type
        self.balance = balance
        self.interest_rate = interest_rate

    # Hash the password with a salt for security
    def hash_password(self, password):
        salt = uuid.uuid4().hex
        hashed_pw = hashlib.sha256(salt.encode() + password.encode()).hexdigest()
        return f"{salt}${hashed_pw}"

    # Check if the given password matches the stored hashed password
    def check_password(self, password):
        salt, hashed_pw = self.password.split('$')
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() == hashed_pw

    # Deposit an amount to the account
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    # Withdraw an amount from the account if sufficient balance is available
    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    # Convert account details to a string for file storage
    def to_string(self):
        return f"{self.account_id},{self.password},{self.account_type},{self.balance},{self.interest_rate}\n"

    # Create an Account object from a string
    @staticmethod
    def from_string(data):
        parts = data.split(',')
        if len(parts) == 4:  # Handle old format without interest rate
            account_id, password, account_type, balance = parts
            interest_rate = 0.01 if account_type == "Personal" else 0.02
        elif len(parts) == 5:  # Handle new format with interest rate
            account_id, password, account_type, balance, interest_rate = parts
        else:
            raise ValueError(f"Incorrect data format: {data}")
        return Account(account_id, password, account_type, float(balance), float(interest_rate))

# Derived class for Business accounts
class BusinessAccount(Account):
    def __init__(self, account_id, password, balance=0):
        super().__init__(account_id, password, 'Business', balance, interest_rate=0.02)

# Derived class for Personal accounts
class PersonalAccount(Account):
    def __init__(self, account_id, password, balance=0):
        super().__init__(account_id, password, 'Personal', balance, interest_rate=0.01)

# Class representing the Bank containing multiple accounts
class Bank:
    def __init__(self, filename="accounts.txt"):
        self.accounts = {}
        self.filename = filename
        self.load_accounts()

    # Load accounts from the file
    def load_accounts(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    try:
                        account = Account.from_string(line.strip())
                        self.accounts[account.account_id] = account
                    except ValueError as e:
                        print(f"Error loading account: {e}")

    # Save accounts to the file
    def save_accounts(self):
        with open(self.filename, 'w') as file:
            for account in self.accounts.values():
                file.write(account.to_string())

    # Create a new account and save it
    def create_account(self, account_type):
        account_id = str(random.randint(100000, 999999))
        password = str(random.randint(1000, 9999))
        if account_type == "Business":
            account = BusinessAccount(account_id, password)
        elif account_type == "Personal":
            account = PersonalAccount(account_id, password)
        else:
            return None

        self.accounts[account.account_id] = account
        self.save_accounts()
        return account_id, password

    # Authenticate an account with ID and password
    def authenticate(self, account_id, password):
        account = self.accounts.get(account_id)
        if account and account.check_password(password):
            return account
        return None

    # Delete an account by ID
    def delete_account(self, account_id):
        if account_id in self.accounts:
            del self.accounts[account_id]
            self.save_accounts()
            return True
        return False

    # Transfer money from one account to another
    def transfer_money(self, from_account, to_account_id, amount):
        if to_account_id not in self.accounts:
            return False, "Receiving account does not exist."
        if from_account.balance < amount:
            return False, "Insufficient funds."
        to_account = self.accounts[to_account_id]
        from_account.withdraw(amount)
        to_account.deposit(amount)
        self.save_accounts()
        return True, "Transfer successful."

# Class for the bank application handling user interaction
class BankApplication:
    def __init__(self):
        self.bank = Bank()

    # Main loop for the application
    def run(self):
        print("Welcome to the Bank Application")

        while True:
            print("\n1. Open Account")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.open_account()
            elif choice == "2":
                self.login()
            elif choice == "3":
                print("Thank you for using the Bank Application. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    # Handle account creation
    def open_account(self):
        account_type = input("Enter account type (Business/Personal): ")
        account_id, password = self.bank.create_account(account_type)
        if account_id:
            print(f"Account created successfully! Your account number is {account_id} and your password is {password}")
        else:
            print("Invalid account type.")

    # Handle user login
    def login(self):
        account_id = input("Enter account number: ")
        password = input("Enter password: ")
        account = self.bank.authenticate(account_id, password)
        if account:
            print(f"Login successful! Welcome, {account.account_type} account holder.")
            self.account_menu(account)
        else:
            print("Authentication failed. Please check your account number and password.")

    # Menu for account-specific operations
    def account_menu(self, account):
        while True:
            print("\n1. Check Balance")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Transfer Money")
            print("5. View Account Details")
            print("6. Delete Account")
            print("7. Logout")
            sub_choice = input("Enter your choice: ")
            if sub_choice == "1":
                print(f"Your balance is: {account.balance}")
            elif sub_choice == "2":
                self.deposit_money(account)
            elif sub_choice == "3":
                self.withdraw_money(account)
            elif sub_choice == "4":
                self.transfer_money(account)
            elif sub_choice == "5":
                self.view_account_details(account)
            elif sub_choice == "6":
                if self.bank.delete_account(account.account_id):
                    print("Account deleted successfully.")
                    break
                else:
                    print("Error in deleting account.")
            elif sub_choice == "7":
                print("Logged out successfully.")
                break
            else:
                print("Invalid choice. Please try again.")

    # Handle depositing money
    def deposit_money(self, account):
        amount = float(input("Enter amount to deposit: "))
        if account.deposit(amount):
            self.bank.save_accounts()
            print(f"Deposited successfully. New balance: {account.balance}")
        else:
            print("Invalid amount.")

    # Handle withdrawing money
    def withdraw_money(self, account):
        amount = float(input("Enter amount to withdraw: "))
        if account.withdraw(amount):
            self.bank.save_accounts()
            print(f"Withdrawn successfully. New balance: {account.balance}")
        else:
            print("Invalid amount or insufficient balance.")

    # Handle transferring money
    def transfer_money(self, from_account):
        to_account_id = input("Enter the account number to transfer to: ")
        amount = float(input("Enter the amount to transfer: "))
        success, message = self.bank.transfer_money(from_account, to_account_id, amount)
        print(message)

    # Display account details
    def view_account_details(self, account):
        print(f"Account ID: {account.account_id}")
        print(f"Account Type: {account.account_type}")
        print(f"Balance: {account.balance}")
        print(f"Interest Rate: {account.interest_rate}")

if __name__ == "__main__":
    app = BankApplication()
    app.run()
