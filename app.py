from flask import Flask, render_template, request, redirect, url_for, flash, session
import function
import os 
import re

"""
This application uses my database to store user accounts and their details, and the function.py module provides 
various functions to interact with the database. The application also uses Flask's session management to 
store user details in the session object. The application has several routes, including /, /login, /register,
/dashboard/, /transactions, /deposit, /withdraw, /balance, /modify/, /delete_account, and /logout. The 
application provides a user-friendly interface for users to perform various banking operations.
"""

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Define the index route
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

# Define the login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        mydb = function.connect_to_database()
        user = function.login(mydb, username, password)
        function.close_connection(mydb)
        if user:
            #stores user details in session
            session['username'] = user[1]
            session['email'] = user[2]
            session['password'] = user[3]
            session['account_number'] = user[4]
            session['pin'] = user[5]
            session['balance'] = user[6]
            #session['is_admin'] = user[7] // 
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    # If the request method is GET
    else:
        return render_template('login.html')

# Define the register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get the username, email, and password from the form
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        pin = request.form['pin']
        mydb = function.connect_to_database()
        function.create_account(mydb,username, password, email, pin)
        function.close_connection(mydb)
        flash('Account created successfully')
        return redirect(url_for('login'))
     # If the request method is GET
    else:
        return render_template('register.html')

# Define the dashboard route
@app.route('/dashboard/')
def dashboard():
    account_number = session.get('account_number')
    username = session.get('username')
    email = session.get('email')
    return render_template('dashboard.html', username=username,email=email,account_number=account_number)


# Define the transactions route
@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    if session.get('balance') is None:
            session['balance'] = 0
    return render_template('transactions.html',balance=session.get('balance'))

# Define the deposit route
@app.route('/deposit', methods=['POST'])
def deposit():
    if request.method == 'POST':
        balance = session.get('balance')
        deposit_amount = request.form.get('depositAmount')
        # If the deposit amount is a valid number
        if deposit_amount is not None and re.match(r'^-?\d+(\.\d+)?$', deposit_amount):
            mydb = function.connect_to_database()
            # Call the deposit_funds function to deposit the funds
            function.deposit_funds(mydb, session.get('account_number'), deposit_amount)
            function.close_connection(mydb)
            session['balance'] = balance + float(deposit_amount)
            flash("Deposit successful!")
            return redirect(url_for('transactions'))
    # If the request method is not POST
    else:
        return redirect(url_for('transactions'))
    
# Define the withdraw route
@app.route('/withdraw', methods=['POST'])
def withdraw():
    if request.method == 'POST':
        balance = session.get('balance')
        withdraw_amount = request.form.get('withdrawAmount')
        # If the deposit amount is a valid number
        if withdraw_amount is not None and re.match(r'^-?\d+(\.\d+)?$', withdraw_amount) and balance >= float(withdraw_amount):
            mydb = function.connect_to_database()
            # Call the withdraw_funds function to withdraw the funds
            function.withdraw_funds(mydb,session.get('account_number'), withdraw_amount, balance)
            function.close_connection(mydb)
            session['balance'] = balance - float(withdraw_amount)
            flash("Withdraw successful!")
        else:
            flash("Withdraw failed. Please try again.")
        return redirect(url_for('transactions'))
    # If the request method is not POST
    else:
        return redirect(url_for('transactions'))

# Define the balance route
@app.route('/balance', methods=['GET', 'POST'])
def balance():
    account_number = session.get('account_number')
    if request.method == 'POST':
        mydb = function.connect_to_database()
        balance = function.check_balance(mydb, account_number)
        function.close_connection(mydb)
        flash("Your current balance is: ${:.2f}".format(balance))
        return redirect(url_for('dashboard'))
    return render_template('transactions.html')

# Define the modify route
@app.route('/modify/', methods=['GET', 'POST'])
def modify():
    if request.method == 'POST':
        # Get the account number, username, password, email, and pin from the form
        account_number = session.get('account_number')
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        pin = request.form['pin']
        mydb = function.connect_to_database()
        # Modify the account in the database
        function.modify_account(mydb,account_number, username, password, email, pin)
        function.close_connection(mydb)
        flash('Account modified successfully')
        # Redirect to the dashboard page after successfully modifying the account
        return redirect(url_for('dashboard', username=username,email=email,account_number=account_number))
    return render_template('modify.html')

# Define the delete_account route
@app.route('/delete_account', methods=['POST'])
def delete_account():
    account_number = session.get('account_number')
    mydb = function.connect_to_database()
    function.delete_account(mydb, account_number)
    function.close_connection(mydb)
    flash('Account deleted successfully!')
    return redirect(url_for('login'))

# Define the logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
