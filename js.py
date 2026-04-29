import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os
from datetime import datetime

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("700x500")
        self.root.resizable(True, True)

        
        self.history_file = "history.json"
        self.history = self.load_history()

        
        self.length_var = tk.IntVar(value=12)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=False)

       
        self.create_widgets()

        
        self.update_history_display()

    def create_widgets(self):
        # Фрейм с настройками
        settings_frame = ttk.LabelFrame(self.root, text="Настройки пароля", padding=10)
        settings_frame.pack(fill="x", padx=10, pady=5)

       
        ttk.Label(settings_frame, text="Длина пароля:").grid(row=0, column=0, sticky="w", padx=5)
        self.length_scale = ttk.Scale(settings_frame, from_=4, to=50, orient="horizontal",
                                      variable=self.length_var, command=self.update_length_label)
        self.length_scale.grid(row=0, column=1, sticky="ew", padx=5)
        self.length_label = ttk.Label(settings_frame, text="12")
        self.length_label.grid(row=0, column=2, padx=5)
        settings_frame.columnconfigure(1, weight=1)

        # Чекбоксы
        ttk.Checkbutton(settings_frame, text="Буквы (A-Z, a-z)", variable=self.use_letters).grid(row=1, column=0, sticky="w", padx=5, pady=2)
        ttk.Checkbutton(settings_frame, text="Цифры (0-9)", variable=self.use_digits).grid(row=1, column=1, sticky="w", padx=5, pady=2)
        ttk.Checkbutton(settings_frame, text="Спецсимволы (!@#$%^&*()_+-=[]{}|;:,.<>?)", variable=self.use_symbols).grid(row=1, column=2, sticky="w", padx=5, pady=2)

       
        generate_btn = ttk.Button(settings_frame, text="Сгенерировать пароль", command=self.generate_and_save)
        generate_btn.grid(row=2, column=0, columnspan=3, pady=10)

       
        history_frame = ttk.LabelFrame(self.root, text="История паролей", padding=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("password", "timestamp", "length", "settings")
        self.tree = ttk.Treeview(history_frame, columns=columns, show="headings")
        self.tree.heading("password", text="Пароль")
        self.tree.heading("timestamp", text="Дата и время")
        self.tree.heading("length", text="Длина")
        self.tree.heading("settings", text="Набор символов")

        self.tree.column("password", width=200)
        self.tree.column("timestamp", width=150)
        self.tree.column("length", width=60)
        self.tree.column("settings", width=180)

        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

       
        clear_btn = ttk.Button(history_frame, text="Очистить историю", command=self.clear_history)
        clear_btn.pack(pady=5)

    def update_length_label(self, event=None):
        self.length_label.config(text=str(self.length_var.get()))

    def generate_password(self):
        length = self.length_var.get()
        if length < 4:
            messagebox.showerror("Ошибка", "Минимальная длина пароля – 4 символа")
            return None
        if length > 50:
            messagebox.showerror("Ошибка", "Максимальная длина пароля – 50 символов")
            return None

        chars = ""
        if self.use_letters.get():
            chars += string.ascii_letters
        if self.use_digits.get():
            chars += string.digits
        if self.use_symbols.get():
            chars += string.punctuation

        if not chars:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов для пароля")
            return None

       
        password = []
        if self.use_letters.get():
            password.append(random.choice(string.ascii_letters))
        if self.use_digits.get():
            password.append(random.choice(string.digits))
        if self.use_symbols.get():
            password.append(random.choice(string.punctuation))

        
        for _ in range(length - len(password)):
            password.append(random.choice(chars))

       
        random.shuffle(password)
        return ''.join(password)

    def generate_and_save(self):
        password = self.generate_password()
        if password is None:
            return

     
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        settings_str = []
        if self.use_letters.get(): settings_str.append("буквы")
        if self.use_digits.get(): settings_str.append("цифры")
        if self.use_symbols.get(): settings_str.append("спецсимволы")
        settings_desc = ", ".join(settings_str)

        entry = {
            "password": password,
            "timestamp": now,
            "length": len(password),
            "settings": settings_desc
        }

        self.history.insert(0, entry)  
        self.save_history()
        self.update_history_display()

        # Показать пароль в диалоге
        messagebox.showinfo("Новый пароль", f"Сгенерирован пароль:\n\n{password}\n\nСохранён в истории.")

    def save_history(self):
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить историю:\n{str(e)}")

    def load_history(self):
        if not os.path.exists(self.history_file):
            return []
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, Exception):
            return []

    def update_history_display(self):
        # Очищаем таблицу
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        for entry in self.history:
            self.tree.insert("", "end", values=(
                entry["password"],
                entry["timestamp"],
                entry["length"],
                entry["settings"]
            ))

    def clear_history(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.history = []
            self.save_history()
            self.update_history_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
    