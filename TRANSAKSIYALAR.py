import sqlite3

conn = sqlite3.connect("my_transactions.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    balance REAL NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_account_id INTEGER,
    to_account_id INTEGER,
    amount REAL NOT NULL,
    FOREIGN KEY (from_account_id) REFERENCES accounts (id),
    FOREIGN KEY (to_account_id) REFERENCES accounts (id)
);
""")

cursor.execute("SELECT COUNT(*) FROM accounts;")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO accounts (name, balance) VALUES ('Alice', 1000);")
    cursor.execute("INSERT INTO accounts (name, balance) VALUES ('Bob', 500);")
    conn.commit()

def transfer_money(from_account_id, to_account_id, amount):
    try:
        cursor.execute("BEGIN;")

        cursor.execute("""
        INSERT INTO transactions (from_account_id, to_account_id, amount) 
        VALUES (?, ?, ?);
        """, (from_account_id, to_account_id, amount))

        cursor.execute("""
        UPDATE accounts 
        SET balance = balance - ? 
        WHERE id = ?;
        """, (amount, from_account_id))

        cursor.execute("""
        UPDATE accounts 
        SET balance = balance + ? 
        WHERE id = ?;
        """, (amount, to_account_id))

        conn.commit()
        print("Transaction completed successfully!")
    except sqlite3.Error as e:
        print(f"Xatolik chiqdi: {e}")
        conn.rollback()

transfer_money(1, 2, 100)

cursor.execute("SELECT * FROM accounts;")
accounts = cursor.fetchall()
print("Account Balances:")
for account in accounts:
    print(f"ID: {account[0]}, Name: {account[1]}, Balance: {account[2]}")

cursor.close()
conn.close()

