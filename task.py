import customtkinter as ctk
import tkcalendar
from datetime import datetime
import random

class TasksPage(ctk.CTkFrame):
    PRIORITY_COLORS = {"High": "#FF4C4C", "Medium": "#FFA500", "Low": "#32CD32"}
    PRIORITY_ORDER = {"High": 1, "Medium": 2, "Low": 3}

    def __init__(self, parent, app=None):
        super().__init__(parent, fg_color="violet")
        self.app = app
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # ===== Header =====
        self.headers = ["Task", "Priority", "Due Date", "Subject", "Grade", "Actions"]
        self.column_widths = [300, 100, 100, 150, 80, 100]

        header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1E90FF")
        header_frame.pack(side="top", fill="x")
        header_frame.configure(height=80)

        header_label = ctk.CTkLabel(
            header_frame, text="📊 Tasks", font=("Arial", 28, "bold"), text_color="white"
        )
        header_label.place(relx=0.05, rely=0.5, anchor="w")

        create_task_btn = ctk.CTkButton(header_frame, text="Create Task", command=self.open_create_task_popup)
        create_task_btn.place(relx=0.95, rely=0.5, anchor="e")

        # ===== Algorithm Selection =====
        algo_frame = ctk.CTkFrame(self, fg_color="violet")
        algo_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(algo_frame, text="Choose Algorithm:").pack(side="left", padx=10)
        self.algo_var = ctk.StringVar(value="Greedy")
        algo_dropdown = ctk.CTkOptionMenu(algo_frame, values=["Greedy", "Insertion", "Bubble"], variable=self.algo_var)
        algo_dropdown.pack(side="left", padx=5)
        ctk.CTkButton(algo_frame, text="Randomize Tasks", command=self.randomize_tasks).pack(side="right", padx=10)
        ctk.CTkButton(algo_frame, text="Sort", command=self.sort_and_display).pack(side="right", padx=10)

        # ===== Table Container =====
        self.table_container = ctk.CTkFrame(self, fg_color="green", corner_radius=15)
        self.table_container.pack(fill="both", expand=True)

        # Header row
        self.header_frame = ctk.CTkFrame(self.table_container, fg_color="red")
        self.header_frame.pack(fill="x")
        for col, text in enumerate(self.headers):
            label = ctk.CTkLabel(
                self.header_frame,
                text=text,
                font=("Arial", 16, "bold"),
                fg_color="blue",
                corner_radius=10,
                text_color="white",
                wraplength=self.column_widths[col]-10,
                justify="center",
                anchor="center"
            )
            label.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)
            self.header_frame.grid_columnconfigure(col, minsize=self.column_widths[col], weight=1)

        # Scrollable rows
        self.scroll_frame = ctk.CTkScrollableFrame(self.table_container, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True)

        # Sample tasks
        self.tasks = [
            ["Finish Homework with a very long description that might overflow", "High", "2026-03-20", "Math", 100],
            ["Study Quiz chapters 5-7", "Medium", "2026-03-22", "Science", 85],
            ["Prepare slides with references", "High", "2026-03-25", "History", 90],
            ["Essay Draft", "Low", "2026-03-28", "English", 80],
        ]
        self.sort_and_display()

    # ===== Row Rendering =====
    def create_rows(self, tasks):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        for row_idx, task in enumerate(tasks):
            row_color = "#433DFA" if row_idx % 2 == 0 else "#7576FF"
            row_frame = ctk.CTkFrame(self.scroll_frame, fg_color=row_color)
            row_frame.pack(fill="x", padx=0, pady=1)

            for col_idx in range(len(self.headers)):

                if self.headers[col_idx] == "Actions":
                    action_btn = ctk.CTkButton(
                        row_frame,
                        text="⚙",
                        width=40,
                        command=lambda t=task: self.open_task_actions(t)
                    )
                    action_btn.grid(row=0, column=col_idx, padx=5, pady=5)
                    row_frame.grid_columnconfigure(col_idx, minsize=self.column_widths[col_idx], weight=1)
                    continue

                value = task[col_idx]
                fg_color = row_color
                due_date_obj = datetime.strptime(task[2], "%Y-%m-%d")
                overdue = due_date_obj < datetime.today()

                # Priority column: show "Missed" if overdue
                if self.headers[col_idx] == "Priority":
                    if overdue:
                        value = "Missed"
                        fg_color = "#808080"
                    else:
                        fg_color = self.PRIORITY_COLORS.get(value, row_color)

                # Due Date column: grey if overdue
                if self.headers[col_idx] == "Due Date" and overdue:
                    fg_color = "#808080"

                wraplength = self.column_widths[col_idx]-10
                label = ctk.CTkLabel(
                    row_frame,
                    text=str(value),
                    fg_color=fg_color,
                    wraplength=wraplength,
                    justify="center",
                    anchor="center"
                )
                label.grid(row=0, column=col_idx, sticky="nsew", padx=1, pady=1)
                row_frame.grid_columnconfigure(col_idx, minsize=self.column_widths[col_idx], weight=1)

    # ===== Create Task Popup =====
    def open_create_task_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Create Task")
        popup.geometry("400x500")
        popup.grab_set()

        ctk.CTkLabel(popup, text="Task").pack(pady=(20,5))
        task_entry = ctk.CTkEntry(popup, width=350)
        task_entry.pack()

        ctk.CTkLabel(popup, text="Priority").pack(pady=(10,5))
        priority_var = ctk.StringVar(value="Medium")
        priority_dropdown = ctk.CTkOptionMenu(popup, values=["High","Medium","Low"], variable=priority_var, width=350)
        priority_dropdown.pack()

        ctk.CTkLabel(popup, text="Due Date").pack(pady=(10,5))
        due_date_entry = tkcalendar.DateEntry(popup, width=12, date_pattern='yyyy-mm-dd')
        due_date_entry.pack()

        ctk.CTkLabel(popup, text="Subject").pack(pady=(10,5))
        subject_entry = ctk.CTkEntry(popup, width=350)
        subject_entry.pack()

        ctk.CTkLabel(popup, text="Grade").pack(pady=(10,5))
        grade_entry = ctk.CTkEntry(popup, width=350)
        grade_entry.pack()

        def add_task():
            try:
                grade = int(grade_entry.get())
            except:
                grade = 0
            new_task = [
                task_entry.get(),
                priority_var.get(),
                due_date_entry.get_date().strftime("%Y-%m-%d"),
                subject_entry.get(),
                grade
            ]
            self.tasks.append(new_task)
            self.sort_and_display()
            popup.destroy()

        ctk.CTkButton(popup, text="Add Task", command=add_task).pack(pady=20)

    # ===== Task Actions Popup =====
    def open_task_actions(self, task):
        popup = ctk.CTkToplevel(self)
        popup.title("Task Options")
        popup.geometry("300x250")
        popup.grab_set()

        ctk.CTkLabel(popup, text="Task Options", font=("Arial",18,"bold")).pack(pady=15)

        def complete_task():
            self.tasks.remove(task)
            self.sort_and_display()
            popup.destroy()

        ctk.CTkButton(popup, text="✅ Mark Complete", command=complete_task).pack(pady=10)
        ctk.CTkButton(popup, text="✏ Edit Task", command=lambda: [popup.destroy(), self.open_edit_task_popup(task)]).pack(pady=10)

        def delete_task():
            self.tasks.remove(task)
            self.sort_and_display()
            popup.destroy()

        ctk.CTkButton(popup, text="🗑 Delete Task", fg_color="red", command=delete_task).pack(pady=10)

    # ===== Edit Task Popup =====
    def open_edit_task_popup(self, task):
        popup = ctk.CTkToplevel(self)
        popup.title("Edit Task")
        popup.geometry("400x500")
        popup.grab_set()

        ctk.CTkLabel(popup, text="Task").pack(pady=(20,5))
        task_entry = ctk.CTkEntry(popup, width=350)
        task_entry.insert(0, task[0])
        task_entry.pack()

        ctk.CTkLabel(popup, text="Priority").pack(pady=(10,5))
        priority_var = ctk.StringVar(value=task[1])
        priority_dropdown = ctk.CTkOptionMenu(popup, values=["High","Medium","Low"], variable=priority_var)
        priority_dropdown.pack()

        ctk.CTkLabel(popup, text="Subject").pack(pady=(10,5))
        subject_entry = ctk.CTkEntry(popup, width=350)
        subject_entry.insert(0, task[3])
        subject_entry.pack()

        ctk.CTkLabel(popup, text="Grade").pack(pady=(10,5))
        grade_entry = ctk.CTkEntry(popup, width=350)
        grade_entry.insert(0, str(task[4]))
        grade_entry.pack()

        def save_changes():
            task[0] = task_entry.get()
            task[1] = priority_var.get()
            task[3] = subject_entry.get()
            try:
                task[4] = int(grade_entry.get())
            except:
                task[4] = 0
            self.sort_and_display()
            popup.destroy()

        ctk.CTkButton(popup, text="Save Changes", command=save_changes).pack(pady=20)

    # ===== Randomizer =====
    def randomize_tasks(self):
        if len(self.tasks) > 1:
            random.shuffle(self.tasks)
            self.create_rows(self.tasks)

    # ===== Sorting =====
    def sort_and_display(self):
        algo = self.algo_var.get()
        today = datetime.today()
        if algo == "Greedy":
            self.tasks.sort(key=lambda t: (
                0 if datetime.strptime(t[2], "%Y-%m-%d") < today else 1,  # overdue first
                self.PRIORITY_ORDER.get(t[1], 4),  # default lower priority if missing
                datetime.strptime(t[2], "%Y-%m-%d"),
                -t[4]
            ))
        elif algo == "Insertion":
            self.tasks = self.insertion_sort(self.tasks)
        elif algo == "Bubble":
            self.tasks = self.bubble_sort(self.tasks)
        self.create_rows(self.tasks)

    # ===== Insertion Sort =====
    def insertion_sort(self, tasks):
        arr = tasks.copy()
        for i in range(1, len(arr)):
            key = arr[i]
            j = i-1
            while j >= 0 and (
                self.PRIORITY_ORDER.get(arr[j][1],4) > self.PRIORITY_ORDER.get(key[1],4)
                or (arr[j][1] == key[1] and datetime.strptime(arr[j][2], "%Y-%m-%d") > datetime.strptime(key[2], "%Y-%m-%d"))
                or (arr[j][1] == key[1] and arr[j][2] == key[2] and arr[j][4] < key[4])
            ):
                arr[j+1] = arr[j]
                j -= 1
            arr[j+1] = key
        return arr

    # ===== Bubble Sort =====
    def bubble_sort(self, tasks):
        arr = tasks.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                swap = False
                if self.PRIORITY_ORDER.get(arr[j][1],4) > self.PRIORITY_ORDER.get(arr[j+1][1],4):
                    swap = True
                elif arr[j][1] == arr[j+1][1] and datetime.strptime(arr[j][2], "%Y-%m-%d") > datetime.strptime(arr[j+1][2], "%Y-%m-%d"):
                    swap = True
                elif arr[j][1] == arr[j+1][1] and arr[j][2] == arr[j+1][2] and arr[j][4] < arr[j+1][4]:
                    swap = True
                if swap:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr