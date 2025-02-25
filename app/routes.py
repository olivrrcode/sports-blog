from flask import Blueprint, render_template, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash 
from app import mysql

main = Blueprint('main',  __name__, template_folder='templates')

#frontend routes
@main.route('/')
def index():
    return render_template("home.html")

@main.route('/createTable', methods=['GET'])
def createTable():
    try:
        cur = mysql.connection.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            firstname VARCHAR(100) NOT NULL,
            lastname VARCHAR(100) NOT NULL,
            username VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY unique_email (email),
            UNIQUE KEY unique_username (username)
        )''')
        mysql.connection.commit()
        cur.close()
        return "Table created successfully"
    except Exception as e:
        return f"Error creating table: {str(e)}", 500

#backend routes
@main.route('/api/register', methods=['POST'])
def register():
    session.clear()
    if request.method == 'POST':
        data = request.get_json()
        firstname = data['firstname']
        lastname = data['lastname']
        username = data['username']
        email = data['email']
        password = data['password']

        if not firstname or not lastname or not username or not email or not password:
            return jsonify({"error": "All fields are required"}), 400
        
        # Create cursor
        cur = mysql.connection.cursor()
        
        # Check if email exists
        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        if cur.fetchone():
            return jsonify({"error": "Email already registered"}), 400

        # Check if username exists
        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        if cur.fetchone():
            return jsonify({"error": "Username already taken"}), 400

        # Hash the password
        hashed_password = generate_password_hash(password)
        
        try:
            # Insert new user
            cur.execute(
                'INSERT INTO users (firstname, lastname, username, email, password) VALUES (%s, %s, %s, %s, %s)',
                (firstname, lastname, username, email, hashed_password)
            )
            mysql.connection.commit()
            return jsonify({"success": "Registration successful"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cur.close()
    
@main.route('/api/login', methods=['POST'])
def login():
    session.clear()
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not (username or email):
            return jsonify({"error": "Email or username is required"}), 400
        
        if not password:
            return jsonify({"error": "Password is required"}), 400

        # Create cursor
        cur = mysql.connection.cursor()
        
        try:
            if email:
                # Check by email
                cur.execute('SELECT * FROM users WHERE email = %s', (email,))
            else:
                # Check by username
                cur.execute('SELECT * FROM users WHERE username = %s', (username,))
            
            user = cur.fetchone()
            
            if user is None:
                return jsonify({"error": "User not found"}), 404

            # Compare password with hash
            if not check_password_hash(user[5], password):  # Assuming password is at index 5
                return jsonify({"error": "Invalid password"}), 401

            # Store user info in session
            session['user_id'] = user[0]
            session['username'] = user[3] 
            
            return jsonify({
                "success": "Login successful",
                "user": {
                    "id": user[0],
                    "username": user[3],
                    "email": user[4]
                }
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cur.close()

            