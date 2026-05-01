import random
import string
import tkinter as tk
from tkinter import messagebox
import pyperclip

# ---------------- PASSWORD GENERATOR FUNCTION ---------------- #
def generate_password():
    try:
        length = int(length_var.get())
    except:
        messagebox.showerror("Error", "Please enter a valid number!")
        return

    if length < 4:
        messagebox.showerror("Error", "Password length must be at least 4")
        return

    characters = ""

    if upper_var.get():
        characters += string.ascii_uppercase
    if lower_var.get():
        characters += string.ascii_lowercase
    if digit_var.get():
        characters += string.digits
    if symbol_var.get():
        characters += string.punctuation

    if characters == "":
        messagebox.showerror("Error", "Select at least one character type!")
        return

    # Exclude characters
    exclude_chars = exclude_entry.get()
    characters = ''.join([c for c in characters if c not in exclude_chars])

    if not characters:
        messagebox.showerror("Error", "No valid characters left after exclusion!")
        return

    password = ''.join(random.choice(characters) for _ in range(length))

    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)


# ---------------- COPY FUNCTION ---------------- #
def copy_password():
    password = password_entry.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showwarning("Warning", "No password to copy!")


# ---------------- UPDATE SELECTION DISPLAY ---------------- #
def update_selection_label():
    selected = []

    if upper_var.get():
        selected.append("Uppercase")
    if lower_var.get():
        selected.append("Lowercase")
    if digit_var.get():
        selected.append("Numbers")
    if symbol_var.get():
        selected.append("Symbols")

    if selected:
        selection_label.config(text="Selected: " + ", ".join(selected))
    else:
        selection_label.config(text="Selected: None")


# ---------------- GUI SETUP ---------------- #
root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("420x500")
root.config(bg="#1e1e2f")

# ---------------- VARIABLES ---------------- #
length_var = tk.StringVar(value="12")
upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
digit_var = tk.BooleanVar(value=True)
symbol_var = tk.BooleanVar(value=True)

# ---------------- TITLE ---------------- #
tk.Label(root, text="Password Generator", font=("Arial", 18, "bold"),
         bg="#1e1e2f", fg="white").pack(pady=10)

# ---------------- LENGTH ---------------- #
tk.Label(root, text="Password Length", bg="#1e1e2f", fg="white").pack()
tk.Entry(root, textvariable=length_var, justify="center").pack(pady=5)

# ---------------- OPTIONS ---------------- #
tk.Checkbutton(root, text="Uppercase", variable=upper_var,
               command=update_selection_label,
               bg="#1e1e2f", fg="white", selectcolor="#333").pack()

tk.Checkbutton(root, text="Lowercase", variable=lower_var,
               command=update_selection_label,
               bg="#1e1e2f", fg="white", selectcolor="#333").pack()

tk.Checkbutton(root, text="Numbers", variable=digit_var,
               command=update_selection_label,
               bg="#1e1e2f", fg="white", selectcolor="#333").pack()

tk.Checkbutton(root, text="Symbols", variable=symbol_var,
               command=update_selection_label,
               bg="#1e1e2f", fg="white", selectcolor="#333").pack()

# ---------------- SELECTED DISPLAY ---------------- #
selection_label = tk.Label(root, text="", bg="#1e1e2f", fg="lightgreen")
selection_label.pack(pady=5)

update_selection_label()

# ---------------- EXCLUDE ---------------- #
tk.Label(root, text="Exclude Characters", bg="#1e1e2f", fg="white").pack(pady=5)
exclude_entry = tk.Entry(root, justify="center")
exclude_entry.pack()

# ---------------- PASSWORD OUTPUT ---------------- #
password_entry = tk.Entry(root, font=("Arial", 14), justify="center")
password_entry.pack(pady=15)

# ---------------- BUTTONS ---------------- #
tk.Button(root, text="Generate Password", command=generate_password,
          bg="#4CAF50", fg="white", width=20).pack(pady=5)

tk.Button(root, text="Copy to Clipboard", command=copy_password,
          bg="#2196F3", fg="white", width=20).pack(pady=5)

# ---------------- RUN ---------------- #
root.mainloop()
