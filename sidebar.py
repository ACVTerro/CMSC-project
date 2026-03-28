import customtkinter as ctk


class Sidebar(ctk.CTkFrame):

    def __init__(self, parent, show_page):
        super().__init__(parent, width=200, fg_color="#CDC6CE")

        ctk.CTkLabel(self, text="My App", font=("Arial", 22), text_color="#3E5C6B").pack(pady=20)

        ctk.CTkButton(
            self, fg_color="#F8EAFA", hover_color="#97A7B2", text="Dashboard", text_color="#3E5C6B",
            command=lambda: show_page("DashboardPage")
        ).pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(
            self, fg_color="#F8EAFA", hover_color="#97A7B2", text="Tasks", text_color="#3E5C6B",
            command=lambda: show_page("TasksPage")
        ).pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(
            self, fg_color="#F8EAFA", hover_color="#97A7B2", text="Calendar", text_color="#3E5C6B",
            command=lambda: show_page("CalendarPage")
        ).pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(
            self, fg_color="#F8EAFA", hover_color="#97A7B2", text="Settings", text_color="#3E5C6B",
            command=lambda: show_page("SettingsPage")
        ).pack(pady=10, padx=20, fill="x")

         # Spacer
        self.pack_propagate(False)
        spacer = ctk.CTkFrame(self, fg_color="transparent")
        spacer.pack(expand=True, fill="both")

        # Logout button with confirmation
        ctk.CTkButton(self, fg_color="#F8EAFA", hover_color="#97A7B2", text="Logout", command=lambda: self.confirm_logout(show_page), text_color="#3E5C6B").pack(pady=20, padx=20, fill="x")

    def confirm_logout(self, show_page):
        """Show confirmation popup before logging out."""
        popup = ctk.CTkToplevel(self, fg_color="#CDC6CE")
        popup.title("Confirm Logout")
        popup.geometry("400x150")
        popup.grab_set()  # Make popup modal

        ctk.CTkLabel(popup, text_color="#3E5C6B", text="Are you sure you want to logout?", font=("Arial", 14)).pack(pady=20, padx=10)

        # Buttons frame
        btn_frame = ctk.CTkFrame(popup, fg_color="transparent")
        btn_frame.pack(pady=10, fill="x", expand=True)

        # Yes button
        def do_logout():
            show_page("LoginPage")   # switch page
            self.pack_forget()       # hide sidebar
            popup.destroy()          # close popup

        ctk.CTkButton(btn_frame, fg_color="#F8EAFA", hover_color="#97A7B2", text="Yes", text_color="#3E5C6B", command=do_logout).pack(side="left", padx=20, expand=True)
        # No button
        ctk.CTkButton(btn_frame, fg_color="#F8EAFA", hover_color="#97A7B2", text="No", text_color="#3E5C6B", command=popup.destroy).pack(side="right", padx=20, expand=True)