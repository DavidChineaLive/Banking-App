from flask import Flask, render_template, request, redirect, url_for, flash, session
import function
import os 

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

"""
@app.route('/')
def index():
    mydb = function.connect_to_database()
    users = function.login(mydb)#not correct parameters
    function.close_connection(mydb)
    return render_template('index.html', users=users)
"""

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        mydb = function.connect_to_database()
        user = function.login(mydb, username, password)
        if user:
            session['user_id'] = user[0]
            session['account_number'] = user[4]
            redirect(url_for('dashboard'))
            return dashboard(username=user[1], email=user[2],pin=user[5])
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
        function.create_account(mydb,username, email, password, pin)
        function.close_connection(mydb)
        flash('Account created successfully')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard/')
def dashboard(username, email,pin):
    return render_template('dashboard.html', username=username,email=email,pin=pin)

"""
@app.route('/balance', methods=['GET', 'POST'])
def balance():
    mydb = function.connect_to_database()
    if request.method == 'POST':
        function.check_balance(mydb, username, email, pin)
        flash('')
        return redirect(url_for('dashboard', user=username))
    return render_template('modify.html')
"""

@app.route('/modify', methods=['GET', 'POST'])
def modify():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        pin = request.form['pin']
        mydb = function.connect_to_database()
        function.modify_account(mydb,username, password, email, pin)
        function.close_connection(mydb)
        flash('Account modified successfully')
        return redirect(url_for('dashboard', user=username))
    return render_template('modify.html')

@app.route('/delete_account', methods=['POST'])
def delete_account(account_number):
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
