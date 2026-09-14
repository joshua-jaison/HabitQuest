import customtkinter as ctk

from core.analytics import weekly_completion, overall_completion
from database.database import get_failure_statistics
import matplotlib.pyplot as plt


class AnalyticsScreen(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        title = ctk.CTkLabel(
            self,
            text="📊 Analytics",
            font=("Arial", 30, "bold")
        )

        title.pack(
            anchor="w",
            padx=30,
            pady=30
        )

        completion = overall_completion()

        card = ctk.CTkFrame(self)

        card.pack(
            fill="x",
            padx=30,
            pady=10
        )

        ctk.CTkLabel(
            card,
            text="Overall Completion",
            font=("Arial", 20, "bold")
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            card,
            text=f"{completion}%",
            font=("Arial", 40, "bold")
        ).pack(pady=(0, 20))

        self.show_failures()

    def show_failures(self):

        title = ctk.CTkLabel(
            self,
            text="🧠 Fallback Analysis",
            font=("Arial", 22, "bold")
        )

        title.pack(
            anchor="w",
            padx=30,
            pady=(30, 10)
        )

        failures = get_failure_statistics()

        if not failures:

            ctk.CTkLabel(
                self,
                text="No fallback data yet."
            ).pack(pady=20)

            return

        for failure in failures:

            ctk.CTkLabel(
                self,
                text=f"{failure['failure_reason']} — "
                f"{failure['count']} times",
                font=("Arial", 16)
            ).pack(
                anchor="w",
                padx=50,
                pady=5
            )
