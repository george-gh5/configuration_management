import tkinter as tk
from tkinter import scrolledtext
import os
import socket
from commands import execute_command
from config import parse_args


class EmulatorGUI:
    def __init__(self):
        # Парсинг аргументов
        args = parse_args()
        self.vfs_path = args.vfs_path
        self.startup_script = args.startup_script

        self.root = tk.Tk()
        self.root.title(f"Эмулятор - [{os.getlogin()}@{socket.gethostname()}]")
        self.root.geometry("800x600")

        self.output = scrolledtext.ScrolledText(self.root, state=tk.DISABLED)
        self.output.pack(fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(self.root)
        self.entry.pack(fill=tk.X, padx=5, pady=5)
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus()

        self.prompt = f"{os.getlogin()}@{socket.gethostname()}$ "
        self.current_dir = "/"
        self.load_vfs(self.vfs_path)

        self.print_output(self.prompt, end="")

        # Выполнение стартового скрипта
        if self.startup_script:
            try:
                with open(self.startup_script, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            self.print_output(self.prompt + line)
                            args_list = line.split()
                            if args_list:
                                cmd = args_list[0]
                                result = execute_command(cmd, args_list[1:], self)
                                if result:
                                    self.print_output(result)
            except FileNotFoundError:
                self.print_output(f"Ошибка: Скрипт {self.startup_script} не найден.")

    def load_vfs(self, path):
        self.vfs = {"/": {"type": "dir", "children": {}, "owner": "root"}}
        try:
            for root_dir, dirs, files in os.walk(path):
                rel_path = os.path.relpath(root_dir, path).replace("\\", "/")
                current = self.vfs["/"]
                if rel_path != ".":
                    parts = rel_path.split("/")
                    for part in parts:
                        if part:
                            if part not in current["children"]:
                                current["children"][part] = {"type": "dir", "children": {}, "owner": "root"}
                            current = current["children"][part]
                for file in files:
                    file_path = os.path.join(root_dir, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    current["children"][file] = {"type": "file", "content": content, "owner": "root"}
        except Exception as e:
            self.print_output(f"Ошибка загрузки VFS: {str(e)}")

    def print_output(self, text, end="\n"):
        self.output.config(state=tk.NORMAL)
        self.output.insert(tk.END, text + end)
        self.output.see(tk.END)
        self.output.config(state=tk.DISABLED)

    def on_enter(self, event):
        command_line = self.entry.get().strip()
        if command_line:
            self.print_output(command_line)
            args = command_line.split()
            if args:
                cmd = args[0]
                result = execute_command(cmd, args[1:], self)
                if result:
                    self.print_output(result)
            self.entry.delete(0, tk.END)
            self.print_output(self.prompt, end="")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = EmulatorGUI()
    app.run()
