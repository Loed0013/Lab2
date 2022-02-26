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
############################################
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

####################################################
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
        invIDs.append(include[0])

    if int(invoice_id) in invIDs:
        update_invoice = "UPDATE Includes " \
                         "SET id_product  = " + product_id + ", quantity = " + quantity + \
                         "WHERE id_invoice =" + invoice_id + ";"
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


#TODO
# Page for products
# Page for Invoices and includes
# Add a trigger, Total spending for a customer
# Specify Foregin keys, inovices and includes
# Video
# ER Diagram