import customtkinter as ctk

class CalendarPage(ctk.CTkFrame):

    def __init__(self, parent,controller=None):
        super().__init__(parent)

        label = ctk.CTkLabel(self, text="Calendar", font=("Arial", 28))
        label.pack(pady=20)