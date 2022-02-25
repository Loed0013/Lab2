import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


con = psycopg2.connect(
    host="postgres.cs.umu.se",
    dbname="c5dv202_vt22_bio18lem",
    user="c5dv202_vt22_bio18lem",
    password="AL4KPaWjuYj4"
)


con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cur = con.cursor()

tables = [
    ["Customer", "(id_customer smallint PRIMARY KEY, first_name text, last_name text);"],
    ["Invoices", "(id_invoice smallint PRIMARY KEY, id_customer smallint);"],
    ["Includes", "(id_invoice smallint NOT NULL, id_product smallint NOT NULL, quantity smallint NOT NULL);"],
    ["Products", "(id_product smallint NOT NULL PRIMARY KEY, name text, unit_price smallint);"]
]
for table in tables:
    tbName = table[0]
    tbCont = table[1]
    sqlDeleteIfExistsTable = "DROP TABLE IF EXISTS "+tbName+" CASCADE;"
    cur.execute(sqlDeleteIfExistsTable)
    sqlCreateTable = "create table "+tbName+tbCont
    cur.execute(sqlCreateTable)

tuples = [
    "INSERT INTO Customer VALUES (1, 'Valentin', 'DEGUIL');",
    "INSERT INTO Customer VALUES (2, 'Joe', 'DASSIN');",
    "INSERT INTO Customer VALUES (3, 'Michel', 'GALABRU');",
    "INSERT INTO Invoices VALUES (1,1);",
    "INSERT INTO Invoices VALUES (2,2);",
    "INSERT INTO Invoices VALUES (3,3);",
    "INSERT INTO Products VALUES (1, 'Orange juice', 15);",
    "INSERT INTO Products VALUES (2, 'Broccoli', 40);",
    "INSERT INTO Products VALUES (3, 'Peanut', 200);",
    "INSERT INTO Includes VALUES (1, 1, 2);",
    "INSERT INTO Includes VALUES (1, 2, 1);",
    "INSERT INTO Includes VALUES (1, 3, 1);",
    "INSERT INTO Includes VALUES (2, 1, 1);",
    "INSERT INTO Includes VALUES (2, 2, 3);",
    "INSERT INTO Includes VALUES (3, 2, 2);",
    "INSERT INTO Includes VALUES (3, 3, 1);"
]

for tuple in tuples:
    cur.execute(tuple)

# Make the changes to the database persistent

con.commit()

# Close communication with the database
cur.close()
con.close()
