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
        cursor.execute("SELECT balance FROM user WHERE account_number = %s OR user_id = %s", (account_number,user_id))
        balance = cursor.fetchone()[0]
        cursor.close()
        return balance
    except mysql.connector.Error as err:
        print('Error checking balance:', err)
        return None


#Create a new account
def create_account(mydb,username, email, password, pin, is_admin=False,user_id=None,account_number=generate_account_number()): #default exceptions
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
def modify_account(mydb,account_number,username,email, password): 
    try:
        cursor = mydb.cursor()
        cursor.execute("UPDATE user SET username = %s, email = %s, password = %s WHERE account_number = %s", (username,email,password,account_number))
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



mydb = connect_to_database()
reset_auto_increment(mydb)
#create_account(mydb,'kevin','kevinballs@gmail.com','bananas',1221)
modify_account(mydb,110346862,None,None,'socks')
#delete_account(mydb,None,2)
#print(check_balance(mydb, None, 2))

close_connection(mydb)







