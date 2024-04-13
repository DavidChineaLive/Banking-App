from flask import Flask, render_template, request, redirect, url_for
from views import views

app = Flask(__name__)
app.secret_key = 'secret_key'
app.register_blueprint(views, url_prefix="/views")

# Dummy user data for demonstration
users = {
    "1234567890": {"pin": "1234", "username": "Alice", "balance": 1000.00},
    "0987654321": {"pin": "4321", "username": "Bob", "balance": 500.00}
}

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        account_number = request.form.get("account_number")
        pin = request.form.get("pin")
        if account_number in users and users[account_number]["pin"] == pin:
            # Redirect to user dashboard or specific functionality
            return redirect(url_for("views.dashboard", account_number=account_number))
        else:
            return "Invalid account number or PIN. Please try again."
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, port =8000)


