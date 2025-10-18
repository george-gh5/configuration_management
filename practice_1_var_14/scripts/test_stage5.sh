#!/bin/sh

python emulator.py --vfs_path vfs --startup_script scripts/startup.emulator

# touch test.txt -> происходит создание файла test.txt и с помощью ls можно увидеть файл в директории
# chown Anton test.txt -> определяется новый владелец файла

#bash scripts/test_stage5.sh
