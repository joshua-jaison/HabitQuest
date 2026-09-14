from datetime import date, timedelta

from database.database import get_connection


def get_habit_streak(habit_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT date
        FROM habit_logs
        WHERE habit_id = ?
        AND completed = 1
        ORDER BY date DESC
    """, (habit_id,))

    rows = cursor.fetchall()

    connection.close()

    if not rows:
        return 0

    dates = [
        date.fromisoformat(row["date"])
        for row in rows
    ]

    today = date.today()

    if dates[0] != today:
        return 0

    streak = 1

    for i in range(1, len(dates)):

        expected = dates[i - 1] - timedelta(days=1)

        if dates[i] == expected:
            streak += 1
        else:
            break

    return streak
