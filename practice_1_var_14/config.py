import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Эмулятор командной оболочки (GUI).")
    # vfs = root
    parser.add_argument("--vfs_path", default="vfs",
                        help="Путь к директории-источнику VFS (по умолчанию vfs).")
    parser.add_argument("--startup_script", default=None,
                        help="Путь к стартовому скрипту (опционально).")
    return parser.parse_args()
