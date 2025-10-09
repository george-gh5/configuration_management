# Эмулятор командной строки UNIX (Вариант №14)

## Описание
Проект реализует эмулятор командной строки UNIX-подобной ОС в рамках индивидуального задания (вариант №14) по дисциплине "Конфигурационное управление". Эмулятор разработан на Python с использованием Tkinter для GUI. Все операции с VFS выполняются в памяти. Реализованы все этапы задания:
- **Этап 1**: REPL с GUI, команды `ls`, `cd`, `exit`.
- **Этап 2**: параметры командной строки (`--vfs_path`, `--startup_script`), стартовый скрипт с комментариями.
- **Этап 3**: виртуальная файловая система (VFS) в памяти, загрузка из `vfs/`.
- **Этап 4**: основные команды `ls`, `cd`, `echo`, `cal`, `clear` с поддержкой VFS.
- **Этап 5**: дополнительные команды `touch`, `chown` для работы с VFS.

## Структура проекта
- `emulator.py`: основной файл эмулятора (GUI и REPL).
- `commands.py`: реализация команд (`ls`, `cd`, `echo`, `cal`, `clear`, `touch`, `chown`).
- `config.py`: обработка параметров командной строки.
- `vfs/`:
  - `deep_vfs/`: многоуровневая структура (`dir1/subdir/file.txt`, `another_file.txt`).
  - `minimal_vfs/`: пустая директория.
  - `simple_vfs/`: файлы `file1.txt`, `file2.txt`.
- `scripts/`:
  - `startup.emulator`: стартовый скрипт для демонстрации команд.
  - `test_stage1.sh`–`test_stage5.sh`: тестовые скрипты для этапов.
- `.gitignore`: исключение временных файлов (`__pycache__`, `*.pyc`, и т.д.).

## Установка и запуск
1. Убедитесь, что установлен Python 3.x и Tkinter:
   ```bash
   python --version
   python -c "import tkinter"
2. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/george-gh5/configuration_management.git
   cd configuration_management
3. Запустите эмулятор:
   ```bash
   python emulator.py --vfs_path vfs --startup_script scripts/startup.emulator
4. Тестирование этапов:
   ```bash
   ./scripts/test_stage1.sh
   ./scripts/test_stage2.sh
   ./scripts/test_stage3.sh
   ./scripts/test_stage4.sh
   ./scripts/test_stage5.sh
