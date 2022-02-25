from flask import Flask, render_template, request
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
def language():
    cur.execute("SELECT * FROM Customer;")
    customers = cur.fetchall()
    return render_template('shop.html', customers=customers)


# Adds a new snack, or updates an existing snack
@app.route('/shop', methods=['POST'])
def add_customer():
    global custo

    customer_id = request.form['costumer_id']
    first_name = (request.form['first_name'])
    last_name = (request.form['last_name'])

    new_customer = Customers(customer_id, first_name, last_name)
    print('Adding new customer:', new_customer)

    # If snack already exists, update values
    for index, old_custo in enumerate(custo):
        if old_custo.id_customer == new_customer.id_customer:
            custo[index] = custo
            break
    else:

        # Else, add the new snack to the list of snacks
        custo.append(new_customer)

    return render_template('shop.html', custo=custo)





