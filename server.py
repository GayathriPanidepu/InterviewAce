from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import hashlib  # To hash passwords for security
from flask_cors import CORS
from flask_pymongo import PyMongo

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management
CORS(app)  # Enable CORS

# Configure MongoDB connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/test"  # Ensure MongoDB is running locally
mongo = PyMongo(app)
db = mongo.db  # Shortcut for accessing the database

# User class to handle user operations
class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def save_to_db(self):
        """Save user to MongoDB."""
        db.users.insert_one({
            'username': self.username,
            'password': self.password,
            'email': self.email,
        })


# Routes
@app.route('/')
def home():
    """Render the homepage."""
    return render_template('homepage.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        email = request.form['loginEmail']
        password = request.form['loginPassword']

        # Hash the password for comparison
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Check user credentials in MongoDB
        user = db.users.find_one({'email': email, 'password': hashed_password})
        if user:
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']  # Use .get() to avoid KeyError
        password = request.form['password']
        email = request.form['email']

        # Hash the password for secure storage
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Check if the username already exists
        if db.users.find_one({'username': username}):
            return "Username already exists. Please choose a different one."

        # Create a new user and save to MongoDB
        new_user = User(username, hashed_password, email)
        new_user.save_to_db()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/dashboard',methods=['POST','GET'])
def dashboard():
    if request.method=='POST':
        return render_template('job-interview.html')
    return render_template('index.html')

@app.route('/jobinterview',methods=['GET'])
def jobinterview():
    return render_template('job-interview.html')

@app.route('/developskills',methods=['GET'])
def developskills():
    return render_template('develop-skills.html')
@app.route('/mock',methods=['GET'])
def mock():
    return render_template('mock.html')
@app.route('/problem-solving/critical',methods=['GET'])
def critical():
    return render_template('/problem-solving/critical-thinking')
if __name__ == "__main__":
    app.run()

