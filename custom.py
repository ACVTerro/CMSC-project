import customtkinter as ctk

from sidebar import Sidebar
from dashboard import DashboardPage
from task import TasksPage
from calendar_page import CalendarPage
from settings import SettingsPage
from login import LoginPage  # new login page

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1000x600")
        self.title("Productivity App")

        # Sidebar created but NOT packed
        self.sidebar = Sidebar(self, self.show_page)

        # Main container
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="right", fill="both", expand=True)

        # Pages dictionary
        self.pages = {}

        for Page in (LoginPage, DashboardPage, TasksPage, CalendarPage, SettingsPage):
            page = Page(self.container, self)
            self.pages[Page.__name__] = page
            page.place(relwidth=1, relheight=1)

        # Show login first
        self.show_page("LoginPage")

    def show_page(self, page_name):
        self.pages[page_name].lift()


if __name__ == "__main__":
    app = App()
    app.mainloop()