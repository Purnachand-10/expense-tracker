from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
# Secret key is needed for session data (like flash messages)
app.secret_key = 'super_secret_key_for_expense_tracker'

DB_PATH = 'expenses.db'

def get_db_connection():
    """Establishes connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database by creating the required table."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    # Check if user_id column exists in expenses
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(expenses)")
    columns = [info[1] for info in cursor.fetchall()]
    if 'user_id' not in columns:
        cursor.execute("ALTER TABLE expenses ADD COLUMN user_id INTEGER DEFAULT 1")
    
    conn.commit()
    conn.close()

# Decorator to require login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Initialize DB on startup
init_db()

@app.route('/')
@login_required
def index():
    """Handles the home page, displays all expenses."""
    conn = get_db_connection()
    # Fetch all expenses ordered by date descending
    expenses = conn.execute(
        'SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC',
        (session['user_id'],)
    ).fetchall()
    conn.close()

    # Calculate total expenses
    total = sum([expense['amount'] for expense in expenses])

    return render_template('index.html', expenses=expenses, total=total)

@app.route('/submit', methods=['POST'])
@login_required
def submit():
    """Handles the form submission from the index page."""
    title = request.form.get('title')
    amount = request.form.get('amount')
    category = request.form.get('category')
    date = request.form.get('date')
    
    # Server-side validation
    if not title or not amount or not category or not date:
        flash("All fields are required!", "danger")
        return redirect(url_for('index'))
    
    try:
        amount = float(amount)
        if amount <= 0:
            flash("Amount must be greater than zero.", "danger")
            return redirect(url_for('index'))
    except ValueError:
        flash("Invalid amount.", "danger")
        return redirect(url_for('index'))

    # Insert into DB
    conn = get_db_connection()
    conn.execute('INSERT INTO expenses (title, amount, category, date, user_id) VALUES (?, ?, ?, ?, ?)',
                 (title, amount, category, date, session['user_id']))
    conn.commit()
    conn.close()

    return redirect(url_for('success'))

@app.route('/success')
@login_required
def success():
    """Displays the success confirmation page."""
    return render_template('success.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not password:
            flash("Username and password are required.", "danger")
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for('register'))

        conn = get_db_connection()
        user = conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
        
        if user:
            flash("Username already exists.", "danger")
            conn.close()
            return redirect(url_for('register'))
            
        password_hash = generate_password_hash(password)
        conn.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
        conn.commit()
        conn.close()
        
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Username and password are required.", "danger")
            return redirect(url_for('login'))

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f"Welcome back, {username}!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password.", "danger")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
