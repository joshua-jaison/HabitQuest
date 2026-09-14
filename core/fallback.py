from database.database import get_connection


def get_recommendation(reason):
    recommendations = {
        "Didn't have time": (
            "Try reducing the habit duration. "
            "A 15-minute version is better than skipping it."
        ),
        "Forgot": (
            "Create a reminder or connect this habit "
            "to an existing routine."
        ),
        "Too tired": (
            "Move the habit to a time when your energy "
            "is usually higher."
        ),
        "Lost motivation": (
            "Make the habit extremely small. "
            "Focus on starting rather than finishing."
        ),
        "Unexpected event": (
            "Create a backup version of the habit "
            "for busy or unusual days."
        ),
        "Other": (
            "Look at your notes and identify what "
            "could be changed next time."
        )
    }

    return recommendations.get(reason, recommendations["Other"])


def get_failure_statistics():
    connection = get_connection()
    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT failure_reason, COUNT(*) AS count
            FROM habit_logs
            WHERE completed = 0
              AND failure_reason IS NOT NULL
            GROUP BY failure_reason
            ORDER BY count DESC
            """
        )

        return cursor.fetchall()
    finally:
        connection.close()
