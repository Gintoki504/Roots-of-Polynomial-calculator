import decimal
import tkinter as tk
from tkinter import messagebox

# Set decimal precision
decimal.getcontext().prec = 10


def get_validated_input(entry: str, is_float: bool = False) -> decimal.Decimal:
    if not entry:
        raise ValueError("Empty input. Please enter a numeric value.")
    try:
        value = decimal.Decimal(entry) if is_float else int(entry)
        return value
    except (ValueError, decimal.InvalidOperation):
        raise ValueError("Invalid input. Please enter a numeric value.")


def compute_roots():
    try:
        degree = get_validated_input(degree_entry.get())
        if degree < 0:
            raise ValueError("Degree must be a non-negative integer.")
    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))
        return
    try:
        coeffs = []
        for entry in coeff_entries:
            coeff = get_validated_input(entry.get(), is_float=True)
            coeffs.append(coeff)
        coeffs.reverse()
        context = list(generate_decimal_range(-20, 20, 0.001))
        labels = [f'x{i + 1}' for i in range(degree)]
        roots = {}
        previous_root = None
        tolerance = decimal.Decimal('1e-5')
        root_spacing = decimal.Decimal('0.25')
        for x in context:
            func_value = evaluate_polynomial(x, coeffs)
            if abs(func_value) < tolerance:
                if previous_root is None or abs(x - previous_root) >= root_spacing:
                    if len(roots) < degree:
                        root_label = labels[len(roots)]
                        roots[root_label] = round(float(x), 3)
                        previous_root = x
        result_label.config(text=f"Roots: {roots}")
    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))


def generate_decimal_range(start: float, stop: float, step: float):
    current = decimal.Decimal(start)
    step = decimal.Decimal(step)
    stop = decimal.Decimal(stop)
    if step == 0:
        raise ValueError("Step size cannot be zero.")
    while (step > 0 and current < stop) or (step < 0 and current > stop):
        yield current
        current += step


def evaluate_polynomial(x: decimal.Decimal, coeffs: list) -> decimal.Decimal:
    result = decimal.Decimal(0)
    for i, coeff in enumerate(coeffs):
        result += coeff * (x ** i)
    return result


def add_coeff_entries():
    clear_coeff_entries()
    try:
        degree = int(degree_entry.get())
    except ValueError:
        return
    if degree >= 0:
        for i in range(degree, -1, -1):
            label_text = f'Enter the coefficient of x^{i}:' if i != 0 else 'Enter the constant term:'
            coeff_label = tk.Label(coeff_frame, text=label_text)
            coeff_label.grid(row=degree - i, column=0, padx=10, pady=5)
            coeff_labels.append(coeff_label)
            coeff_entry = tk.Entry(coeff_frame)
            coeff_entry.grid(row=degree - i, column=1, padx=10, pady=5)
            coeff_entries.append(coeff_entry)


def clear_coeff_entries():
    for label in coeff_labels:
        label.destroy()
    for entry in coeff_entries:
        entry.destroy()
    coeff_labels.clear()
    coeff_entries.clear()


def show_main_frame():
    home_frame.grid_remove()
    main_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)


app = tk.Tk()
app.title("Polynomial Root Finder")
app.geometry("805x375")
app.configure(bg='#11212D')
home_frame = tk.Frame(app)
home_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
tk.Label(home_frame, text="Polynomial Root Finder!", bg="lightgray", font=("Helvetica", 16), bd=0).grid(row=0, columnspan=4, padx=180, pady=50)
start_button = tk.Button(home_frame, text="Start", command=lambda: show_main_frame(), font=("Helvetica", 12),
                         bg="lightgray", width=20, height=2, relief="flat", bd=0)
start_button.grid(row=1, column=1, padx=300, pady=10)


# Function to show 'Help' message
def show_help():
    messagebox.showinfo(
        "Help",
        "Usage:\n\n"
        "1. Enter the Polynomial Degree.\n"
        "2. Input Coefficients (highest power first).\n"
        "3. Click 'Compute Roots'.\n"
        "4. Click 'Clear' to reset.\n"
        "5. Click 'Clear Roots' to remove displayed roots."
    )


# Help Button
help_button = tk.Button(home_frame, text="Help", command=show_help, font=("Helvetica", 10), bg="lightgray", relief="flat", width=10, height=2)
help_button.grid(row=2, column=1, padx=300, pady=10)



main_frame = tk.Frame(app)
tk.Label(main_frame, text="Enter the Degree:").grid(row=0, column=0, padx=10, pady=10)
degree_entry = tk.Entry(main_frame)
degree_entry.grid(row=0, column=1, padx=10, pady=10)
coeff_frame = tk.Frame(main_frame)
coeff_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

coeff_entries = []
coeff_labels = []
tk.Button(main_frame, text="Set Degree", command=add_coeff_entries, bg="pink").grid(row=0, column=2, padx=10, pady=10)
tk.Button(main_frame, text="Compute Roots", command=compute_roots, bg="pink").grid(row=0, column=3, padx=10, pady=10)
tk.Button(main_frame, text="Clear", command=clear_coeff_entries, bg="pink").grid(row=0, column=4, padx=10, pady=10)
result_label = tk.Label(main_frame, text="Roots: ", wraplength=200, font=("Helvetica", 8), anchor="e", justify="right")
tk.Button(main_frame, text="Clear Roots", command=lambda: result_label.config(text="Roots: "), bg="pink").grid(row=1,column=3,padx=10,pady=10)
result_label.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="w")


# ratatatatata
def show_home_frame():
    main_frame.grid_remove()
    home_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)


# Back Button
tk.Button(main_frame, text="Back", command=show_home_frame, bg="lightgray").grid(row=1, column=4, padx=10, pady=10)

# Exit Button
exit_button = tk.Button(home_frame, text="Exit", command=app.quit, font=("Helvetica", 10), bg="lightgray",
                        relief="flat", width=10, height=2)
exit_button.grid(row=3, column=1, padx=300, pady=10)

# Info Button Functionality
def show_info():
    messagebox.showinfo(
        "About Polynomial Root Solver",
        "Polynomial Root Solver Details:\n\n"
        "This application helps you find the roots of a polynomial by:\n"
        "1. Taking the degree of the polynomial.\n"
        "2. Accepting coefficients from highest power to the constant term.\n"
        "3. Calculating roots and displaying them.\n\n"
        
        "Project for CS ELECTIVE1 for Sir.Joel."
    )


# Info Button
info_button = tk.Label(home_frame, text="Informasyon:", font=("Helvetica", 9), fg="gray", bg="#f0f0f0", cursor="hand2")
info_button.grid(row=4, column=1, padx=10, pady=10, sticky="se")
info_button.bind("<Button-1>", lambda e: show_info())


app.mainloop()

