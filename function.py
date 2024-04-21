# Importing module 
import mysql.connector
import random


# Establish connection to MySQL database
def connect_to_database():
    try:
        mydb = mysql.connector.connect(host="localhost", user="root", password="DCcode2@07")
        print("Connected to the database\n")
        return mydb
    except mysql.connector.Error as err:
        print("Error connecting to the database:", err)
        return None

# Generates a random 10-digit account number
def generate_account_number():
    return int(random.random() * (10**9 - 1) + 10**8)

# Authenticate user login
def login(mydb,username,password,is_admin=False):
    try:
        # Check if account exists
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM sys.user WHERE username = %s AND password = %s AND is_admin = %s", (username, password, is_admin))
        user = cursor.fetchone()
        cursor.close()

        if user:
            print(user)
            print(user[4])
            print("Login successful!")            
            return user
        else:
            print("Invalid username or password.\n")
            return None
    except mysql.connector.Error as err:
        print("Error during login:", err)
        return None


#Check Account Balance
def check_balance(mydb, account_number, user_id=None):
    try:
        # Retrieving balance from database
        cursor = mydb.cursor()
        cursor.execute("SELECT balance FROM sys.user WHERE account_number = %s OR user_id = %s", (account_number,user_id))
        balance = cursor.fetchone()[0]
        cursor.close()
        return balance
    except mysql.connector.Error as err:
        print('Error checking balance:', err)
        return None

#Checks PIN for depositing and withdrawing
def check_pin(mydb, account_number, pin):
    try:
        # Retrieving PIN from database
        cursor = mydb.cursor()
        cursor.execute("SELECT pin FROM sys.user WHERE account_number = %s", (account_number,))
        realPin = cursor.fetchone()
        cursor.close()
        if realPin[0] == pin:
            return True
        else:
            return False
    except mysql.connector.Error as err:
        print("Error entering pin funds:", err)
        return False

# Deposit funds into an account
def deposit_funds(mydb, account_number, amount):
    try:
        # Updating balance in the database
        cursor = mydb.cursor()
        cursor.execute("UPDATE sys.user SET balance = balance + %s WHERE account_number = %s", (amount, account_number))
        mydb.commit()
        cursor.close()
        print("Funds deposited successfully")
    except mysql.connector.Error as err:
       print("Error depositing funds:", err)

# Withdraw funds from an account
def withdraw_funds(mydb, account_number, amount, balance):
    try:
        # Checking balance and updating database
        if balance >= float(amount):
            cursor = mydb.cursor()
            cursor.execute("UPDATE sys.user SET balance = balance - %s WHERE account_number = %s", (amount, account_number))
            mydb.commit()
            cursor.close()
            print("Funds withdrawn successfully")
        else:
            print("Insufficient funds")
    except mysql.connector.Error as err:
        print("Error withdrawing funds:", err)


#Create a new account
def create_account(mydb,username, password, email, pin, is_admin=False,user_id=None,account_number=generate_account_number()): #default exceptions
    try:
        # Inserting new account details into the database
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO sys.user (user_id,username,email,password,pin,is_admin,account_number,balance) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (user_id,username,email,password,pin,is_admin,account_number,0))
        mydb.commit()
        cursor.close()
        print('Account created successfully. Account Number is', account_number)
    except mysql.connector.Error as err:
        print('Error creating account:', err)
        
#Deletes an account
def delete_account(mydb,account_number,user_id=None): #default exceptions
    try:
        # Deleting account from the database
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM sys.user WHERE account_number = %s OR user_id = %s", (account_number,user_id)) 
        mydb.commit()
        cursor.close()
        print('Account deleted successfully')
    except mysql.connector.Error as err:
        print('Error deleting account:', err)

#Modify account details 
def modify_account(mydb,account_number,new_username=None, new_password=None, new_email=None,new_pin=None, is_admin=None): 
    try:
        # Modifying account details in the database
        cursor = mydb.cursor()
        if new_username is not None:
            cursor.execute("UPDATE sys.user SET username = %s WHERE account_number = %s", (new_username,account_number))
        if new_password is not None:
            cursor.execute("UPDATE sys.user SET password = %s WHERE account_number = %s", (new_password,account_number))
        if new_email is not None:
            cursor.execute("UPDATE sys.user SET email = %s WHERE account_number = %s", (new_email,account_number))
        if new_pin is not None:
            cursor.execute("UPDATE sys.user SET pin = %s WHERE account_number = %s", (new_pin,account_number))
        if is_admin is not None:
            cursor.execute("UPDATE sys.user SET is_admin = %s WHERE account_number = %s", (is_admin,account_number))
        mydb.commit()
        cursor.close()
        print('Modified Account successfully')
    except mysql.connector.Error as err:
        print('Error Modifying Account:', err)

#Resets auto incrementation
def reset_auto_increment(mydb): #
    try:
        # Resetting auto increment in the database
        cursor = mydb.cursor()
        cursor.execute("ALTER TABLE sys.user AUTO_INCREMENT = 1")
        mydb.commit()
        cursor.close()
        #print('Reset auto incrementation successfully')
    except mysql.connector.Error as err:
        print('Error resetting auto incrementation:', err)

# Gets user data from the database
def get_user_data(mydb,account_number):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM sys.user WHERE account_number = %s", (account_number,))
    user_data = cursor.fetchone()
    cursor.close()
    return user_data

# Views all users in the database
def view_database(mydb):
    try:
         # Retrieving all users from the database
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM sys.user")
        users = cursor.fetchall()
        cursor.close()

        if users:
            print("-------------------------------------------------------------")
            print("Users in the Database:")
            for user in users:
                print("User: "+str(user[0])+", "+ user[1]+", "+ user[2]+", "+ str(user[4]))  
        else:
            print("No users found in the database.")
    except mysql.connector.Error as err:
        print("Error viewing database:", err)

# Close connection to MySQL database
def close_connection(mydb):
    mydb.close()
    print("\nConnection to the database closed")

