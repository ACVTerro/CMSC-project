import customtkinter as ctk
from matplotlib import container
from matplotlib import container

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#CDC6CE")
        self.controller = controller

        # Centering container
        container = ctk.CTkFrame(self, fg_color="#E4D6E7", width=400, height=300, corner_radius=10)
        container.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(container, text="Login", font=("Arial", 28), text_color="#17313E").pack(pady=20)

        ctk.CTkLabel(container, text="Username", text_color="#3E5C6B").pack(pady=(10,5))
        self.username_entry = ctk.CTkEntry(container, fg_color="#E7E7E7", border_width=0.4, border_color="#8394A0", placeholder_text="Enter username", text_color="#8394A0")
        self.username_entry.pack(pady=5, padx=20, fill="x")

        ctk.CTkLabel(container, text="Password", text_color="#3E5C6B").pack(pady=(10,5))
        self.password_entry = ctk.CTkEntry(container, fg_color="#E7E7E7", border_width=0.4, border_color="#8394A0", placeholder_text="Enter password", text_color="#8394A0", show="*")
        self.password_entry.pack(pady=5, padx=20, fill="x")

        ctk.CTkButton(container, fg_color="#F8EAFA", hover_color="#97A7B2", text="Login", text_color="#3E5C6B", command=self.login).pack(pady=15, padx=20, fill="x")
        ctk.CTkButton(container, fg_color="#F8EAFA", hover_color="#97A7B2", text="Sign Up", text_color="#3E5C6B").pack(pady=5, padx=20, fill="x")

    def login(self):
        # Show sidebar and go to dashboard
        self.controller.sidebar.pack(side="left", fill="y")
        self.controller.show_page("DashboardPage")
