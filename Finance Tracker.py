import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class FinanceTracker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Personal Finance Tracker")
        self.geometry("800x600")
        self.configure(bg="#F0F0F0")

        # Create the main frame
        main_frame = ttk.Frame(self, padding="20")
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Customize widget style
        style = ttk.Style()
        style.configure("TLabel", font=("Verdana", 14), foreground="black")
        style.configure("TEntry", font=("Verdana", 14), foreground="black")
        style.configure("TButton", font=("Verdana", 14), background="#3498db", foreground="white")
        style.configure("TText", font=("Verdana", 14), foreground="black")

        # Create labels and entry fields
        ttk.Label(main_frame, text="Income:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        self.income_var = tk.DoubleVar()
        ttk.Entry(main_frame, textvariable=self.income_var).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(main_frame, text="Expenses:").grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        self.expenses_var = tk.DoubleVar()
        ttk.Entry(main_frame, textvariable=self.expenses_var).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(main_frame, text="Savings:").grid(row=2, column=0, sticky=tk.W, pady=(0, 10))
        self.savings_var = tk.DoubleVar()
        ttk.Entry(main_frame, textvariable=self.savings_var).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(0, 10))

        # Create buttons
        ttk.Button(main_frame, text="Add Income", command=self.add_income).grid(row=0, column=2, sticky=(tk.W, tk.E), padx=(10, 0), pady=(0, 10))
        ttk.Button(main_frame, text="Add Expenses", command=self.add_expenses).grid(row=1, column=2, sticky=(tk.W, tk.E), padx=(10, 0), pady=(0, 10))
        ttk.Button(main_frame, text="Calculate Savings", command=self.calculate_savings).grid(row=2, column=2, sticky=(tk.W, tk.E), padx=(10, 0), pady=(0, 10))

        # Transaction history
        ttk.Label(main_frame, text="Transaction History:").grid(row=3, column=0, sticky=tk.W, pady=(10, 0))
        self.transaction_history = tk.Text(main_frame, width=50, height=10, wrap=tk.WORD)
        self.transaction_history.grid(row=4, column=0, columnspan=3, pady=(5, 10))

        # Category-wise expense breakdown
        ttk.Label(main_frame, text="Expense Categories:").grid(row=5, column=0, sticky=tk.W, pady=(10, 0))
        self.expense_categories = tk.Text(main_frame, width=50, height=10, wrap=tk.WORD)
        self.expense_categories.grid(row=6, column=0, columnspan=3, pady=(5, 10))

        main_frame.columnconfigure(1, weight=1)

 
    def add_income(self):
        amount = self.ask_amount("Add Income")
        if amount:
            income = self.income_var.get()
            self.income_var.set(income + amount)
            self.transaction_history.insert(tk.END, f"Income: +${amount:.2f}\n")
            self.transaction_history.see(tk.END)

    def add_expenses(self):
        amount, category = self.ask_expense_details()
        if amount and category:
            expenses = self.expenses_var.get()
            self.expenses_var.set(expenses + amount)
            self.transaction_history.insert(tk.END, f"Expense: -${amount:.2f} ({category})\n")
            self.transaction_history.see(tk.END)
            self.add_expense_category(category, amount)

    def calculate_savings(self):
        income = self.income_var.get()
        expenses = self.expenses_var.get()
        savings = income - expenses
        self.savings_var.set(savings)

    def ask_amount(self, title):
        amount = simpledialog.askfloat(title, "Enter the amount:")
        return amount

    def ask_expense_details(self):
        dialog = ExpenseDialog(self)
        self.wait_window(dialog)
        return dialog.amount, dialog.category

    def add_expense_category(self, category, amount):
        current_data = self.expense_categories.get(1.0, tk.END)
        category_line = f"{category}: ${amount:.2f}\n"

        if category in current_data:
            lines = current_data.split('\n')
            for idx, line in enumerate(lines):
                if category in line:
                    current_amount = float(line.split('$')[-1])
                    new_amount = current_amount + amount
                    lines[idx] = f"{category}: ${new_amount:.2f}"
                    break
            new_data = '\n'.join(lines)
            self.expense_categories.delete(1.0, tk.END)
            self.expense_categories.insert(tk.END, new_data)
        else:
            self.expense_categories.insert(tk.END, category_line)

class ExpenseDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Expense")
        self.geometry("300x200")

        frame = ttk.Frame(self, padding="10")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        ttk.Label(frame, text="Amount:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        self.amount_var = tk.DoubleVar()
        ttk.Entry(frame, textvariable=self.amount_var).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(frame, text="Category:").grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        self.category_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.category_var).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Button(frame, text="Add", command=self.add_expense).grid(row=2, column=0, columnspan=2, pady=(10, 0))

        frame.columnconfigure(1, weight=1)

    def add_expense(self):
        self.amount = self.amount_var.get()
        self.category = self.category_var.get().strip()
        if self.amount > 0 and self.category:
            self.destroy()
        else:
            messagebox.showerror("Error", "Please enter a valid amount and category.")

if __name__ == "__main__":
    app = FinanceTracker()
    app.mainloop()
