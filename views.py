from flask import Blueprint, render_template, request, redirect, url_for
import function

views = Blueprint(__name__,"views")

"""
@views.route("/")
def home():
    return render_template("index.html", name="David Chinea")
"""
mydb = function.connect_to_database()

function.close_connection(mydb)

@views.route("/dashboard/<account_number>")
def dashboard(account_number):
    # Fetch user data and display dashboard
    return render_template("dashboard.html", user=function.get_user_data(mydb,110346862))

@views.route("/check_balance")
def check_balance():
    # Implement check balance functionality
    return "Check Balance"

@views.route("/deposit")
def deposit():
    # Implement deposit functionality
    return "Deposit"

@views.route("/withdraw")
def withdraw():
    # Implement withdraw functionality
    return "Withdraw"

@views.route("/create_account")
def create_account():
    # Implement create account functionality
    return "Create Account"

@views.route("/delete_account")
def delete_account():
    # Implement delete account functionality
    return "Delete Account"

@views.route("/modify_account")
def modify_account():
    # Implement modify account functionality
    return "Modify Account Details"