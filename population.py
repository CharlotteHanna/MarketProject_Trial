from faker import Faker
import random
import sqlite3  

# Initialize Faker
fake = Faker()

# Connect to the database
connection = sqlite3.connect('marketplace.db')
cursor = connection.cursor()

# Enum values for payment_status
payment_status_choices = ["pending", "completed", "failed"]
payment_methods = ["credit_card", "debit_card", "paypal", "bank_transfer"]

# Ensure the table exists (adjust schema if needed)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        payment_amount REAL,
        payment_status TEXT,
        payment_method TEXT
    )
''')
connection.commit()

# Function to insert random data
def populate_payments_table(n):
    for _ in range(n):
        payment_amount = round(random.uniform(10.0, 500.0), 2)  # Random amount between 10 and 1000
        payment_status = random.choice(payment_status_choices)    # Randomly select a status
        payment_method = random.choice(payment_methods)           # Randomly select a payment method

        # Insert data into the payments table
        cursor.execute('''
            INSERT INTO payments (payment_amount, payment_status, payment_method)
            VALUES (?, ?, ?)
        ''', (payment_amount, payment_status, payment_method))
    
    # Commit the inserts
    connection.commit()
    print(f"{n} records inserted successfully.")

# Populate the table with 100 random payment records
populate_payments_table(10)

# Close the connection
connection.close()
