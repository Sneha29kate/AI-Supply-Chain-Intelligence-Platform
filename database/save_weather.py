from database.db_connection import get_connection

def save_weather(
    city,
    temperature,
    humidity,
    condition,
    risk
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO weather_logs
        (
            city,
            temperature,
            humidity,
            weather_condition,
            risk
        )
        VALUES (%s,%s,%s,%s,%s)
        """,
        (
            city,
            temperature,
            humidity,
            condition,
            risk
        )
    )

    conn.commit()

    cur.close()
    conn.close()