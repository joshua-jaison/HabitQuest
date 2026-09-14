import sqlite3
import customtkinter as ctk
from datetime import date, timedelta

from database.database import get_connection


class ReflectionScreen(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        title = ctk.CTkLabel(
            self,
            text="📝 Weekly Reflection",
            font=("Arial", 30, "bold")
        )
        title.pack(anchor="w", padx=30, pady=30)

        self.create_field("What went well?", "went_well")
        self.create_field("What held you back?", "held_back")
        self.create_field("What will you change next week?", "next_change")
        self.create_field("What was your biggest improvement?", "improvement")

        button = ctk.CTkButton(
            self,
            text="Save Reflection",
            command=self.save
        )
        button.pack(pady=20)

    def create_field(self, title, attribute):
        label = ctk.CTkLabel(
            self,
            text=title,
            font=("Arial", 17, "bold")
        )
        label.pack(anchor="w", padx=30, pady=(10, 5))

        text = ctk.CTkTextbox(self, height=80)
        text.pack(fill="x", padx=30)

        setattr(self, attribute, text)

    def save(self):
        today = date.today()
        week_start = today - timedelta(days=today.weekday())

        connection = get_connection()
        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO reflections (
                    week_start,
                    went_well,
                    held_back,
                    next_change,
                    improvement,
                    created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(week_start) DO UPDATE SET
                    went_well = excluded.went_well,
                    held_back = excluded.held_back,
                    next_change = excluded.next_change,
                    improvement = excluded.improvement,
                    created_at = excluded.created_at
                """,
                (
                    week_start.isoformat(),
                    self.went_well.get("1.0", "end").strip(),
                    self.held_back.get("1.0", "end").strip(),
                    self.next_change.get("1.0", "end").strip(),
                    self.improvement.get("1.0", "end").strip(),
                    today.isoformat()
                )
            )

            connection.commit()

        except sqlite3.OperationalError as e:
            # Fallback for older SQLite or missing unique constraint
            if "ON CONFLICT" in str(e):
                cursor = connection.cursor()
                cursor.execute(
                    """
                    UPDATE reflections
                    SET went_well = ?, held_back = ?, next_change = ?, improvement = ?, created_at = ?
                    WHERE week_start = ?
                    """,
                    (
                        self.went_well.get("1.0", "end").strip(),
                        self.held_back.get("1.0", "end").strip(),
                        self.next_change.get("1.0", "end").strip(),
                        self.improvement.get("1.0", "end").strip(),
                        today.isoformat(),
                        week_start.isoformat()
                    )
                )

                if cursor.rowcount == 0:
                    cursor.execute(
                        """
                        INSERT INTO reflections (
                            week_start,
                            went_well,
                            held_back,
                            next_change,
                            improvement,
                            created_at
                        ) VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (
                            week_start.isoformat(),
                            self.went_well.get("1.0", "end").strip(),
                            self.held_back.get("1.0", "end").strip(),
                            self.next_change.get("1.0", "end").strip(),
                            self.improvement.get("1.0", "end").strip(),
                            today.isoformat()
                        )
                    )

                connection.commit()
            else:
                raise
        finally:
            connection.close()
