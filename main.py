from flask import Flask, render_template, request, redirect, url_for, session, g
import re
import cx_Oracle

cx_Oracle.init_oracle_client(lib_dir=r"D:\Oracle\instantclient_21_8") #path of instantclient directory

#connecting to database
app = Flask(__name__)

app.secret_key= 'your secret key'

DB_USER = "SYSTEM"
DB_PASSWORD = "" #enter your password here
DB_HOST = "localhost"
DB_PORT = "1521"
DB_SERVICE = "xe"

#CONNECT TO database IDENTIFIED BY user USING "password";

def get_connection():
    dsn = cx_Oracle.makedsn(DB_HOST, DB_PORT, service_name=DB_SERVICE)
    connection = cx_Oracle.connect(user=DB_USER, password=DB_PASSWORD, dsn=dsn)
    return connection

#connecting webpages
#all html templates placed in html
#redirects to /template/name.html

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form: 
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        # Check if account exists
        connection = get_connection()
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM SignUpTable WHERE email = :email AND password = :password"
        cursor.execute(query, {'email': email, 'password': password})
        account = cursor.fetchone()[0]
        # If account exists show error and validation checks
        if account > 0:
        #     # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session["email"] = email
        #     # Redirect to home page
            return redirect(url_for('index'))
        else:
        #     # Login failed, render the login page with an error message
            error_message = "Invalid username or password"
            return render_template("login.html", error_message=error_message)
    else:
        # Render the login page
        return render_template("login.html", msg=msg)

@app.route('/login/signup', methods=['GET', 'POST'])
def signup():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST':

        custID = request.form["custID"];
        dob = request.form["dob"];
        fname = request.form["fname"]; 
        lname = request.form["lname"]; 
        address = request.form["address"];
        phoneNo = request.form["phoneNo"];
        email = request.form["email"];
        password = request.form['psw']; 
        cpassword = request.form['psw-repeat'];

        connection = get_connection()
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM SignUpTable WHERE email = :email"
        cursor.execute(query, {'email': email})
        account = cursor.fetchone()[0]
        # If account exists show error and validation checks
        if account > 0:
            msg = 'User Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(cpassword, password):
            msg = 'Check password again!'
        elif not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO SignUpTable ( custID, dob, firstName, lastName, address, phoneNo, email, password) VALUES (:custID, :dob, :fname, :lname, :address, :phoneNo, :email, :password)', {"password" : password, "custID" : custID, "dob" : dob, "fname" : fname, "lname" : lname, "address" : address, "phoneNo" : phoneNo, "email" : email})
            connection.commit()
            return redirect(url_for('login'))


    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('signup.html', msg=msg)

@app.route('/index')
def index():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('index.html', email=session['email'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route("/index/details")
def details():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM SignUpTable WHERE email = :email", {"email": session["email"]})
    row = cursor.fetchone()
    user = {
        'custID' : row[0],
        'dob' : row[1],
        'firstName' : row[2],
        'lastName' : row[3],
        'address' : row[4],
        'phoneNo' : row[5],
        'email' : row[6]
    }
    return render_template("details.html", user=user)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('email', None)
    # Redirect to login page
    return redirect(url_for('landing'))

if __name__ == "__main__":
    app.run(debug=True)
