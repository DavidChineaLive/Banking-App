# Importing module 
import mysql.connector
import random


# Establish connection to MySQL database
def connect_to_database():
    try:
        mydb = mysql.connector.connect(host="localhost", user="root", password="DCcode2@07")
        print("Connected to the database")
        return mydb
    except mysql.connector.Error as err:
        print("Error connecting to the database:", err)
        return None
    
def generate_account_number():
    # Generate a 10-digit random number
    return int(random.random() * (10**9 - 1) + 10**8)


#Check Balance
def check_balance(mydb, account_number, user_id=None):
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT balance FROM sys.user WHERE account_number = %s OR user_id = %s", (account_number,user_id))
        balance = cursor.fetchone()[0]
        cursor.close()
        return balance
    except mysql.connector.Error as err:
        print('Error checking balance:', err)
        return None

# Deposit funds
def deposit_funds(mydb, account_number, amount):
    try:
        cursor = mydb.cursor()
        cursor.execute("UPDATE sys.user SET balance = balance + %s WHERE account_number = %s", (amount, account_number))
        mydb.commit()
        cursor.close()
        print("Funds deposited successfully")
    except mysql.connector.Error as err:
       print("Error depositing funds:", err)

def withdraw_funds(mydb, account_number, amount):
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT balance FROM sys.user WHERE account_number = %s", (account_number,))
        balance = cursor.fetchone()[0]
        if balance >= amount:
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
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM sys.user WHERE account_number = %s OR user_id = %s", (account_number,user_id)) 
        mydb.commit()
        cursor.close()
        print('Account deleted successfully')
    except mysql.connector.Error as err:
        print('Error deleting account:', err)

#Modify account details #remeber to add email to modify
def modify_account(mydb,account_number,new_username=None, new_password=None, new_email=None,new_pin=None, is_admin=None): 
    try:
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
        cursor = mydb.cursor()
        cursor.execute("ALTER TABLE sys.user AUTO_INCREMENT = 1")
        mydb.commit()
        cursor.close()
        #print('Reset auto incrementation successfully')
    except mysql.connector.Error as err:
        print('Error resetting auto incrementation:', err)

# Close connection to MySQL database
def close_connection(mydb):
    mydb.close()
    print("Connection to the database closed")
