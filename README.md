# Expense Tracker Application

A lightweight, responsive Expense Tracker built with Flask, Bootstrap 5, jQuery, and SQLite. This project fulfills standard guidelines for a full-stack CRUD application with both front-end and back-end logic.

## Technologies Used
- **Backend:** Python, Flask, SQLite3
- **Frontend Structure:** HTML5 Semantic Tags
- **Frontend Styling:** Bootstrap 5, Minimal Custom CSS
- **Frontend Logic:** JavaScript, jQuery (DOM manipulation, form validation)

## Setup Instructions

### 1. Prerequisites
Ensure you have Python 3.8+ installed on your system.

### 2. Installation
Clone or navigate to the project directory:

```bash
cd expense_tracker
```

Create a virtual environment (optional but recommended):
```bash
python -m venv venv
```

Activate the virtual environment:
- **Windows:** `venv\Scripts\activate`
- **macOS/Linux:** `source venv/bin/activate`

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Running the Application
Start the Flask development server:
```bash
python app.py
```
*Note: The SQLite database (`expenses.db`) and table will automatically be created on the first run.*

### 4. Usage
Open your web browser and go to:
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

- Use the form to add a new expense (Title, Amount, Category, Date are validated locally via jQuery and server-side).
- Added expenses will be dynamically displayed in the Recent Expenses table along with the calculated total.
