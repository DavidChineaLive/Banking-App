from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
import function

views = Blueprint(__name__,"views")

@views.route("/")
def home():
    return render_template("index.html")

