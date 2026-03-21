import customtkinter as ctk
from matplotlib import container
from matplotlib import container

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Centering container
        container = ctk.CTkFrame(self, width=400, height=300, corner_radius=10)
        container.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(container, text="Login", font=("Arial", 28)).pack(pady=20)

        ctk.CTkLabel(container, text="Username").pack(pady=(10,5))
        self.username_entry = ctk.CTkEntry(container, placeholder_text="Enter username")
        self.username_entry.pack(pady=5, padx=20, fill="x")

        ctk.CTkLabel(container, text="Password").pack(pady=(10,5))
        self.password_entry = ctk.CTkEntry(container, placeholder_text="Enter password", show="*")
        self.password_entry.pack(pady=5, padx=20, fill="x")

        ctk.CTkButton(container, text="Login", command=self.login).pack(pady=15, padx=20, fill="x")
        ctk.CTkButton(container, text="Sign Up").pack(pady=5, padx=20, fill="x")

    def login(self):
        # Show sidebar and go to dashboard
        self.controller.sidebar.pack(side="left", fill="y")
        self.controller.show_page("DashboardPage")
