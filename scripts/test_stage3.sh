#!/bin/bash
echo "Тест с минимальным VFS:"
python emulator.py --vfs_path vfs/minimal_vfs --startup_script scripts/startup.emulator

echo "Тест с простым VFS (несколько файлов):"
python emulator.py --vfs_path vfs/simple_vfs --startup_script scripts/startup.emulator

echo "Тест с глубоким VFS (3 уровня):"
python emulator.py --vfs_path vfs/deep_vfs --startup_script scripts/startup.emulator