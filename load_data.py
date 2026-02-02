from sqlalchemy import create_engine
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()


def db_connect():
    conn = psycopg2.connect(
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT")
    )
    return conn


def load_to_db():

    # connect to db
    db_conn = db_connect()
    cur = db_conn.cursor()

    try:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS retail_sales (
            customer_name VARCHAR(100),
            store VARCHAR(50),
            category VARCHAR(50),
            quantity INTEGER,
            product_price NUMERIC(10,2),
            total_amount NUMERIC(10,2),
            date DATE
        );
        
        """
        cur.execute(create_table_query)
        print("Table created successfully")

        with open('sales_data.csv', 'r') as sd:
            sql_copy_query = "COPY retail_sales FROM STDIN WITH CSV HEADER"
            cur.copy_expert(sql_copy_query, sd)
            print('Sales data copied successfully to database')

        conn.commit()
    except Exception as e:
        print(f"an error occured when copying to the database: {e}")
        conn.rollback()

    finally:
        # cleanup connections
        cur.close()
        conn.close()


load_to_db()
