from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import config

app = Flask(__name__)

app.secret_key = "SIMS_FATIR_DEV_STUDIO_121"

db = mysql.connector.connect(
    user=config.DB_USER,
    host=config.DB_HOST,
    password=config.DB_PASSWORD,
    database=config.DB_NAME,
)


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/signup", methods=["GET"])
def signup_page():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup():

    data = request.get_json()

    fullname = data["fullname"]
    username = data["username"]
    email = data["email"]
    phone = data["phone"]
    password = data["password"]

    hashed_password = generate_password_hash(password)

    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO users(fullname,username,email,phone,password)
        VALUES( %s , %s , %s, %s ,%s)
        """,
        (fullname, username, email, phone, hashed_password),
    )
    db.commit()
    cursor.close()

    return jsonify({"success": True, "message": "Account created successfully."})


@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    username_or_email = data["username"]
    password = data["password"]

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT * FROM users 
        WHERE username = %s OR email = %s    
      """,
        (username_or_email, username_or_email),
        # SELECT * FROM users WHERE username = fatir  OR email = fatir@gmail.com
    )

    user = cursor.fetchone()

    cursor.close()

    if user:
        if check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return jsonify({"success": True, "message": "Login successfully."})

    return jsonify({"success": False, "message": "Invalid Credentials"})


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/logout")
def logout():
    session.clear()
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
