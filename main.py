from flask import Flask, request, render_template, jsonify, url_for, session, redirect
import sqlite3

app = Flask(__name__)

def connect_sqlite():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT NOT NULL,
                   password TEXT NOT NULL)
""")
    return conn

@app.route('/')
def home():
    return render_template("index.html")


@app.route("/signup", methods=["GET"])
def showSignup():
    return render_template('signup.html')


@app.route("/signup", methods=["POST"])
def handle_signup():
    username = request.form["username"]
    password = request.form["password"]

    conn = connect_sqlite()
    cursr = conn.cursor()
    cursr.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                   (username, password))
    conn.commit()
    return f"""
        <h3>{username} muvaffaqiyatli ro'yxatdan o'tdi!</h3>
        <meta http-equiv="refresh" content="2; url={url_for('view_login')}">
    """


@app.route('/login', methods=['GET'])
def view_login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def handle_login():
    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    if not user:
        return render_template("login.html", message="Bunday user yo'q")
    return jsonify(dict(user))

@app.route("/users", methods=["GET"])
def users():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    users = [dict(row) for row in rows]
    return jsonify(users)


@app.route("/users/<int:user_id>")
def get_user(user_id):
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user is None:
        return jsonify({"message": "User topilmadi"}), 404
    return jsonify(dict(user))
if __name__ == "__main__":
    app.run(debug=True)