import sqlite3

class DatabaseManager:
    def __init__(self, db_name="products.db"):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def create_table(self):
        """Create products table if it doesn't exist"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT,
                price REAL
            )
        """)
        self.conn.commit()

    def add_products_from_text_file(self, file_path):
        """Add products to the database from a text file"""
        with open(file_path, 'r') as f:
            lines = f.readlines()

        for line in lines[1:]:  # Skip header line
                name, description, category, price = line.strip().split(',')
                self.add_products(name, description, category, float(price))

    def add_products(self, name, description, category, price):
        """Add a new product to the database"""
        self.cursor.execute("""
            INSERT INTO products (name, description, category, price)
            VALUES (?, ?, ?, ?)
        """, (name, description, category, price))
        self.conn.commit()

    def get_all_products(self):
        """Retrieve all products from the database"""
        self.cursor.execute("SELECT * FROM products")
        return self.cursor.fetchall()
    
    def search_products(self, keyword):
        """Search for products by name or description"""
        self.cursor.execute("""
            SELECT * FROM products
            WHERE name LIKE ? OR description LIKE ?
        """, (f'%{keyword}%', f'%{keyword}%'))
        return self.cursor.fetchall()
        