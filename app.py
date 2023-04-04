from flask import Flask, render_template
import sqlite3


DATABASE = "coffee.db.db"

app = Flask(__name__)


def create_connection(db_file):
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
    con = create_connection(DATABASE)
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


app.run(host='0.0.0.0', debug=True)