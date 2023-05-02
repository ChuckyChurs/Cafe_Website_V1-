from flask import Flask, render_template, redirect, request, session
import sqlite3
from sqlite3 import Error
from flask_bcrypt import Bcrypt


DATABASE = "C:/Users/19229/OneDrive - Wellington College/13 DTS/coffee/coffee.db.db"

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "kzgsdlit3e"


def open_database(db_file):
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except ValueError as e:
        print(e)
    return None



@app.route('/')
def render_home():
    return render_template('home.html')


@app.route('/menu/<cat_id>')
def render_menu(cat_id):
    con = open_database(DATABASE)
    query = "SELECT name, description, volume, image, price FROM products WHERE cat_id=?"
    cur = con.cursor()
    cur.execute(query, (cat_id, ))
    product_list = cur.fetchall()
    query = "SELECT id, name FROM category"
    cur = con.cursor()
    cur.execute(query)
    category_list = cur.fetchall()
    con.close()
    print(product_list)
    return render_template('menu.html', products=product_list, categories=category_list )


@app.route('/contact')
def render_contact():
    return render_template('contact.html')


@app.route('/login', methods=['POST', 'GET'])
def render_login():
    print("logging in")
    if request.method == "POST":
        email = request.form['email'].strip().lower()
        password = request.form['password'].strip()
        print(email)
        query = "SELECT id, fname, password FROM user WHERE email = ?"
        con = open_database(DATABASE)
        cur = con.cursor()
        cur.execute(query, (email,))
        user_data = cur.fetchone()
        con.close()
        print(user_data)


        try:
            user_id = user_data[0]
            first_name = user_data[1]
            db_password = user_data[2]
        except IndexError:
            return redirect("/login?error=Email+invalid+or+password+incorrect")

        if not bcrypt.check_password_hash(db_password, password):
            return redirect(request.referrer + "?error=Email+invalid+or+password+incorrect")

        session['email'] = email
        session['user_id'] = user_id
        session['first_name'] = first_name
        print(session)
        return redirect('/')



    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def render_signup():
    if request.method == "POST":
        print(request.form)
        fname = request.form.get('fname').title().strip()
        lname = request.form.get('lname').title()
        email = request.form.get('email').lower().strip()
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if password != password2:
            return redirect("\signup?error=Passwords+do+not+match")
        if len(password) < 8:
            return redirect("\signup?error=Password+msut+be+at+least+8+characters+long")

        hashed_password = bcrypt.generate_password_hash(password)
        con = open_database(DATABASE)
        query = "INSERT INTO user(fname, lname, email, password) VALUES (?, ?, ?, ?)"
        cur = con.cursor()

        try:
            cur.execute(query, (fname, lname, email, hashed_password))
        except:
            con.close()
            return redirect("\signup?error=Email+is+already+used")

        con.commit()
        con.close()

    return render_template('signup.html')


app.run(host='0.0.0.0', debug=True)