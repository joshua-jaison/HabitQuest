import sqlite3
from datetime import datetime
from pathlib import Path

# Find the main HabitQuest folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Database will be created here
DB_PATH = BASE_DIR / "habitquest.db"


def get_connection():
    """
    Creates and returns a connection to the SQLite database.
    """
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """
    Creates all required database tables.
    """
    connection = get_connection()
    cursor = connection.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        total_xp INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    )
    """)

    # HABITS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        xp INTEGER NOT NULL,
        frequency TEXT NOT NULL,
        created_at TEXT NOT NULL,
        active INTEGER DEFAULT 1
    )
    """)

    # HABIT LOGS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS habit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        completed INTEGER DEFAULT 0,
        xp_earned INTEGER DEFAULT 0,
        failure_reason TEXT,
        failure_note TEXT,
        FOREIGN KEY (habit_id) REFERENCES habits(id),
        UNIQUE(habit_id, date)
    )
    """)

    # REFLECTIONS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reflections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        week_start TEXT NOT NULL UNIQUE,
        went_well TEXT,
        held_back TEXT,
        next_change TEXT,
        improvement TEXT,
        created_at TEXT NOT NULL
    )
    """)

    # CREATE DEFAULT USER
    cursor.execute("SELECT COUNT(*) AS count FROM users")
    result = cursor.fetchone()

    if result["count"] == 0:
        cursor.execute(
            """
            INSERT INTO users (name, total_xp, created_at)
            VALUES (?, ?, ?)
            """,
            ("Player", 0, datetime.now().isoformat())
        )

    connection.commit()
    connection.close()


def get_user():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users LIMIT 1")
    user = cursor.fetchone()
    connection.close()
    return user


def update_user_xp(total_xp):
    connection = get_connection()
    connection.execute(
        "UPDATE users SET total_xp = ? WHERE id = 1",
        (total_xp,)
    )
    connection.commit()
    connection.close()


def update_user_name(name):
    connection = get_connection()
    connection.execute(
        "UPDATE users SET name = ? WHERE id = 1",
        (name,)
    )
    connection.commit()
    connection.close()


def add_habit(name, category, difficulty, xp, frequency):
    connection = get_connection()
    connection.execute(
        """
        INSERT INTO habits (name, category, difficulty, xp, frequency, created_at, active)
        VALUES (?, ?, ?, ?, ?, ?, 1)
        """,
        (
            name,
            category,
            difficulty,
            xp,
            frequency,
            datetime.now().isoformat()
        )
    )
    connection.commit()
    connection.close()


def get_habits():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT *
        FROM habits
        WHERE active = 1
        ORDER BY id DESC
    """)
    habits = cursor.fetchall()
    connection.close()
    return habits


def delete_habit(habit_id):
    connection = get_connection()
    connection.execute(
        "UPDATE habits SET active = 0 WHERE id = ?",
        (habit_id,)
    )
    connection.commit()
    connection.close()


def get_log(habit_id, date_value):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT *
        FROM habit_logs
        WHERE habit_id = ?
        AND date = ?
    """, (habit_id, date_value))
    result = cursor.fetchone()
    connection.close()
    return result


def complete_habit(habit_id, date_value, xp):
    connection = get_connection()
    connection.execute("""
        INSERT INTO habit_logs (habit_id, date, completed, xp_earned, failure_reason, failure_note)
        VALUES (?, ?, 1, ?, NULL, NULL)
        ON CONFLICT(habit_id, date)
        DO UPDATE SET
            completed = 1,
            xp_earned = excluded.xp_earned,
            failure_reason = NULL,
            failure_note = NULL
    """, (
        habit_id,
        date_value,
        xp
    ))
    connection.commit()
    connection.close()


def get_today_logs(date_value):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT *
        FROM habit_logs
        WHERE date = ?
    """, (date_value,))
    results = cursor.fetchall()
    connection.close()
    return results


def get_today_habits(date_value):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT
            h.*,
            COALESCE(l.completed, 0) AS completed,
            COALESCE(l.xp_earned, 0) AS xp_earned
        FROM habits h
        LEFT JOIN habit_logs l
        ON h.id = l.habit_id
        AND l.date = ?
        WHERE h.active = 1
        ORDER BY h.id
    """, (date_value,))
    results = cursor.fetchall()
    connection.close()
    return results


def get_completion_count():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT COUNT(*) AS count
        FROM habit_logs
        WHERE completed = 1
    """)
    result = cursor.fetchone()
    connection.close()
    return result["count"]


def get_best_streak():
    from core.streak_system import get_habit_streak

    habits = get_habits()
    best = 0

    for habit in habits:
        streak = get_habit_streak(habit["id"])
        if streak > best:
            best = streak

    return best


def record_failure(habit_id, date_value, reason, note=""):
    connection = get_connection()
    connection.execute("""
        INSERT INTO habit_logs
        (habit_id, date, completed, xp_earned, failure_reason, failure_note)
        VALUES (?, ?, 0, 0, ?, ?)
        ON CONFLICT(habit_id, date)
        DO UPDATE SET
            completed = 0,
            xp_earned = 0,
            failure_reason = excluded.failure_reason,
            failure_note = excluded.failure_note
    """, (
        habit_id,
        date_value,
        reason,
        note
    ))
    connection.commit()
    connection.close()


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


if __name__ == "__main__":
    initialize_database()
    print("Database initialised successfully!")
    print(f"Database location: {DB_PATH}")
