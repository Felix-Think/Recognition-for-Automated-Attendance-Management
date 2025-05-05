import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pymysql
import csv
from datetime import datetime, date
import calendar

class SalaryViewer:
    def __init__(self, root, main_ui):
        self.root = tk.Toplevel(root)
        self.main_ui = main_ui
        self.root.title("Department Salary Report")
        self.root.geometry("1200x650")

        # Database connection
        self.conn = pymysql.connect(
            host="localhost",
            user="root",
            password="5812",
            database="NCKH",
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.conn.cursor()

        self.build_ui()

    def build_ui(self):
        top_frame = tk.Frame(self.root, height=80, bg="#2C3E50")
        top_frame.pack(pady=10, fill='x')

        label_bg = '#FFFACD'  # Light yellowish-white
        entry_bg = '#FFFACD'

        tk.Label(top_frame, text="Department ID:", font=("Arial", 13), bg="#2C3E50", fg="white").grid(row=0, column=0, padx=5, pady=10)
        self.entry_dept_id = tk.Entry(top_frame, font=("Arial", 13), bg=entry_bg)
        self.entry_dept_id.grid(row=0, column=1, padx=5, pady=10)

        tk.Label(top_frame, text="Month:", font=("Arial", 13), bg="#2C3E50", fg="white").grid(row=0, column=2, padx=5, pady=10)
        self.entry_month = tk.Entry(top_frame, width=5, font=("Arial", 13), bg=entry_bg)
        self.entry_month.grid(row=0, column=3, padx=5, pady=10)

        tk.Label(top_frame, text="Year:", font=("Arial", 13), bg="#2C3E50", fg="white").grid(row=0, column=4, padx=5, pady=10)
        self.entry_year = tk.Entry(top_frame, width=7, font=("Arial", 13), bg=entry_bg)
        self.entry_year.grid(row=0, column=5, padx=5, pady=10)

        tk.Button(top_frame, text="View Salary", font=("Arial", 13), command=self.load_salary).grid(row=0, column=6, padx=10, pady=10)
        tk.Button(top_frame, text="Export CSV", font=("Arial", 13), command=self.export_csv).grid(row=0, column=7, padx=10, pady=10)

        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview",
            background="#2C3E50",
            foreground="white",
            rowheight=25,
            fieldbackground="#2C3E50"
        )
        style.map('Treeview', background=[('selected', '#34495E')])
        style.configure("Treeview.Heading", background="cyan", foreground="black")

        self.tree = ttk.Treeview(self.root, show="headings")
        self.tree.pack(fill="both", expand=True, pady=10)

        tk.Button(self.root, text="Back", bg="#E74C3C", fg="white", font=("Arial", 12, "bold"),
                  command=self.go_back).pack(pady=10)

    def load_salary(self):
        dept_id = self.entry_dept_id.get()
        month = self.entry_month.get()
        year = self.entry_year.get()

        if not (dept_id and month and year):
            messagebox.showwarning("Missing Input", "Please fill in Department ID, Month, and Year.")
            return

        try:
            today = date.today()
            current_day = today.day
            current_month = today.month
            current_year = today.year

            num_days = calendar.monthrange(int(year), int(month))[1]
            day_names = [calendar.day_name[calendar.weekday(int(year), int(month), i)] for i in range(1, num_days + 1)]

            query = f"""
                SELECT e.employee_id, e.full_name, e.position,
                {', '.join([f"SUM(CASE WHEN DAY(a.work_date) = {i} THEN a.hours_worked ELSE NULL END) AS '{i}'" for i in range(1, 32)])},
                COUNT(a.work_date) AS 'Total Working Days',
                SUM(CASE WHEN a.hours_worked > 8 THEN a.hours_worked - 8 ELSE 0 END) AS 'Overtime Hours'
                FROM Employees e
                LEFT JOIN Attendance a ON e.employee_id = a.employee_id
                WHERE MONTH(a.work_date) = %s AND YEAR(a.work_date) = %s AND e.department_id = %s
                GROUP BY e.employee_id
            """

            self.cursor.execute(query, (int(month), int(year), dept_id))
            self.results = self.cursor.fetchall()

            self.tree.delete(*self.tree.get_children())
            columns = ["No", "Name", "Position"] + [str(i) for i in range(1, 32)] + ["Total Working Days", "Overtime Hours", "Note"]
            self.tree.config(columns=columns)

            for col in columns:
                if col == "No":
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=60, anchor="center")
                elif col == "Name":
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=200, anchor="w")
                elif col == "Position":
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=150, anchor="w")
                elif col.isdigit():
                    day_index = int(col) - 1
                    if day_index < len(day_names):
                        day_label = day_names[day_index][:2]
                        heading_label = f"{col}\n{day_label}"
                    else:
                        heading_label = col
                    self.tree.heading(col, text=heading_label)
                    self.tree.column(col, width=80, anchor="center")
                else:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=110, anchor="center")

            for idx, row in enumerate(self.results, 1):
                row_data = [idx, row['full_name'], row['position']] + [
                    row.get(str(i), '') if (int(month) < current_month or int(year) < current_year or i <= current_day) else ''
                    for i in range(1, 32)
                ] + [row['Total Working Days'] or 0, row['Overtime Hours'] or 0, '']
                self.tree.insert("", "end", values=row_data)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve data: {e}")

    def export_csv(self):
        if not hasattr(self, 'results') or not self.results:
            messagebox.showinfo("Export CSV", "No data to export. Please view salary first.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[["CSV files", "*.csv"]])
        if not file_path:
            return

        try:
            columns = ["No", "Name", "Position"] + [str(i) for i in range(1, 32)] + ["Total Working Days", "Overtime Hours", "Note"]
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(columns)
                for idx, row in enumerate(self.results, 1):
                    row_data = [idx, row['full_name'], row['position']] + [
                        row.get(str(i), '') for i in range(1, 32)
                    ] + [row['Total Working Days'] or 0, row['Overtime Hours'] or 0, '']
                    writer.writerow(row_data)
            messagebox.showinfo("Export Success", f"CSV file saved to: {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Could not export CSV: {e}")

    def go_back(self):
        self.cursor.close()
        self.conn.close()
        self.root.destroy()
        self.main_ui.deiconify()
