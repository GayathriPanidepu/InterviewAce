from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_pymongo import PyMongo
import bcrypt
import os
import certifi

app = Flask(__name__)

# Secret key for session management
app.secret_key = os.environ.get("SECRET_KEY", "default_secret_key")

# Configure MongoDB connection
app.config["MONGO_URI"] = os.environ.get("ATLAS_URI") + certifi.where()
mongo = PyMongo(app)
db = mongo.db  # Shortcut for accessing the database

# Utility Function: Login Required Decorator
def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# Routes
@app.route('/')
def home():
    """Render the homepage."""
    return render_template('homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        email = request.form.get('loginEmail')
        password = request.form.get('loginPassword')

        # Fetch the user by email
        user = db.users.find_one({'email': email})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials. Please try again.", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logs the user out."""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        # Check if email or username already exists
        if db.users.find_one({'$or': [{'username': username}, {'email': email}]}):
            flash("Username or email already exists. Please choose different ones.", "danger")
            return redirect(url_for('signup'))

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Save user to MongoDB
        db.users.insert_one({
            'username': username,
            'password': hashed_password.decode('utf-8'),
            'email': email
        })
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """Render the user dashboard."""
    return render_template('index.html', username=session.get('username', 'User'))

@app.route('/jobinterview')
@login_required
def jobinterview():
    """Render the job interview preparation page."""
    return render_template('job-interview.html')

@app.route('/developskills')
@login_required
def developskills():
    """Render the skill development page."""
    return render_template('develop-skills.html')

@app.route('/mock')
@login_required
def mock():
    """Render the mock interview page."""
    return render_template('mock.html')

@app.route('/problem-solving/critical')
@login_required
def critical():
    """Render the critical thinking problem-solving page."""
    return render_template('problem-solving/critical-thinking.html')

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 error handler."""
    return render_template('page-not-found.html'), 404

if __name__ == "__main__":
    app.run()