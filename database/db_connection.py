import psycopg2

def get_connection():

    conn = psycopg2.connect(
        host="localhost",
        port="5433",
        database="supply_chain_db",
        user="postgres",
        password="sneha2924"
    )

    return conn