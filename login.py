import customtkinter as ctk
from PIL import Image, ImageFilter


class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        if not hasattr(self.controller, "users"):
            self.controller.users = {}

        self.signup_window = None

        # ---------------- LOAD & BLUR BACKGROUND ----------------
        bg = Image.open("bg.jpg")
        self.blur_bg = bg.filter(ImageFilter.GaussianBlur(10))

        # ---------------- BACKGROUND LABEL ----------------
        self.bg_label = ctk.CTkLabel(self, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # update background whenever window resizes
        self.bind("<Configure>", self.resize_background)

        # ---------------- LOGIN CARD ----------------
        card = ctk.CTkFrame(
            self,
            width=340,
            height=270,
            fg_color="#FFFFFF",
            border_width=0
        )

        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        # ---------------- TITLE ----------------
        ctk.CTkLabel(
            card,
            text="Login",
            font=("Arial", 28, "bold"),
            text_color="#17313E"
        ).pack(pady=(20, 10))

        # ---------------- USERNAME ----------------
        self.username_entry = ctk.CTkEntry(
            card,
            placeholder_text="Username",
            height=35
        )
        self.username_entry.pack(pady=8, padx=30, fill="x")

        # ---------------- PASSWORD ----------------
        self.password_entry = ctk.CTkEntry(
            card,
            placeholder_text="Password",
            show="*",
            height=35
        )
        self.password_entry.pack(pady=8, padx=30, fill="x")

        # ---------------- LOGIN BUTTON ----------------
        ctk.CTkButton(
            card,
            text="Login",
            height=35,
            command=self.login
        ).pack(pady=(15, 5), padx=30, fill="x")

        # ---------------- SIGN UP BUTTON ----------------
        ctk.CTkButton(
            card,
            text="Sign Up",
            height=35,
            
            border_width=1,
            command=self.open_signup_window
        ).pack(pady=5, padx=30, fill="x")

    # ---------------- RESIZE BACKGROUND ----------------
    def resize_background(self, event):
        resized = self.blur_bg.resize((event.width, event.height))
        self.bg_image = ctk.CTkImage(resized, size=(event.width, event.height))
        self.bg_label.configure(image=self.bg_image)

    # ---------------- LOGIN FUNCTION ----------------
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.controller.users and self.controller.users[username] == password:
            print("Login successful")

            if hasattr(self.controller, "sidebar"):
                self.controller.sidebar.pack(side="left", fill="y")

            if hasattr(self.controller, "show_page"):
                self.controller.show_page("DashboardPage")

        else:
            print("Invalid username or password")

    # ---------------- SIGN UP WINDOW ----------------
    def open_signup_window(self):

        if self.signup_window is not None and self.signup_window.winfo_exists():
            self.signup_window.focus()
            return

        self.signup_window = ctk.CTkToplevel(self)
        self.signup_window.geometry("320x220")
        self.signup_window.title("Sign Up")

        ctk.CTkLabel(
            self.signup_window,
            text="Create Account",
            font=("Arial", 20)
        ).pack(pady=15)

        username_entry = ctk.CTkEntry(
            self.signup_window,
            placeholder_text="Username"
        )
        username_entry.pack(padx=20, pady=8, fill="x")

        password_entry = ctk.CTkEntry(
            self.signup_window,
            placeholder_text="Password",
            show="*"
        )
        password_entry.pack(padx=20, pady=8, fill="x")

        def create_account():
            username = username_entry.get()
            password = password_entry.get()

            if username in self.controller.users:
                print("User already exists")
            else:
                self.controller.users[username] = password
                print("Account created")

                self.signup_window.destroy()
                self.signup_window = None

        ctk.CTkButton(
            self.signup_window,
            text="Create Account",
            command=create_account
        ).pack(pady=15)