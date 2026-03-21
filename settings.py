import customtkinter as ctk

class SettingsPage(ctk.CTkFrame):

    def __init__(self, parent, controller=None):
        super().__init__(parent)

        label = ctk.CTkLabel(self, text="Settings", font=("Arial", 28))
        label.pack(pady=20)