# Importing module 
from flask import Flask
import function




#print(function.check_balance(mydb,110346862))
#create_account(mydb,'kevin','bananas', 'kevinballs@gmail.com',1221)
#modify_account(mydb,110346862,'kevinRules','socksOff','kevinRules@gmail.com', 1221,)
#function.delete_account(mydb,None,2)
#print(check_balance(mydb, None, 2))
#deposit_funds(mydb, 110346862, 20)
#withdraw_funds(mydb, 110346862, 20)
#print(check_balance(mydb,110346862))

def display_options():
    print("-------------------------------------------------------------")
    print("Welcome to Online Banking! Please Login or Create an Account:")
    print("-------------------------------------------------------------")
    print("1. Login")
    print("2. Create an Account")
    print("-------------------------------------------------------------")

def create_account(mydb):
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    email = input("Enter your email: ")
    pin = input("Enter your PIN: ")
    function.create_account(mydb,username, password, email, pin)
    return function.login(mydb,username,pin)

def login(mydb):
    username = input("Enter your username: ")
    pin = input("Enter your PIN: ")
    return function.login(mydb,username,pin)
    

def dashboard(mydb,user):
    while True:
        print("-------------------------------------------------------------")
        print("Welcome to Your Dashboard, "+user[1]+"!")  
        print("-------------------------------------------------------------")
        print("1. Check Balance")
        print("2. Deposit Funds")
        print("3. Withdraw Funds")
        print("4. Modify Account Details")
        print("5. Logout")
        print("-------------------------------------------------------------")
        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            balance = function.check_balance(mydb, user[4]) 
            if balance is not None:
                print("Your current balance is: ${:.2f}".format(balance))
        elif choice == "2":
            amount = float(input("Enter the amount to deposit: $"))
            function.deposit_funds(mydb, user[4], amount)  
        elif choice == "3":
            amount = float(input("Enter the amount to withdraw: $"))
            function.withdraw_funds(mydb, user[4], amount) 
        elif choice == "4":
            modify_menu(mydb, user)
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
    
def modify_menu(mydb, user):
    while True:
        print("-------------------------------------------------------------")
        print("Modify Account Details:")
        print("1. Change Username")
        print("2. Change Password")
        print("3. Change Email")
        print("4. Delete Account")
        print("5. Go Back")
        print("-------------------------------------------------------------")
        choice = input("Enter your choice (1-5): ")

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
            function.delete_account(mydb,user[4])
            break
        elif choice == "5":
            break
            #pass  # Go back to dashboard
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

mydb = function.connect_to_database()
while True:
    
    function.reset_auto_increment(mydb)
    display_options()
    choice = input("Enter your choice (1 or 2): ")
    if choice == "1":
        user = login(mydb)
        if user:
            dashboard(mydb,user)
    elif choice == "2":
        user = create_account(mydb)
        dashboard(mydb,user)
    elif choice == "-1":
        break
    else:
        print("Invalid choice. Please enter 1 or 2.")
    

function.close_connection(mydb)


