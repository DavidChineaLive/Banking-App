# Importing module 
import mysql.connector

# Establish connection to MySQL database
def connect_to_database():
    try:
        mydb = mysql.connector.connect(host="localhost", user="root", password="DCcode2@07")
        print("Connected to the database")
        return mydb
    except mysql.connector.Error as err:
        print("Error connecting to the database:", err)
        return None
    
#Check Balance
#def check_balance(mydb, account_number):
    #cursor = mydb.cursor()
    #cursor.execute("SELECT balance FROM account WHERE account_number = %s", (account_number,))

#Create a new account
def create_account(mydb,username, password, pin, is_admin=False, user_id = None): #default exceptions
    try:
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO sys.user (user_id,username,password,pin,is_admin) VALUES (%s,%s,%s,%s,%s)", (user_id,username,password,pin,is_admin))
        mydb.commit()
        cursor.close()
        print('Account created successfully')
    except mysql.connector.Error as err:
        print('Error creating account:', err)
        
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
#reset_auto_increment(mydb)
create_account(mydb,'monkeysBank','bananas',4444, is_admin = True)

close_connection(mydb)







