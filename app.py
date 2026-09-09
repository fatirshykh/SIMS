from flask import Flask, request, jsonify, render_template
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import config

app = Flask(__name__)

db = mysql.connector.connect(
    user=config.DB_USER,
    host=config.DB_HOST,
    password=config.DB_PASSWORD,
    database=config.DB_NAME,
)


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/signup")
def signup_page():
    return render_template("signup.html")


@app.route("/login")
def login_page():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
