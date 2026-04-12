import customtkinter as ctk
from sidebar import Sidebar
from dashboard import DashboardPage
from task import TasksPage
from calendar_page import CalendarPage
from settings import SettingsPage
from login import LoginPage  # Login page first

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1080x600")
        self.title("Productivity App")

        # Sidebar (optional)
        self.sidebar = Sidebar(self, self.show_page)

        # Main container
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="right", fill="both", expand=True)

        # Shared tasks list
        self.tasks = []  # Used by Dashboard & Tasks

        # Pages dictionary
        self.pages = {}

        for Page in (LoginPage, DashboardPage, TasksPage, CalendarPage, SettingsPage):
            page = Page(self.container, self)  # pass controller
            self.pages[Page.__name__] = page
            page.place(relwidth=1, relheight=1)

        # Show login first
        self.show_page("LoginPage")

    def show_page(self, page_name):
        page = self.pages.get(page_name)
        if page:
            page.lift()
            # Update dashboard if switching to it
            if page_name == "DashboardPage":
                page.update_labels()
                page.update_table()


if __name__ == "__main__":
    app = App()
    app.mainloop()