from flask import Flask, render_template, request, redirect, url_for, flash, session
import function
import os 

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management


@app.route('/')
def index():
    return redirect(url_for('dashboard'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        mydb = function.connect_to_database()
        user = function.login(mydb, username, password)
        function.close_connection(mydb)
        if user:
            session['username'] = user[1]
            session['email'] = user[2]
            session['password'] = user[3]
            session['account_number'] = user[4]
            session['pin'] = user[5]
            session['balance'] = user[6]
            
            return redirect(url_for('dashboard'))#,username=user[1], email=user[2],account_number=user[4]))#dashboard(username=user[1], email=user[2],pin=user[5])
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        pin = request.form['pin']
        mydb = function.connect_to_database()
        function.create_account(mydb,username, password, email, pin)
        function.close_connection(mydb)
        flash('Account created successfully')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard/')
def dashboard():
    account_number = session.get('account_number')
    username = session.get('username')
    email = session.get('email')
    return render_template('dashboard.html', username=username,email=email,account_number=account_number)

@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    balance = session.get('balance')
    #if request.method == 'POST':
    return render_template('transactions.html',balance=balance)

@app.route('/deposit', methods=['POST'])
def deposit():
    if request.method == 'POST':
        balance = session.get('balance')
        account_number = session.get('account_number')
        deposit_amount = request.form.get('depositAmount')
        if deposit_amount is not None and deposit_amount.isdigit():
            mydb = function.connect_to_database()
            function.deposit_funds(mydb,account_number, deposit_amount)
            function.close_connection(mydb)
            session['balance'] = balance + float(deposit_amount)
            flash("Deposit successful!")
            return redirect(url_for('transactions'))
    else:
        return redirect(url_for('transactions'))
    
@app.route('/withdraw', methods=['POST'])
def withdraw():
    if request.method == 'POST':
        balance = session.get('balance')
        account_number = session.get('account_number')
        withdraw_amount = request.form.get('withdrawAmount')
        if withdraw_amount is not None and withdraw_amount.isdigit():
            mydb = function.connect_to_database()
            function.withdraw_funds(mydb,account_number, withdraw_amount, balance)
            function.close_connection(mydb)
            session['balance'] = balance - float(withdraw_amount)
            flash("Withdraw successful!")
            return redirect(url_for('transactions'))
    else:
        return redirect(url_for('transactions'))

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


@app.route('/modify/', methods=['GET', 'POST'])
def modify():
    if request.method == 'POST':
        account_number = session.get('account_number')
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        pin = request.form['pin']
        mydb = function.connect_to_database()
        function.modify_account(mydb,account_number, username, password, email, pin)
        function.close_connection(mydb)
        flash('Account modified successfully')
        return redirect(url_for('dashboard', username=username,email=email,account_number=account_number))
    return render_template('modify.html')

@app.route('/delete_account', methods=['POST'])
def delete_account():
    account_number = session.get('account_number')
    mydb = function.connect_to_database()
    function.delete_account(mydb, account_number)
    function.close_connection(mydb)
    flash('Account deleted successfully!')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
