from flask import Flask, render_template, request , redirect
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

# Define a model
# Not strictly needed, but simplifies this example.

con = psycopg2.connect(
    host="postgres.cs.umu.se",
    dbname="c5dv202_vt22_bio18lem",
    user="c5dv202_vt22_bio18lem",
    password="AL4KPaWjuYj4"
)

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = con.cursor()


# The first page the user will see
@app.route('/')
def index():
    # render_template automatically looks for templates in the "templates" directory
    return render_template('index.html')


# Shows all the available customers
@app.route('/shop', methods=['GET'])
def language(): #TODO Chage name
    cur.execute("SELECT * FROM Customer;")
    customers = cur.fetchall()
    return render_template('shop.html', customers=customers)


# Adds a new snack, or updates an existing snack
@app.route('/shop', methods=['POST'])
def add_customer():
    cur.execute("SELECT * FROM Customer;")
    customers = cur.fetchall()

    customer_id = str(request.form['costumer_id'])
    first_name = str(request.form['first_name'])
    last_name = str(request.form['last_name'])

    custIDs=[]
    for customer in customers:
        custIDs.append(customer[0])

    if int(customer_id) in custIDs:
        update_customer = "UPDATE Customer " \
                          "SET first_name = '" + first_name + "', last_name = '" + last_name + \
                          "'WHERE id_customer =" + customer_id + ";"
        cur.execute(update_customer)

    else:
        insert_customer = "INSERT INTO Customer VALUES(" + customer_id + ",'" + first_name + "','" + last_name + "');"
        cur.execute(insert_customer)

    cur.execute("SELECT * FROM Customer;")
    new_customers = cur.fetchall()

    return render_template('shop.html', customers=new_customers)


# Deletes a customer
@app.route('/customer/delete', methods=['POST'])
def delete_language():
    id_to_delete = str(request.form['id_customer'])
    customer_to_delete = "DELETE FROM Customer WHERE id_customer =" + id_to_delete + ";"
    cur.execute(customer_to_delete)

    # Send user back to shop page
    return redirect('/shop')

