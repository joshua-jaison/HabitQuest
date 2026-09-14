import customtkinter as ctk

from database.database import get_user, get_completion_count, get_best_streak
from core.xp_system import calculate_level


class AchievementsScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        title = ctk.CTkLabel(
            self,
            text="🏆 Achievements",
            font=("Arial", 30, "bold")
        )
        title.pack(anchor="w", padx=30, pady=30)

        try:
            from core.achievements import get_unlocked_achievements
        except Exception:
            get_unlocked_achievements = None

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
            best_streak = get_best_streak()
        except Exception:
            best_streak = 0

        stats = {
            "xp": xp,
            "level": level,
            "completed": completed,
            "best_streak": best_streak
        }

        if get_unlocked_achievements is None:
            achievements = []
        else:
            try:
                value = get_unlocked_achievements(stats)
                achievements = value if isinstance(value, list) else []
            except Exception:
                achievements = []

        if not achievements:
            ctk.CTkLabel(
                self,
                text="No achievements unlocked yet.\nComplete your first quest!",
                font=("Arial", 18)
            ).pack(pady=50)
            return

        for achievement in achievements:
            card = ctk.CTkFrame(self)
            card.pack(fill="x", padx=30, pady=8)

            ctk.CTkLabel(
                card,
                text=f"🏆 {achievement.get('name', 'Achievement')}",
                font=("Arial", 18, "bold")
            ).pack(anchor="w", padx=20, pady=(15, 5))

            ctk.CTkLabel(
                card,
                text=achievement.get("description", "Keep going!")
            ).pack(anchor="w", padx=20, pady=(0, 15))
