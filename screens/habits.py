import customtkinter as ctk
from tkinter import messagebox

from database.database import (
    add_habit,
    get_habits,
    delete_habit
)


class HabitsScreen(ctk.CTkFrame):

    def __init__(self, parent, refresh_callback=None):
        super().__init__(parent)

        self.refresh_callback = refresh_callback

        self.grid_columnconfigure(0, weight=1)

        self.create_header()
        self.create_add_form()
        self.create_habit_list()

    def create_header(self):

        header = ctk.CTkFrame(self)
        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=20,
            pady=20
        )

        title = ctk.CTkLabel(
            header,
            text="🎯 Your Habits",
            font=("Arial", 28, "bold")
        )

        title.pack(
            side="left",
            padx=20,
            pady=15
        )

    def create_add_form(self):

        frame = ctk.CTkFrame(self)
        frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=20,
            pady=10
        )

        self.name_entry = ctk.CTkEntry(
            frame,
            placeholder_text="Habit name"
        )

        self.name_entry.grid(
            row=0,
            column=0,
            padx=10,
            pady=15
        )

        self.category_menu = ctk.CTkOptionMenu(
            frame,
            values=[
                "Health",
                "Study",
                "Fitness",
                "Mind",
                "Work",
                "Other"
            ]
        )

        self.category_menu.grid(
            row=0,
            column=1,
            padx=10
        )

        self.difficulty_menu = ctk.CTkOptionMenu(
            frame,
            values=[
                "Easy",
                "Medium",
                "Hard",
                "Epic"
            ],
            command=self.update_xp
        )

        self.difficulty_menu.set("Medium")

        self.difficulty_menu.grid(
            row=0,
            column=2,
            padx=10
        )

        self.xp_label = ctk.CTkLabel(
            frame,
            text="40 XP"
        )

        self.xp_label.grid(
            row=0,
            column=3,
            padx=10
        )

        add_button = ctk.CTkButton(
            frame,
            text="+ Add Habit",
            command=self.create_habit
        )

        add_button.grid(
            row=0,
            column=4,
            padx=10
        )

    def update_xp(self, difficulty):

        xp_values = {
            "Easy": 20,
            "Medium": 40,
            "Hard": 70,
            "Epic": 100
        }

        self.xp_label.configure(
            text=f"{xp_values[difficulty]} XP"
        )

    def create_habit(self):

        name = self.name_entry.get().strip()

        if not name:
            messagebox.showwarning(
                "Missing Habit",
                "Please enter a habit name."
            )
            return

        difficulty = self.difficulty_menu.get()

        xp_values = {
            "Easy": 20,
            "Medium": 40,
            "Hard": 70,
            "Epic": 100
        }

        add_habit(
            name=name,
            category=self.category_menu.get(),
            difficulty=difficulty,
            xp=xp_values[difficulty],
            frequency="Daily"
        )

        self.name_entry.delete(0, "end")

        self.refresh_habits()

        messagebox.showinfo(
            "Habit Created",
            f"{name} has been added!"
        )

    def create_habit_list(self):

        self.list_frame = ctk.CTkScrollableFrame(self)

        self.list_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=20,
            pady=20
        )

        self.grid_rowconfigure(2, weight=1)

        self.refresh_habits()

    def refresh_habits(self):

        for widget in self.list_frame.winfo_children():
            widget.destroy()

        habits = get_habits()

        if not habits:

            label = ctk.CTkLabel(
                self.list_frame,
                text="No habits yet.\nCreate your first habit above!",
                font=("Arial", 18)
            )

            label.pack(pady=50)

            return

        for habit in habits:

            card = ctk.CTkFrame(
                self.list_frame
            )

            card.pack(
                fill="x",
                padx=10,
                pady=8
            )

            title = ctk.CTkLabel(
                card,
                text=habit["name"],
                font=("Arial", 18, "bold")
            )

            title.pack(
                side="left",
                padx=20,
                pady=15
            )

            info = ctk.CTkLabel(
                card,
                text=f'{habit["category"]} • '
                f'{habit["difficulty"]} • '
                f'{habit["xp"]} XP'
            )

            info.pack(
                side="left",
                padx=20
            )

            delete_button = ctk.CTkButton(
                card,
                text="Delete",
                width=80,
                command=lambda h=habit["id"]:
                    self.remove_habit(h)
            )

            delete_button.pack(
                side="right",
                padx=20
            )

    def remove_habit(self, habit_id):

        delete_habit(habit_id)

        self.refresh_habits()
