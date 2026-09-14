import customtkinter as ctk

from database.database import get_user, get_completion_count, get_best_streak
from core.xp_system import calculate_level


class DashboardScreen(ctk.CTkFrame):
    def __init__(self, parent, refresh_callback=None):
        super().__init__(parent)

        self.refresh_callback = refresh_callback

        title = ctk.CTkLabel(
            self,
            text="📊 Dashboard",
            font=("Arial", 30, "bold")
        )
        title.pack(anchor="w", padx=30, pady=30)

        try:
            user = get_user()
        except Exception:
            user = None

        xp = 0
        level = calculate_level(0)
        if user is not None:
            xp = int(user["total_xp"]) if user["total_xp"] is not None else 0
            level = calculate_level(xp)

        try:
            completed = get_completion_count()
        except Exception:
            completed = 0

        try:
            streak = get_best_streak()
        except Exception:
            streak = 0

        stats = [
            ("Level", str(level)),
            ("XP", str(xp)),
            ("Completed", str(completed)),
            ("Best streak", f"{streak} days"),
        ]

        for label_text, value in stats:
            card = ctk.CTkFrame(self)
            card.pack(fill="x", padx=30, pady=8)

            ctk.CTkLabel(
                card,
                text=f"{label_text}: {value}",
                font=("Arial", 18, "bold")
            ).pack(padx=20, pady=15)
