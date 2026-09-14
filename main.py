import customtkinter as ctk

from database.database import initialize_database
from screens.habits import HabitsScreen
from screens.dashboard import DashboardScreen
from screens.analytics import AnalyticsScreen
from screens.achievements import AchievementsScreen
from screens.reflection import ReflectionScreen
from screens.settings import SettingsScreen

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class HabitQuestApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("HabitQuest - Level Up Your Life")
        self.geometry("1200x700")
        self.minsize(1000, 600)

        initialize_database()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_content_area()
        self.show_dashboard()

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        title = ctk.CTkLabel(
            self.sidebar,
            text="HABITQUEST",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=(30, 40))

        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Habits", self.show_habits),
            ("Analytics", self.show_analytics),
            ("Achievements", self.show_achievements),
            ("Reflection", self.show_reflection),
            ("Settings", self.show_settings),
        ]

        for text, command in buttons:
            button = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                height=45,
                anchor="w"
            )
            button.pack(fill="x", padx=20, pady=6)

    def create_content_area(self):
        self.content = ctk.CTkFrame(self, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_content()
        screen = DashboardScreen(
            self.content,
            refresh_callback=self.show_dashboard
        )
        screen.pack(fill="both", expand=True)

    def show_habits(self):
        self.clear_content()
        screen = HabitsScreen(
            self.content,
            refresh_callback=self.show_dashboard
        )
        screen.pack(fill="both", expand=True)

    def show_analytics(self):
        self.clear_content()
        screen = AnalyticsScreen(self.content)
        screen.pack(fill="both", expand=True)

    def show_achievements(self):
        self.clear_content()
        screen = AchievementsScreen(self.content)
        screen.pack(fill="both", expand=True)

    def show_reflection(self):
        self.clear_content()
        screen = ReflectionScreen(self.content)
        screen.pack(fill="both", expand=True)

    def show_settings(self):
        self.clear_content()
        screen = SettingsScreen(self.content)
        screen.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = HabitQuestApp()
    app.mainloop()
