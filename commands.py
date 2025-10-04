def execute_command(cmd, args, gui):
    if cmd == "ls":
        return f"Команда: ls {' '.join(args)}"
    elif cmd == "cd":
        return f"Команда: cd {' '.join(args)}"
    elif cmd == "exit":
        gui.root.quit()
        return "Выход из эмулятора."
    else:
        return f"Неизвестная команда: {cmd}"
