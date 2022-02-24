CREATE TABLE Customer (
    id_customer smallint NOT NULL PRIMARY KEY,
    first_name text,
    last_name text,
);

CREATE TABLE Invoices (
    id_invoice smallint,
    id_customer smallint,
);

CREATE TABLE Includes (
    id_invoice smallint NOT NULL,
    id_product smallint NOT NULL,
    quantity smallint NOT NULL,
);

CREATE TABLE Products (
    id_product smallint NOT NULL,
    name text,
    unit_price
);

"Receive"  "Products"


class Products:
    def __init__(self, id_product, name, unit_price):
        self.id_product = id_product
        self.name = name
        self.unit_price = unit_price

    def __str__(self):
        return f'id_product: {self.id_product}, Name: {self.name}, Unit price: {self.unit_price}'

