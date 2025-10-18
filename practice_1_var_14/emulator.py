import tkinter as tk
from tkinter import scrolledtext
import os
import socket
import getpass
import shlex

from practice_1_var_14.config import parse_args
from practice_1_var_14 import commands as cmdmod


class EmulatorGUI:
    def __init__(self):
        args = parse_args()
        self.vfs_path = args.vfs_path
        self.startup_script = args.startup_script

        # user and host
        try:
            self.user = getpass.getuser()
        except Exception:
            self.user = os.environ.get("USER", "user")
        self.hostname = socket.gethostname()

        self.root = tk.Tk()
        self.root.title(f"Эмулятор - [{self.user}@{self.hostname}]")
        self.root.geometry("900x600")

        self.output = scrolledtext.ScrolledText(self.root, state=tk.DISABLED, wrap=tk.WORD)
        self.output.pack(fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(self.root)
        self.entry.pack(fill=tk.X, padx=5, pady=5)
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus()

        # VFS state
        self.vfs = {"type": "dir", "children": {}, "owner": "root"}
        self.current_dir = "/"
        self.prompt = f"{self.user}@{self.hostname}:{self.current_dir}$ "

        self.print_output(f"Параметры запуска: vfs_path={self.vfs_path}, startup_script={self.startup_script}")

        # load vfs (from disk into memory)
        if os.path.exists(self.vfs_path) and os.path.isdir(self.vfs_path):
            self.vfs = cmdmod.build_vfs_from_disk(self.vfs_path)
            self.print_output(f"Загружен VFS из: {self.vfs_path}")
        else:
            self.print_output(f"VFS путь '{self.vfs_path}' не найден или не директория — загружен пустой VFS.")

        self.print_output(self.prompt, end="")

        if self.startup_script:
            self._run_startup_script(self.startup_script)

    def print_output(self, text, end="\n"):
        self.output.config(state=tk.NORMAL)
        if text is None:
            text = ""
        self.output.insert(tk.END, str(text) + end)
        self.output.see(tk.END)
        self.output.config(state=tk.DISABLED)

    def on_enter(self, event):
        cmdline = self.entry.get()
        self.entry.delete(0, tk.END)
        if not cmdline.strip():
            self.print_output(self.prompt, end="")
            return
        self.print_output(self.prompt + cmdline)
        try:
            parts = shlex.split(cmdline)
        except Exception as e:
            self.print_output(f"Ошибка разбора команды: {e}")
            self.print_output(self.prompt, end="")
            return
        cmd = parts[0]
        args = parts[1:]
        result = cmdmod.execute_command(cmd, args, self)

        if cmd == "clear":
            self.output.config(state=tk.NORMAL)
            self.output.delete(1.0, tk.END)
            self.output.config(state=tk.DISABLED)

            self.print_output(self.prompt, end="")
            return

        if result is None:
            try:
                self.root.quit()
            except Exception:
                pass
            return

        if result != "":
            self.print_output(result)
        else:

            pass

        self.prompt = f"{self.user}@{self.hostname}:{self.current_dir}$ "
        self.print_output(self.prompt, end="")

    def _run_startup_script(self, path):
        if not os.path.exists(path):
            self.print_output(f"Ошибка: Скрипт {path} не найден.")
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                for raw in f:
                    line = raw.rstrip("\n")
                    if not line.strip():
                        self.print_output("")
                        continue
                    if line.strip().startswith("#"):
                        self.print_output(line)
                        continue

                    self.print_output(self.prompt + line)
                    try:
                        parts = shlex.split(line)
                    except Exception as e:
                        self.print_output(f"Ошибка разбора строки: {e}")
                        continue
                    cmd = parts[0]
                    args = parts[1:]
                    result = cmdmod.execute_command(cmd, args, self)
                    if cmd == "clear":
                        self.output.config(state=tk.NORMAL)
                        self.output.delete(1.0, tk.END)
                        self.output.config(state=tk.DISABLED)
                        continue
                    if result is None:

                        try:
                            self.root.quit()
                        except Exception:
                            pass
                        return
                    if result != "":
                        self.print_output(result)

                    self.prompt = f"{self.user}@{self.hostname}:{self.current_dir}$ "

                self.print_output(self.prompt, end="")
        except Exception as e:
            self.print_output(f"Ошибка выполнения стартового скрипта: {e}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = EmulatorGUI()
    app.run()
