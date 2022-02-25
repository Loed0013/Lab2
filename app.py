from flask import Flask, render_template, request
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

app = Flask(__name__)

# Define a model
# Not strictly needed, but simplifies this example.

con = psycopg2.connect(
    host="postgres.cs.umu.se",
    dbname="c5dv202_vt22_bio18lem",
    user="c5dv202_vt22_bio18lem",
    password="x"
    )

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cur = con.cursor()

class Customers:
    def __init__(self, id_customer, first_name, last_name):
        self.id_customer = id_customer
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        return f'id_customer: {self.id_customer}, First name: {self.first_name}, Last name: {self.last_name}'


class Invoices:
    def __init__(self, id_invoice, id_customer):
        self.id_invoice = id_invoice
        self.id_customer = id_customer

    def __str__(self):
        return f'id_invoice: {self.id_invoice}, id_customer: {self.id_customer}'


class Products:
    def __init__(self, id_product, name, unit_price):
        self.id_product = id_product
        self.name = name
        self.unit_price = unit_price

    def __str__(self):
        return f'id_product: {self.id_product}, Name: {self.name}, Unit price: {self.unit_price}'


class Includes:
    def __init__(self, id_invoice, id_product, quantity):
        self.id_invoice = id_invoice
        self.id_product = id_product
        self.quantity = quantity

    def __str__(self):
        return f'id_invoice: {self.id_invoice}, id_product: {self.id_product}, quantity: {self.quantity}'




# The first page the user will see
@app.route('/')
def index():
    # render_template automatically looks for templates in the "templates" directory
    return render_template('index.html')


# Shows all the available customers
@app.route('/shop', methods=['GET'])
def language():
    cur.execute("SELECT * FROM Customer;")
    cur.fetchall()
    return render_template('shop.html')


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

# Deletes a snack
#@app.route('/snacks/delete', methods=['POST'])
#def delete_language():
#    global snacks
#
#    snack_to_delete = request.form['snack_name']
#
#    print(f'Deleting snack {snack_to_delete}')
#
#    snacks = [snack for snack in snacks if snack.name != snack_to_delete]
#
#    # Send user back to snacks page
#    return redirect('/snacks')


# Make the changes to the database persistent
con.commit()
# Close communication with the database
cur.close()
con.close()


# Base customers
baseCustomers = [Customers(1, 'Valentin', 'DEGUIL'),
                 Customers(2, 'Joe', 'DASSIN'),
                 Customers(3, 'Michel', 'GALABRU')]

baseInvoices = [Invoices(1, 1),
                Invoices(2, 2),
                Invoices(3, 3)]

baseProducts = [Products(1, 'Orange juice', 15),
                Products(2, 'Broccoli', 40),
                Products(3, 'Peanut', 200)]

baseIncludes = [Includes(1, 1, 2),
                Includes(1, 2, 1),
                Includes(1, 3, 0.5),
                Includes(2, 1, 1),
                Includes(2, 2, 3),
                Includes(3, 2, 2),
                Includes(3, 3, 0.75)]
