import customtkinter as ctk

from database.database import initialize_database

# APPEARANCE

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# MAIN APPLICATION


class HabitQuestApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # window settings
        self.title("HabitQuest - Level Up Your Life")

        self.geometry("1200x700")

        self.minsize(1000, 600)

        initialize_database()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # create interface
        self.create_sidebar()
        self.create_content_area()

        # show initial screen
        self.show_dashboard()

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(False)

        title = ctk.CTkLabel(
            self.sidebar,
            text="HABITQUEST",
            font=("Arial", 22, "bold")
        )

        title.pack(
            pady=(30, 40)
        )

    # navigationbuttons
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

            button.pack(
                fill="x",
                padx=20,
                pady=6

            )
# CONTENT AREA

    def create_content_area(self):

        self.content = ctk.CTkFrame(
            self,
            corner_radius=0
        )

        self.content.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=10,
            pady=10
        )


# TO CLEAR CONTENT


    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):

        self.clear_content()

        label = ctk.CTkLabel(
            self.content,
            text="Dashboard",
            font=("Arial", 30, "bold")

        )

        label.pack(
            pady=50
        )

    def show_habits(self):

        self.clear_content()

        label = ctk.CTkLabel(
            self.content,
            text="Habits",
            font=("Arial", 30, "bold")
        )

        label.pack(
            pady=50
        )

    def show_analytics(self):

        self.clear_content()

        label = ctk.CTkLabel(
            self.content,
            text="Analytics",
            font=("Arial", 30, "bold")
        )

        label.pack(
            pady=50
        )

    def show_achievements(self):

        self.clear_content()

        label = ctk.CTkLabel(
            self.content,
            text="Achievements",
            font=("Arial", 30, "bold")
        )

        label.pack(
            pady=50
        )

    def show_reflection(self):

        self.clear_content()

        label = ctk.CTkLabel(
            self.content,
            text="Reflection",
            font=("Arial", 30, "bold")
        )

        label.pack(
            pady=50
        )

    def show_settings(self):

        self.clear_content()

        label = ctk.CTkLabel(
            self.content,
            text="Settings",
            font=("Arial", 30, "bold")

        )

        label.pack(
            pady=50
        )

# START APPLICATION


if __name__ == "__main__":
    app = HabitQuestApp()
    app.mainloop()
