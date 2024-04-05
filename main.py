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
    

def close_connection(mydb):
    mydb.close()
    print("Connection to the database closed")


mydb = connect_to_database()
print(mydb)
close_connection(mydb)










