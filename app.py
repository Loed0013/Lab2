from flask import Flask, render_template, request, redirect
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

# Define a model
# Not strictly needed, but simplifies this example.

con = psycopg2.connect(
    host="postgres.cs.umu.se",
    dbname="c5dv202_vt22_ens21vdl",
    user="c5dv202_vt22_ens21vdl",
    password="7Kfz9MJmnrix"
)

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = con.cursor()


# The first page the user will see
@app.route('/')
def index():
    # render_template automatically looks for templates in the "templates" directory
    return render_template('index.html')


# Shows all the available customers
@app.route('/customer', methods=['GET'])
def current_customers():
    cur.execute("SELECT * FROM Customer;")
    customers = cur.fetchall()
    return render_template('customers.html', customers=customers)


# Adds a new customer, or updates an existing customer
@app.route('/customer', methods=['POST'])
def add_customer():
    cur.execute("SELECT * FROM Customer;")
    customers = cur.fetchall()

    customer_id = str(request.form['costumer_id'])
    first_name = str(request.form['first_name'])
    last_name = str(request.form['last_name'])

    custIDs = []
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

    return render_template('customers.html', customers=new_customers)


# Deletes a customer
@app.route('/customer/delete', methods=['POST'])
def delete_customer():
    id_to_delete = str(request.form['id_customer'])
    customer_to_delete = "DELETE FROM Customer WHERE id_customer =" + id_to_delete + ";"
    cur.execute(customer_to_delete)

    # Send user back to customer page
    return redirect('/customer')

@app.route('/invoice', methods=['GET'])
def current_invoice():
    cur.execute("SELECT * FROM Invoices;")
    invoices = cur.fetchall()
    cur.execute("SELECT * FROM Includes;")
    includes = cur.fetchall()
    return render_template('invoices.html', invoices=invoices, includes=includes)

# Adds a new invoice, or updates an existing invoice
@app.route('/invoice/adinvoice', methods=['POST'])
def add_invoice():
    cur.execute("SELECT * FROM Invoices;")
    invoices = cur.fetchall()

    invoice_id = str(request.form['invoice_id'])
    customer_id = str(request.form['customer_id'])

    invIDs = []
    for invoice in invoices:
        invIDs.append(invoice[0])

    if int(invoice_id) in invIDs:
        update_invoice = "UPDATE Invoices SET id_customer  = '" + customer_id + "'WHERE id_invoice =" + invoice_id + ";"
        cur.execute(update_invoice)

    else:
        insert_invoice = "INSERT INTO Invoices VALUES(" + invoice_id + ",'" + customer_id +"');"
        cur.execute(insert_invoice)

    return redirect('/invoice')

# Deletes a invoice
@app.route('/invoice/delete', methods=['POST'])
def delete_invoice():
    id_to_delete = str(request.form['id_invoice'])
    invoice_to_delete = "DELETE FROM Invoices WHERE id_invoice =" + id_to_delete + ";"
    cur.execute(invoice_to_delete)

    # Send user back to invoice page
    return redirect('/invoice')

# Adds a new invoice, or updates an existing invoice
@app.route('/invoice/adinclude', methods=['POST'])
def add_included():
    cur.execute("SELECT * FROM Includes;")
    included = cur.fetchall()

    invoice_id = str(request.form['invoice_id'])
    product_id = str(request.form['product_id'])
    quantity = str(request.form['quantity'])
    invIDs = []
    for include in included:
        invIDs.append(include[0:2])

    inv_prod = (int(invoice_id), int(product_id))
    if inv_prod in invIDs:
        update_invoice = "UPDATE Includes " \
                         "SET  quantity = " + quantity + \
                         "WHERE id_product  = " + product_id + "and id_invoice =" + invoice_id + ";"
        cur.execute(update_invoice)

    else:
        insert_invoice = "INSERT INTO Includes VALUES(" + invoice_id + "," + product_id + "," + quantity + ");"
        cur.execute(insert_invoice)

    return redirect('/invoice')

@app.route('/invoice/delinclude', methods=['POST'])
def delete_included():
    invoice_to_delete = str(request.form['id_invoice'])
    product_to_delete = str(request.form['id_product'])

    included_to_delete = "DELETE FROM Includes " \
                         "WHERE id_invoice =" + invoice_to_delete + "and id_product=" + product_to_delete + ";"
    cur.execute(included_to_delete)

    # Send user back to invoice page
    return redirect('/invoice')

# Shows all the available products
@app.route('/products', methods=['GET'])
def current_products():
    cur.execute("SELECT * FROM Products;")
    products = cur.fetchall()
    return render_template('products.html', products=products)


# Adds a new product, or updates an existing product
@app.route('/products', methods=['POST'])
def add_product():
    cur.execute("SELECT * FROM Products;")
    products = cur.fetchall()

    product_id = str(request.form['product_id'])
    product_name = str(request.form['product_name'])
    product_price = str(request.form['Product_price'])

    prodIDs = []
    for product in products:
        prodIDs.append(product[0])

    if int(product_id) in prodIDs:
        update_product = "UPDATE Products " \
                          "SET name = '" + product_name + "', unit_price = '" + product_price + \
                          "'WHERE id_product =" + product_id + ";"
        cur.execute(update_product)

    else:
        insert_product = "INSERT INTO Products VALUES(" + product_id + ",'" + product_name + "','" + product_price + "');"
        cur.execute(insert_product)

    cur.execute("SELECT * FROM Products;")
    new_products = cur.fetchall()

    return render_template('products.html', products=new_products)


# Deletes a product
@app.route('/products/delete', methods=['POST'])
def delete_product():
    id_to_delete = str(request.form['id_product'])
    product_to_delete = "DELETE FROM Products WHERE id_product =" + id_to_delete + ";"
    cur.execute(product_to_delete)

    # Send user back to product page
    return redirect('/products')

#TODO
# Add a trigger, Total spending for a customer
# Specify Foregin keys, inovices and includes
# Video
# ER Diagram
