import customtkinter as ctk


class Sidebar(ctk.CTkFrame):

    def __init__(self, parent, show_page):
        super().__init__(parent, width=200)

        ctk.CTkLabel(self, text="My App", font=("Arial", 22)).pack(pady=20)

        ctk.CTkButton(
            self, text="Dashboard",
            command=lambda: show_page("DashboardPage")
        ).pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(
            self, text="Tasks",
            command=lambda: show_page("TasksPage")
        ).pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(
            self, text="Calendar",
            command=lambda: show_page("CalendarPage")
        ).pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(
            self, text="Settings",
            command=lambda: show_page("SettingsPage")
        ).pack(pady=10, padx=20, fill="x")

         # Spacer
        self.pack_propagate(False)
        spacer = ctk.CTkFrame(self, fg_color="transparent")
        spacer.pack(expand=True, fill="both")

        # Logout button with confirmation
        ctk.CTkButton(self, text="Logout", command=lambda: self.confirm_logout(show_page)).pack(pady=20, padx=20, fill="x")

    def confirm_logout(self, show_page):
        """Show confirmation popup before logging out."""
        popup = ctk.CTkToplevel(self)
        popup.title("Confirm Logout")
        popup.geometry("400x150")
        popup.grab_set()  # Make popup modal

        ctk.CTkLabel(popup, text="Are you sure you want to logout?", font=("Arial", 14)).pack(pady=20, padx=10)

        # Buttons frame
        btn_frame = ctk.CTkFrame(popup, fg_color="transparent")
        btn_frame.pack(pady=10, fill="x", expand=True)

    # Yes button
        def do_logout():
            show_page("LoginPage")   # switch page
            self.pack_forget()       # hide sidebar
            popup.destroy()          # close popup

        ctk.CTkButton(btn_frame, text="Yes", command=do_logout).pack(side="left", padx=20, expand=True)
        # No button
        ctk.CTkButton(btn_frame, text="No", command=popup.destroy).pack(side="right", padx=20, expand=True)