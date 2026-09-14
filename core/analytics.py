from datetime import date, timedelta

from database.database import get_connection


def weekly_completion():
    today = date.today()
    start = today - timedelta(days=6)

    connection = get_connection()
    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT date, COUNT(*) AS completed
            FROM habit_logs
            WHERE completed = 1
            AND date BETWEEN ? AND ?
            GROUP BY date
            ORDER BY date
            """,
            (start.isoformat(), today.isoformat())
        )

        rows = cursor.fetchall()

        # Build a full 7-day range so missing days show as 0
        result = []
        current = start
        lookup = {row["date"]: row["completed"] for row in rows}

        while current <= today:
            result.append({
                "date": current.isoformat(),
                "completed": lookup.get(current.isoformat(), 0)
            })
            current += timedelta(days=1)

        return result

    finally:
        connection.close()


def overall_completion():
    connection = get_connection()
    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                COALESCE(SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END), 0) AS completed,
                COUNT(*) AS total
            FROM habit_logs
            """
        )

        result = cursor.fetchone()

        if result is None or result["total"] in (None, 0):
            return 0

        return round((result["completed"] / result["total"]) * 100, 1)

    finally:
        connection.close()
