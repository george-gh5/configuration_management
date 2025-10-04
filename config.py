import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Эмулятор командной строки")
    parser.add_argument("--vfs_path", default="vfs/minimal_vfs", help="Путь к VFS")
    parser.add_argument("--startup_script", default=None, help="Путь к стартовому скрипту")
    args = parser.parse_args()

    # Отладочный вывод в консоли
    print(f"Отладка: vfs_path={args.vfs_path}, startup_script={args.startup_script}")
    return args