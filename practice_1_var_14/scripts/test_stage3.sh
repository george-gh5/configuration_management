#!/bin/sh

python emulator.py --vfs_path vfs/minimal_vfs
python emulator.py --vfs_path vfs/simple_vfs
python emulator.py --vfs_path vfs/deep_vfs

# Для --vfs_path vfs/minimal_vfs:
# ls -> пусто

# Для --vfs_path vfs/simple_vfs:
# ls -> file1.txt file2.txt
# cat file1.txt -> выводит содержимое файла file1.txt

# Для --vfs_path vfs/deep_vfs:
# ls -> another_file.txt dir1/
# cd dir1/subdir -> user@hostname:/dir1/subdir$
# ls -> file.txt

# bash scripts/test_stage3.sh
