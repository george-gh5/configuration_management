#!/bin/bash
echo "Тест без параметров:"
python emulator.py

echo "Тест с VFS-путём:"
python emulator.py --vfs_path vfs/simple_vfs

echo "Тест со стартовым скриптом:"
python emulator.py --startup_script scripts/startup.emulator

echo "Тест с обоими параметрами:"
python emulator.py --vfs_path vfs/minimal_vfs --startup_script scripts/startup.emulator