import customtkinter as ctk

from database.database import (
    get_user,
    update_user_name
)


class SettingsScreen(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        title = ctk.CTkLabel(
            self,
            text="⚙ Settings",
            font=("Arial", 30, "bold")
        )

        title.pack(
            anchor="w",
            padx=30,
            pady=30
        )

        user = get_user()

        ctk.CTkLabel(
            self,
            text="Player Name",
            font=("Arial", 18, "bold")
        ).pack(
            anchor="w",
            padx=30,
            pady=(20, 5)
        )

        self.name_entry = ctk.CTkEntry(
            self,
            width=300
        )

        self.name_entry.insert(
            0,
            user["name"]
        )

        self.name_entry.pack(
            anchor="w",
            padx=30
        )

        ctk.CTkButton(
            self,
            text="Save Name",
            command=self.save_name
        ).pack(
            anchor="w",
            padx=30,
            pady=15
        )

        ctk.CTkLabel(
            self,
            text="Theme"
        ).pack(
            anchor="w",
            padx=30,
            pady=(30, 5)
        )

        theme = ctk.CTkOptionMenu(
            self,
            values=[
                "Dark",
                "Light",
                "System"
            ],
            command=ctk.set_appearance_mode
        )

        theme.set("Dark")

        theme.pack(
            anchor="w",
            padx=30
        )

    def save_name(self):

        name = self.name_entry.get().strip()

        if name:
            update_user_name(name)
