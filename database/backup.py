"""
Создание резервной копии базы данных PostgreSQL с помощью pg_dump.

Запускать ВРУЧНУЮ на хост-машине (там, где установлен Docker и запущены контейнеры):

    python database/backup.py

Дамп сохраняется в папку backups/ в корне проекта, с датой и временем в имени:

    backups/backup_2026-06-17_153000.sql
"""
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Настройки берём из docker-compose.yaml (сервис db)
CONTAINER = 'image_server_db'   # container_name контейнера с базой
DB_USER = 'postgres'            # POSTGRES_USER
DB_NAME = 'images_db'           # POSTGRES_DB

BASE_DIR = Path(__file__).resolve().parent.parent
BACKUPS_DIR = BASE_DIR / 'backups'


def create_backup():
    BACKUPS_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    backup_file = BACKUPS_DIR / f'backup_{timestamp}.sql'

    command = [
        'docker', 'exec', '-t', CONTAINER,
        'pg_dump', '-U', DB_USER, DB_NAME,
    ]

    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            result = subprocess.run(command, stdout=f, stderr=subprocess.PIPE, text=True)
    except FileNotFoundError:
        print('Ошибка: команда "docker" не найдена. '
              'Запускай скрипт на хосте, где установлен Docker.')
        sys.exit(1)

    if result.returncode != 0:
        print('Ошибка при создании резервной копии:')
        print(result.stderr.strip())
        backup_file.unlink(missing_ok=True)   # не оставляем пустой/битый файл
        sys.exit(1)

    print(f'Резервная копия создана: {backup_file}')


if __name__ == '__main__':
    create_backup()