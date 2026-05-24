import tkinter as tk
from itertools import product
from tkinter import ttk, messagebox

from pyexpat.errors import messages

from database import Database


class WarehouseApp:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.root.title('Warehouse')

        # Fields
        tk.Label(root, text='Title').grid(row=0, column=0)
        tk.Label(root, text='Quantity').grid(row=1, column=0)
        tk.Label(root, text='Price').grid(row=2, column=0)

        # Entries
        self.name_entry = tk.Entry(root)
        self.quantity_entry = tk.Entry(root)
        self.price_entry = tk.Entry(root)

        self.name_entry.grid(row=0, column=1)
        self.quantity_entry.grid(row=1, column=1)
        self.price_entry.grid(row=2, column=1)

        # Buttons
        tk.Button(root, text='Add', width=12, command=self.add_product).grid(row=3, column=0)
        tk.Button(root, text='Delete', width=12, command=self.delete_product).grid(row=3, column=1)
        tk.Button(root, text='Sell', width=12, command=self.sell_product).grid(row=4, column=1)
        tk.Button(root, text='Update', width=12, command=self.update_product).grid(row=4, column=0)

        # Table
        self.tree = ttk.Treeview(root, columns=('ID', 'Title', 'Quantity', 'Price'), show='headings')
        for col in ('ID', 'Title', 'Quantity', 'Price'):
            self.tree.heading(col, text=col)
        self.tree.grid(row=5, column=0, columnspan=2)

    def load_data(self):
        """
        Load data into the table.

        This function clears all existing rows in the Treeview.
        Then it gets product data from the database and inserts
        each product as a new row in the table.
        """

        for row in self.tree.get_children():
            self.tree.delete(row)

        for product in self.db.get_products():
            self.tree.insert('', tk.END, values=product)

    def add_product(self):
        """
        Add a new product to the database.

        Retrieves input values (name, quantity, price) from the UI fields,
        converts them to the appropriate types, and stores them in the database.
        Refreshes the table after successful insertion.

        Raises:
            ValueError: If the name is empty or if quantity/price cannot be
            converted to int/float.

        Notes:
            Any exception is caught and an error message is shown to the user
            via a message box.

            Result:
                The product is added to the database and displayed in the table.
        """

        try:
            name = self.name_entry.get()
            quantity = int(self.quantity_entry.get())
            price = float(self.price_entry.get())

            if not name:
                raise ValueError

            self.db.add_product(name, quantity, price)
            self.load_data()
        except Exception as e:
            messagebox.showerror('Error', 'Enter correct values')
            print(e)

    def delete_product(self):
        """
        Delete a product from the table.

        This function checks if the user selected a row.
        If nothing is selected, it does nothing.
        If a row is selected, it gets the product ID,
        deletes the product from the database,
        and updates the table.
        """
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        product_id = item['values'][0]
        self.db.delete_product(product_id)
        self.load_data()

    def update_product(self):
        """
        Update the quantity of a selected product.

        This function checks if a row is selected in the table.
        If nothing is selected, it does nothing.
        It then reads the quantity from the input field.
        If the value is not a valid number, it shows an error message.

        If everything is correct, it gets the product ID,
        updates the quantity in the database,
        and reloads the table data.
        """
        selected = self.tree.selection()
        if not selected:
            return
        try:
            quantity = int(self.quantity_entry.get())
        except:
            messagebox.showerror('Error', 'Enter correct values')
            return
        item = self.tree.item(selected[0])
        product_id = item['values'][0]

        self.db.update_quantity(quantity, product_id)
        self.load_data()

    def sell_product(self):
        """
        Sell product from the table.

        This function checks if a row is selected.
        If not, it shows an error.
        It gets the quantity from the input.
        If the value is not a number, it shows an error.

        Then it tries to sell the product.
        If success, it refreshes the table.
        If not enough product, it shows an error.
        """
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror('Error', 'Enter correct values')
            return

        try:
            quantity = int(self.quantity_entry.get())
        except:
            messagebox.showerror('Error', 'Enter correct values')

        item = self.tree.item(selected[0])
        product_id = item['values'][0]

        success = self.db.sell_product(product_id, quantity)
        if success:
            self.load_data()
        else:
            messagebox.showerror('Error', 'Not enough product')


if __name__ == '__main__':
    root = tk.Tk()
    app = WarehouseApp(root)
    root.mainloop()
