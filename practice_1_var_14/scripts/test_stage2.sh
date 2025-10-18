#!/bin/sh

python emulator.py --vfs_path vfs --startup_script scripts/startup.emulator

# В GUI должен отобразиться стартовый вывод: "Параметры запуска: vfs_path=vfs,
# startup_script=scripts/startup.emulator."
# Комментарии (# ...) отображаются в GUI без выполнения.

# bash scripts/test_stage2.sh
