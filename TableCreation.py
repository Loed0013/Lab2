import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

con = psycopg2.connect(
    host="postgres.cs.umu.se",
    dbname="c5dv202_vt22_ens21vdl",
    user="c5dv202_vt22_ens21vdl",
    password="x")

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS Customer CASCADE;")
cur.execute("DROP TABLE IF EXISTS Invoices CASCADE;")
cur.execute("DROP TABLE IF EXISTS Includes CASCADE;")
cur.execute("DROP TABLE IF EXISTS Products CASCADE;")


tables = [
    ["Customer", "(id_customer smallint PRIMARY KEY, first_name text, last_name text, totalSpending smallint);"],
    ["Invoices", "(id_invoice smallint PRIMARY KEY, id_customer smallint);"],
    ["Includes", "(id_invoice smallint NOT NULL, id_product smallint NOT NULL, quantity smallint NOT NULL);"],
    ["Products", "(id_product smallint NOT NULL PRIMARY KEY, name text, unit_price smallint);"]
]

for table in tables:
    tbName = table[0]
    tbCont = table[1]
    sqlDeleteIfExistsTable = "DROP TABLE IF EXISTS " + tbName + " CASCADE;"
    cur.execute(sqlDeleteIfExistsTable)
    sqlCreateTable = "create table " + tbName + tbCont
    cur.execute(sqlCreateTable)

cur.execute("CREATE OR REPLACE FUNCTION increaseSpending()" +
            "RETURNS trigger AS " +
            "$$" +
            "BEGIN " +
            "UPDATE Customer SET totalSpending = totalSpending + " +
            "NEW.quantity*(SELECT unit_price FROM Products WHERE id_product = NEW.id_product) " +
            "WHERE id_customer = (SELECT id_customer FROM Invoices WHERE id_invoice = NEW.id_invoice);" +
            "RETURN NEW;" +
            "END;" +
            "$$ LANGUAGE plpgsql;")

cur.execute("CREATE OR REPLACE FUNCTION decreaseSpending()" +
            "RETURNS trigger AS " +
            "$$" +
            "BEGIN " +
            "UPDATE Customer SET totalSpending = totalSpending - " +
            "OLD.quantity*(SELECT unit_price FROM Products WHERE id_product = OLD.id_product) " +
            "WHERE id_customer = (SELECT id_customer FROM Invoices WHERE id_invoice = OLD.id_invoice);" +
            "RETURN OLD;" +
            "END;" +
            "$$ LANGUAGE plpgsql;")

cur.execute("CREATE TRIGGER newSpending " +
            "AFTER INSERT " +
            "ON Includes " +
            "FOR EACH ROW " +
            "EXECUTE FUNCTION increaseSpending();")

cur.execute("CREATE TRIGGER deleteSpending " +
            "AFTER DELETE " +
            "ON Includes " +
            "FOR EACH ROW " +
            "EXECUTE FUNCTION decreaseSpending();")

cur.execute("ALTER TABLE Includes ENABLE TRIGGER ALL")



tuples = [
    "INSERT INTO Customer VALUES (1, 'Valentin', 'DEGUIL', 0);",
    "INSERT INTO Customer VALUES (2, 'Joe', 'DASSIN', 0);",
    "INSERT INTO Customer VALUES (3, 'Michel', 'GALABRU', 0);",
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

cur.execute("SELECT * FROM Customer;")
cus = cur.fetchall()
print(cus)
# Make the changes to the database persistent

con.commit()

# Close communication with the database
cur.close()
con.close()
