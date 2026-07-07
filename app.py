from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pickle
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Initialize Extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Load the trained Machine Learning model
model = None
cv = None

try:
    with open('spam_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('vectorizer.pkl', 'rb') as vocab_file:
        cv = pickle.load(vocab_file)
except FileNotFoundError:
    print("Error: model.pkl or vectorizer.pkl not found. Run train_model.py first.")

# --- Database Models ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index() :
    return render_template('index.html')

# --- Routes ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('register'))
            
        # Hash password and save user
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        # Verify user exists and password is correct
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    prediction = None
    if request.method == 'POST':
        message = request.form.get('message')

        # Check if model and vectorizer were loaded successfully
        if cv is None or model is None:
            flash("Error: The machine learning model is missing. Please run train_model.py first.")
            return render_template('dashboard.html', prediction=None, message=message)

        if message:
            # Transform text and predict
            vect = cv.transform([message]).toarray()
            my_prediction = model.predict(vect)
            prediction = 'SPAM' if my_prediction[0] == 1 else 'NOT SPAM'
            
    return render_template('index.html', prediction=prediction, message=request.form.get('message', ''))

# Initialize database tables before running
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    host = os.getenv('HOST')
    app.run(debug=True, host=host)