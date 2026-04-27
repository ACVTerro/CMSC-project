"""import customtkinter as ctk
import tkcalendar
from datetime import datetime
import random

class TasksPage(ctk.CTkFrame):
    PRIORITY_COLORS = {"High": "#FF4C4C", "Medium": "#FFA500", "Low": "#32CD32"}
    PRIORITY_ORDER = {"High": 1, "Medium": 2, "Low": 3}

    def __init__(self, parent, app=None):
        super().__init__(parent, fg_color="#E4D6E7")
        self.app = app
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # ===== Header =====
        self.headers = ["Task", "Priority", "Due Date", "Subject", "Grade", "Status", "Actions"]
        self.column_widths = [250, 100, 100, 150, 80, 100, 100]

        header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#8EAABD")
        header_frame.pack(side="top", fill="x")
        header_frame.configure(height=80)

        header_label = ctk.CTkLabel(
            header_frame, text="📊 Tasks", font=("Arial", 28, "bold"), text_color="white"
        )
        header_label.place(relx=0.05, rely=0.5, anchor="w")

        create_task_btn = ctk.CTkButton(
            header_frame,
            text="Create Task",
            command=self.open_create_task_popup,
            fg_color="#536D7F",
            hover_color="#3F5C6B",
            text_color="#FFFFFF"
        )
        create_task_btn.place(relx=0.95, rely=0.5, anchor="e")

        # ===== Algorithm Selection =====
        algo_frame = ctk.CTkFrame(self, fg_color="transparent")
        algo_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(algo_frame, text="Choose Algorithm:", text_color="#17313E").pack(side="left", padx=10)

        self.algo_var = ctk.StringVar(value="Greedy")

        algo_dropdown = ctk.CTkOptionMenu(
            algo_frame,
            fg_color="#536D7F",
            text_color="white",
            values=["Greedy", "Insertion", "Bubble"],
            variable=self.algo_var
        )
        algo_dropdown.pack(side="left", padx=5)

        randomize_btn = ctk.CTkButton(
            algo_frame,
            fg_color="#536D7F",
            hover_color="#3F5C6B",
            text="Randomize Tasks",
            text_color="white",
            command=self.randomize_tasks
        )
        randomize_btn.pack(side="right", padx=10)

        sort_btn = ctk.CTkButton(
            algo_frame,
            fg_color="#536D7F",
            hover_color="#3F5C6B",
            text="Sort",
            text_color="white",
            command=self.sort_and_display
        )
        sort_btn.pack(side="right", padx=10)

        # ===== Table Container =====
        self.table_container = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        self.table_container.pack(fill="both", expand=True)

        self.header_frame = ctk.CTkFrame(self.table_container, fg_color="#97A7B2")
        self.header_frame.pack(fill="x")

        for col, text in enumerate(self.headers):
            label = ctk.CTkLabel(
                self.header_frame,
                text=text,
                font=("Arial", 16, "bold"),
                fg_color="transparent",
                text_color="white",
                wraplength=self.column_widths[col]-10,
                justify="center",
                anchor="center"
            )
            label.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)
            self.header_frame.grid_columnconfigure(col, minsize=self.column_widths[col], weight=1)

        self.scroll_frame = ctk.CTkScrollableFrame(self.table_container, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True)

        self.sort_and_display()

    # ===== Row Rendering =====
    def create_rows(self, tasks):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        today = datetime.today().date()
        display_index = 0

        for task in tasks:
            due_date_obj = datetime.strptime(task[2], "%Y-%m-%d").date()

            # FIXED: consistent status logic
            if task[5] != "Completed":
                task[5] = "Missed" if due_date_obj < today else "Pending"

            if task[5] in ["Missed", "Completed"]:
                continue

            row_color = "#556571" if display_index % 2 == 0 else "#758D9E"
            row_frame = ctk.CTkFrame(self.scroll_frame, fg_color=row_color)
            row_frame.pack(fill="x", padx=0, pady=1)

            for col_idx in range(len(self.headers)):
                if self.headers[col_idx] == "Actions":
                    action_btn = ctk.CTkButton(
                        row_frame,
                        text="⚙",
                        width=40,
                        fg_color="#356BFF",
                        hover_color="#1E4CAF",
                        text_color="#FFFFFF",
                        command=lambda t=task: self.open_task_actions(t)
                    )
                    action_btn.grid(row=0, column=col_idx, padx=5, pady=5)
                    row_frame.grid_columnconfigure(col_idx, minsize=self.column_widths[col_idx], weight=1)
                    continue

                value = task[col_idx] if col_idx < len(task) else ""
                fg_color = row_color

                if self.headers[col_idx] == "Priority":
                    fg_color = self.PRIORITY_COLORS.get(value, row_color)

                label = ctk.CTkLabel(
                    row_frame,
                    text=str(value),
                    fg_color=fg_color,
                    wraplength=self.column_widths[col_idx]-10,
                    justify="center",
                    anchor="center"
                )
                label.grid(row=0, column=col_idx, sticky="nsew", padx=1, pady=1)
                row_frame.grid_columnconfigure(col_idx, minsize=self.column_widths[col_idx], weight=1)

            display_index += 1

    # ===== Create Task Popup =====
    def open_create_task_popup(self):
        popup = ctk.CTkToplevel(self, fg_color="#CDC6CE")
        popup.title("Create Task")
        popup.geometry("400x500")
        popup.grab_set()

        task_entry = self.create_labeled_entry(popup, "Task")
        priority_var = self.create_labeled_dropdown(popup, "Priority", ["High","Medium","Low"], "Medium")
        due_date_entry = self.create_labeled_date(popup, "Due Date")
        subject_entry = self.create_labeled_entry(popup, "Subject")
        grade_entry = self.create_labeled_entry(popup, "Grade")

        def add_task():
            try:
                grade = int(grade_entry.get())
            except:
                grade = 0

            due_date = due_date_entry.get_date()

            # FIXED: always start as Pending
            status = "Pending"

            new_task = [
                task_entry.get(),
                priority_var.get(),
                due_date.strftime("%Y-%m-%d"),
                subject_entry.get(),
                grade,
                status
            ]

            self.app.tasks.append(new_task)
            self.sort_and_display()
            self.update_dashboard()
            popup.destroy()

        ctk.CTkButton(
            popup,
            fg_color="#F8EAFA",
            hover_color="#97A7B2",
            text="Add Task",
            text_color="#3E5C6B",
            command=add_task
        ).pack(pady=20)

    # ===== Task Actions Popup =====
    def open_task_actions(self, task):
        popup = ctk.CTkToplevel(self, fg_color="#CDC6CE")
        popup.title("Task Options")
        popup.geometry("250x175")
        popup.grab_set()

        def complete_task():
            task[5] = "Completed"
            self.sort_and_display()
            self.update_dashboard()
            popup.destroy()

        def delete_task():
            if task in self.app.tasks:
                self.app.tasks.remove(task)
            self.sort_and_display()
            self.update_dashboard()
            popup.destroy()

        ctk.CTkButton(
            popup,
            fg_color="#F8EAFA",
            hover_color="#97A7B2",
            text="✅ Mark Complete",
            text_color="#3E5C6B",
            command=complete_task
        ).pack(pady=10)

        ctk.CTkButton(
            popup,
            fg_color="#F8EAFA",
            hover_color="#97A7B2",
            text="✏ Edit Task",
            text_color="#3E5C6B",
            command=lambda:[popup.destroy(), self.open_edit_task_popup(task)]
        ).pack(pady=10)

        ctk.CTkButton(
            popup,
            fg_color="red",
            hover_color="#D20404",
            text="🗑 Delete Task",
            text_color="white",
            command=delete_task
        ).pack(pady=10)

    # ===== Edit Task Popup =====
    def open_edit_task_popup(self, task):
        popup = ctk.CTkToplevel(self, fg_color="#CDC6CE")
        popup.title("Edit Task")
        popup.geometry("400x550")
        popup.grab_set()

        task_entry = self.create_labeled_entry(popup, "Task", task[0])

        priority_var = self.create_labeled_dropdown(
            popup,
            "Priority",
            ["High","Medium","Low"],
            task[1]
        )

        due_date_entry = self.create_labeled_date(popup, "Due Date")
        due_date_entry.set_date(task[2])

        subject_entry = self.create_labeled_entry(popup, "Subject", task[3])
        grade_entry = self.create_labeled_entry(popup, "Grade", str(task[4]))

        def save_changes():
            task[0] = task_entry.get()
            task[1] = priority_var.get()

            new_due_date = due_date_entry.get_date()
            task[2] = new_due_date.strftime("%Y-%m-%d")

            task[3] = subject_entry.get()

            try:
                task[4] = int(grade_entry.get())
            except:
                task[4] = 0

            # FIXED: consistent logic only
            if task[5] != "Completed":
                task[5] = "Pending"

            self.sort_and_display()
            self.update_dashboard()
            popup.destroy()

        ctk.CTkButton(
            popup,
            fg_color="#F8EAFA",
            hover_color="#97A7B2",
            text="Save Changes",
            text_color="#3E5C6B",
            command=save_changes
        ).pack(pady=20)

    # ===== Sorting =====
    def sort_and_display(self):
        tasks = self.app.tasks
        today = datetime.today().date()
        algo = self.algo_var.get()

        # FIXED: consistent status sync
        for t in tasks:
            if t[5] != "Completed":
                due_date_obj = datetime.strptime(t[2], "%Y-%m-%d").date()
                t[5] = "Missed" if due_date_obj < today else "Pending"

        if algo == "Greedy":
            tasks.sort(key=lambda t: (
                0 if t[5] == "Completed" else 1,
                0 if t[5] == "Missed" else 1,
                self.PRIORITY_ORDER.get(t[1], 4),
                datetime.strptime(t[2], "%Y-%m-%d"),
                -t[4]
            ))

        elif algo == "Insertion":
            tasks = self.insertion_sort(tasks)

        elif algo == "Bubble":
            tasks = self.bubble_sort(tasks)

        self.create_rows(tasks)
        self.update_dashboard()

    # ===== Utility Methods =====
    def create_labeled_entry(self, parent, label_text, default=""):
        ctk.CTkLabel(parent, text=label_text, text_color="#17313E").pack(pady=(10,5))
        entry = ctk.CTkEntry(parent, fg_color="#E7E7E7", border_color="#8394A0", text_color="black", width=350)
        entry.insert(0, default)
        entry.pack()
        return entry

    def create_labeled_dropdown(self, parent, label_text, options, default):
        ctk.CTkLabel(parent, text=label_text, text_color="#17313E").pack(pady=(10,5))
        var = ctk.StringVar(value=default)
        dropdown = ctk.CTkOptionMenu(parent, fg_color="#8394A0", values=options, variable=var)
        dropdown.pack()
        return var

    def create_labeled_date(self, parent, label_text):
        ctk.CTkLabel(parent, text=label_text, text_color="#17313E").pack(pady=(10,5))
        date_entry = tkcalendar.DateEntry(parent, width=12, date_pattern='yyyy-mm-dd')
        date_entry.pack()
        return date_entry

    # ===== Randomize =====
    def randomize_tasks(self):
        if len(self.app.tasks) > 1:
            random.shuffle(self.app.tasks)
            self.create_rows(self.app.tasks)

    # ===== Dashboard Update =====
    def update_dashboard(self):
        if hasattr(self.app, "pages") and "DashboardPage" in self.app.pages:
            dashboard = self.app.pages["DashboardPage"]
            if hasattr(dashboard, "update_labels"):
                dashboard.update_labels()"""