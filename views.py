from flask import Blueprint, render_template, request, redirect, url_for
import function

views = Blueprint(__name__,"views")

"""
@views.route("/")
def home():
    return render_template("index.html", name="David Chinea")
"""
mydb = function.connect_to_database()

@views.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        account_number = request.form.get("account_number")
        pin = request.form.get("pin")
        # Validate login credentials
        mydb = function.connect_to_database()
        user_data = function.get_user_data(mydb, account_number)
        function.close_connection(mydb)
        if user_data and user_data["pin"] == pin:
            return redirect(url_for("views.dashboard", account_number=account_number))
        else:
            return "Invalid account number or PIN. Please try again."
    return render_template("index.html")



@views.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        # Get account details from form
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        pin = request.form.get("pin")
        # Create account
        mydb = function.connect_to_database()
        function.create_account(mydb, username, password, email, pin)
        function.close_connection(mydb)
        return "Account created successfully. You can now login."
    return render_template("create_account.html")


@views.route("/dashboard/<account_number>")
def dashboard(account_number):
    mydb = function.connect_to_database()
    user_data = function.get_user_data(mydb, account_number)
    function.close_connection(mydb)
    return render_template("dashboard.html", user=user_data)

@views.route("/check_balance")
def check_balance():
    mydb = function.connect_to_database()
    # Get account_number from request
    account_number = request.args.get("account_number")
    balance = function.check_balance(mydb, account_number)
    function.close_connection(mydb)
    return f"Balance: {balance}"

@views.route("/deposit")
def deposit():
    mydb = function.connect_to_database()
    # Get account_number and amount from request
    account_number = request.args.get("account_number")
    amount = request.args.get("amount")
    function.deposit_funds(mydb, account_number, amount)
    function.close_connection(mydb)
    return "Funds deposited successfully"

@views.route("/withdraw")
def withdraw():
    conn = function.connect_to_database()
    # Get account_number and amount from request
    account_number = request.args.get("account_number")
    amount = request.args.get("amount")
    function.withdraw_funds(conn, account_number, amount)
    function.close_connection(conn)
    return "Funds withdrawn successfully"
    
"""
@views.route("/create_account")
def create_account():
    # Implement create account functionality
    return "Create Account"
"""

@views.route("/delete_account")
def delete_account():
    mydb = function.connect_to_database()
    # Get account_number from request
    account_number = request.args.get("account_number")
    function.delete_account(mydb, account_number)
    function.close_connection(mydb)
    return "Account deleted successfully"

@views.route("/modify_account")
def modify_account():
    mydb = function.connect_to_database()
    # Get account_number and new details from request
    account_number = request.args.get("account_number")
    new_username = request.args.get("new_username")
    new_password = request.args.get("new_password")
    new_email = request.args.get("new_email")
    function.modify_account_details(mydb, account_number, new_username, new_password, new_email)
    function.close_connection(mydb)
    return "Account details modified successfully"


function.close_connection(mydb)