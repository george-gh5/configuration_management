#!/bin/sh

python emulator.py --vfs_path vfs/minimal_vfs

# ls -> пусто, так как minimal_vfs пуста
# cd / -> остаётся user@hostname:/$
# exit -> GUI закрывается

# bash scripts/test_stage1.sh
