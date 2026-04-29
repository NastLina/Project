import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

root = tk.Tk()
root.title("Генератор случайных паролей")
root.geometry("600x500")

# Переменные (без изменений)
length_var = tk.IntVar(value=12)
digits_var = tk.BooleanVar()
upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar()

# Элементы интерфейса (без изменений до истории)
tk.Label(root, text="Длина:").grid(row=0, column=0, sticky="w")
length_scale = tk.Scale(root, from_=4, to=64, variable=length_var, orient=tk.HORIZONTAL)
length_scale.grid(row=0, column=1, sticky="ew")
tk.Label(root, textvariable=length_var).grid(row=0, column=2)

tk.Checkbutton(root, text="Цифры", variable=digits_var).grid(row=1, column=0)
tk.Checkbutton(root, text="Верхний регистр", variable=upper_var).grid(row=1, column=1)
tk.Checkbutton(root, text="Нижний регистр", variable=lower_var).grid(row=1, column=2)
tk.Checkbutton(root, text="Спецсимволы", variable=symbols_var).grid(row=1, column=3)

password_entry = tk.Entry(root, width=50, font=("Courier", 12))
password_entry.grid(row=2, column=0, columnspan=4, pady=10)
tk.Button(root, text="Генерировать", command=lambda: generate_password()).grid(row=3, column=1, pady=10)
tk.Button(root, text="Копировать", command=lambda: copy_to_clipboard()).grid(row=3, column=2, pady=10)
tk.Button(root, text="Очистить историю", command=clear_history).grid(row=3, column=3, pady=10)

# История (без изменений)
history_frame = ttk.Frame(root)
history_frame.grid(row=4, column=0, columnspan=4, pady=10, sticky="nsew")
tree = ttk.Treeview(history_frame, columns=("Дата", "Пароль", "Длина"), show="headings", height=10)
tree.heading("Дата", text="Дата")
tree.heading("Пароль", text="Пароль")
tree.heading("Длина", text="Длина")
tree.column("Дата", width=120)
tree.column("Пароль", width=300)
tree.column("Длина", width=60)
v_scroll = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=v_scroll.set)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(4, weight=1)

history = []

def load_history():
    global history
    try:
        if os.path.exists("history.json"):
            with open("history.json", "r", encoding="utf-8") as f:
                history = json.load(f)
    except (json.JSONDecodeError, IOError, OSError) as e:
        messagebox.showwarning("Предупреждение", f"Ошибка загрузки истории: {e}\nИспользуется пустая история.")
        history = []
    for item in tree.get_children():
        tree.delete(item)
    for h in history:
        pwd_short = h["password"][:20] + "..." if len(h["password"]) > 20 else h["password"]
        tree.insert("", tk.END, values=(h["date"], pwd_short, h["length"]))

def save_history():
    try:
        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4, ensure_ascii=False)
    except (IOError, OSError) as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {e}")

load_history()

def generate_password():
    length = length_var.get()
    if length < 4 or length > 64:
        messagebox.showerror("Ошибка", "Длина от 4 до 64")
        return
    chars = ""
    if digits_var.get(): chars += "0123456789"
    if upper_var.get(): chars += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if lower_var.get(): chars += "abcdefghijklmnopqrstuvwxyz"
    if symbols_var.get(): chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not chars:
        messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов")
        return
    pwd = ''.join(random.choices(chars, k=length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, pwd)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    history.append({"date": now, "password": pwd, "length": length})
    save_history()
    load_history()

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(password_entry.get())
    messagebox.showinfo("Копировано", "Пароль скопирован в буфер обмена")

def clear_history():
    if messagebox.askyesno("Подтверждение", "Очистить историю?"):
        global history
        history = []
        save_history()
        load_history()

root.mainloop()
