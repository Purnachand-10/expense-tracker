from flask import Flask, render_template, request, redirect, url_for, flash
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
    conn.commit()
    conn.close()

# Initialize DB on startup
init_db()

@app.route('/')
def index():
    """Handles the home page, displays all expenses."""
    conn = get_db_connection()
    # Fetch all expenses ordered by date descending
    expenses = conn.execute('SELECT * FROM expenses ORDER BY date DESC').fetchall()
    conn.close()

    # Calculate total expenses
    total = sum([expense['amount'] for expense in expenses])

    return render_template('index.html', expenses=expenses, total=total)

@app.route('/submit', methods=['POST'])
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
    conn.execute('INSERT INTO expenses (title, amount, category, date) VALUES (?, ?, ?, ?)',
                 (title, amount, category, date))
    conn.commit()
    conn.close()

    return redirect(url_for('success'))

@app.route('/success')
def success():
    """Displays the success confirmation page."""
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
