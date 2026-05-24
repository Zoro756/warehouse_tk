import sqlite3

class Database:
    def __init__(self, db_name="warehouse.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            quantity INTEGER,
            price REAL
        )
        """)
        self.conn.commit()

    def add_product(self, name, quantity, price):
        self.cursor.execute("SELECT id, quantity FROM products WHERE name=?", (name,))
        result = self.cursor.fetchone()

        if result:
            product_id, current_quantity = result
            new_quantity = current_quantity + quantity

            self.cursor.execute(
                "UPDATE products SET quantity=? WHERE id=?",
                (new_quantity, product_id)
            )
        else:
            self.cursor.execute(
                "INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)",
                (name, quantity, price)
            )

        self.conn.commit()

    def get_products(self):
        self.cursor.execute("SELECT * FROM products")
        return self.cursor.fetchall()

    def delete_product(self, product_id):
        self.cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        self.conn.commit()

    def update_quantity(self, product_id, quantity):
        self.cursor.execute(
            "UPDATE products SET quantity=? WHERE id=?",
            (quantity, product_id)
        )
        self.conn.commit()

    def sell_product(self, product_id, quantity):
        self.cursor.execute(
            "SELECT quantity FROM products WHERE id=?",
            (product_id,)
        )
        result = self.cursor.fetchone()

        if result:
            current_quantity = result[0]

            if current_quantity >= quantity:
                new_quantity = current_quantity - quantity

                self.cursor.execute(
                    "UPDATE products SET quantity=? WHERE id=?",
                    (new_quantity, product_id)
                )
                self.conn.commit()
                return True
            else:
                return False
