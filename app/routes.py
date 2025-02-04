from flask import Blueprint, render_template, request


main = Blueprint('main',  __name__, template_folder='templates')

#frontend routes
@main.route('/')
def index():
    return render_template("home.html")

#backend routes
@main.route('/api/register', methods=['POST'])
def register():
    session.clear()
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not firstname or not lastname or not username or not email or not password:
            return render_template("home.html", error="All fields are required"), 400
        
        #check if the email is already registered

        #check if the username is already registered

        #hash the password

        #store the user in the database

        return render_template("home.html", user={} ,success="You have successfully registered"), 201
    
    
@main.route('/api/login', methods=['POST'])
def register():
    session.clear()
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email:
            return render_template("home.html", error="An email or username is required"), 400
        
        if not password:
            return render_template("home.html", error="A password is required"), 400

        #check if the email is present and registered

        #else check if the username is present and registered

        #compare the password with the hash

        return render_template("home.html", user={} ,success="You have successfully logged in"), 201