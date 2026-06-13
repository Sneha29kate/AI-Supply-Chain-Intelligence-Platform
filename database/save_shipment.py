from database.db_connection import get_connection

def save_shipment(
    distance,
    warehouse,
    shipping_mode,
    priority,
    delayed
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO shipments
        (
            distance,
            warehouse,
            shipping_mode,
            priority,
            delayed
        )
        VALUES (%s,%s,%s,%s,%s)
        """,
        (
            distance,
            warehouse,
            shipping_mode,
            priority,
            delayed
        )
    )

    conn.commit()

    cur.close()
    conn.close()