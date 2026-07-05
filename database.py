import sqlite3

DATABASE_NAME = "loan_workbench.db"

def get_connection():
    return sqlite3.connect(DATABASE_NAME)

def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS loan_applications(

        application_id TEXT PRIMARY KEY,

        customer_name TEXT,

        age INTEGER,

        mobile TEXT,

        email TEXT,

        pan TEXT,

        aadhaar TEXT,

        employment_type TEXT,

        experience INTEGER,

        loan_type TEXT,

        loan_amount REAL,

        monthly_income REAL,

        existing_emi REAL,

        credit_score INTEGER,

        status TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_application(data):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO loan_applications
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)

    """, data)

    conn.commit()
    conn.close()

def get_all_applications():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM loan_applications")

    data = cursor.fetchall()

    conn.close()

    return data

def generate_application_id():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM loan_applications")

    count = cursor.fetchone()[0] + 1

    conn.close()

    return f"APP{count:06d}"