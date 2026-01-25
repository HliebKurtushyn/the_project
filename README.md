# Онлайн магазин одягу

## Readme coming soon...

## Налаштування
_Потрібно мати встановлений Python 3.8 або новішу версію і також git._

1. Склонуйте репозиторій:
   ```
   git clone https://github.com/HliebKurtushyn/the_project.git
   ```
2. Перейдіть у директорію проєкту:
   ```
   cd the_project
   ```
3. Встановіть віртуальне оточення (рекомендується):
   ```
   python -m venv venv
    ```
4. Активуйте віртуальне оточення:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```
5. Встановіть залежності:
   ```
   pip install -r requirements.txt
   ```
6. Застосуйте міграції:
   ```
   python manage.py migrate
   ```
7. Запустіть сервер розробки:
   ```
   python manage.py runserver
   ```
   

Додаткова документація:
- [Огляд проєкту](docs/overview.md)
- [Архітектура проєкту](docs/architecture.md)
- [Для команди](docs/for_team.md)
- [Workflow](docs/workflow.md)
- [Trash (чорновик)](docs/trash.md)
- [Ролі в команді](docs/roles.md)