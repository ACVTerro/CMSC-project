import customtkinter as ctk
from datetime import datetime

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color="#E4D6E7")
        self.controller = controller

        # ===== Header =====
        header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#8EAABD")
        header_frame.pack(side="top", fill="x")
        header_frame.configure(height=80)

        header_label = ctk.CTkLabel(
            header_frame,
            text="📊 Dashboard",
            font=("Arial", 28, "bold"),
            text_color="white"
        )
        header_label.place(relx=0.05, rely=0.5, anchor="w")

        # ===== Summary Row =====
        top_row = ctk.CTkFrame(self, fg_color="transparent")
        top_row.pack(pady=10, padx=20, fill="x")

        card_container = ctk.CTkFrame(top_row, fg_color="transparent")
        card_container.pack(side="left")

        # ===== TOTAL TASKS CARD =====
        total_card = ctk.CTkFrame(card_container, fg_color="#DDE6ED", corner_radius=10)
        total_card.grid(row=0, column=0, padx=10, pady=10)

        self.total_tasks_label = ctk.CTkLabel(
            total_card,
            text="",
            font=("Arial", 16, "bold"),
            text_color="#3E5C6B"
        )
        self.total_tasks_label.pack(padx=15, pady=10)

        # ===== COMPLETED TASKS CARD =====
        completed_card = ctk.CTkFrame(card_container, fg_color="#DDE6ED", corner_radius=10)
        completed_card.grid(row=0, column=1, padx=10, pady=10)

        self.completed_tasks_label = ctk.CTkLabel(
            completed_card,
            text="",
            font=("Arial", 16, "bold"),
            text_color="#3E5C6B"
        )
        self.completed_tasks_label.pack(padx=15, pady=10)

        # ===== MISSED TASKS CARD =====
        missed_card = ctk.CTkFrame(card_container, fg_color="#DDE6ED", corner_radius=10)
        missed_card.grid(row=0, column=2, padx=10, pady=10)

        self.missed_tasks_label = ctk.CTkLabel(
            missed_card,
            text="",
            font=("Arial", 16, "bold"),
            text_color="#3E5C6B"
        )
        self.missed_tasks_label.pack(padx=15, pady=10)

        # ===== PENDING TASKS CARD =====
        pending_card = ctk.CTkFrame(card_container, fg_color="#DDE6ED", corner_radius=10)
        pending_card.grid(row=0, column=3, padx=10, pady=10)

        self.pending_tasks_label = ctk.CTkLabel(
            pending_card,
            text="",
            font=("Arial", 16, "bold"),
            text_color="#3E5C6B"
        )
        self.pending_tasks_label.pack(padx=15, pady=10)

        # ===== Dropdown =====
        dropdown_frame = ctk.CTkFrame(top_row, fg_color="transparent")
        dropdown_frame.pack(side="right")

        self.table_type_var = ctk.StringVar(value="Completed Tasks")

        table_dropdown = ctk.CTkOptionMenu(
            dropdown_frame,
            values=["Completed Tasks", "Missed Tasks"],
            variable=self.table_type_var,
            command=lambda _: self.update_table()
        )
        table_dropdown.pack()

        # ===== Table container =====
        self.table_container = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        self.table_container.pack(fill="both", expand=True, padx=20, pady=10)

        self.header_frame = ctk.CTkFrame(self.table_container, fg_color="#97A7B2")
        self.header_frame.pack(fill="x")

        self.headers = ["Task", "Status", "Due Date", "Subject", "Grade", "Action"]
        self.column_widths = [300, 100, 100, 150, 80, 100]

        for col, text in enumerate(self.headers):
            label = ctk.CTkLabel(
                self.header_frame,
                text=text,
                font=("Arial", 16, "bold"),
                fg_color="transparent",
                text_color="white",
                wraplength=self.column_widths[col] - 10,
                justify="center",
                anchor="center"
            )
            label.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)
            self.header_frame.grid_columnconfigure(col, minsize=self.column_widths[col], weight=1)

        self.scroll_frame = ctk.CTkScrollableFrame(self.table_container, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True)

        self.update_labels()
        self.update_table()

    # ===== Update Labels =====
    def update_labels(self):
        tasks = getattr(self.controller, "tasks", [])

        total = len(tasks)
        completed = len([t for t in tasks if t[5] == "Completed"])
        missed = len([t for t in tasks if t[5] == "Missed"])
        pending = len([t for t in tasks if t[5] == "Pending"])

        self.total_tasks_label.configure(text=f"Total Tasks: {total}")
        self.completed_tasks_label.configure(text=f"Completed: {completed}")
        self.missed_tasks_label.configure(text=f"Missed: {missed}")
        self.pending_tasks_label.configure(text=f"Pending: {pending}")

    # ===== Update Table =====
    def update_table(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        tasks = getattr(self.controller, "tasks", [])

        if self.table_type_var.get() == "Completed Tasks":
            display_tasks = [t for t in tasks if t[5] == "Completed"]
        else:
            display_tasks = [t for t in tasks if t[5] == "Missed"]

        for row_idx, task in enumerate(display_tasks):
            row_color = "#556571" if row_idx % 2 == 0 else "#758D9E"
            row_frame = ctk.CTkFrame(self.scroll_frame, fg_color=row_color)
            row_frame.pack(fill="x", padx=0, pady=1)

            for col_idx in range(len(self.headers)):
                if self.headers[col_idx] == "Action":
                    if task[5] == "Completed":
                        action_btn = ctk.CTkButton(
                            row_frame,
                            text="🗑 Delete",
                            width=80,
                            fg_color="red",
                            hover_color="#D20404",
                            text_color="white",
                            command=lambda t=task: self.delete_task(t)
                        )
                    else:
                        action_btn = ctk.CTkButton(
                            row_frame,
                            text="✅ Complete",
                            width=80,
                            fg_color="#356BFF",
                            hover_color="#1E4CAF",
                            text_color="white",
                            command=lambda t=task: self.complete_task(t)
                        )

                    action_btn.grid(row=0, column=col_idx, padx=5, pady=5)
                    row_frame.grid_columnconfigure(col_idx, minsize=self.column_widths[col_idx], weight=1)
                    continue

                value = task[5] if self.headers[col_idx] == "Status" else task[col_idx]

                label = ctk.CTkLabel(
                    row_frame,
                    text=str(value),
                    fg_color=row_color,
                    wraplength=self.column_widths[col_idx] - 10,
                    justify="center",
                    anchor="center"
                )
                label.grid(row=0, column=col_idx, sticky="nsew", padx=1, pady=1)
                row_frame.grid_columnconfigure(col_idx, minsize=self.column_widths[col_idx], weight=1)

    # ===== Actions =====
    def complete_task(self, task):
        task[5] = "Completed"
        self.update_labels()
        self.update_table()

    def delete_task(self, task):
        if task in self.controller.tasks:
            self.controller.tasks.remove(task)
        self.update_labels()
        self.update_table()