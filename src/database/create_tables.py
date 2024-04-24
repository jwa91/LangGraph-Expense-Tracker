from dotenv import load_dotenv
from db_connection import conn, cursor

# Load the environment variables from the .env file
load_dotenv()

# SQL commands to create the tables
create_categories_table = """
CREATE TABLE IF NOT EXISTS categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE
);
"""

create_payment_methods_table = """
CREATE TABLE IF NOT EXISTS payment_methods (
    payment_method_id SERIAL PRIMARY KEY,
    payment_method_name VARCHAR(50) UNIQUE
);
"""

create_expenses_table = """
CREATE TABLE IF NOT EXISTS expenses (
    transaction_id SERIAL PRIMARY KEY,
    date DATE,
    category_id INTEGER,
    description TEXT,
    amount DECIMAL(10, 2),
    vat DECIMAL(10, 2),
    payment_method_id INTEGER,
    business_personal VARCHAR(50),
    declared_on DATE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (payment_method_id) REFERENCES payment_methods(payment_method_id)
);
"""

# Execute the SQL commands to create the tables
cursor.execute(create_categories_table)
cursor.execute(create_payment_methods_table)
cursor.execute(create_expenses_table)

# Commit the changes
conn.commit()

# Close the cursor and the connection
cursor.close()
conn.close()
