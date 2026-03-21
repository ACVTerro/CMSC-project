import customtkinter as ctk

class DashboardPage(ctk.CTkFrame):

    def __init__(self, parent, controller=None):
        super().__init__(parent,fg_color="violet")

        # Full-width header frame
        header_frame = ctk.CTkFrame(
            self,
            corner_radius=0,          # straight edges for full width
            fg_color="#1E90FF"        # blue header background
        )
        header_frame.pack(side="top", fill="x")  # fills entire top width

        # Give it a fixed height
        header_frame.configure(height=80)

        # Header label centered in the frame
        header_label = ctk.CTkLabel(
            header_frame,
            text="📊 Dashboard",
            font=("Arial", 28, "bold"),
            text_color="white"
        )
        header_label.place(relx=0.05, rely=0.5, anchor="w")  # center in frame

        card_container = ctk.CTkFrame(self)
        card_container.pack(pady=10, padx=20, fill="both", expand=True)

        # Make a grid layout with 2 columns for cards
        card_container.grid_rowconfigure(0, weight=1)
        card_container.grid_rowconfigure(1, weight=1)
        card_container.grid_columnconfigure(0, weight=1)
        card_container.grid_columnconfigure(1, weight=1)

        # Example Card 1: Tasks Today
        card1 = ctk.CTkFrame(card_container, corner_radius=10)
        card1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(card1, text="Tasks Today", font=("Arial", 20)).pack(pady=20)
        ctk.CTkLabel(card1, text="You have 5 tasks pending").pack(pady=5)

        # Example Card 2: Calendar Reminder
        card2 = ctk.CTkFrame(card_container, corner_radius=10)
        card2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(card2, text="Upcoming Event", font=("Arial", 20)).pack(pady=20)
        ctk.CTkLabel(card2, text="Team meeting at 3 PM").pack(pady=5)

        # Example Card 3: Stats
        card3 = ctk.CTkFrame(card_container, corner_radius=10)
        card3.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(card3, text="Statistics", font=("Arial", 20)).pack(pady=20)
        ctk.CTkLabel(card3, text="Completed: 10 / 15 tasks").pack(pady=5)

        # Example Card 4: Notes
        card4 = ctk.CTkFrame(card_container, corner_radius=10)
        card4.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(card4, text="Quick Notes", font=("Arial", 20)).pack(pady=20)
        ctk.CTkLabel(card4, text="Remember to submit the report").pack(pady=5)