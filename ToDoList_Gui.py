import tkinter as tk
from tkinter import ttk
import sqlite3
import csv
import json
from tkinter import filedialog
from tkinter import messagebox

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Management App")

        # Dark theme colors
        self.dark_background_color = "#CDE8E6"
        self.dark_foreground_color = "black"

        # Database
        self.conn = sqlite3.connect("tasks.db")
        self.create_table()

        # UI Components
        self.root.configure(bg=self.dark_background_color)

        self.title_label = tk.Label(root, text="To-Do List", bg=self.dark_background_color, fg=self.dark_foreground_color)
        self.title_label.pack(pady=10)

        self.task_frame = tk.Frame(root, bg=self.dark_background_color)
        self.task_frame.pack()

        self.task_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Not Started")
        self.deadline_var = tk.StringVar()

        self.task_entry = tk.Entry(self.task_frame, textvariable=self.task_var, width=30, bg=self.dark_background_color, fg=self.dark_foreground_color)
        self.status_dropdown = ttk.Combobox(self.task_frame, textvariable=self.status_var, values=["Completed", "Not Started", "In Progress"], style="Dark.TCombobox")
        self.deadline_entry = tk.Entry(self.task_frame, textvariable=self.deadline_var, width=30, bg=self.dark_background_color, fg=self.dark_foreground_color)

        self.task_label = tk.Label(self.task_frame, text="Task:", bg=self.dark_background_color, fg=self.dark_foreground_color)
        self.status_label = tk.Label(self.task_frame, text="Status:", bg=self.dark_background_color, fg=self.dark_foreground_color)
        self.deadline_label = tk.Label(self.task_frame, text="Deadline (YYYY-MM-DD):", bg=self.dark_background_color, fg=self.dark_foreground_color)

        self.task_label.grid(row=0, column=0, padx=10, pady=5)
        self.task_entry.grid(row=0, column=1, padx=10, pady=5)
        self.status_label.grid(row=1, column=0, padx=10, pady=5)
        self.status_dropdown.grid(row=1, column=1, padx=10, pady=5)
        self.deadline_label.grid(row=2, column=0, padx=10, pady=5)
        self.deadline_entry.grid(row=2, column=1, padx=10, pady=5)

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task, fg="black", bg=self.dark_background_color)
        self.add_button.pack(pady=10)


        # Set the style for Combobox and Treeview
        self.style = ttk.Style()
        self.style.configure("Dark.TCombobox", background=self.dark_background_color, foreground=self.dark_foreground_color)
        self.style.configure("Dark.Treeview.Heading", background=self.dark_background_color, foreground=self.dark_foreground_color)
        self.style.configure("Dark.Treeview", background=self.dark_background_color, foreground=self.dark_foreground_color, fieldbackground=self.dark_background_color)

        self.tree = ttk.Treeview(root, columns=("Task", "Status", "Deadline"), show="headings", selectmode="browse", style="Dark.Treeview")
        self.tree.heading("Task", text="Task", anchor=tk.W)
        self.tree.heading("Status", text="Status", anchor=tk.W)
        self.tree.heading("Deadline", text="Deadline", anchor=tk.W)
        self.tree.column("Task", anchor=tk.W, width=200)
        self.tree.column("Status", anchor=tk.W, width=200)
        self.tree.column("Deadline", anchor=tk.W, width=200)
        self.tree.pack(padx = 10, pady=10)


        self.edit_button = tk.Button(root, text="Edit Task", command=self.edit_task, fg="black", bg=self.dark_background_color)
        self.edit_button.pack(pady=5)

        self.update_button = tk.Button(root, text="Update Task", command=self.update_task, fg="black", bg=self.dark_background_color)
        self.update_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task, fg="black", bg=self.dark_background_color)
        self.delete_button.pack(pady=5)

        self.clear_button = tk.Button(root, text="Clear All", command=self.clear_all, fg="black", bg=self.dark_background_color)
        self.clear_button.pack(pady=5)
        
        self.import_csv_button = tk.Button(root, text="Import from CSV", command=self.import_from_csv, fg="black", bg=self.dark_background_color)
        self.import_csv_button.pack(pady=5)

        self.export_csv_button = tk.Button(root, text="Export to CSV", command=self.export_to_csv, fg="black", bg=self.dark_background_color)
        self.export_csv_button.pack(pady=5, padx=5, side=tk.RIGHT)

        self.export_json_button = tk.Button(root, text="Export to JSON", command=self.export_to_json, fg="black", bg=self.dark_background_color)
        self.export_json_button.pack(pady=5, padx=5, side=tk.LEFT)


        # Populate tree with initial data
        self.populate_tree()

    def add_task(self):
        task = self.task_var.get()
        status = self.status_var.get()
        deadline = self.deadline_var.get()

        if task:
            self.insert_task(task, status, deadline)
            self.populate_tree()
            self.clear_task_entry()
            messagebox.showinfo('Success', 'Data has been added')

    def edit_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            task_id = self.tree.item(selected_item, "tags")[0]
            task = self.get_task_by_id(task_id)
            if task:
                self.task_var.set(task[1])
                self.status_var.set(task[2])
                self.deadline_var.set(task[3])

    def update_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            task_id = self.tree.item(selected_item, "tags")[0]
            new_task = self.task_var.get()
            new_status = self.status_var.get()
            new_deadline = self.deadline_var.get()
            self.update_task_in_db(task_id, new_task, new_status, new_deadline)
            self.populate_tree()
            self.clear_task_entry()
            messagebox.showinfo('Success', 'Data has been updated')

    def delete_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            task_id = self.tree.item(selected_item, "tags")[0]
            self.delete_task_in_db(task_id)
            self.populate_tree()
            self.clear_task_entry()
            messagebox.showinfo('Success', 'Data has been deleted')

    def clear_all(self):
        self.delete_all_tasks()
        self.populate_tree()
        self.clear_task_entry()
        messagebox.showinfo('Success', 'All Data has been cleared')

    def clear_task_entry(self):
        self.task_var.set("")
        self.status_var.set("Not Started")
        self.deadline_var.set("")

    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            tasks = self.get_all_tasks()
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Task", "Status", "Deadline"])
                writer.writerows(tasks)

    def import_from_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                tasks_to_import = [row[1:] for row in reader]
                self.insert_tasks(tasks_to_import)
                self.populate_tree()

    def export_to_json(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            tasks = self.get_all_tasks()
            with open(file_path, 'w') as file:
                json.dump(tasks, file)

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT,
                status TEXT,
                deadline TEXT
            )
        ''')
        self.conn.commit()

    def insert_task(self, task, status, deadline):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (task, status, deadline)
            VALUES (?, ?, ?)
        ''', (task, status, deadline))
        self.conn.commit()

    def insert_tasks(self, tasks):
        cursor = self.conn.cursor()
        cursor.executemany('''
            INSERT INTO tasks (task, status, deadline)
            VALUES (?, ?, ?)
        ''', tasks)
        self.conn.commit()

    def get_all_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM tasks')
        return cursor.fetchall()

    def get_task_by_id(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        return cursor.fetchone()

    def update_task_in_db(self, task_id, new_task, new_status, new_deadline):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE tasks
            SET task = ?, status = ?, deadline = ?
            WHERE id = ?
        ''', (new_task, new_status, new_deadline, task_id))
        self.conn.commit()

    def delete_task_in_db(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.conn.commit()

    def delete_all_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM tasks')
        self.conn.commit()

    def load_data(self):
        # Load initial data or perform database connection here
        # For simplicity, using static data
        self.insert_tasks([
            ("Task1", "Not Started", "2024-01-20"),
            ("Task2", "Completed", "2024-01-22"),
            ("Task3", "In Progress", "2024-01-25")
        ])

    def populate_tree(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Populate tree with current data
        tasks = self.get_all_tasks()
        for task in tasks:
            self.tree.insert("", "end", values=task[1:], tags=(task[0],))



