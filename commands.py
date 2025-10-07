import os
import getpass
import calendar
from datetime import datetime


def build_vfs_from_disk(path_on_disk):
    root = {"type": "dir", "children": {}, "owner": "root"}
    base = os.path.abspath(path_on_disk)

    for r, dirs, files in os.walk(base):
        rel = os.path.relpath(r, base)

        if rel == ".":
            node = root
        else:
            parts = rel.replace("\\", "/").split("/")
            node = root
            for p in parts:
                if p not in node["children"]:
                    node = node["children"].setdefault(p, {"type": "dir", "children": {}, "owner": "root"})
                else:
                    node = node["children"][p]

        for d in dirs:
            node["children"].setdefault(d, {"type": "dir", "children": {}, "owner": "root"})

        for f in files:
            fpath = os.path.join(r, f)
            try:
                with open(fpath, "r", encoding="utf-8") as fh:
                    content = fh.read()
            except Exception:
                content = None
            node["children"][f] = {"type": "file", "content": content, "owner": "root"}

    return root


def normalize_vfs_path(current_dir, path):
    if path is None or path == "":
        return current_dir or "/"
    if path == "~":
        return "/home/" + getpass.getuser()
    if path.startswith("~"):
        rest = path[1:].lstrip("/")
        return "/home/" + getpass.getuser() + ("/" + rest if rest else "")
    if path.startswith("/"):
        parts = [p for p in path.split("/") if p]
    else:
        base = current_dir if current_dir else "/"
        combined = (base.rstrip("/") + "/" + path) if base != "/" else "/" + path
        parts = [p for p in combined.split("/") if p]
    stack = []
    for p in parts:
        if p == "." or p == "":
            continue
        if p == "..":
            if stack:
                stack.pop()
            continue
        stack.append(p)
    return "/" + "/".join(stack) if stack else "/"


def path_to_parts(path):
    if path == "/" or path == "" or path is None:
        return []
    return [p for p in path.lstrip("/").split("/") if p]


def get_node_by_path(vfs_root, path):
    parts = path_to_parts(path)
    node = vfs_root
    for p in parts:
        if node["type"] != "dir":
            return None
        if p not in node["children"]:
            return None
        node = node["children"][p]
    return node


def cmd_pwd(gui):
    return gui.current_dir


def cmd_ls(gui, args):
    # support: ls [-a] [path]
    show_hidden = False
    path_arg = None
    for a in args:
        if a.startswith("-") and "a" in a:
            show_hidden = True
        elif path_arg is None:
            path_arg = a
    if not path_arg:
        path_arg = "."
    resolved = normalize_vfs_path(gui.current_dir, path_arg)
    node = get_node_by_path(gui.vfs, resolved)
    if node is None:
        return f"ls: невозможно получить доступ к '{path_arg}': Нет такого файла или директории"
    if node["type"] == "file":
        return path_arg
    items = []
    for name, n in node["children"].items():
        if not show_hidden and name.startswith("."):
            continue
        items.append(name + ("/" if n["type"] == "dir" else ""))
    return "  ".join(sorted(items)) if items else ""


def cmd_cd(gui, args):
    target = args[0] if args else ""
    if not target:
        home = "/home/" + getpass.getuser()
        if get_node_by_path(gui.vfs, home):
            newp = home
        else:
            newp = "/"
    else:
        newp = normalize_vfs_path(gui.current_dir, target)
    node = get_node_by_path(gui.vfs, newp)
    if node is None:
        return f"cd: {target}: Нет такого файла или директории"
    if node["type"] != "dir":
        return f"cd: {target}: Не директория"
    gui.current_dir = newp
    return f"Текущая директория изменена на {gui.current_dir}"


def cmd_echo(gui, args):
    if not args:
        return ""
    out = []
    for a in args:
        if a.startswith("$"):
            out.append(str(__import__("os").environ.get(a[1:], "")))
        else:
            out.append(a)
    return " ".join(out)


def cmd_cal(gui, args):
    try:
        if len(args) == 2:
            m = int(args[0]); y = int(args[1])
        elif len(args) == 1:
            m = int(args[0]); y = datetime.now().year
        else:
            m = datetime.now().month; y = datetime.now().year
        return calendar.month(y, m)
    except Exception as e:
        return f"cal: неверные аргументы: {e}"


def cmd_clear(gui, args):
    return ""


def cmd_cat(gui, args):
    if not args:
        return "cat: требуется имя файла"
    path = normalize_vfs_path(gui.current_dir, args[0])
    node = get_node_by_path(gui.vfs, path)
    if node is None:
        return f"cat: {args[0]}: Нет такого файла"
    if node["type"] != "file":
        return f"cat: {args[0]}: Это не файл"
    return node.get("content") or ""


def cmd_touch(gui, args):
    if not args:
        return "touch: требуется имя файла"
    name = args[0]
    full = normalize_vfs_path(gui.current_dir, name)
    if full == "/":
        return "touch: неверное имя файла"
    parts = path_to_parts(full)
    parent_path = "/" + "/".join(parts[:-1]) if parts[:-1] else "/"
    parent = get_node_by_path(gui.vfs, parent_path)
    if parent is None or parent["type"] != "dir":
        return f"touch: {name}: Нет такой директории"
    fname = parts[-1]
    if fname in parent["children"]:
        return ""
    parent["children"][fname] = {"type": "file", "content": "", "owner": getpass.getuser()}
    return f"Файл {full} создан (в памяти)"


def cmd_chown(gui, args):
    if len(args) < 2:
        return "chown: требуется имя пользователя и имя файла/директории"
    new_owner = args[0]
    target = args[1]
    resolved = normalize_vfs_path(gui.current_dir, target)
    node = get_node_by_path(gui.vfs, resolved)
    if node is None:
        return f"chown: {target}: Нет такого файла или директории"
    node["owner"] = new_owner
    return f"Владелец {resolved} изменён на {new_owner}"


def cmd_exit(gui, args):
    return None


# Словарь команд
COMMANDS = {
    "pwd": cmd_pwd,
    "ls": cmd_ls,
    "cd": cmd_cd,
    "echo": cmd_echo,
    "cal": cmd_cal,
    "clear": cmd_clear,
    "cat": cmd_cat,
    "touch": cmd_touch,
    "chown": cmd_chown,
    "exit": cmd_exit,
}


def execute_command(cmd, args, gui):
    fn = COMMANDS.get(cmd)
    if fn:
        return fn(gui, args)
    else:
        return f"Неизвестная команда: {cmd}"
