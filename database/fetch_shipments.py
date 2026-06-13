import pandas as pd
from database.db_connection import get_connection

def get_shipments():

    conn = get_connection()

    query = """
    SELECT *
    FROM shipments
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df