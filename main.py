from flask import Flask
import function


"""
This file displays an extra testing file for the functions in function.py.
Demonstrates a fully functional Command Line Interface (CLI) for the Online Banking program.
This file is not used in the final version of the program.
Run the app.py file to run the program using flask.
"""

# Function to display login or account creation options
def display_options():
    print("-------------------------------------------------------------")
    print("Welcome to Online Banking! Please Login or Create an Account:")
    print("-------------------------------------------------------------")
    print("1. Login")
    print("2. Create an Account")
    print("-------------------------------------------------------------")

# Create a new account using function.create_account()
def create_account(mydb):
    username = input("Enter your username: ")
    is_admin = False
    if username.lower() == "admin":
        username = input("Enter your admin username: ")
        password = input("Enter your admin password: ")
        is_admin = True
    else:
        password = input("Enter your password: ")
    email = input("Enter your email: ")
    pin = input("Enter your PIN: ")
    function.create_account(mydb,username, password, email, pin, is_admin)
    return function.login(mydb,username,password,is_admin)

# For user login using function.login()
def login(mydb):
    username = input("Enter your username: ")
    is_admin = False
    if username.lower() == "admin":
        username = input("Enter your admin username: ")
        password = input("Enter your admin password: ")
        is_admin = True
    else:
        password = input("Enter your password: ")
    return function.login(mydb,username,password,is_admin)


# Display user dashboard
def dashboard(mydb,user):
    while True:
        print("\n-------------------------------------------------------------")
        print("Welcome to Your Dashboard, "+user[1]+"!")  
        print("-------------------------------------------------------------")
        print("1. Check Balance")
        print("2. Deposit Funds")
        print("3. Withdraw Funds")
        print("4. Modify Account Details")
        print("5. Logout")
        if user[7]: # Checking admin privileges
            print("6. View Database")
        print("-------------------------------------------------------------")
        choice = input("Enter your choice (1-5): ")

        # Handling user choices
        if choice == "1":
            balance = function.check_balance(mydb, user[4]) 
            if balance is not None:
                print("Your current balance is: ${:.2f}".format(balance))
        elif choice == "2":
            pin = int(input("PIN: "))
            if(function.check_pin(mydb,user[4],pin)):
                amount = float(input("Enter the amount to deposit: $"))
                function.deposit_funds(mydb, user[4], amount) 
            else:
                print("Incorrect PIN. Please try again.") 
        elif choice == "3":
            pin = int(input("PIN: "))
            if(function.check_pin(mydb,user[4],pin)):
                amount = float(input("Enter the amount to withdraw: $"))
                function.withdraw_funds(mydb, user[4], amount,user[6]) 
            else:
                print("Incorrect PIN. Please try again.")
        elif choice == "4":
            delete_account_flag =modify_menu(mydb, user)
            if delete_account_flag:
                print("Logging out...")
                break
        elif choice == "5":
            print("Logging out...")
            break
        elif choice == "6":
            if  user[7]: # Checking admin privileges
                function.view_database(mydb) 
                print("\n1. Back\n")  
            else:
                print("Access denied. Please enter a number between 1 and 5.")  
        elif choice == "-1":
            break  
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
    
# For modifying account details
def modify_menu(mydb, user):
    while True:
        print("-------------------------------------------------------------")
        print("Modify Account Details:")
        print("1. Change Username")
        print("2. Change Password")
        print("3. Change Email")
        print("4. Change PIN")
        print("5. Delete Account")
        print("6. Go Back")
        print("-------------------------------------------------------------")
        choice = input("Enter your choice (1-5): ")

        # Handling modification choices
        if choice == "1":
            new_username  = input("Enter your new username: ")
            function.modify_account(mydb, user[4], new_username=new_username)  
        elif choice == "2":
            new_password = input("Enter your new password: ")
            function.modify_account(mydb, user[4], new_password=new_password)  
        elif choice == "3":
            new_email = input("Enter your new email: ")
            function.modify_account(mydb, user[4], new_email=new_email) 
        elif choice == "4":
            new_pin = input("Enter your PIN: ")
            function.modify_account(mydb, user[4], new_pin=new_pin) 
        elif choice == "5":
            function.delete_account(mydb,user[4])
            return True
        elif choice == "6":
            return False
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


# Establishing a connection to the database
mydb = function.connect_to_database()

# Main loop for user interaction
while True:
    
    function.reset_auto_increment(mydb)
    display_options()
    choice = input("Enter your choice (1 or 2): ")
    if choice == "1":
        user = login(mydb)
        if user:
            if user[7]: # Checking admin privileges
                
                dashboard(mydb,user)
            else:
                dashboard(mydb,user)
    elif choice == "2":
        user = create_account(mydb)
        if user[7]: # Checking admin privileges
            dashboard(mydb,user)
        else:
            dashboard(mydb,user)
    elif choice == "-1":
        break
    else:
        print("Invalid choice. Please enter 1 or 2.")
    
# Closing the database connection
function.close_connection(mydb)


